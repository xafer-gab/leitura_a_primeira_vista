import data.duracoes as duracoes


def dur_formata(
    lis_dur: list[float], lis_alt: list[str], tempos: int, uni_temp: int
) -> list[str]:
    """
    Formata as durações e alturas para o formato LilyPond,
    lidando com quebras de compasso e agrupamentos rítmicos.
    """
    f_comp = f"{tempos}/{uni_temp}"
    quebra_sistema = duracoes.quebras[f_comp]
    agrup = duracoes.agrupamento[f_comp]
    c_agrup = sum(agrup)
    n_agrup = len(agrup)

    qsis_count = 0
    compasso_restante = agrup[0]
    agrup_idx = 0

    lis_notas_form = []

    for dur, altura in zip(lis_dur, lis_alt, strict=False):
        d_restante = dur
        fig_acumulada = 0

        while d_restante > 0:
            # Realiza quebra de sistema
            if qsis_count >= quebra_sistema:
                lis_notas_form.append("\\break")
                qsis_count = 0

            # Tenta preencher com figuras longas inteiras (8, 12, 16)
            pode_longa = (
                d_restante in [8, 12, 16]
                and d_restante <= c_agrup
                and compasso_restante == agrup[agrup_idx % n_agrup]
            )

            if pode_longa:
                lis_notas_form.append(f"{altura}{duracoes.lilydur[d_restante]}")
                for _ in range(int(d_restante)):
                    compasso_restante -= 1
                    qsis_count += 1
                    if compasso_restante <= 0:
                        agrup_idx += 1
                        compasso_restante = agrup[agrup_idx % n_agrup]
                break

            # Quebra em figuras menores com ligadura
            d_restante -= 1
            compasso_restante -= 1
            fig_acumulada += 1
            qsis_count += 1

            if d_restante == 0:
                lis_notas_form.append(f"{altura}{duracoes.lilydur[fig_acumulada]}")

            if compasso_restante == 0:
                agrup_idx += 1
                compasso_restante = agrup[agrup_idx % n_agrup]
                if d_restante > 0:
                    lis_notas_form.append(f"{altura}{duracoes.lilydur[fig_acumulada]}~")
                    fig_acumulada = 0

    return lis_notas_form
