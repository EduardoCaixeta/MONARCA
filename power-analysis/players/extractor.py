import easyocr
import re
from datetime import datetime
from player import Player, PowerRegister

class PowerExtractor:
    def __init__(self, dao, languages=None):
        self.dao = dao
        self.reader = easyocr.Reader(
            languages if languages else ['en', 'pt', 'es', 'fr', 'de', 'it'],
            gpu=False
        )

    def extract_text_from_image(self, image_path):
        try:
            result = self.reader.readtext(image_path)
            return "\n".join([text for (_, text, _) in result])
        except Exception as e:
            print(f"Erro ao processar {image_path}: {e}")
            return ""

    def parse_names_and_powers(self, text):
        pattern = r"([A-Za-z0-9\s\[\]À-ÿ()\-_.]+?)\s+Poder\s+(\d+\.\d+)"
        matches = re.findall(pattern, text, re.MULTILINE)

        extracted_data = []
        for name, power in matches:
            name = name.strip()
            try:
                power_value = float(power)
                extracted_data.append({
                    "name": name,
                    "power": power_value
                })
            except ValueError:
                print(f"[WARN] Valor de poder inválido: '{power}' para jogador '{name}'")
        return extracted_data
            
    def process(self, image_info_list):
        all_seen_players = {}  # rank -> set of player names

        for image_info in image_info_list:
            print(f"Processando {image_info.rank} na data {image_info.date}...")
            print(f"  Imagem: {image_info.image}")

            text = self.extract_text_from_image(image_info.image)
            data = self.parse_names_and_powers(text)

            seen_names = set()
            for entry in data:
                name = entry["name"]
                power = entry["power"]

                if not name or power <= 0:
                    print(f"[WARN] Dados inválidos ignorados - Nome: '{name}', Poder: {power}")
                    continue

                seen_names.add(name)
                player = self.dao.get_player_by_name_and_rank(name, image_info.rank)
                if not player:
                    player = Player(name=name, rank=image_info.rank, join_date=image_info.date, stars=0, active=True)
                    self.dao.add_player(player)
                    player = self.dao.get_player_by_name_and_rank(name, image_info.rank)

                elif not player.active:
                    self.dao.set_player_active_status(name, image_info.rank, True)  # Reativa se aparecer

                power_record = PowerRegister(player=player, power_level=power, date=image_info.date)
                self.dao.add_power_register(power_record)

            if image_info.rank not in all_seen_players:
                all_seen_players[image_info.rank] = set()
            all_seen_players[image_info.rank].update(seen_names)

        # Após processar todos os ranks, verificamos jogadores que ficaram de fora
        all_players = self.dao.get_all_active_players()
        seen_global = set()
        for names in all_seen_players.values():
            seen_global.update(names)

        for player in all_players:
            if player.name not in seen_global:
                print(f"[INFO] Marcando jogador como inativo: {player.name} (Rank: {player.rank})")
                self.dao.set_player_active_status(player.name, player.rank, False)
