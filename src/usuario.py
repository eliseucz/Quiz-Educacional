"""Define a classe Usuario."""

import re

from .tentativa import Tentativa


class Usuario:
    """Representa um usuário e seu histórico de tentativas de quiz."""

    def __init__(self, nome: str, email: str, matricula_id: str):
        self.nome = nome
        self.email = email
        self.matricula_id = matricula_id
        self._tentativas: list[Tentativa] = []

    @property
    def nome(self) -> str:
        """Retorna o nome do usuário."""
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        """Valida e define o nome."""
        if not isinstance(valor, str):
            raise TypeError("O nome deve ser uma string.")

        if not valor.strip():
            raise ValueError("O nome não pode ser vazio.")

        self._nome = valor.strip()

    @property
    def email(self) -> str:
        """Retorna o e-mail do usuário."""
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        """Valida e define o e-mail."""
        if not isinstance(valor, str):
            raise TypeError("O e-mail deve ser uma string.")

        valor = valor.strip()

        # Formato simples: algo@algo.algo, sem espaços.
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor):
            raise ValueError("O e-mail informado é inválido.")

        self._email = valor

    @property
    def matricula_id(self) -> str:
        """Retorna a matrícula ou ID do usuário."""
        return self._matricula_id

    @matricula_id.setter
    def matricula_id(self, valor: str) -> None:
        """Valida e define a matrícula/ID."""
        if not isinstance(valor, str):
            raise TypeError("A matrícula/ID deve ser uma string.")

        if not valor.strip():
            raise ValueError("A matrícula/ID não pode ser vazia.")

        self._matricula_id = valor.strip()

    @property
    def tentativas(self) -> list[Tentativa]:
        """Retorna uma cópia da lista de tentativas."""
        return self._tentativas.copy()

    def adicionar_tentativa(self, tentativa: Tentativa) -> None:
        """Associa uma tentativa a este usuário."""
        if not isinstance(tentativa, Tentativa):
            raise TypeError("A tentativa deve ser um objeto Tentativa.")

        # Mantém as duas pontas da relação combinando:
        # a tentativa precisa apontar de volta para ESTE usuário.
        if tentativa.usuario is not self:
            raise ValueError("A tentativa pertence a outro usuário.")

        if tentativa in self._tentativas:
            raise ValueError("Esta tentativa já foi adicionada.")

        self._tentativas.append(tentativa)

    def calcular_taxa_acerto(self) -> float:
        """Acertos sobre o total de perguntas das tentativas concluídas.

        Retorna um valor de 0.0 a 1.0. Tentativas incompletas são ignoradas.
        """
        acertos = 0
        total = 0

        for tentativa in self._tentativas:
            if not tentativa.concluida:
                continue

            for _, acertou in tentativa.resultados_por_pergunta():
                total += 1
                if acertou:
                    acertos += 1

        if total == 0:
            return 0.0

        return acertos / total

    def __str__(self) -> str:
        """Retorna um resumo do usuário."""
        return (
            f"{self._nome} ({self._matricula_id}) - "
            f"{len(self._tentativas)} tentativas"
        )

    def to_dict(self) -> dict:
        """Converte o usuário em dicionário (sem as tentativas)."""
        return {
            "nome": self._nome,
            "email": self._email,
            "matricula_id": self._matricula_id,
        }

    @classmethod
    def from_dict(cls, dados: dict):
        """Cria um usuário a partir de um dicionário."""
        return cls(dados["nome"], dados["email"], dados["matricula_id"])