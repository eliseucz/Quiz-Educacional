"""Pequena demonstração do projeto. Execute com: python main.py"""

from src.pergunta import Pergunta
from src.quiz import Quiz

p1 = Pergunta("Quanto é 2 + 2?", ["3", "4", "5"], 1, "FÁCIL", "Matemática")
p2 = Pergunta("Quanto é 7 x 8?", ["54", "56", "64"], 1, "DIFÍCIL", "Matemática")

quiz = Quiz("Quiz de teste")
quiz.adicionar_pergunta(p1)
quiz.adicionar_pergunta(p2)

print(quiz)
print("Quantidade de perguntas:", len(quiz))
print("Pontuação máxima:", quiz.pontuacao_maxima)

for pergunta in quiz:
    print("-", pergunta)

try:
    quiz.adicionar_pergunta(p1)  # repetida
except ValueError as erro:
    print("Erro esperado:", erro)
