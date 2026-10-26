"""Funções de persistência (salvar e carregar) em arquivos JSON."""

import json
from pathlib import Path

from .pergunta_multipla_escolha import PerguntaMultiplaEscolha
from .quiz import Quiz
from .tentativa import Tentativa
from .usuario import Usuario

# Pasta "dados" ao lado de "src", não importa de onde o programa seja rodado.
PASTA_DADOS = Path(__file__).resolve().parent.parent / "dados"
CAMINHO_PERGUNTAS = PASTA_DADOS / "perguntas.json"
CAMINHO_QUIZZES = PASTA_DADOS / "quizzes.json"
CAMINHO_USUARIOS = PASTA_DADOS / "usuarios.json"
CAMINHO_TENTATIVAS = PASTA_DADOS / "tentativas.json"


# ---------- funções internas (auxiliares) ----------

def _gravar_json(caminho, conteudo) -> None:
    """Grava o conteúdo em JSON, criando a pasta se ela não existir."""
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(conteudo, arquivo, ensure_ascii=False, indent=2)


def _ler_json(caminho) -> list:
    """Lê um arquivo JSON. Se ele não existir ainda, devolve lista vazia."""
    caminho = Path(caminho)

    if not caminho.exists():
        return []

    with open(caminho, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


# ---------- perguntas ----------

def salvar_perguntas(perguntas, caminho=CAMINHO_PERGUNTAS) -> None:
    _gravar_json(caminho, [pergunta.to_dict() for pergunta in perguntas])


def carregar_perguntas(caminho=CAMINHO_PERGUNTAS) -> list:
    return [
        PerguntaMultiplaEscolha.from_dict(dados)
        for dados in _ler_json(caminho)
    ]


# ---------- quizzes ----------

def salvar_quizzes(quizzes, caminho=CAMINHO_QUIZZES) -> None:
    _gravar_json(caminho, [quiz.to_dict() for quiz in quizzes])


def carregar_quizzes(perguntas, caminho=CAMINHO_QUIZZES) -> list:
    """Carrega os quizzes ligando-os às perguntas já carregadas."""
    return [Quiz.from_dict(dados, perguntas) for dados in _ler_json(caminho)]


# ---------- usuários ----------

def salvar_usuarios(usuarios, caminho=CAMINHO_USUARIOS) -> None:
    _gravar_json(caminho, [usuario.to_dict() for usuario in usuarios])


def carregar_usuarios(caminho=CAMINHO_USUARIOS) -> list:
    return [Usuario.from_dict(dados) for dados in _ler_json(caminho)]


# ---------- tentativas ----------

def salvar_tentativas(tentativas, caminho=CAMINHO_TENTATIVAS) -> None:
    _gravar_json(caminho, [tentativa.to_dict() for tentativa in tentativas])


def carregar_tentativas(usuarios, quizzes, caminho=CAMINHO_TENTATIVAS) -> list:
    """Carrega as tentativas e as reconecta ao usuário e ao quiz certos."""
    usuario_por_id = {usuario.matricula_id: usuario for usuario in usuarios}
    quiz_por_titulo = {quiz.titulo: quiz for quiz in quizzes}

    tentativas = []

    for dados in _ler_json(caminho):
        usuario = usuario_por_id.get(dados["usuario_id"])
        quiz = quiz_por_titulo.get(dados["quiz_titulo"])

        if usuario is None:
            raise ValueError(f"Usuário não encontrado: {dados['usuario_id']!r}.")

        if quiz is None:
            raise ValueError(f"Quiz não encontrado: {dados['quiz_titulo']!r}.")

        tentativa = Tentativa.from_dict(dados, usuario, quiz)
        usuario.adicionar_tentativa(tentativa)
        tentativas.append(tentativa)

    return tentativas