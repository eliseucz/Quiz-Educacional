import json

import pytest

from src import dados
from src.pergunta import Pergunta
from src.pergunta_multipla_escolha import PerguntaMultiplaEscolha
from src.quiz import Quiz
from src.tentativa import Tentativa
from src.usuario import Usuario


def criar_pergunta(enunciado="Quanto é 2 + 2?", resposta=1, dificuldade="FÁCIL"):
    return PerguntaMultiplaEscolha(
        enunciado, ["3", "4", "5"], resposta, dificuldade, "Matemática"
    )


def criar_cenario():
    """Monta perguntas, um quiz, um usuário e uma tentativa concluída."""
    p1 = criar_pergunta("Quanto é 2 + 2?", 1, "FÁCIL")
    p2 = criar_pergunta("Quanto é 3 x 3?", 0, "DIFÍCIL")
    quiz = Quiz("Quiz de Matemática", [p1, p2], numero_tentativas_maximo=2)
    usuario = Usuario("Ana", "ana@exemplo.com", "2024001")

    tentativa = Tentativa(usuario, quiz)
    tentativa.iniciar()
    tentativa.registrar_resposta(1)
    tentativa.registrar_resposta(2)
    tentativa.finalizar()
    usuario.adicionar_tentativa(tentativa)

    return [p1, p2], quiz, usuario, tentativa


# ---------- to_dict / from_dict ----------

def test_pergunta_vira_dicionario_e_volta():
    original = criar_pergunta()
    copia = PerguntaMultiplaEscolha.from_dict(original.to_dict())

    assert copia == original
    assert copia.alternativas == original.alternativas
    assert copia.indice_resposta_correta == original.indice_resposta_correta
    assert copia.dificuldade == original.dificuldade


def test_from_dict_cria_objeto_da_classe_que_chamou():
    dicionario = criar_pergunta().to_dict()

    assert type(Pergunta.from_dict(dicionario)) is Pergunta
    assert type(PerguntaMultiplaEscolha.from_dict(dicionario)) is PerguntaMultiplaEscolha


def test_dicionario_de_pergunta_e_serializavel_em_json():
    texto = json.dumps(criar_pergunta().to_dict(), ensure_ascii=False)

    assert "Matemática" in texto


def test_quiz_guarda_so_referencias_as_perguntas():
    perguntas, quiz, _, _ = criar_cenario()

    assert quiz.to_dict()["perguntas"] == [
        {"enunciado": "Quanto é 2 + 2?", "tema": "Matemática"},
        {"enunciado": "Quanto é 3 x 3?", "tema": "Matemática"},
    ]


def test_quiz_recarregado_usa_os_mesmos_objetos_pergunta():
    perguntas, quiz, _, _ = criar_cenario()
    copia = Quiz.from_dict(quiz.to_dict(), perguntas)

    assert copia.titulo == quiz.titulo
    assert copia.numero_tentativas_maximo == 2
    assert copia.perguntas[0] is perguntas[0]
    assert copia.perguntas[1] is perguntas[1]


def test_quiz_com_pergunta_inexistente():
    perguntas, quiz, _, _ = criar_cenario()

    with pytest.raises(ValueError):
        Quiz.from_dict(quiz.to_dict(), [perguntas[0]])


def test_usuario_vira_dicionario_sem_tentativas():
    _, _, usuario, _ = criar_cenario()

    assert usuario.to_dict() == {
        "nome": "Ana",
        "email": "ana@exemplo.com",
        "matricula_id": "2024001",
    }


def test_usuario_vira_dicionario_e_volta():
    _, _, usuario, _ = criar_cenario()
    copia = Usuario.from_dict(usuario.to_dict())

    assert copia.nome == usuario.nome
    assert copia.email == usuario.email
    assert copia.matricula_id == usuario.matricula_id
    assert copia.tentativas == []


def test_tentativa_guarda_id_do_usuario_e_titulo_do_quiz():
    _, _, _, tentativa = criar_cenario()
    dicionario = tentativa.to_dict()

    assert dicionario["usuario_id"] == "2024001"
    assert dicionario["quiz_titulo"] == "Quiz de Matemática"
    assert dicionario["respostas"] == [1, 2]
    assert dicionario["concluida"] is True


def test_tentativa_concluida_vira_dicionario_e_volta():
    _, quiz, usuario, tentativa = criar_cenario()
    copia = Tentativa.from_dict(tentativa.to_dict(), usuario, quiz)

    assert copia.respostas == [1, 2]
    assert copia.concluida is True
    assert copia.pontuacao == tentativa.pontuacao
    assert copia.data_hora == tentativa.data_hora


def test_tentativa_incompleta_continua_incompleta():
    _, quiz, usuario, _ = criar_cenario()
    parcial = Tentativa(usuario, quiz)
    parcial.iniciar()
    parcial.registrar_resposta(1)

    copia = Tentativa.from_dict(parcial.to_dict(), usuario, quiz)

    assert copia.concluida is False
    assert copia.respostas == [1]

    copia.registrar_resposta(0)  # ainda aceita continuar respondendo
    assert copia.respostas == [1, 0]


def test_tentativa_com_resposta_invalida_no_arquivo():
    _, quiz, usuario, tentativa = criar_cenario()
    dicionario = tentativa.to_dict()
    dicionario["respostas"] = [1, 99]

    with pytest.raises(ValueError):
        Tentativa.from_dict(dicionario, usuario, quiz)


def test_tentativa_concluida_com_dados_inconsistentes():
    _, quiz, usuario, tentativa = criar_cenario()
    dicionario = tentativa.to_dict()
    dicionario["respostas"] = [1]  # concluída, mas faltam respostas

    with pytest.raises(ValueError):
        Tentativa.from_dict(dicionario, usuario, quiz)


# ---------- arquivos JSON ----------

def test_carregar_arquivo_inexistente_devolve_lista_vazia(tmp_path):
    assert dados.carregar_perguntas(tmp_path / "nao_existe.json") == []


def test_salvar_cria_a_pasta_se_necessario(tmp_path):
    caminho = tmp_path / "pasta_nova" / "perguntas.json"
    dados.salvar_perguntas([criar_pergunta()], caminho)

    assert caminho.exists()


def test_arquivo_guarda_acentos_legiveis(tmp_path):
    caminho = tmp_path / "perguntas.json"
    dados.salvar_perguntas([criar_pergunta()], caminho)

    texto = caminho.read_text(encoding="utf-8")

    assert "Matemática" in texto
    assert "\\u00e1" not in texto


def test_salvar_e_carregar_perguntas(tmp_path):
    caminho = tmp_path / "perguntas.json"
    originais = [criar_pergunta("A?"), criar_pergunta("B?")]
    dados.salvar_perguntas(originais, caminho)

    carregadas = dados.carregar_perguntas(caminho)

    assert carregadas == originais
    assert all(isinstance(p, PerguntaMultiplaEscolha) for p in carregadas)


def test_salvar_e_carregar_usuarios(tmp_path):
    caminho = tmp_path / "usuarios.json"
    _, _, usuario, _ = criar_cenario()
    dados.salvar_usuarios([usuario], caminho)

    carregados = dados.carregar_usuarios(caminho)

    assert len(carregados) == 1
    assert carregados[0].matricula_id == "2024001"


def test_json_invalido_gera_erro(tmp_path):
    caminho = tmp_path / "perguntas.json"
    caminho.write_text("isso não é json", encoding="utf-8")

    with pytest.raises(ValueError):
        dados.carregar_perguntas(caminho)


# ---------- fluxo completo ----------

def test_salvar_tudo_e_carregar_tudo_reconstroi_as_relacoes(tmp_path):
    perguntas, quiz, usuario, tentativa = criar_cenario()

    dados.salvar_perguntas(perguntas, tmp_path / "perguntas.json")
    dados.salvar_quizzes([quiz], tmp_path / "quizzes.json")
    dados.salvar_usuarios([usuario], tmp_path / "usuarios.json")
    dados.salvar_tentativas(usuario.tentativas, tmp_path / "tentativas.json")

    perguntas_2 = dados.carregar_perguntas(tmp_path / "perguntas.json")
    quizzes_2 = dados.carregar_quizzes(perguntas_2, tmp_path / "quizzes.json")
    usuarios_2 = dados.carregar_usuarios(tmp_path / "usuarios.json")
    tentativas_2 = dados.carregar_tentativas(
        usuarios_2, quizzes_2, tmp_path / "tentativas.json"
    )

    usuario_2 = usuarios_2[0]
    tentativa_2 = tentativas_2[0]

    # a relação Usuario -> Tentativa foi reconstruída
    assert usuario_2.tentativas == [tentativa_2]
    assert tentativa_2.usuario is usuario_2
    # a relação Tentativa -> Quiz -> Pergunta também
    assert tentativa_2.quiz is quizzes_2[0]
    assert tentativa_2.quiz.perguntas[0] is perguntas_2[0]
    # e os números batem com os originais
    assert tentativa_2.pontuacao == tentativa.pontuacao
    assert usuario_2.calcular_taxa_acerto() == usuario.calcular_taxa_acerto()


def test_carregar_tentativa_de_usuario_desconhecido(tmp_path):
    _, quiz, usuario, tentativa = criar_cenario()
    dados.salvar_tentativas([tentativa], tmp_path / "tentativas.json")

    with pytest.raises(ValueError):
        dados.carregar_tentativas([], [quiz], tmp_path / "tentativas.json")


def test_carregar_tentativa_de_quiz_desconhecido(tmp_path):
    _, quiz, usuario, tentativa = criar_cenario()
    dados.salvar_tentativas([tentativa], tmp_path / "tentativas.json")

    with pytest.raises(ValueError):
        dados.carregar_tentativas([usuario], [], tmp_path / "tentativas.json")