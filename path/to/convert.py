import os
from PIL import Image, ImageFilter

def unir_imagens_patches(pasta_imagens, prefixo="00000_patch_", formato=".png", aplicar_suavizacao=True, raio_borda=2):
    # Coletar todas as imagens que seguem o padrão "00000_patch_digit.png"
    imagens = sorted([img for img in os.listdir(pasta_imagens) if img.startswith(prefixo) and img.endswith(formato)])

    # Verificar se há 162 imagens
    if len(imagens) != 162:
        raise ValueError(f"Esperado 162 imagens, mas encontrado {len(imagens)}.")

    # Definir o tamanho de cada patch e o tamanho final da imagem
    largura_patch_original, altura_patch_original = 224, 224
    largura_total, altura_total = 3584, 1792  # Resolução final

    # Calcular o novo tamanho do patch após o ajuste
    largura_patch_novo = largura_total // 18  # 18 colunas
    altura_patch_novo = altura_total // 9     # 9 linhas

    # Criar uma nova imagem em branco com o tamanho da imagem final
    imagem_final = Image.new('RGB', (largura_total, altura_total))

    # Número de colunas e linhas
    num_colunas = 18
    num_linhas = 9

    # Colocar as imagens no local correto
    for idx, nome_imagem in enumerate(imagens):
        img_patch = Image.open(os.path.join(pasta_imagens, nome_imagem))

        # Redimensionar cada patch para o novo tamanho
        img_patch = img_patch.resize((largura_patch_novo, altura_patch_novo))

        # Calcular a posição x, y com base no índice
        coluna = idx % num_colunas
        linha = idx // num_colunas
        posicao_x = coluna * largura_patch_novo
        posicao_y = linha * altura_patch_novo

        # Colocar o patch na posição correta
        imagem_final.paste(img_patch, (posicao_x, posicao_y))

    # Se solicitado, aplicar suavização na imagem final
    if aplicar_suavizacao:
        imagem_final = imagem_final.filter(ImageFilter.GaussianBlur(raio_borda))

    # Salvar a imagem final
    imagem_final.save(os.path.join(pasta_imagens, "imagem_final_suavizada5.png"))
    print("Imagem final criada e salva como 'imagem_final_suavizada.png'!")

# Exemplo de uso
pasta_imagens = "dataset_28_224/sr_28_224"  # Altere para o caminho correto da pasta
unir_imagens_patches(pasta_imagens)
