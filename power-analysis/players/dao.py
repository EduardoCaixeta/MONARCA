import sqlite3
from datetime import datetime
from player import Player, PowerRegister

class PlayerDAO:
    def __init__(self, db_path="players.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                rank TEXT NOT NULL,
                join_date TEXT NOT NULL,
                stars INTEGER NOT NULL,
                active INTEGER NOT NULL DEFAULT 1  -- 1 = True, 0 = False
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS power_registers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                power_level REAL NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY(player_id) REFERENCES players(id)
            )
        ''')
        self.conn.commit()

    def get_player_by_name_and_rank(self, name, rank):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM players WHERE name = ? AND rank = ?
        """, (name, rank))
        row = cursor.fetchone()
        if row:
            return Player(
                name=row["name"],
                rank=row["rank"],
                join_date=datetime.fromisoformat(row["join_date"]),
                stars=row["stars"],
                active=bool(row["active"])
            )
        return None

    def add_player(self, player: Player):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO players (name, rank, join_date, stars, active)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            player.name,
            player.rank,
            player.join_date.isoformat(),
            player.stars,
            1 if player.active else 0
        ))
        self.conn.commit()
        return cursor.lastrowid  # Retorna o ID do novo jogador

    def add_power_register(self, power_register: PowerRegister):
        cursor = self.conn.cursor()
        # Obtém o ID do player
        cursor.execute('SELECT id FROM players WHERE name = ? AND rank = ?', 
                       (power_register.player.name, power_register.player.rank))
        player_row = cursor.fetchone()
        if not player_row:
            # Se o jogador não existe, insere
            player_id = self.add_player(power_register.player)
        else:
            player_id = player_row["id"]

        cursor.execute('''
            INSERT INTO power_registers (player_id, power_level, date)
            VALUES (?, ?, ?)
        ''', (player_id, power_register.power_level, power_register.date.isoformat()))
        self.conn.commit()
        return cursor.lastrowid

    def get_power_registers_for_player(self, player: Player):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT power_level, date FROM power_registers
            WHERE player_id = (
                SELECT id FROM players WHERE name = ? AND rank = ?
            )
        ''', (player.name, player.rank))
        rows = cursor.fetchall()
        return [
            PowerRegister(player=player, power_level=row["power_level"], date=datetime.fromisoformat(row["date"]))
            for row in rows
        ]

    def set_player_active_status(self, name, rank, active: bool):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE players SET active = ? WHERE name = ? AND rank = ?
        """, (1 if active else 0, name, rank))
        self.conn.commit()

    def get_all_active_players(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM players WHERE active = 1")
        rows = cursor.fetchall()
        return [
            Player(
                name=row["name"],
                rank=row["rank"],
                join_date=datetime.fromisoformat(row["join_date"]),
                stars=row["stars"],
                active=True
            )
            for row in rows
        ]


    def close(self):
        self.conn.close()
