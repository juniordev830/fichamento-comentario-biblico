'Monte uma ficha de pesquisa com edição, página, paráfrase e sua avaliação.'

import re


def texto(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Use texto não vazio.")
    return value.strip()


def inteiro(value, minimo=0):
    if type(value) is not int or value < minimo:
        raise ValueError(f"Use um número inteiro a partir de {minimo}.")
    return value


def texto_markdown(value):
    """Preserva metadados como texto em uma única linha do documento."""
    uma_linha = " ".join(value.split())
    return re.sub(r"([\\`*_{}\[\]()<>#+!|~&.\-])", r"\\\1", uma_linha)


def run(data):
    if not isinstance(data, dict):
        raise ValueError("A entrada deve ser um objeto JSON.")
    inicio = inteiro(data["pagina_inicial"], 1)
    fim = inteiro(data.get("pagina_final", inicio), inicio)
    pagina = f"p. {inicio}" if inicio == fim else f"p. {inicio}–{fim}"
    ano = inteiro(data["ano"], 1)
    fonte = f"{texto(data['autor'])}. {texto(data['obra'])}. {texto(data['edicao'])}, {ano}, {pagina}."
    referencia = texto(data["referencia"])
    parafrase = texto(data["parafrase"])
    avaliacao = texto(data["avaliacao"])
    markdown = (
        f"# {texto_markdown(referencia)}\n\n{texto_markdown(fonte)}"
        f"\n\n## Paráfrase\n\n{parafrase}\n\n## Avaliação\n\n{avaliacao}"
    )
    resultado = {"fonte": fonte, "localizador": pagina, "markdown": markdown}
    for campo, titulo in (("palavras_chave", "Palavras-chave"), ("questoes", "Questões de pesquisa")):
        if campo not in data:
            continue
        itens = data[campo]
        if not isinstance(itens, list):
            raise ValueError(f"{campo} deve ser uma lista de textos.")
        valores = list(dict.fromkeys(texto(item) for item in itens))
        resultado[campo] = valores
        if valores:
            resultado["markdown"] += "\n\n## " + titulo + "\n\n" + "\n".join("- " + texto_markdown(item) for item in valores)
    return resultado


import argparse
from contextlib import nullcontext
import sys
import json
from pathlib import Path


def objeto_sem_campos_repetidos(pares):
    objeto = {}
    for chave, valor in pares:
        if chave in objeto:
            raise ValueError(f"Campo JSON repetido: {chave!r}.")
        objeto[chave] = valor
    return objeto


def rejeitar_constante_json(constante):
    raise ValueError(f"Constante numérica inválida em JSON: {constante}.")


MAX_JSON_BYTES = 1_000_000


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada", help="Arquivo JSON com os dados ou - para a entrada padrão")
    parser.add_argument("--markdown", action="store_true", help="Exportar a ficha de leitura em MARKDOWN")
    args = parser.parse_args()

    try:
        entrada = nullcontext(sys.stdin.buffer) if args.entrada == "-" else Path(args.entrada).open("rb")
        with entrada as source:
            raw = source.read(MAX_JSON_BYTES + 1)
        if len(raw) > MAX_JSON_BYTES:
            raise ValueError("JSON excede o limite de 1 MB.")
        data = json.loads(
            raw.decode("utf-8-sig"),
                object_pairs_hook=objeto_sem_campos_repetidos,
                parse_constant=rejeitar_constante_json,
            )
        if not isinstance(data, dict):
            raise ValueError("A entrada deve ser um objeto JSON.")
        result = run(data)
    except RecursionError:
        parser.exit(2, "O JSON tem níveis de aninhamento demais.\n")
    except (KeyError, TypeError, ValueError, UnicodeError, OSError) as exc:
        parser.exit(2, f"Erro nos dados ou na execução: {exc}\n")

    sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    if args.markdown:
        print(result['markdown'])
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()

