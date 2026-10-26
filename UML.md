# UML textual - Sistema de Quiz Educacional

Legenda: itens marcados com *(planejado)* ainda não foram implementados e estão previstos para as próximas etapas. Os demais já existem no código.

## 1. Pergunta

**Pergunta**
- `enunciado: str`
- `alternativas: list[str]`
- `indice_resposta_correta: int`
- `dificuldade: str` — valores válidos: FÁCIL, MÉDIO, DIFÍCIL
- `tema: str`

Constantes de classe:
- `PESOS_POR_DIFICULDADE: dict` — `{"FÁCIL": 1, "MÉDIO": 2, "DIFÍCIL": 3}`
- `DIFICULDADES_VALIDAS: set`

Propriedade calculada:
- `peso: int` — pontos que a pergunta vale, conforme a dificuldade

Métodos principais:
- `validar_alternativas(): bool`
- `validar_indice_resposta(): bool`
- `verificar_resposta(indice: int): bool`
- `to_dict(): dict`
- `from_dict(dados: dict): Pergunta` — método de classe (`@classmethod`)
- `__str__(): str`
- `__eq__(outra): bool` — compara enunciado e tema
- `__hash__(): int` — coerente com `__eq__`

## 2. ValidadorAlternativas

**ValidadorAlternativas** (mixin)

Constantes de classe:
- `MIN_ALTERNATIVAS: int` — 3
- `MAX_ALTERNATIVAS: int` — 5

Métodos principais (métodos de classe):
- `validar_quantidade(alternativas: list[str]): bool`
- `validar_indice(indice: int, alternativas: list[str]): bool`

## 3. PerguntaMultiplaEscolha

**PerguntaMultiplaEscolha : Pergunta, ValidadorAlternativas**

Herança múltipla que separa a representação da pergunta das regras auxiliares de validação. Ordem de resolução de métodos (MRO): `PerguntaMultiplaEscolha → Pergunta → ValidadorAlternativas → object`.

Métodos principais:
- `validar(): bool`
- `__str__(): str`

## 4. Quiz

**Quiz**
- `titulo: str`
- `perguntas: list[Pergunta]`
- `numero_tentativas_maximo: int`
- `tempo_limite_minutos: int | None`
- `pontuacao_maxima: int` — calculada automaticamente

Métodos principais:
- `adicionar_pergunta(pergunta: Pergunta): None` — recusa duplicatas (mesmo enunciado e tema)
- `calcular_pontuacao_maxima(): int`
- `to_dict(): dict` — guarda apenas referências (enunciado e tema) às perguntas
- `from_dict(dados: dict, perguntas_disponiveis: list[Pergunta]): Quiz` — método de classe
- `pode_realizar(usuario: Usuario): bool` *(planejado)*
- `__str__(): str`
- `__len__(): int`
- `__iter__()`

## 5. Usuario

**Usuario**
- `nome: str`
- `email: str`
- `matricula_id: str`
- `tentativas: list[Tentativa]`

Métodos principais:
- `adicionar_tentativa(tentativa: Tentativa): None` — só aceita tentativas que apontam para este usuário e recusa duplicatas
- `calcular_taxa_acerto(): float` — acertos sobre o total de perguntas das tentativas concluídas
- `to_dict(): dict` — não inclui as tentativas
- `from_dict(dados: dict): Usuario` — método de classe
- `__str__(): str`

## 6. Tentativa

**Tentativa**
- `usuario: Usuario`
- `quiz: Quiz`
- `respostas: list[int]`
- `pontuacao: float` — calculada
- `tempo_total: float` — em segundos, definido ao finalizar
- `taxa_acertos: float` — calculada
- `concluida: bool`
- `data_hora: str | None` — início da tentativa (ISO 8601)

Estados: criada → iniciada → concluída.

Métodos principais:
- `iniciar(): None`
- `registrar_resposta(indice: int): None`
- `finalizar(): None`
- `calcular_pontuacao(): float` — soma dos pesos das perguntas acertadas
- `calcular_taxa_acertos(): float`
- `resultados_por_pergunta(): list[tuple[Pergunta, bool]]`
- `to_dict(): dict` — guarda apenas o ID do usuário e o título do quiz
- `from_dict(dados: dict, usuario: Usuario, quiz: Quiz): Tentativa` — método de classe

Erros levantados: `TypeError` (tipo incorreto), `ValueError` (valor inválido) e `RuntimeError` (operação fora do estado correto).

## 7. Estatistica

**Estatistica** (métodos estáticos, sem estado próprio)

Implementados:
- `desempenho_usuario(usuario: Usuario): dict`
- `desempenho_por_tema(usuario: Usuario): dict`
- `relatorio_usuario(usuario: Usuario): str`

Planejados:
- `ranking_usuarios(usuarios: list[Usuario]): list` *(planejado)*
- `questoes_mais_erradas(tentativas: list[Tentativa]): list` *(planejado)*
- `evolucao_usuario(usuario: Usuario): list` *(planejado)*

Todos os cálculos consideram apenas tentativas concluídas.

## 8. Dados

**Módulo `dados.py`**

Funções (o parâmetro `caminho` tem valor padrão dentro da pasta `dados/`):
- `salvar_perguntas(perguntas, caminho)` / `carregar_perguntas(caminho)`
- `salvar_quizzes(quizzes, caminho)` / `carregar_quizzes(perguntas, caminho)`
- `salvar_usuarios(usuarios, caminho)` / `carregar_usuarios(caminho)`
- `salvar_tentativas(tentativas, caminho)` / `carregar_tentativas(usuarios, quizzes, caminho)`

Arquivos: `perguntas.json`, `quizzes.json`, `usuarios.json` e `tentativas.json`.

Ordem de carregamento: perguntas → quizzes → usuários → tentativas. Ao carregar tentativas, cada uma é reconectada ao usuário (pelo `matricula_id`) e ao quiz (pelo título) e adicionada à lista do usuário.

## 9. Relacionamentos

- `PerguntaMultiplaEscolha --|> Pergunta`
- `PerguntaMultiplaEscolha --|> ValidadorAlternativas`
- `Quiz "1" o-- "1..*" Pergunta`
- `Usuario "1" o-- "0..*" Tentativa`
- `Tentativa "*" --> "1" Usuario`
- `Tentativa "*" --> "1" Quiz`
- `Estatistica ..> Usuario`
- `Estatistica ..> Tentativa`
- `dados.py ..> Pergunta, Quiz, Usuario, Tentativa` (usa `to_dict` e `from_dict`)

## 10. Regras que a modelagem suporta

Implementadas:
- Cada pergunta possui entre 3 e 5 alternativas.
- O índice da resposta correta aponta para uma alternativa existente.
- Não há duplicidade de enunciado dentro do mesmo tema em um quiz.
- A pontuação máxima do quiz é a soma dos pesos das perguntas conforme a dificuldade.
- Uma tentativa só aceita respostas depois de iniciada, dentro das alternativas existentes, e só pode ser finalizada com todas as perguntas respondidas.
- Tentativas incompletas não participam das estatísticas.

Planejadas:
- O usuário não pode ultrapassar o limite de tentativas configurado *(planejado)*.
- Se o tempo limite for excedido, o quiz é encerrado automaticamente *(planejado)*.
- Tentativas incompletas não participam do ranking *(planejado, junto do ranking)*.
