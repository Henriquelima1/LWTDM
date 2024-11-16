  
import os
from PIL import Image

# Função para processar uma única imagem
def process_image(img_path, output_dir):
    # Abrindo a imagem
    img = Image.open(img_path)

    # Verificar se o tamanho é 2048x1024
    if img.size != (2048, 1024):
        print(f"Imagem {img_path} tem tamanho incorreto, ignorando.")
        return

    # Cortar a imagem ao meio
    left_img = img.crop((0, 0, 1024, 1024))  # Parte esquerda
    right_img = img.crop((1024, 0, 2048, 1024))  # Parte direita

    # Redimensionar para 896x896
    left_img = left_img.resize((896, 896), Image.Resampling.LANCZOS)
    right_img = right_img.resize((896, 896), Image.Resampling.LANCZOS)

    # Gerar nomes dos arquivos de saída
    base_name = os.path.splitext(os.path.basename(img_path))[0]
    left_output_path = os.path.join(output_dir, f"{base_name}_left_896x896.png")
    right_output_path = os.path.join(output_dir, f"{base_name}_right_896x896.png")

    # Salvar as imagens resultantes
    left_img.save(left_output_path)
    right_img.save(right_output_path)

# Função principal para processar várias imagens
def process_images(input_dir, output_dir, num_images=100):
    # Criar o diretório de saída se não existir
    os.makedirs(output_dir, exist_ok=True)

    # Listar arquivos no diretório de entrada
    img_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Processar até 'num_images' imagens
    for i, img_file in enumerate(img_files[:num_images]):
        img_path = os.path.join(input_dir, img_file)
        process_image(img_path, output_dir)
        print(f"Processada {i+1}/{num_images} imagens.")

# Exemplo de uso
input_directory = '/home/henrique/Documentos/360° SR/CNN360/HR'  # Diretório onde estão as imagens 2048x1024
output_directory = 'hr_224'  # Diretório para salvar as imagens resultantes
num_images = 50  # Número de imagens que você deseja processar

# Processa as primeiras 'num_images' imagens
process_images(input_directory, output_directory, num_images)
