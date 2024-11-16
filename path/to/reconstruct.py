import os
import re
from PIL import Image
import numpy as np

def get_patch_info(filename):
    # Extrair o nome base e a posição a partir do padrão "00000_patch_0094.png"
    match = re.match(r"(\d{5})_patch_(\d{4})\.png", filename)
    if match:
        image_name = match.group(1)
        patch_pos = int(match.group(2))  # posição do patch como um número inteiro
        return image_name, patch_pos
    return None, None

def reconstruct_image(patches_dir, output_dir, patch_size=(224, 224), grid_shape=(16, 16)):
    os.makedirs(output_dir, exist_ok=True)
    
    # Agrupar patches por nome de imagem
    patches_by_image = {}
    
    for patch_file in os.listdir(patches_dir):
        if patch_file.endswith('.png'):
            img_name, patch_pos = get_patch_info(patch_file)
            if img_name is not None:
                if img_name not in patches_by_image:
                    patches_by_image[img_name] = []
                patches_by_image[img_name].append((patch_pos, patch_file))
    
    # Reconstruir as imagens a partir dos patches
    for img_name, patches in patches_by_image.items():
        # Criar uma imagem vazia para reconstrução
        reconstructed_img = Image.new('RGB', (grid_shape[1] * patch_size[0], grid_shape[0] * patch_size[1]))
        
        # Organizar os patches de acordo com a posição e montar a imagem
        for patch_pos, patch_file in patches:
            patch = Image.open(os.path.join(patches_dir, patch_file))
            
            # Calcular a posição do patch na imagem original
            row = patch_pos // grid_shape[1]
            col = patch_pos % grid_shape[1]
            reconstructed_img.paste(patch, (col * patch_size[0], row * patch_size[1]))
        
        # Salvar a imagem reconstruída
        output_path = os.path.join(output_dir, f"{img_name}_reconstructed.png")
        reconstructed_img.save(output_path)
        print(f"Imagem {img_name} reconstruída e salva em {output_path}.")

# Exemplo de uso
patches_directory = 'dataset_28_224/sr_28_224'  # Diretório onde os patches estão localizados
output_directory = 'dataset_28_224/SR'  # Diretório para salvar as imagens reconstruídas

# Tamanho dos patches e a grade em que eles estão organizados (assumindo 16x16 blocos de 224x224)
patch_size = (224, 224)
grid_shape = (16, 16)  # Isso deve ser ajustado de acordo com a quantidade de patches por imagem

# Reconstruir as imagens
reconstruct_image(patches_directory, output_directory, patch_size, grid_shape)
