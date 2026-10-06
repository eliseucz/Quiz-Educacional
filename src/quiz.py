"""Define a classe Quiz do sistema de quiz educacional."""

from .pergunta import Pergunta


class Quiz:
    """Representa um quiz composto por perguntas."""

    def __init__(
        self,
        titulo: str,
        perguntas: list[Pergunta] | None = None,
        numero_tentativas_maximo: int = 1,
        tempo_limite_minutos: int | None = None,
    ):
        self.titulo = titulo
        self.perguntas = [] if perguntas is None else perguntas
        self.numero_tentativas_maximo = numero_tentativas_maximo
        self.tempo_limite_minutos = tempo_limite_minutos

    @property
    def titulo(self) -> str:
        """Retorna o título do quiz."""
        return self._titulo

    @titulo.setter
    def titulo(self, valor: str) -> None:
        """Valida e define o título do quiz."""
        if not isinstance(valor, str):
            raise TypeError(
                "O título deve ser uma string."
            )

        if not valor.strip():
            raise ValueError(
                "O título não pode ser vazio."
            )

        self._titulo = valor.strip()

    @property
    def perguntas(self) -> list[Pergunta]:
        """Retorna uma cópia da lista de perguntas."""
        return self._perguntas.copy()

    @perguntas.setter
    def perguntas(self, valor: list[Pergunta]) -> None:
        """Valida e define a lista de perguntas."""
        if not isinstance(valor, list):
            raise TypeError(
                "As perguntas devem ser uma lista."
            )

        if any(
            not isinstance(pergunta, Pergunta)
            for pergunta in valor
        ):
            raise TypeError(
                "A lista deve conter apenas objetos Pergunta."
            )

        # Não permite duas perguntas iguais (mesmo enunciado e tema).
        sem_duplicatas = []
        for pergunta in valor:
            if pergunta in sem_duplicatas:
                raise ValueError(
                    "Pergunta duplicada: já existe uma pergunta com o "
                    "mesmo enunciado e tema."
                )
            sem_duplicatas.append(pergunta)

        self._perguntas = sem_duplicatas

    @property
    def numero_tentativas_maximo(self) -> int:
        """Retorna o limite máximo de tentativas."""
        return self._numero_tentativas_maximo

    @numero_tentativas_maximo.setter
    def numero_tentativas_maximo(self, valor: int) -> None:
        """Valida e define o limite de tentativas."""
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise TypeError(
                "O número máximo de tentativas deve ser um inteiro."
            )

        if valor < 1:
            raise ValueError(
                "O número máximo de tentativas deve ser maior que zero."
            )

        self._numero_tentativas_maximo = valor

    @property
    def tempo_limite_minutos(self) -> int | None:
        """Retorna o tempo limite do quiz."""
        return self._tempo_limite_minutos

    @tempo_limite_minutos.setter
    def tempo_limite_minutos(self, valor: int | None) -> None:
        """Valida e define o tempo limite."""
        if valor is not None:
            if not isinstance(valor, int) or isinstance(valor, bool):
                raise TypeError(
                    "O tempo limite deve ser um inteiro ou None."
                )

            if valor <= 0:
                raise ValueError(
                    "O tempo limite deve ser maior que zero."
                )

        self._tempo_limite_minutos = valor

    def adicionar_pergunta(self, pergunta: Pergunta) -> None:
        """Adiciona uma pergunta ao quiz."""
        if not isinstance(pergunta, Pergunta):
            raise TypeError(
                "A pergunta deve ser um objeto Pergunta."
            )

        if pergunta in self._perguntas:
            raise ValueError(
                "Pergunta duplicada: já existe uma pergunta com o "
                "mesmo enunciado e tema."
            )

        self._perguntas.append(pergunta)

    def calcular_pontuacao_maxima(self) -> int:
        """Soma os pesos de todas as perguntas do quiz."""
        return sum(pergunta.peso for pergunta in self._perguntas)

    @property
    def pontuacao_maxima(self) -> int:
        """Pontuação máxima do quiz, sempre calculada automaticamente."""
        return self.calcular_pontuacao_maxima()

    def __str__(self) -> str:
        """Retorna um resumo do quiz."""
        return (
            f"Quiz: {self._titulo} "
            f"({len(self._perguntas)} perguntas)"
        )

    def __len__(self) -> int:
        """Retorna a quantidade de perguntas do quiz."""
        return len(self._perguntas)

    def __iter__(self):
        """Permite iterar pelas perguntas do quiz."""
        return iter(self._perguntas)