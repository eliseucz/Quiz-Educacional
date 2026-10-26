from src.pergunta import Pergunta
from src.pergunta_multipla_escolha import PerguntaMultiplaEscolha
from src.validador import ValidadorAlternativas


def criar_pergunta_mc():
    return PerguntaMultiplaEscolha(
        "Quanto é 2 + 2?", ["3", "4", "5"], 1, "FÁCIL", "Matemática"
    )


# ---------- herança ----------

def test_herda_de_pergunta_e_do_validador():
    pergunta = criar_pergunta_mc()

    assert isinstance(pergunta, Pergunta)
    assert isinstance(pergunta, ValidadorAlternativas)


def test_ordem_de_heranca_mro():
    nomes = [classe.__name__ for classe in PerguntaMultiplaEscolha.__mro__]

    assert nomes == [
        "PerguntaMultiplaEscolha",
        "Pergunta",
        "ValidadorAlternativas",
        "object",
    ]


def test_reaproveita_validacoes_de_pergunta():
    pergunta = criar_pergunta_mc()

    assert pergunta.peso == 1
    assert pergunta.tema == "Matemática"


# ---------- validador (mixin) ----------

def test_validar_quantidade_aceita_de_3_a_5():
    assert ValidadorAlternativas.validar_quantidade(["a", "b", "c"])
    assert ValidadorAlternativas.validar_quantidade(["a", "b", "c", "d", "e"])


def test_validar_quantidade_recusa_menos_de_3_e_mais_de_5():
    assert not ValidadorAlternativas.validar_quantidade(["a", "b"])
    assert not ValidadorAlternativas.validar_quantidade(list("abcdef"))


def test_validar_indice():
    alternativas = ["a", "b", "c"]

    assert ValidadorAlternativas.validar_indice(0, alternativas)
    assert ValidadorAlternativas.validar_indice(2, alternativas)
    assert not ValidadorAlternativas.validar_indice(3, alternativas)
    assert not ValidadorAlternativas.validar_indice(-1, alternativas)
    assert not ValidadorAlternativas.validar_indice("1", alternativas)


# ---------- métodos próprios ----------

def test_validar_retorna_true_para_pergunta_correta():
    assert criar_pergunta_mc().validar() is True


def test_str_mostra_o_tipo_da_pergunta():
    texto = str(criar_pergunta_mc())

    assert texto == "[Múltipla escolha] Quanto é 2 + 2? (Matemática - FÁCIL)"


def test_igualdade_herdada_compara_enunciado_e_tema():
    assert criar_pergunta_mc() == criar_pergunta_mc()