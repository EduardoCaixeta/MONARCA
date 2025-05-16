import os
from PIL import ImageGrab, Image
import pyautogui
import keyboard
from time import sleep

# Função para criar uma pasta se ela não existir
def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

# Função para obter o próximo número de imagem na pasta
def get_next_image_number(folder_name):
    existing_files = [f for f in os.listdir(folder_name) if f.startswith("image_") and f.endswith(".png")]
    if not existing_files:
        return 1
    numbers = [int(f.replace("image_", "").replace(".png", "")) for f in existing_files]
    return max(numbers) + 1

# Função para capturar imagem da área de transferência e salvar
def save_image_from_clipboard(folder_name):
    try:
        # Captura a imagem da área de transferência
        image = ImageGrab.grabclipboard()
        if image is None:
            print("Nenhuma imagem encontrada na área de transferência!")
            return False
        
        # Obtém o próximo número para o nome do arquivo
        image_number = get_next_image_number(folder_name)
        file_path = os.path.join(folder_name, f"image_{image_number}.png")
        
        # Salva a imagem
        image.save(file_path, "PNG")
        print(f"Imagem salva como {file_path}")
        return True
    except Exception as e:
        print(f"Erro ao salvar a imagem: {e}")
        return False

# Função principal
def main():
    # Opções de menu
    ranks = {
        "1": "RANK_1",
        "2": "RANK_2",
        "3": "RANK_3",
        "4": "RANK_4"
    }
    
    while True:
        # Exibe o menu
        print("\nMenu:")
        for key, value in ranks.items():
            print(f"[{key}] - {value.replace('_', ' ')}")
        print("Digite o número do RANK ou '0' para sair:")
        
        choice = input().strip()
        
        # Verifica se o usuário quer sair
        if choice == "0":
            print("Saindo...")
            break
        
        # Verifica se a escolha é válida
        if choice not in ranks:
            print("Opção inválida! Tente novamente.")
            continue
        
        # Cria a pasta do RANK selecionado
        folder_name = ranks[choice]
        create_folder(folder_name)
        
        while True:
            # Solicita ao usuário para tirar o print
            print(f"\nPor favor, tire um print dos membros do {folder_name.replace('_', ' ')}.")
            print("Pressione Enter para capturar a imagem da área de transferência (ou digite 'EXIT' para voltar ao menu):")
            
            user_input = input().strip().upper()
            
            # Verifica se o usuário quer voltar ao menu
            if user_input == "EXIT":
                break
            
            # Captura e salva a imagem
            save_image_from_clipboard(folder_name)
            sleep(1)  # Pequena pausa para evitar problemas com a área de transferência

if __name__ == "__main__":
    main()