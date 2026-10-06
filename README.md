  # Sistema de Quiz Educacional

## 1. Descrição do projeto

O Quiz Educacional será uma aplicação orientada a objetos para criação, gerenciamento e execução de quizzes com perguntas de múltipla escolha. O sistema deverá permitir o cadastro de perguntas, a montagem de quizzes, a realização de tentativas por usuários e o registro de resultados. Também estão previstos recursos de pontuação, desempenho por tema, estatísticas, ranking e evolução do desempenho ao longo do tempo.
A persistência dos dados será planejada para JSON ou SQLite, sem uso de frameworks ORM. 
A interface poderá ser implementada posteriormente como uma aplicação de linha de comando (CLI).

## 2. Objetivo

Desenvolver um sistema educacional simples que organize quizzes, registre as respostas dos usuários e permita acompanhar o desempenho obtido nas diferentes avaliações.

## 3. Estrutura planejada de classes

* `Pergunta`: classe base do sistema.
* `ValidadorAlternativas`: responsável pelas validações das alternativas.
* `PerguntaMultiplaEscolha`: especialização de `Pergunta`.
* `Quiz`: representa um quiz e sua coleção de perguntas.
* `Usuario`: representa o usuário e seu histórico.
* `Tentativa`: representa uma execução de um quiz.
* `Estatistica`: responsável pelos cálculos e relatórios.

## 4. Relacionamentos principais

* `Quiz` agrega várias perguntas.
* `Usuario` possui uma lista de tentativas.
* `Tentativa` referencia um usuário e um quiz.
* `PerguntaMultiplaEscolha` herda de `Pergunta` e `ValidadorAlternativas`.
* `Estatistica` utiliza dados das demais entidades para gerar relatórios.

## 5. Persistência planejada

O módulo `dados.py` será responsável por salvar e carregar quizzes, perguntas, usuários e tentativas utilizando JSON ou SQLite.

## 6. Estado atual

Esta versão corresponde à segunda etapa do Projeto 1. 
As classes foram criadas como estrutura inicial, contendo docstrings que registram sua finalidade. 
A implementação das regras de negócio, validações, persistência, testes e interface será realizada nas etapas seguintes.
