# Fichamento de comentário bíblico

Monte uma ficha de pesquisa com edição, página, paráfrase e sua avaliação.

## Rodar

Python 3.10 ou mais recente. Cada execução lê um JSON local e imprime outro JSON no terminal.

```bash
python app.py exemplo.json
python -m unittest -v
```

## Uso

Preencha a página da edição consultada. O exemplo usa uma obra fictícia para demonstrar o formato. O programa separa a paráfrase da sua avaliação e exporta a ficha no campo `markdown`.

## Fontes e exemplos

Os exemplos incluem referências bíblicas, perguntas e anotações de demonstração. Consulte o texto e o contexto em uma [tradução publicada pela Sociedade Bíblica do Brasil](https://www.sbb.org.br/traducoes-da-biblia). Para aprofundar, o catálogo da [Nova Bíblia de Estudo Almeida](https://www.sbb.org.br/nova-almeida/biblias-de-estudo/biblia-de-estudo-almeida) e o do [Comentário Bíblico Pentecostal do Novo Testamento, CPAD](https://www.cpad.com.br/comentario-biblico-pentecostal-novo-testamento-/p) ajudam a identificar edições. Registre as páginas verificadas na sua própria consulta.

## Exportação para notas

Use `python app.py exemplo.json --markdown > relatorio.md` para exportar a ficha de leitura. O arquivo pode ser aberto diretamente no Obsidian ou em outro editor Markdown. O JSON continua sendo a saída padrão.

Também é possível encadear a ferramenta com outro comando usando `-` como entrada. Exemplo em um terminal Bash:

```bash
cat exemplo.json | python app.py -
```
