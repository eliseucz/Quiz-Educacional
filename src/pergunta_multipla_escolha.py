"""Define a classe PerguntaMultiplaEscolha."""

from .pergunta import Pergunta
from .validador import ValidadorAlternativas


class PerguntaMultiplaEscolha(Pergunta, ValidadorAlternativas):
    """Pergunta de múltipla escolha, com herança múltipla."""

    def validar(self) -> bool:
        """Confere as duas regras da pergunta usando o mixin."""
        quantidade_ok = self.validar_quantidade(self.alternativas)
        indice_ok = self.validar_indice(
            self.indice_resposta_correta, self.alternativas
        )
        return quantidade_ok and indice_ok

    def __str__(self) -> str:
        """Reaproveita o __str__ de Pergunta e acrescenta o tipo."""
        return f"[Múltipla escolha] {super().__str__()}"