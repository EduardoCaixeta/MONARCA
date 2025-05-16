from dao import PlayerDAO
from extractor import PowerExtractor
from datetime import datetime
import os
from image import ImageInfo
dao = PlayerDAO("power.db")
extractor = PowerExtractor(dao)

def scan_images_folder(folder_path):
    image_infos = []
    # Caminho para a pasta 'images', que está uma pasta acima da pasta do script atual
    images_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images")
    images_dir = os.path.abspath(images_dir)  # resolve o '..' para caminho absoluto

    print(images_dir)

    # Listar arquivos na pasta images_dir
    for fname in os.listdir(images_dir):
        if fname.lower().endswith(".png"):
            try:
                info = ImageInfo.from_filename(os.path.join(images_dir,fname))
                image_infos.append(info)
            except ValueError as e:
                print(f"Warning: {e}")
    return image_infos

# Exemplo
folder = "images"
all_images = scan_images_folder(folder)
print(all_images)
extractor.process(all_images)
