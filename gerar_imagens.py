import os
import math
from PIL import Image, ImageDraw

def obter_pontos_estrela(x, y, r_externo, r_interno):
    """Calcula os 10 vértices de uma estrela de 5 pontas."""
    pontos = []
    for i in range(10):
        r = r_externo if i % 2 == 0 else r_interno
        # Rotaciona para apontar a primeira ponta diretamente para cima (-90 graus)
        angulo = i * math.pi / 5 - math.pi / 2
        px = x + r * math.cos(angulo)
        py = y + r * math.sin(angulo)
        pontos.append((px, py))
    return pontos

def gerar_imagens():
    """Gera o verso e as 18 frentes das cartas salvando na pasta 'imagens'."""
    os.makedirs('imagens', exist_ok=True)
    
    # Paleta de Cores Vibrantes (Catppuccin Macchiato)
    vermelho = (243, 139, 168, 255)
    azul = (137, 180, 250, 255)
    verde = (166, 227, 161, 255)
    cores = [vermelho, azul, verde]
    
    # 1. Gerar imagem do Verso (verso.png)
    verso = Image.new('RGBA', (200, 200), (30, 30, 46, 255)) # Fundo cinza escuro azulado
    draw = ImageDraw.Draw(verso)
    # Padrão geométrico interno do verso
    draw.rectangle([10, 10, 190, 190], outline=(49, 50, 68, 255), width=4)
    draw.polygon([(100, 40), (160, 100), (100, 160), (40, 100)], outline=(137, 180, 250, 255), width=6)
    draw.polygon([(100, 60), (140, 100), (100, 140), (60, 100)], outline=(166, 227, 161, 255), width=3)
    draw.ellipse([90, 90, 110, 110], fill=(137, 180, 250, 255))
    verso.save('imagens/verso.png')
    
    # 2. Gerar 18 frentes de cartas (carta_1.png até carta_18.png)
    # Formas: Círculo (0), Quadrado (1), Triângulo (2), Cruz (3), Losango (4), Estrela (5)
    indice_imagem = 1
    for shape_type in range(6):
        for color in cores:
            # Fundo interno da carta revelada
            frente = Image.new('RGBA', (200, 200), (49, 50, 68, 255))
            draw = ImageDraw.Draw(frente)
            
            # Moldura sutil
            draw.rectangle([10, 10, 190, 190], outline=(69, 71, 90, 255), width=3)
            
            # Desenha a forma baseada no tipo
            if shape_type == 0:
                # Círculo
                draw.ellipse([50, 50, 150, 150], fill=color, outline=(255, 255, 255, 255), width=2)
            elif shape_type == 1:
                # Quadrado
                draw.rectangle([55, 55, 145, 145], fill=color, outline=(255, 255, 255, 255), width=2)
            elif shape_type == 2:
                # Triângulo
                draw.polygon([(100, 48), (50, 145), (150, 145)], fill=color, outline=(255, 255, 255, 255), width=2)
            elif shape_type == 3:
                # Cruz (desenhada como dois retângulos sobrepostos)
                draw.rectangle([85, 45, 115, 155], fill=color)
                draw.rectangle([45, 85, 155, 115], fill=color)
                draw.rectangle([85, 45, 115, 155], outline=(255, 255, 255, 255), width=2)
                draw.rectangle([45, 85, 155, 115], outline=(255, 255, 255, 255), width=2)
            elif shape_type == 4:
                # Losango
                draw.polygon([(100, 42), (158, 100), (100, 158), (42, 100)], fill=color, outline=(255, 255, 255, 255), width=2)
            elif shape_type == 5:
                # Estrela
                pontos = obter_pontos_estrela(100, 100, 58, 25)
                draw.polygon(pontos, fill=color, outline=(255, 255, 255, 255), width=2)
                
            frente.save(f'imagens/carta_{indice_imagem}.png')
            indice_imagem += 1
            
    print("Sucesso: 19 imagens de cartas geradas na pasta 'imagens'.")

if __name__ == '__main__':
    gerar_imagens()
