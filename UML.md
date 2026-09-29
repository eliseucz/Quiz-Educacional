# UML - Sistema de Quiz Educacional

```mermaid
classDiagram

    class Pergunta {
        -enunciado
        -alternativas
        -indice_resposta_correta
        -dificuldade
        -tema
        +validar_alternativas()
        +validar_indice_resposta() 
        +__str__()
        +__eq__(outra) 
    }

    class ValidadorAlternativas {
        +validar_quantidade(alternativas)
        +validar_indice(indice, alternativas) 
    }

    class PerguntaMultiplaEscolha {
        +validar() 
        +__str__()
    }

    class Quiz {
        -titulo
        -perguntas
        -numero_tentativas_maximo
        -tempo_limite_minutos
        -pontuacao_maxima
        +adicionar_pergunta(pergunta) 
        +calcular_pontuacao_maxima()
        +pode_realizar(usuario) 
        +__str__() 
        +__len__() 
        +__iter__()
    }

    class Usuario {
        -nome
        -email
        -matricula_id
        -tentativas
        +adicionar_tentativa(tentativa) 
        +calcular_taxa_acerto() 
        +calcular_desempenho_por_tema() 
        +__str__() 
    }

    class Tentativa {
        -Usuario usuario
        -Quiz quiz
        -respostas
        -pontuacao
        -tempo_total
        -taxa_acertos
        -concluida
        -data_hora
        +iniciar() 
        +registrar_resposta(indice) 
        +finalizar() 
        +calcular_pontuacao() 
        +calcular_taxa_acertos() 
    }

    class Estatistica {
        +desempenho_usuario(usuario) 
        +desempenho_por_tema(usuario) 
        +ranking_usuarios(usuarios) 
        +questoes_mais_erradas(tentativas) 
        +evolucao_usuario(usuario) 
    }

    PerguntaMultiplaEscolha --|> Pergunta
    PerguntaMultiplaEscolha --|> ValidadorAlternativas

    Quiz "1" o-- "1..*" Pergunta
    Usuario "1" o-- "0..*" Tentativa

    Tentativa "*" --> "1" Usuario
    Tentativa "*" --> "1" Quiz

    Estatistica ..> Usuario
    Estatistica ..> Tentativa
    Estatistica ..> Quiz
```
