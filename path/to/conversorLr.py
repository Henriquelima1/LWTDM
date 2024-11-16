import os
from PIL import Image

# Função para redimensionar a imagem para dimensões divisíveis por 28
def resize_image(img, target_width, target_height):
    # Redimensionar para as novas dimensões divisíveis por 28
    return img.resize((target_width, target_height), Image.Resampling.LANCZOS)

# Função para cortar a imagem em blocos de 28x28
def cut_image_into_patches(img_path, output_dir, patch_size=28, resize_dims=(504, 252)):
    # Abrir a imagem
    img = Image.open(img_path)

    # Redimensionar a imagem para dimensões divisíveis por 28
    img = resize_image(img, *resize_dims)

    width, height = img.size

    # Criar diretório de saída se não existir
    os.makedirs(output_dir, exist_ok=True)

    patch_number = 0
    # Iterar sobre a imagem e cortar em blocos de 28x28
    for top in range(0, height, patch_size):
        for left in range(0, width, patch_size):
            # Definir a área do bloco
            box = (left, top, left + patch_size, top + patch_size)
            patch = img.crop(box)

            # Salvar o bloco
            patch.save(os.path.join(output_dir, f"{os.path.basename(img_path).split('.')[0]}_patch_{patch_number:04d}.png"))
            patch_number += 1

    print(f"{patch_number} blocos de {patch_size}x{patch_size} foram gerados para a imagem {img_path}.")

# Função principal para processar as primeiras 100 imagens
def process_images(input_dir, output_dir, resize_dims=(504, 252), num_images=25):
    # Listar arquivos no diretório de entrada
    img_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Processar as primeiras 'num_images' imagens
    for i, img_file in enumerate(img_files[:num_images]):
        img_path = os.path.join(input_dir, img_file)
        print(f"Processando {i+1}/{num_images}: {img_path}")
        cut_image_into_patches(img_path, output_dir, resize_dims=resize_dims)

# Exemplo de uso
input_directory = '/home/henrique/Documentos/360° SR/CNN360/LR'  # Diretório onde estão as imagens 512x256
output_directory = 'dataset_28_224/lr_28'   # Diretório para salvar os blocos 28x28
num_images = 25  # Número de imagens que você deseja processar

# Definir dimensões para redimensionamento (divisíveis por 28)
resize_dims = (504, 252)  # Dimensões ajustadas para serem divisíveis por 28

# Processar as primeiras 100 imagens
process_images(input_directory, output_directory, resize_dims=resize_dims, num_images=num_images)
