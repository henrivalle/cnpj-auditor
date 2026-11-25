# CNPJ Auditor

[English](README.en.md)

Confira uma coluna de CNPJs antes de importar uma planilha ou colocar uma exportação em produção. A ferramenta valida o formato numérico e alfanumérico, identifica indícios de conversão em número pela planilha e gera um relatório com a linha e o status. O arquivo é processado localmente, e o relatório omite os CNPJs e os demais campos.

## Usar

Na raiz do repositório, com Python 3.9 ou posterior:

```bash
python3 -m cnpj_auditor exemplos/amostra.csv --delimitador ponto-e-virgula
```

A amostra inclui casos válidos e erros para demonstração. Ela retorna código `1`. Para conferir um arquivo real e salvar o relatório, informe o nome exato da coluna e o delimitador do CSV.

```bash
python3 -m cnpj_auditor clientes.csv --coluna cnpj --delimitador ponto-e-virgula > relatorio.csv
```

- **Entrada.** CSV em UTF-8, com ou sem BOM. O delimitador padrão é vírgula. Também são aceitos `ponto-e-virgula` e `tab`.
- **Saída.** CSV com `linha,status`. A linha é o início físico do registro, contando o cabeçalho e as quebras de linha dentro de campos entre aspas.
- **Códigos de saída.** `0` indica que todos os registros passaram. `1` indica problemas nas linhas ou ausência de um exemplo alfanumérico exigido. `2` indica erro de leitura, estrutura ou opção, com diagnóstico no terminal. Descarte qualquer relatório parcial quando a saída for `2`.

### Usar em um teste de migração

Prepare uma massa de teste com um CNPJ numérico e o exemplo alfanumérico `12.ABC.345/01DE-35`, publicado no manual oficial. Exporte a massa com o sistema que você quer testar e passe a exportação para o auditor.

```bash
python3 -m cnpj_auditor exportacao-de-teste.csv --exigir-alfanumerico
```

O comando falha se a exportação não contiver ao menos um CNPJ alfanumérico válido. Use também uma comparação de contagem ou conteúdo quando precisar detectar linhas ausentes ou alterações que ainda produzam um CNPJ válido.

### Interpretar o relatório

| Status | Significado |
| --- | --- |
| `valido_numerico`, `valido_alfanumerico` | Formato e dígitos verificadores válidos. |
| `numerico_curto`, `notacao_cientifica` | Possível perda de representação ao exportar. Confira o valor na origem. |
| `formato_invalido`, `digitos_invalidos` | Máscara, caracteres ou dígitos incompatíveis com o formato. |
| `vazio`, `colunas_inconsistentes` | Campo em branco ou linha com quantidade de colunas diferente do cabeçalho. |

A checagem verifica a representação e os dígitos. A consulta oficial de situação cadastral fica na Receita Federal. O programa não calcula tributos e não altera o CSV de origem.

## Fontes e contribuição

O cálculo segue o manual de dígitos verificadores da Receita Federal e do Serpro. O primeiro registro no novo formato foi emitido em 31 de julho de 2026, e os CNPJs numéricos existentes continuam válidos. [Manual oficial](https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/publicacoes/documentos-tecnicos/cnpj/manual-dv-cnpj.pdf) · [Cronograma e primeiro registro](https://www.gov.br/fazenda/pt-br/assuntos/noticias/2026/julho/receita-federal-gera-o-primeiro-cnpj-em-formato-alfanumerico)

Veja as [tarefas para iniciantes](https://github.com/henrivalle/cnpj-auditor/contribute) e o [guia de contribuição](CONTRIBUTING.md). Código sob [MIT](LICENSE).
