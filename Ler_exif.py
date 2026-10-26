from PIL import Image
from pathlib import Path
from datetime import datetime
from pathlib import Path


## Escolha do usuário
print("Como deseja separar as fotos?")
print("1 - Ano")
print("2 - Mês")
print("3 - Dia")

opcao = input("Escolha uma opção: ")


todas_fotos = []
# Caminho relativo à pasta do projeto
pasta_projeto = Path(__file__).parent
pasta_foto = pasta_projeto / "fotos teste"

# Lê as fotos e suas datas
for foto in pasta_foto.iterdir():

    # Pula o item atual se ele *NÃO* for um arquivo (ex: pasta)
    if not foto.is_file():
        continue

    try:
        with Image.open(foto) as imagem:
            exif = imagem.getexif()

            # Obtém a data em que a foto foi tirada
            data = exif.get(36867)  # DateTimeOriginal

        # Imprime as informações
            if data is None:
                data = exif.get(306)  # DateTime

            # Adiciona as informações ao dicionário
            todas_fotos.append({
                "nome": foto.name,
                "data": datetime.strptime(data, "%Y:%m:%d %H:%M:%S")
                        if data else None})

    except Exception as erro:
        print(f"Não foi possível ler {foto.name}: {erro}")

print(todas_fotos)


# Função para separar por data
def separar_por_data(opcao, todas_fotos):
    listas = {}
    lista_sem_data = []

    for foto in todas_fotos:
        data = foto["data"]

        if data is None:
            lista_sem_data.append(foto)
            continue

        if opcao == 1:
            separacao = str(data.year)
        elif opcao == 2:
            separacao = data.strftime("%Y-%m")
        elif opcao == 3:
            separacao = data.strftime("%Y-%m-%d")

        if separacao not in listas:
            listas[separacao] = []
        
        listas[separacao].append(foto)

    return listas, lista_sem_data


listas, lista_sem_data = separar_por_data(int(opcao), todas_fotos)

# Imprime as fotos separadas por período
for periodo, fotos in sorted(listas.items()):
    print(f"\nPeríodo: {periodo}")

    for foto in fotos:
        print(f"  Nome: {foto['nome']} | Data: {foto['data']}")

# Imprime as fotos sem data
print("\nFotos sem data:")

for foto in lista_sem_data:
    print(f"  Nome: {foto['nome']}")

#cria pasta principal
pasta_fotos_separadas = pasta_projeto / "fotos_separadas"
pasta_fotos_separadas.mkdir(exist_ok=True)

# Cria as pastas e move as fotos com data
for periodo, fotos in listas.items():

    for foto in fotos:
        data = foto["data"]

        # Pasta do ano
        pasta_destino = pasta_fotos_separadas / str(data.year)

        # Separação por mês
        if int(opcao) == 2:
            ano_mes = data.strftime("%Y-%m")
            pasta_destino = pasta_destino / ano_mes

        # Separação por dia
        elif int(opcao) == 3:
            ano_mes = data.strftime("%Y-%m")
            ano_mes_dia = data.strftime("%Y-%m-%d")

            pasta_destino = pasta_destino / ano_mes / ano_mes_dia

        # Cria toda a hierarquia de pastas
        pasta_destino.mkdir(parents=True, exist_ok=True)

        # Localiza e move a foto
        arquivo = pasta_foto / foto["nome"]
        arquivo.rename(pasta_destino / foto["nome"])

# Cria a pasta para fotos sem data
if lista_sem_data:
    pasta_sem_data = pasta_fotos_separadas / "sem_data"
    pasta_sem_data.mkdir(parents=True, exist_ok=True)

    for foto in lista_sem_data:
        arquivo = pasta_foto / foto["nome"]
        arquivo.rename(pasta_sem_data / foto["nome"])




