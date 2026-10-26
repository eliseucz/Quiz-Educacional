import pytest

from src.pergunta import Pergunta
from src.quiz import Quiz
from src.tentativa import Tentativa
from src.usuario import Usuario


def criar_usuario(nome="Ana", email="ana@exemplo.com", matricula="2024001"):
    return Usuario(nome, email, matricula)


def criar_quiz():
    return Quiz("Quiz", [
        Pergunta("A?", ["x", "y", "z"], 0, "FÁCIL", "Tema"),
        Pergunta("B?", ["x", "y", "z"], 1, "DIFÍCIL", "Tema"),
    ])


def criar_tentativa(usuario, respostas=(), concluir=False):
    tentativa = Tentativa(usuario, criar_quiz())
    tentativa.iniciar()

    for resposta in respostas:
        tentativa.registrar_resposta(resposta)

    if concluir:
        tentativa.finalizar()

    return tentativa


# ---------- criação e validações ----------

def test_criacao_de_usuario():
    usuario = criar_usuario()

    assert usuario.nome == "Ana"
    assert usuario.email == "ana@exemplo.com"
    assert usuario.matricula_id == "2024001"
    assert usuario.tentativas == []


def test_nome_vazio():
    with pytest.raises(ValueError):
        criar_usuario(nome="   ")


def test_nome_nao_string():
    with pytest.raises(TypeError):
        criar_usuario(nome=123)


def test_email_invalido():
    with pytest.raises(ValueError):
        criar_usuario(email="ana-sem-arroba")


def test_email_nao_string():
    with pytest.raises(TypeError):
        criar_usuario(email=None)


def test_matricula_vazia():
    with pytest.raises(ValueError):
        criar_usuario(matricula="")


def test_matricula_nao_string():
    with pytest.raises(TypeError):
        criar_usuario(matricula=2024001)


# ---------- relação Usuario -> Tentativa ----------

def test_adicionar_tentativa():
    usuario = criar_usuario()
    tentativa = criar_tentativa(usuario)
    usuario.adicionar_tentativa(tentativa)

    assert usuario.tentativas == [tentativa]


def test_adicionar_objeto_que_nao_e_tentativa():
    usuario = criar_usuario()

    with pytest.raises(TypeError):
        usuario.adicionar_tentativa("não sou uma tentativa")


def test_tentativa_de_outro_usuario_e_recusada():
    ana = criar_usuario()
    bia = criar_usuario(nome="Bia", email="bia@exemplo.com", matricula="2024002")
    tentativa_da_bia = criar_tentativa(bia)

    with pytest.raises(ValueError):
        ana.adicionar_tentativa(tentativa_da_bia)

    assert ana.tentativas == []


def test_tentativa_duplicada_e_recusada():
    usuario = criar_usuario()
    tentativa = criar_tentativa(usuario)
    usuario.adicionar_tentativa(tentativa)

    with pytest.raises(ValueError):
        usuario.adicionar_tentativa(tentativa)


def test_tentativas_retorna_copia():
    usuario = criar_usuario()
    usuario.adicionar_tentativa(criar_tentativa(usuario))

    copia = usuario.tentativas
    copia.clear()

    assert len(usuario.tentativas) == 1


# ---------- taxa de acerto ----------

def test_taxa_sem_tentativas_e_zero():
    assert criar_usuario().calcular_taxa_acerto() == 0.0


def test_taxa_ignora_tentativas_incompletas():
    usuario = criar_usuario()
    # concluída, acertou tudo (taxa 1.0)
    usuario.adicionar_tentativa(criar_tentativa(usuario, [0, 1], concluir=True))
    # incompleta, errou a única resposta dada (não deve contar)
    usuario.adicionar_tentativa(criar_tentativa(usuario, [2]))

    assert usuario.calcular_taxa_acerto() == 1.0


def test_taxa_e_media_das_tentativas_concluidas():
    usuario = criar_usuario()
    usuario.adicionar_tentativa(criar_tentativa(usuario, [0, 1], concluir=True))  # 1.0
    usuario.adicionar_tentativa(criar_tentativa(usuario, [0, 2], concluir=True))  # 0.5

    assert usuario.calcular_taxa_acerto() == 0.75


# ---------- métodos especiais ----------

def test_str():
    usuario = criar_usuario()
    usuario.adicionar_tentativa(criar_tentativa(usuario))

    assert str(usuario) == "Ana (2024001) - 1 tentativas"



def test_taxa_considera_todas_as_perguntas_e_nao_a_media_das_tentativas():
    usuario = criar_usuario()
    # quiz de 2 perguntas, acerta as 2 (2 acertos de 2)
    usuario.adicionar_tentativa(criar_tentativa(usuario, [0, 1], concluir=True))

    # quiz de 4 perguntas, erra as 4 (0 acertos de 4)
    quiz_grande = Quiz("Grande", [
        Pergunta(f"G{i}?", ["x", "y", "z"], 0, "FÁCIL", "Tema") for i in range(4)
    ])
    tentativa = Tentativa(usuario, quiz_grande)
    tentativa.iniciar()
    for _ in range(4):
        tentativa.registrar_resposta(2)
    tentativa.finalizar()
    usuario.adicionar_tentativa(tentativa)

    # 2 acertos em 6 perguntas = 1/3 (a média das tentativas daria 0.5)
    assert usuario.calcular_taxa_acerto() == 2 / 6