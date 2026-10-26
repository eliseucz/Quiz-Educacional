import pytest

from src.pergunta import Pergunta
from src.quiz import Quiz
from src.tentativa import Tentativa


class UsuarioFalso:
    """Dublê de teste: faz o papel de Usuario até ele existir (Passo 3)."""


def criar_quiz():
    return Quiz("Quiz", [
        Pergunta("A?", ["x", "y", "z"], 0, "FÁCIL", "Tema"),      # vale 1
        Pergunta("B?", ["x", "y", "z"], 1, "DIFÍCIL", "Tema"),    # vale 3
    ])


def criar_tentativa_iniciada():
    tentativa = Tentativa(UsuarioFalso(), criar_quiz())
    tentativa.iniciar()
    return tentativa


# ---------- criação ----------

def test_estado_inicial():
    tentativa = Tentativa(UsuarioFalso(), criar_quiz())

    assert tentativa.respostas == []
    assert tentativa.concluida is False
    assert tentativa.data_hora is None
    assert tentativa.pontuacao == 0
    assert tentativa.tempo_total == 0


def test_quiz_de_tipo_errado():
    with pytest.raises(TypeError):
        Tentativa(UsuarioFalso(), "não sou um quiz")


def test_quiz_sem_perguntas():
    with pytest.raises(ValueError):
        Tentativa(UsuarioFalso(), Quiz("Vazio"))


def test_usuario_obrigatorio():
    with pytest.raises(ValueError):
        Tentativa(None, criar_quiz())


# ---------- fluxo ----------

def test_iniciar_registra_data_hora():
    tentativa = criar_tentativa_iniciada()

    assert tentativa.data_hora is not None


def test_iniciar_duas_vezes():
    tentativa = criar_tentativa_iniciada()

    with pytest.raises(RuntimeError):
        tentativa.iniciar()


def test_responder_sem_iniciar():
    tentativa = Tentativa(UsuarioFalso(), criar_quiz())

    with pytest.raises(RuntimeError):
        tentativa.registrar_resposta(0)


def test_registrar_resposta_valida():
    tentativa = criar_tentativa_iniciada()
    tentativa.registrar_resposta(0)

    assert tentativa.respostas == [0]


def test_resposta_com_indice_invalido_nao_e_registrada():
    tentativa = criar_tentativa_iniciada()

    with pytest.raises(ValueError):
        tentativa.registrar_resposta(7)

    assert tentativa.respostas == []


def test_nao_aceita_mais_respostas_que_perguntas():
    tentativa = criar_tentativa_iniciada()
    tentativa.registrar_resposta(0)
    tentativa.registrar_resposta(1)

    with pytest.raises(RuntimeError):
        tentativa.registrar_resposta(0)


def test_finalizar_incompleta():
    tentativa = criar_tentativa_iniciada()
    tentativa.registrar_resposta(0)

    with pytest.raises(RuntimeError):
        tentativa.finalizar()


def test_finalizar_completa():
    tentativa = criar_tentativa_iniciada()
    tentativa.registrar_resposta(0)
    tentativa.registrar_resposta(1)
    tentativa.finalizar()

    assert tentativa.concluida is True
    assert tentativa.tempo_total >= 0


def test_responder_depois_de_concluida():
    tentativa = criar_tentativa_iniciada()
    tentativa.registrar_resposta(0)
    tentativa.registrar_resposta(1)
    tentativa.finalizar()

    with pytest.raises(RuntimeError):
        tentativa.registrar_resposta(0)


def test_respostas_retorna_copia():
    tentativa = criar_tentativa_iniciada()
    tentativa.registrar_resposta(0)

    copia = tentativa.respostas
    copia.append(99)

    assert tentativa.respostas == [0]


# ---------- pontuação ----------

def test_pontuacao_ponderada_acertando_tudo():
    tentativa = criar_tentativa_iniciada()
    tentativa.registrar_resposta(0)   # acerta a fácil: 1 ponto
    tentativa.registrar_resposta(1)   # acerta a difícil: 3 pontos

    assert tentativa.pontuacao == 4
    assert tentativa.taxa_acertos == 1.0


def test_pontuacao_acertando_so_a_dificil():
    tentativa = criar_tentativa_iniciada()
    tentativa.registrar_resposta(2)   # erra a fácil
    tentativa.registrar_resposta(1)   # acerta a difícil

    assert tentativa.pontuacao == 3
    assert tentativa.taxa_acertos == 0.5


def test_pontuacao_errando_tudo():
    tentativa = criar_tentativa_iniciada()
    tentativa.registrar_resposta(2)
    tentativa.registrar_resposta(2)

    assert tentativa.pontuacao == 0
    assert tentativa.taxa_acertos == 0


def test_str():
    tentativa = criar_tentativa_iniciada()
    tentativa.registrar_resposta(0)

    assert str(tentativa) == "Tentativa no quiz 'Quiz': 1/4 pontos (em andamento)"



def test_resultados_por_pergunta():
    tentativa = criar_tentativa_iniciada()
    tentativa.registrar_resposta(0)   # acerta A
    tentativa.registrar_resposta(2)   # erra B

    resultados = tentativa.resultados_por_pergunta()

    assert [acertou for _, acertou in resultados] == [True, False]
    assert resultados[0][0].enunciado == "A?"


def test_resultados_por_pergunta_so_inclui_as_respondidas():
    tentativa = criar_tentativa_iniciada()
    tentativa.registrar_resposta(0)

    assert len(tentativa.resultados_por_pergunta()) == 1