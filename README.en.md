# CNPJ Auditor

[Português](README.md)

Audit Brazilian company registration numbers (CNPJ) in a local CSV. The tool checks legacy numeric and new alphanumeric forms, flags common spreadsheet conversions, and emits a report containing only physical line numbers and status codes.

```bash
python3 -m cnpj_auditor exemplos/amostra.csv --delimitador ponto-e-virgula
```

Run from the repository root with Python 3.9 or later. The sample includes intentional errors and exits with code 1. Use `--coluna` for a different column name. Select `virgula`, `ponto-e-virgula`, or `tab` through `--delimitador`. Input is UTF-8, optionally with a BOM. Status codes and diagnostics are in Portuguese. Exit codes are 0 for a clean report, 1 for findings, and 2 for unreadable or unusable input.

Use `--exigir-alfanumerico` with a controlled test export that includes the official example `12.ABC.345/01DE-35`. It fails when the exported file contains no valid alphanumeric CNPJ. The check covers shape and check digits. Registration status is available through the Brazilian Federal Revenue Service.

See the [official calculation manual](https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/publicacoes/documentos-tecnicos/cnpj/manual-dv-cnpj.pdf), [contributing guide](CONTRIBUTING.md), and [MIT license](LICENSE).
