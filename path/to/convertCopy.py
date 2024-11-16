import os
import numpy as np
from PIL import Image
import cv2  # Para processamento de imagem

def calcular_ws_psnr(imagem_original, imagem_suavizada):
    """Calcula o WS-PSNR entre duas imagens."""
    mse = np.mean((imagem_original - imagem_suavizada) ** 2)
    if mse == 0:  # Imagens idênticas
        return float('inf')
    max_pixel = 255.0
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    return psnr

def suavizar_imagem(imagem_array, sigma):
    """Aplica um filtro gaussiano para suavizar a imagem."""
    return cv2.GaussianBlur(imagem_array, (0, 0), sigma)

def suavizar_ate_ws_psnr(imagem_path, ws_psnr_desejado):
    """Suaviza a imagem até que o WS-PSNR atinja o valor desejado."""
    # Carregar a imagem
    imagem_original = Image.open(imagem_path).convert('RGB')
    imagem_original_array = np.array(imagem_original)

    # Inicializa o sigma para o filtro gaussiano
    sigma = 2
    ws_psnr_atual = calcular_ws_psnr(imagem_original_array, imagem_original_array)  # PSNR inicial com a própria imagem

    print(f"PSNR inicial: {ws_psnr_atual:.2f}")

    while ws_psnr_atual >= ws_psnr_desejado:  # Suaviza até que PSNR caia abaixo do desejado
        # Suavizar a imagem
        imagem_suavizada_array = suavizar_imagem(imagem_original_array, sigma)
        # Calcular WS-PSNR
        ws_psnr_atual = calcular_ws_psnr(imagem_original_array, imagem_suavizada_array)

        print(f"PSNR com sigma {sigma}: {ws_psnr_atual:.2f}")

        # Aumenta o sigma para suavizar mais
        sigma += 0.5  # Ajuste para um incremento mais suave

    # Salvar a imagem suavizada
    imagem_suavizada = Image.fromarray(imagem_suavizada_array)
    imagem_suavizada.save(os.path.join(os.path.dirname(imagem_path), "imagem10.png"))
    print(f"Imagem suavizada criada com WS-PSNR: {ws_psnr_atual:.2f} e salva como 'imagem_suavizada.png'!")

# Exemplo de uso
imagem_path = "/home/henrique/Documentos/360° SR/CNN360/HR/00000.png"  # Altere para o caminho correto da imagem
ws_psnr_desejado = 35  # Defina o WS-PSNR desejado
suavizar_ate_ws_psnr(imagem_path, ws_psnr_desejado)
