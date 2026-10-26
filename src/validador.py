"""Define o mixin ValidadorAlternativas."""


class ValidadorAlternativas:
    """Mixin com as regras de validação das alternativas."""

    MIN_ALTERNATIVAS = 3
    MAX_ALTERNATIVAS = 5

    @classmethod
    def validar_quantidade(cls, alternativas: list[str]) -> bool:
        """Retorna True se houver entre 3 e 5 alternativas."""
        return (
            isinstance(alternativas, list)
            and cls.MIN_ALTERNATIVAS <= len(alternativas) <= cls.MAX_ALTERNATIVAS
        )

    @classmethod
    def validar_indice(cls, indice: int, alternativas: list[str]) -> bool:
        """Retorna True se o índice apontar para uma alternativa existente."""
        if not isinstance(indice, int) or isinstance(indice, bool):
            return False

        return 0 <= indice < len(alternativas)