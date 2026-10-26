"""Define a classe Estatistica, que gera os relatórios do sistema."""


class Estatistica:
    """Calcula o desempenho dos usuários e monta relatórios.

    Não guarda dados próprios: só recebe objetos e calcula em cima deles,
    por isso os métodos são estáticos.
    """

    @staticmethod
    def desempenho_por_tema(usuario) -> dict:
        """Acertos, total e taxa de acerto do usuário em cada tema.

        Considera só as tentativas concluídas.
        """
        por_tema = {}

        for tentativa in usuario.tentativas:
            if not tentativa.concluida:
                continue

            for pergunta, acertou in tentativa.resultados_por_pergunta():
                contagem = por_tema.setdefault(
                    pergunta.tema, {"acertos": 0, "total": 0}
                )
                contagem["total"] += 1

                if acertou:
                    contagem["acertos"] += 1

        for contagem in por_tema.values():
            contagem["taxa"] = contagem["acertos"] / contagem["total"]

        return dict(sorted(por_tema.items()))

    @staticmethod
    def desempenho_usuario(usuario) -> dict:
        """Resumo do desempenho: taxa geral e taxa por tema."""
        concluidas = [t for t in usuario.tentativas if t.concluida]

        return {
            "usuario": usuario.nome,
            "tentativas_concluidas": len(concluidas),
            "taxa_acerto_geral": usuario.calcular_taxa_acerto(),
            "por_tema": Estatistica.desempenho_por_tema(usuario),
        }

    @staticmethod
    def relatorio_usuario(usuario) -> str:
        """Monta o relatório de desempenho do usuário em texto."""
        desempenho = Estatistica.desempenho_usuario(usuario)

        linhas = [
            f"Relatório de desempenho - {usuario.nome} ({usuario.matricula_id})"
        ]

        if desempenho["tentativas_concluidas"] == 0:
            linhas.append("Nenhuma tentativa concluída ainda.")
            return "\n".join(linhas)

        linhas.append(
            f"Tentativas concluídas: {desempenho['tentativas_concluidas']}"
        )
        linhas.append(
            f"Taxa de acerto geral: {desempenho['taxa_acerto_geral']:.1%}"
        )
        linhas.append("Por tema:")

        for tema, contagem in desempenho["por_tema"].items():
            linhas.append(
                f"  - {tema}: {contagem['acertos']}/{contagem['total']} "
                f"({contagem['taxa']:.1%})"
            )

        return "\n".join(linhas)