import os
from PIL import Image

def merge_images_in_folder(input_folder, output_folder):
    # Garantir que a pasta de saída exista
    os.makedirs(output_folder, exist_ok=True)

    # Obter uma lista de todas as imagens na pasta de entrada
    images = [f for f in os.listdir(input_folder) if f.endswith((".png", ".jpg", ".jpeg"))]

    # Filtrar apenas imagens com o sufixo _e ou _d
    left_images = sorted([img for img in images if img.endswith("_e.png")])
    right_images = sorted([img for img in images if img.endswith("_d.png")])

    # Iterar sobre as imagens de acordo com os pares _e e _d
    for left_img_name, right_img_name in zip(left_images, right_images):
        # Nome base para a imagem de saída
        base_name = left_img_name.replace("_e.png", "")

        # Caminhos completos para as imagens esquerda e direita
        left_img_path = os.path.join(input_folder, left_img_name)
        right_img_path = os.path.join(input_folder, right_img_name)

        # Abrir as imagens
        left_img = Image.open(left_img_path)
        right_img = Image.open(right_img_path)

        # Verificar se ambas as imagens têm o tamanho correto de 1024x1024
        if left_img.size == (1024, 1024) and right_img.size == (1024, 1024):
            # Criar uma nova imagem de 2048x1024
            merged_img = Image.new("RGB", (2048, 1024))
            
            # Colar as imagens esquerda e direita na nova imagem
            merged_img.paste(left_img, (0, 0))
            merged_img.paste(right_img, (1024, 0))
            
            # Caminho de saída para a imagem unida
            output_path = os.path.join(output_folder, f"{base_name}.png")
            
            # Salvar a imagem unida
            merged_img.save(output_path)
            
            print(f"Imagem unida salva como {output_path}")
        else:
            print(f"As imagens {left_img_name} e {right_img_name} não têm o tamanho 1024x1024 e foram ignoradas.")

# Exemplo de uso:
input_folder = "path/to/datasetOmniD_256_1024/sr_256_1024"    # Substitua pelo caminho da pasta com as imagens de entrada
output_folder = "path/to/datasetOmniD_256_1024/sr_256_1024D"     # Substitua pelo caminho da pasta onde salvar as imagens unidas
merge_images_in_folder(input_folder, output_folder)
