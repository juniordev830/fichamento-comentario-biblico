'Monte uma ficha de pesquisa com edição, página, paráfrase e sua avaliação.'


def texto(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Use texto não vazio.")
    return value.strip()


def inteiro(value, minimo=0):
    if type(value) is not int or value < minimo:
        raise ValueError(f"Use um número inteiro a partir de {minimo}.")
    return value


def run(data):
    inicio = inteiro(data["pagina_inicial"], 1)
    fim = inteiro(data.get("pagina_final", inicio), inicio)
    pagina = f"p. {inicio}" if inicio == fim else f"p. {inicio}–{fim}"
    ano = inteiro(data["ano"], 1)
    fonte = f"{texto(data['autor'])}. {texto(data['obra'])}. {texto(data['edicao'])}, {ano}, {pagina}."
    referencia = texto(data["referencia"])
    parafrase = texto(data["parafrase"])
    avaliacao = texto(data["avaliacao"])
    markdown = f"# {referencia}\n\n{fonte}\n\n## Paráfrase\n\n{parafrase}\n\n## Avaliação\n\n{avaliacao}"
    return {"fonte": fonte, "localizador": pagina, "markdown": markdown}


import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada", type=Path, help="Arquivo JSON com os dados")
    args = parser.parse_args()

    try:
        with args.entrada.open(encoding="utf-8") as source:
            data = json.load(source)
        if not isinstance(data, dict):
            raise ValueError("A entrada deve ser um objeto JSON.")
        result = run(data)
    except (KeyError, TypeError, ValueError, OSError) as exc:
        parser.exit(2, f"Erro nos dados ou na execução: {exc}\n")

    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
