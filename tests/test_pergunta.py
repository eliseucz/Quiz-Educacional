import pytest

from src.pergunta import Pergunta


def criar_pergunta():
    return Pergunta(
        "Quanto é 2 + 2?",
        ["3", "4", "5"],
        1,
        "FÁCIL",
        "Matemática",
    )


def test_criacao_de_pergunta():
    pergunta = criar_pergunta()

    assert pergunta.enunciado == "Quanto é 2 + 2?"
    assert pergunta.alternativas == ["3", "4", "5"]
    assert pergunta.indice_resposta_correta == 1
    assert pergunta.dificuldade == "FÁCIL"
    assert pergunta.tema == "Matemática"


def test_menos_de_tres_alternativas():
    with pytest.raises(ValueError):
        Pergunta(
            "Pergunta?",
            ["A", "B"],
            0,
            "FÁCIL",
            "Teste",
        )


def test_mais_de_cinco_alternativas():
    with pytest.raises(ValueError):
        Pergunta(
            "Pergunta?",
            ["A", "B", "C", "D", "E", "F"],
            0,
            "FÁCIL",
            "Teste",
        )


def test_indice_invalido():
    with pytest.raises(ValueError):
        Pergunta(
            "Pergunta?",
            ["A", "B", "C"],
            3,
            "FÁCIL",
            "Teste",
        )


def test_dificuldade_invalida():
    with pytest.raises(ValueError):
        Pergunta(
            "Pergunta?",
            ["A", "B", "C"],
            0,
            "IMPOSSÍVEL",
            "Teste",
        )


def test_enunciado_vazio():
    with pytest.raises(ValueError):
        Pergunta(
            "   ",
            ["A", "B", "C"],
            0,
            "FÁCIL",
            "Teste",
        )


def test_str():
    pergunta = criar_pergunta()

    assert str(pergunta) == (
        "Quanto é 2 + 2? (Matemática - FÁCIL)"
    )


def test_perguntas_iguais():
    p1 = criar_pergunta()

    p2 = Pergunta(
        "Quanto é 2 + 2?",
        ["2", "4", "6"],
        1,
        "MÉDIO",
        "Matemática",
    )

    assert p1 == p2


def test_diferentes_temas():
    p1 = criar_pergunta()

    p2 = Pergunta(
        "Quanto é 2 + 2?",
        ["3", "4", "5"],
        1,
        "FÁCIL",
        "Física",
    )

    assert p1 != p2


def test_alternativas_nao_podem_ser_alteradas_diretamente():
    pergunta = criar_pergunta()

    alternativas = pergunta.alternativas
    alternativas.append("6")

    assert len(pergunta.alternativas) == 3

def test_peso_depende_da_dificuldade():
    facil = criar_pergunta()
    dificil = Pergunta("Pergunta?", ["A", "B", "C"], 0, "DIFÍCIL", "Teste")

    assert facil.peso == 1
    assert dificil.peso == 3


def test_pergunta_pode_ser_usada_em_set():
    p1 = criar_pergunta()
    p2 = criar_pergunta()

    assert len({p1, p2}) == 1
