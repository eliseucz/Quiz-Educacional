"""Define a classe Pergunta do sistema de quiz educacional."""


class Pergunta:
    """Representa uma pergunta de múltipla escolha."""

    # Peso (pontos) de cada nível de dificuldade.
    # Nas próximas etapas esses valores virão do settings.json.
    PESOS_POR_DIFICULDADE = {"FÁCIL": 1, "MÉDIO": 2, "DIFÍCIL": 3}
    DIFICULDADES_VALIDAS = set(PESOS_POR_DIFICULDADE)

    def __init__(
        self,
        enunciado: str,
        alternativas: list[str],
        indice_resposta_correta: int,
        dificuldade: str,
        tema: str,
    ):
        self.enunciado = enunciado
        self.alternativas = alternativas
        self.indice_resposta_correta = indice_resposta_correta
        self.dificuldade = dificuldade
        self.tema = tema

    @property
    def enunciado(self) -> str:
        """Retorna o enunciado da pergunta."""
        return self._enunciado

    @enunciado.setter
    def enunciado(self, valor: str) -> None:
        """Valida e define o enunciado."""
        if not isinstance(valor, str):
            raise TypeError("O enunciado deve ser uma string.")

        if not valor.strip():
            raise ValueError("O enunciado não pode ser vazio.")

        self._enunciado = valor.strip()

    @property
    def alternativas(self) -> list[str]:
        """Retorna uma cópia das alternativas."""
        return self._alternativas.copy()

    @alternativas.setter
    def alternativas(self, valor: list[str]) -> None:
        """Valida e define as alternativas."""
        if not isinstance(valor, list):
            raise TypeError("As alternativas devem ser uma lista.")

        if not 3 <= len(valor) <= 5:
            raise ValueError(
                "A pergunta deve possuir entre 3 e 5 alternativas."
            )

        alternativas_validas = []

        for alternativa in valor:
            if not isinstance(alternativa, str):
                raise TypeError(
                    "Cada alternativa deve ser uma string."
                )

            if not alternativa.strip():
                raise ValueError(
                    "As alternativas não podem ser vazias."
                )

            alternativas_validas.append(alternativa.strip())

        self._alternativas = alternativas_validas

    @property
    def indice_resposta_correta(self) -> int:
        """Retorna o índice da resposta correta."""
        return self._indice_resposta_correta

    @indice_resposta_correta.setter
    def indice_resposta_correta(self, valor: int) -> None:
        """Valida e define o índice da resposta correta."""
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise TypeError(
                "O índice da resposta correta deve ser um inteiro."
            )

        if not 0 <= valor < len(self._alternativas):
            raise ValueError(
                "O índice da resposta correta é inválido."
            )

        self._indice_resposta_correta = valor

    @property
    def dificuldade(self) -> str:
        """Retorna a dificuldade da pergunta."""
        return self._dificuldade

    @dificuldade.setter
    def dificuldade(self, valor: str) -> None:
        """Valida e define a dificuldade."""
        if not isinstance(valor, str):
            raise TypeError(
                "A dificuldade deve ser uma string."
            )

        if valor not in self.DIFICULDADES_VALIDAS:
            raise ValueError(
                "A dificuldade deve ser FÁCIL, MÉDIO ou DIFÍCIL."
            )

        self._dificuldade = valor

    @property
    def tema(self) -> str:
        """Retorna o tema da pergunta."""
        return self._tema

    @tema.setter
    def tema(self, valor: str) -> None:
        """Valida e define o tema."""
        if not isinstance(valor, str):
            raise TypeError(
                "O tema deve ser uma string."
            )

        if not valor.strip():
            raise ValueError(
                "O tema não pode ser vazio."
            )

        self._tema = valor.strip()

    @property
    def peso(self) -> int:
        """Retorna quantos pontos a pergunta vale (depende da dificuldade)."""
        return self.PESOS_POR_DIFICULDADE[self._dificuldade]

    def validar_alternativas(self) -> bool:
        """Verifica se a quantidade de alternativas é válida."""
        return 3 <= len(self._alternativas) <= 5

    def validar_indice_resposta(self) -> bool:
        """Verifica se o índice aponta para uma alternativa existente."""
        return 0 <= self._indice_resposta_correta < len(
            self._alternativas
        )

    def __str__(self) -> str:
        """Retorna um resumo da pergunta."""
        return (
            f"{self._enunciado} "
            f"({self._tema} - {self._dificuldade})"
        )

    def __eq__(self, outra) -> bool:
        """Compara perguntas pelo enunciado e pelo tema."""
        if not isinstance(outra, Pergunta):
            return NotImplemented

        return (
            self._enunciado == outra._enunciado
            and self._tema == outra._tema
        )

    def __hash__(self) -> int:
        """Permite usar Pergunta em set/dict (coerente com o __eq__)."""
        return hash((self._enunciado, self._tema))
