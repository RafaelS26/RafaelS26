"""
foto_para_ascii_svg.py

Converte uma foto em um retrato ASCII monocromatico, animado (digita
sozinho na tela), em formato SVG -- pronto pra usar no README do
perfil do GitHub (repositorio <seu-usuario>/<seu-usuario>).

>>> COMO USAR <<<
1. Coloque sua foto na mesma pasta deste script.
2. Troque o valor de CAMINHO_DA_FOTO logo abaixo pelo nome do seu
   arquivo (ex: "minha_foto.jpg").
   >>> AQUI E ONDE VOCE COLOCA O CAMINHO/NOME DA SUA FOTO <<<
3. Instale a dependencia (uma vez so): pip install Pillow
4. Rode: python foto_para_ascii_svg.py
5. Vai gerar o arquivo avi-ascii.svg na mesma pasta.
6. Suba esse .svg pro repositorio <seu-usuario>/<seu-usuario> no GitHub.
7. No README.md desse repositorio, coloque (veja tambem
   trecho_readme.md, que ja vem pronto):
   <img src="https://raw.githubusercontent.com/RafaelS26/RafaelS26/main/avi-ascii.svg" alt="ASCII portrait" />
"""

from PIL import Image

# ============================================================
# >>> COLOQUE AQUI O CAMINHO/NOME DA SUA FOTO <<<
CAMINHO_DA_FOTO = "C:/Users/Rafael/OneDrive/Documentos/GithbubPerfil/WhatsApp Image 2026-03-18 at 11.38.30.jpeg"
# ============================================================

ARQUIVO_SAIDA = "avi-ascii.svg"
LARGURA_CARACTERES = 70          # quantos caracteres de largura tera o retrato
RAMPA = " .:-=+*#%@"             # do mais claro pro mais escuro
FONTE_TAMANHO = 8                # tamanho da fonte no SVG (px)
ESPACAMENTO_LINHA = FONTE_TAMANHO * 1.0
ATRASO_ENTRE_LINHAS = 0.05       # segundos entre cada linha "digitando"
COR_TEXTO = "#e0dada"            # verde neon (estilo terminal). Troque se quiser outra cor
COR_FUNDO = "#212122"            # fundo escuro estilo GitHub dark mode


def imagem_para_ascii(caminho, largura_chars):
    img = Image.open(caminho).convert("L")  # converte pra escala de cinza
    razao_altura = img.height / img.width
    # 0.55 compensa o fato de um caractere ser mais alto do que largo
    altura_chars = max(1, int(largura_chars * razao_altura * 0.55))
    img = img.resize((largura_chars, altura_chars))

    linhas = []
    pixels = img.load()
    for y in range(altura_chars):
        linha = ""
        for x in range(largura_chars):
            brilho = pixels[x, y]
            indice = int((brilho / 255) * (len(RAMPA) - 1))
            linha += RAMPA[indice]
        linhas.append(linha)
    return linhas


def gerar_svg(linhas):
    largura_svg = LARGURA_CARACTERES * (FONTE_TAMANHO * 0.6) + 20
    altura_svg = len(linhas) * ESPACAMENTO_LINHA + 20

    partes = []
    partes.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {largura_svg:.0f} {altura_svg:.0f}" '
        f'font-family="monospace" font-size="{FONTE_TAMANHO}">'
    )
    partes.append("<style>.linha { fill: %s; opacity: 0; white-space: pre; }</style>" % COR_TEXTO)
    partes.append(f'<rect width="100%" height="100%" fill="{COR_FUNDO}" />')

    for i, linha in enumerate(linhas):
        y = 15 + i * ESPACAMENTO_LINHA
        inicio = i * ATRASO_ENTRE_LINHAS
        linha_escapada = (
            linha.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )
        partes.append(
            f'<text x="10" y="{y:.1f}" class="linha">{linha_escapada}'
            f'<animate attributeName="opacity" from="0" to="1" '
            f'begin="{inicio:.2f}s" dur="0.15s" fill="freeze" />'
            f"</text>"
        )

    partes.append("</svg>")
    return "\n".join(partes)


if __name__ == "__main__":
    linhas = imagem_para_ascii(CAMINHO_DA_FOTO, LARGURA_CARACTERES)
    svg = gerar_svg(linhas)
    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Pronto! Arquivo gerado: {ARQUIVO_SAIDA}")