"""Audita uma coluna CSV sem reproduzir os valores de entrada."""

import argparse
import csv
import sys
from typing import TextIO

from . import classify


_DELIMITERS = {"virgula": ",", "ponto-e-virgula": ";", "tab": "\t"}
_VALID = {"valido_numerico", "valido_alfanumerico"}


class InputError(Exception):
    """O arquivo não pode ser auditado com as opções fornecidas."""


def audit(source: TextIO, report: TextIO, column: str, delimiter: str) -> tuple[bool, bool]:
    reader = csv.reader(source, delimiter=delimiter, strict=True)
    header = next(reader, None)
    if not header:
        raise InputError("Cabeçalho CSV ausente.")
    if header.count(column) != 1:
        raise InputError("A coluna escolhida deve aparecer exatamente uma vez no cabeçalho.")
    column_index = header.index(column)

    writer = csv.writer(report, lineterminator="\n")
    writer.writerow(("linha", "status"))
    has_records = False
    has_problems = False
    has_alphanumeric = False
    next_line = reader.line_num + 1
    for row in reader:
        record_line, next_line = next_line, reader.line_num + 1
        if not row:
            continue
        has_records = True
        status = (
            classify(row[column_index]) if len(row) == len(header)
            else "colunas_inconsistentes"
        )
        writer.writerow((record_line, status))
        has_problems |= status not in _VALID
        has_alphanumeric |= status == "valido_alfanumerico"

    if not has_records:
        raise InputError("O CSV não contém registros para auditar.")
    return has_problems, has_alphanumeric


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audita formato e dígitos de CNPJ em um CSV local."
    )
    parser.add_argument("arquivo", help="CSV em UTF-8")
    parser.add_argument("--coluna", default="cnpj", help="nome exato da coluna (padrão: cnpj)")
    parser.add_argument("--delimitador", choices=_DELIMITERS, default="virgula")
    parser.add_argument(
        "--exigir-alfanumerico",
        action="store_true",
        help="exige pelo menos um CNPJ alfanumérico válido, para testar uma exportação",
    )
    args = parser.parse_args()

    try:
        with open(args.arquivo, encoding="utf-8-sig", newline="") as source:
            has_problems, has_alphanumeric = audit(
                source, sys.stdout, args.coluna, _DELIMITERS[args.delimitador]
            )
    except InputError as exc:
        print(exc, file=sys.stderr)
        return 2
    except (csv.Error, UnicodeError):
        print("Não foi possível processar o CSV em UTF-8.", file=sys.stderr)
        return 2
    except OSError:
        print("Não foi possível abrir o arquivo ou gravar o relatório.", file=sys.stderr)
        return 2

    if args.exigir_alfanumerico and not has_alphanumeric:
        print("Nenhum CNPJ alfanumérico válido foi encontrado.", file=sys.stderr)
        return 1
    return int(has_problems)


if __name__ == "__main__":
    raise SystemExit(main())
