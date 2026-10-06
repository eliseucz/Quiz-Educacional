"""Definição inicial da especialização de pergunta de múltipla escolha."""

from .pergunta import Pergunta
from .validador import ValidadorAlternativas


class PerguntaMultiplaEscolha(Pergunta, ValidadorAlternativas):
    """Representa uma pergunta de múltipla escolha com herança múltipla."""

    pass
