"""Validação local de formato e dígitos verificadores de CNPJ."""

import re


_COMPACT = re.compile(r"[A-Z0-9]{12}[0-9]{2}")
_MASKED = re.compile(r"([A-Z0-9]{2})\.([A-Z0-9]{3})\.([A-Z0-9]{3})/([A-Z0-9]{4})-([0-9]{2})")
_SCIENTIFIC = re.compile(r"[+-]?[0-9]+(?:[.,][0-9]+)?E[+-]?[0-9]+")
_SHORT_NUMBER = re.compile(r"[0-9]{1,13}")


def _check_digit(prefix: str) -> str:
    # Receita Federal / Serpro: ASCII - 48, pesos de 2 a 9 da direita para a esquerda.
    # https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/publicacoes/documentos-tecnicos/cnpj/manual-dv-cnpj.pdf
    remainder = sum(
        (ord(character) - 48) * (2 + index % 8)
        for index, character in enumerate(reversed(prefix))
    ) % 11
    return "0" if remainder < 2 else str(11 - remainder)


def classify(value: str) -> str:
    """Classifica o texto original sem preencher, remover ou adivinhar dígitos."""
    text = value.strip()
    if not text:
        return "vazio"
    if not text.isascii():
        return "formato_invalido"
    text = text.upper()
    masked = _MASKED.fullmatch(text)
    if masked:
        text = "".join(masked.groups())
    elif not _COMPACT.fullmatch(text):
        if _SHORT_NUMBER.fullmatch(text):
            return "numerico_curto"
        if _SCIENTIFIC.fullmatch(text):
            return "notacao_cientifica"
        return "formato_invalido"
    if text == "00000000000000":
        return "formato_invalido"

    prefix = text[:12]
    first = _check_digit(prefix)
    if text[12:] != first + _check_digit(prefix + first):
        return "digitos_invalidos"
    return "valido_numerico" if prefix.isdecimal() else "valido_alfanumerico"
