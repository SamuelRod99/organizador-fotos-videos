
from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path

# Caminho relativo à pasta do projeto
pasta_projeto = Path(__file__).parent
pasta_foto = pasta_projeto / "fotos teste"

for foto in pasta_foto.iterdir():
    if not foto.is_file():
        continue

    try:
        imagem = Image.open(foto)
        exif = imagem.getexif()

        # Imprime as informações
        if exif:
            for codigo, valor in exif.items():
                nome = TAGS.get(codigo, codigo)
                print(f"{nome}: {valor}")
        else:
            print("Essa imagem não possui dados EXIF.")

        imagem.close()

    except Exception as erro:
        print(f"Não foi possível ler {foto.name}: {erro}")

    print("-" * 50)
