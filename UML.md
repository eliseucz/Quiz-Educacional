Pergunta
- enunciado: str
- alternativas: list[str]
- indice_resposta_correta: int
- dificuldade: str
- tema: str

Métodos:
+ validar_alternativas(): bool
+ validar_indice_resposta(): bool
+ __str__(): str
+ __eq__(outra): bool


ValidadorAlternativas
Métodos:
+ validar_quantidade(alternativas): bool
+ validar_indice(indice, alternativas): bool


PerguntaMultiplaEscolha : Pergunta, ValidadorAlternativas

Métodos:
+ validar(): bool
+ __str__(): str


Quiz
- titulo: str
- perguntas: list[Pergunta]
- numero_tentativas_maximo: int
- tempo_limite_minutos: int | None
- pontuacao_maxima: int

Métodos:
+ adicionar_pergunta(pergunta): None
+ calcular_pontuacao_maxima(): int
+ pode_realizar(usuario): bool
+ __str__(): str
+ __len__(): int
+ __iter__()


Usuario
- nome: str
- email: str
- matricula_id: str
- tentativas: list[Tentativa]

Métodos:
+ adicionar_tentativa(tentativa): None
+ calcular_taxa_acerto(): float
+ calcular_desempenho_por_tema(): dict
+ __str__(): str


Tentativa
- usuario: Usuario
- quiz: Quiz
- respostas: list[int]
- pontuacao: float
- tempo_total: float
- taxa_acertos: float
- concluida: bool
- data_hora: str

Métodos:
+ iniciar(): None
+ registrar_resposta(indice): None
+ finalizar(): None
+ calcular_pontuacao(): float
+ calcular_taxa_acertos(): float


Estatistica

Métodos:
+ desempenho_usuario(usuario): dict
+ desempenho_por_tema(usuario): dict
+ ranking_usuarios(usuarios): list
+ questoes_mais_erradas(tentativas): list
+ evolucao_usuario(usuario): list


Relacionamentos:

PerguntaMultiplaEscolha --|> Pergunta
PerguntaMultiplaEscolha --|> ValidadorAlternativas

Quiz "1" o-- "1..*" Pergunta
Usuario "1" o-- "0..*" Tentativa

Tentativa "*" --> "1" Usuario
Tentativa "*" --> "1" Quiz

Estatistica ..> Usuario
Estatistica ..> Tentativa
Estatistica ..> Quiz
