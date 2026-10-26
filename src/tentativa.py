"""Define a classe Tentativa."""

import time
from datetime import datetime

from .quiz import Quiz
from .validador import ValidadorAlternativas


class Tentativa:
    """Representa uma execução de um quiz realizada por um usuário."""

    def __init__(self, usuario, quiz: Quiz):
        if usuario is None:
            raise ValueError("A tentativa precisa de um usuário.")

        if not isinstance(quiz, Quiz):
            raise TypeError("O quiz deve ser um objeto da classe Quiz.")

        if len(quiz) == 0:
            raise ValueError("Não é possível tentar um quiz sem perguntas.")

        self._usuario = usuario
        self._quiz = quiz
        self._respostas: list[int] = []
        self._concluida = False
        self._data_hora: str | None = None
        self._tempo_total = 0.0
        self._inicio: float | None = None

    # ---------- propriedades (somente leitura) ----------

    @property
    def usuario(self):
        return self._usuario

    @property
    def quiz(self) -> Quiz:
        return self._quiz

    @property
    def respostas(self) -> list[int]:
        """Retorna uma cópia das respostas registradas."""
        return self._respostas.copy()

    @property
    def concluida(self) -> bool:
        return self._concluida

    @property
    def data_hora(self) -> str | None:
        """Data e hora em que a tentativa foi iniciada."""
        return self._data_hora

    @property
    def tempo_total(self) -> float:
        """Tempo gasto, em segundos (só é definido ao finalizar)."""
        return self._tempo_total

    @property
    def pontuacao(self) -> float:
        return self.calcular_pontuacao()

    @property
    def taxa_acertos(self) -> float:
        return self.calcular_taxa_acertos()

    # ---------- fluxo da tentativa ----------

    def iniciar(self) -> None:
        """Marca o início da tentativa."""
        if self._inicio is not None:
            raise RuntimeError("A tentativa já foi iniciada.")

        self._inicio = time.monotonic()
        self._data_hora = datetime.now().isoformat(timespec="seconds")

    def registrar_resposta(self, indice: int) -> None:
        """Registra a resposta da pergunta atual."""
        if self._inicio is None:
            raise RuntimeError("Inicie a tentativa antes de responder.")

        if self._concluida:
            raise RuntimeError("A tentativa já foi concluída.")

        if len(self._respostas) >= len(self._quiz):
            raise RuntimeError(
                "Todas as perguntas já foram respondidas. Finalize a tentativa."
            )

        pergunta_atual = self._quiz.perguntas[len(self._respostas)]

        if not ValidadorAlternativas.validar_indice(
            indice, pergunta_atual.alternativas
        ):
            raise ValueError("Resposta inválida para esta pergunta.")

        self._respostas.append(indice)

    def finalizar(self) -> None:
        """Conclui a tentativa e registra o tempo total."""
        if self._inicio is None:
            raise RuntimeError("Inicie a tentativa antes de finalizar.")

        if self._concluida:
            raise RuntimeError("A tentativa já foi concluída.")

        if len(self._respostas) < len(self._quiz):
            raise RuntimeError("Responda todas as perguntas para finalizar.")

        self._tempo_total = time.monotonic() - self._inicio
        self._concluida = True

    # ---------- cálculos ----------

    def _contar_acertos(self) -> int:
        acertos = 0

        for pergunta, resposta in zip(self._quiz.perguntas, self._respostas):
            if pergunta.verificar_resposta(resposta):
                acertos += 1

        return acertos

    def resultados_por_pergunta(self) -> list[tuple]:
        """Lista (pergunta, acertou) para cada pergunta já respondida."""
        return [
            (pergunta, pergunta.verificar_resposta(resposta))
            for pergunta, resposta in zip(self._quiz.perguntas, self._respostas)
        ]

    def calcular_pontuacao(self) -> float:
        """Soma os pesos das perguntas respondidas corretamente."""
        total = 0

        for pergunta, resposta in zip(self._quiz.perguntas, self._respostas):
            if pergunta.verificar_resposta(resposta):
                total += pergunta.peso

        return float(total)

    def calcular_taxa_acertos(self) -> float:
        """Retorna a fração de acertos (0.0 a 1.0) sobre o total de perguntas."""
        return self._contar_acertos() / len(self._quiz)

    def __str__(self) -> str:
        situacao = "concluída" if self._concluida else "em andamento"
        return (
            f"Tentativa no quiz '{self._quiz.titulo}': "
            f"{self.pontuacao:g}/{self._quiz.pontuacao_maxima} pontos "
            f"({situacao})"
        )

    def to_dict(self) -> dict:
       #Converte a tentativa em dicionário.
       #Guarda só o ID do usuário e o título do quiz, e não os objetos inteiros, para evitar ciclos e repetição de dados no JSON.
        return {
            "usuario_id": self._usuario.matricula_id,
            "quiz_titulo": self._quiz.titulo,
            "respostas": self._respostas.copy(),
            "concluida": self._concluida,
            "data_hora": self._data_hora,
            "tempo_total": self._tempo_total,
        }

    @classmethod
    def from_dict(cls, dados: dict, usuario, quiz: Quiz):
        """Recria uma tentativa salva, ligada ao usuário e ao quiz informados."""
        tentativa = cls(usuario, quiz)

        respostas = dados["respostas"]
        concluida = dados["concluida"]
        data_hora = dados["data_hora"]

        if not isinstance(respostas, list) or len(respostas) > len(quiz):
            raise ValueError("Respostas inválidas no arquivo de tentativas.")

        for resposta, pergunta in zip(respostas, quiz.perguntas):
            if not ValidadorAlternativas.validar_indice(
                resposta, pergunta.alternativas
            ):
                raise ValueError("Resposta inválida no arquivo de tentativas.")

        if concluida and (len(respostas) != len(quiz) or data_hora is None):
            raise ValueError("Tentativa concluída com dados inconsistentes.")

        tentativa._respostas = list(respostas)
        tentativa._concluida = bool(concluida)
        tentativa._data_hora = data_hora
        tentativa._tempo_total = float(dados["tempo_total"])

        # Uma tentativa que já tinha sido iniciada continua "iniciada".
        # (O cronômetro interno recomeça: o tempo não é salvo enquanto corre.)
        if data_hora is not None:
            tentativa._inicio = time.monotonic()

        return tentativa