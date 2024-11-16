import os
from PIL import Image

def split_images_in_folder(input_folder, output_folder):
    # Garantir que a pasta de saída exista
    os.makedirs(output_folder, exist_ok=True)

    # Percorrer todas as imagens na pasta de entrada
    for filename in os.listdir(input_folder):
        # Verificar se o arquivo é uma imagem (png ou jpg)
        if filename.endswith((".png", ".jpg", ".jpeg")):
            # Caminho completo para a imagem de entrada
            input_path = os.path.join(input_folder, filename)
            # Nome base do arquivo sem extensão
            base_name = os.path.splitext(filename)[0]

            # Carregar a imagem
            image = Image.open(input_path)
            
            # Verificar se o tamanho da imagem é 512x256
            if image.size == (512, 256):
                # Dividir a imagem em metade esquerda e direita
                left_image = image.crop((0, 0, 256, 256))
                right_image = image.crop((256, 0, 512, 256))
                
                # Caminhos de saída para as imagens divididas
                left_output_path = os.path.join(output_folder, f"{base_name}_e.png")
                right_output_path = os.path.join(output_folder, f"{base_name}_d.png")
                
                # Salvar as imagens divididas
                left_image.save(left_output_path)
                right_image.save(right_output_path)
                
                print(f"Imagem dividida e salva como {left_output_path} e {right_output_path}")
            else:
                print(f"A imagem {filename} não tem o tamanho 512x256 e foi ignorada.")

# Exemplo de uso:
input_folder = "/home/henrique/Documentos/360° SR/CNN360/LR"    # Substitua pelo caminho da pasta com as imagens originais
output_folder = "/home/henrique/Documentos/360° SR/CNN360/LRD"     # Substitua pelo caminho da pasta onde salvar as imagens divididas
split_images_in_folder(input_folder, output_folder)
