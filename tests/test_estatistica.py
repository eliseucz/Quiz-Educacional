from src.estatistica import Estatistica
from src.pergunta import Pergunta
from src.quiz import Quiz
from src.tentativa import Tentativa
from src.usuario import Usuario


def criar_usuario():
    return Usuario("Ana", "ana@exemplo.com", "2024001")


def criar_quiz():
    """Quiz com 2 perguntas de Matemática e 1 de Física (todas com resposta 0)."""
    return Quiz("Quiz Misto", [
        Pergunta("M1?", ["x", "y", "z"], 0, "FÁCIL", "Matemática"),
        Pergunta("M2?", ["x", "y", "z"], 0, "MÉDIO", "Matemática"),
        Pergunta("F1?", ["x", "y", "z"], 0, "FÁCIL", "Física"),
    ])


def adicionar_tentativa(usuario, respostas, concluir=True):
    tentativa = Tentativa(usuario, criar_quiz())
    tentativa.iniciar()

    for resposta in respostas:
        tentativa.registrar_resposta(resposta)

    if concluir:
        tentativa.finalizar()

    usuario.adicionar_tentativa(tentativa)
    return tentativa


# ---------- desempenho por tema ----------

def test_desempenho_por_tema_conta_acertos_de_cada_tema():
    usuario = criar_usuario()
    # acerta M1, erra M2, acerta F1
    adicionar_tentativa(usuario, [0, 1, 0])

    por_tema = Estatistica.desempenho_por_tema(usuario)

    assert por_tema["Matemática"] == {"acertos": 1, "total": 2, "taxa": 0.5}
    assert por_tema["Física"] == {"acertos": 1, "total": 1, "taxa": 1.0}


def test_desempenho_por_tema_soma_varias_tentativas():
    usuario = criar_usuario()
    adicionar_tentativa(usuario, [0, 0, 0])  # tudo certo
    adicionar_tentativa(usuario, [1, 1, 1])  # tudo errado

    por_tema = Estatistica.desempenho_por_tema(usuario)

    assert por_tema["Matemática"] == {"acertos": 2, "total": 4, "taxa": 0.5}
    assert por_tema["Física"] == {"acertos": 1, "total": 2, "taxa": 0.5}


def test_desempenho_por_tema_ignora_tentativas_incompletas():
    usuario = criar_usuario()
    adicionar_tentativa(usuario, [0, 0, 0])
    adicionar_tentativa(usuario, [1], concluir=False)

    por_tema = Estatistica.desempenho_por_tema(usuario)

    assert por_tema["Matemática"]["total"] == 2


def test_desempenho_por_tema_sem_tentativas_e_vazio():
    assert Estatistica.desempenho_por_tema(criar_usuario()) == {}


def test_temas_aparecem_em_ordem_alfabetica():
    usuario = criar_usuario()
    adicionar_tentativa(usuario, [0, 0, 0])

    assert list(Estatistica.desempenho_por_tema(usuario)) == [
        "Física",
        "Matemática",
    ]


# ---------- desempenho do usuário ----------

def test_desempenho_usuario_resume_geral_e_por_tema():
    usuario = criar_usuario()
    adicionar_tentativa(usuario, [0, 1, 0])  # 2 de 3

    desempenho = Estatistica.desempenho_usuario(usuario)

    assert desempenho["usuario"] == "Ana"
    assert desempenho["tentativas_concluidas"] == 1
    assert desempenho["taxa_acerto_geral"] == 2 / 3
    assert set(desempenho["por_tema"]) == {"Matemática", "Física"}


def test_taxa_geral_bate_com_a_do_usuario():
    usuario = criar_usuario()
    adicionar_tentativa(usuario, [0, 1, 0])

    desempenho = Estatistica.desempenho_usuario(usuario)

    assert desempenho["taxa_acerto_geral"] == usuario.calcular_taxa_acerto()


def test_desempenho_sem_tentativas_concluidas():
    usuario = criar_usuario()
    adicionar_tentativa(usuario, [0], concluir=False)

    desempenho = Estatistica.desempenho_usuario(usuario)

    assert desempenho["tentativas_concluidas"] == 0
    assert desempenho["taxa_acerto_geral"] == 0.0
    assert desempenho["por_tema"] == {}


# ---------- relatório em texto ----------

def test_relatorio_em_texto():
    usuario = criar_usuario()
    adicionar_tentativa(usuario, [0, 1, 0])

    assert Estatistica.relatorio_usuario(usuario) == (
        "Relatório de desempenho - Ana (2024001)\n"
        "Tentativas concluídas: 1\n"
        "Taxa de acerto geral: 66.7%\n"
        "Por tema:\n"
        "  - Física: 1/1 (100.0%)\n"
        "  - Matemática: 1/2 (50.0%)"
    )


def test_relatorio_sem_tentativas_concluidas():
    texto = Estatistica.relatorio_usuario(criar_usuario())

    assert texto == (
        "Relatório de desempenho - Ana (2024001)\n"
        "Nenhuma tentativa concluída ainda."
    )