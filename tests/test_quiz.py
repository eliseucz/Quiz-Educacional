import pytest

from src.pergunta import Pergunta
from src.quiz import Quiz


def criar_pergunta(enunciado="Quanto é 2 + 2?", dificuldade="FÁCIL",
                   tema="Matemática"):
    return Pergunta(enunciado, ["3", "4", "5"], 1, dificuldade, tema)


# ---------- criação e validações ----------

def test_criacao_de_quiz():
    quiz = Quiz("Quiz 1")

    assert quiz.titulo == "Quiz 1"
    assert quiz.perguntas == []
    assert quiz.numero_tentativas_maximo == 1
    assert quiz.tempo_limite_minutos is None


def test_titulo_vazio():
    with pytest.raises(ValueError):
        Quiz("   ")


def test_titulo_nao_string():
    with pytest.raises(TypeError):
        Quiz(123)


def test_tentativas_menor_que_um():
    with pytest.raises(ValueError):
        Quiz("Quiz", numero_tentativas_maximo=0)


def test_tempo_limite_invalido():
    with pytest.raises(ValueError):
        Quiz("Quiz", tempo_limite_minutos=-5)


def test_tempo_limite_opcional_aceita_none():
    quiz = Quiz("Quiz", tempo_limite_minutos=None)

    assert quiz.tempo_limite_minutos is None


# ---------- perguntas dentro do quiz ----------

def test_adicionar_pergunta():
    quiz = Quiz("Quiz")
    quiz.adicionar_pergunta(criar_pergunta())

    assert len(quiz) == 1


def test_adicionar_objeto_que_nao_e_pergunta():
    quiz = Quiz("Quiz")

    with pytest.raises(TypeError):
        quiz.adicionar_pergunta("não sou uma pergunta")


def test_impede_pergunta_duplicada_no_mesmo_tema():
    quiz = Quiz("Quiz")
    quiz.adicionar_pergunta(criar_pergunta())

    with pytest.raises(ValueError):
        quiz.adicionar_pergunta(criar_pergunta())


def test_mesmo_enunciado_em_temas_diferentes_e_permitido():
    quiz = Quiz("Quiz")
    quiz.adicionar_pergunta(criar_pergunta(tema="Matemática"))
    quiz.adicionar_pergunta(criar_pergunta(tema="Física"))

    assert len(quiz) == 2


def test_lista_inicial_com_duplicadas_e_rejeitada():
    with pytest.raises(ValueError):
        Quiz("Quiz", [criar_pergunta(), criar_pergunta()])


def test_perguntas_nao_podem_ser_alteradas_diretamente():
    quiz = Quiz("Quiz", [criar_pergunta()])

    copia = quiz.perguntas
    copia.append(criar_pergunta("Outra?"))

    assert len(quiz) == 1


# ---------- métodos especiais ----------

def test_len():
    quiz = Quiz("Quiz", [criar_pergunta("A?"), criar_pergunta("B?")])

    assert len(quiz) == 2


def test_str():
    quiz = Quiz("Quiz de Mat", [criar_pergunta()])

    assert str(quiz) == "Quiz: Quiz de Mat (1 perguntas)"


def test_iter():
    p1 = criar_pergunta("A?")
    p2 = criar_pergunta("B?")
    quiz = Quiz("Quiz", [p1, p2])

    assert list(quiz) == [p1, p2]


# ---------- pontuação ----------

def test_pontuacao_maxima_de_quiz_vazio_e_zero():
    assert Quiz("Quiz").pontuacao_maxima == 0


def test_pontuacao_maxima_soma_pesos_por_dificuldade():
    quiz = Quiz("Quiz", [
        criar_pergunta("A?", "FÁCIL"),    # 1
        criar_pergunta("B?", "MÉDIO"),    # 2
        criar_pergunta("C?", "DIFÍCIL"),  # 3
    ])

    assert quiz.pontuacao_maxima == 6


def test_pontuacao_atualiza_ao_adicionar_pergunta():
    quiz = Quiz("Quiz", [criar_pergunta("A?", "FÁCIL")])
    assert quiz.pontuacao_maxima == 1

    quiz.adicionar_pergunta(criar_pergunta("B?", "DIFÍCIL"))
    assert quiz.pontuacao_maxima == 4
