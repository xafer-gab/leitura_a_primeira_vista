import random
from typing import Any, Union

import data.duracoes as duracoes
import data.escalas as escalas


def permuta(lista: list, tipo: str = "permuta") -> Union[list, Any]:
    """Permuta uma lista ou seleciona um elemento aleatório dela."""
    if tipo == "permuta":
        copia = lista[:]
        random.shuffle(copia)
        return copia
    if tipo == "seleciona":
        return random.choice(lista)
    raise ValueError("Tipos válidos: 'permuta' e 'seleciona'")


def gera_lista_dur(duracoes_lis: list[str]) -> list[float]:
    """Converte nomes de figuras rítmicas para seus valores numéricos."""
    return [duracoes.dur_dic[dur] for dur in duracoes_lis]


def deduz_semicol(tempos: int, uni_tempo: int) -> int:
    """Calcula a duração total de um compasso em unidades de semicolcheia."""
    f_comp = f"{tempos}/{uni_tempo}"
    return sum(duracoes.agrupamento[f_comp])


def adiciona_valores(
    lista_dur: list[float],
    tempos: int,
    uni_tempo: int,
    num_comp: int,
    ligadura: bool = False,
) -> list[float]:
    """Gera uma sequência de durações rítmicas randômicas."""
    duracoes_res = []
    duracao_total_compasso = deduz_semicol(tempos, uni_tempo)

    if not ligadura:
        for _ in range(num_comp):
            restante = duracao_total_compasso
            while restante > 0:
                possiveis = [d for d in lista_dur if d <= restante]

                if not possiveis:
                    duracoes_res.append(restante)
                    break

                escolha = random.choice(possiveis)
                duracoes_res.append(escolha)
                restante -= escolha
    else:
        total_geral = num_comp * duracao_total_compasso
        while total_geral > 0:
            possiveis = [d for d in lista_dur if d <= total_geral]
            if not possiveis:
                duracoes_res.append(total_geral)
                break
            escolha = random.choice(possiveis)
            duracoes_res.append(escolha)
            total_geral -= escolha

    return duracoes_res


def _get_modelo_harm(modelo: str, escala_len: int) -> list[float]:
    """Retorna os pesos para o modelo probabilístico."""
    if modelo == "Igual":
        return [1.0] * escala_len

    pesos = escalas.modelos_probabilisticos.get(modelo, [])
    if escala_len > len(pesos):
        return pesos + [0.0] * (escala_len - len(pesos))
    return pesos[:escala_len]


def nota_randomica(
    fund: str,
    modo: str,
    modelo: str,
    n_notas: int,
    clave: str,
    oitavas: int,
    pausa_probab: int = 20,
) -> list[str]:
    """Gera uma sequência de alturas (notas) randômicas."""
    escala = escalas.escala(fund, modo)
    escala_len = len(escala)

    # Prepara oitavas disponíveis
    oitavas_map = {"Sol": escalas.c_sol, "Fá": escalas.c_fa, "Dó": escalas.c_do}
    oitavas_disponiveis = oitavas_map.get(clave, escalas.c_sol)[:oitavas]

    # Prepara modelo para Dodecafônico
    serie_dodeca = []
    if modelo == "Dodecafônico":
        serie_dodeca = list(range(escala_len))
        random.shuffle(serie_dodeca)

    pesos = _get_modelo_harm(modelo, escala_len)
    alturas = []
    idx_dodeca = 0

    for _ in range(n_notas):
        # Sorteia pausa
        if pausa_probab > 0 and random.randint(1, 100) <= pausa_probab:
            alturas.append("r")
            continue

        # Sorteia nota
        if modelo == "Dodecafônico":
            nota = escala[serie_dodeca[idx_dodeca]]
            idx_dodeca = (idx_dodeca + 1) % escala_len
        else:
            nota = random.choices(escala, weights=pesos, k=1)[0]

        # Sorteia oitava
        oitava = random.choice(oitavas_disponiveis)
        alturas.append(f"{nota}{oitava}")

    return alturas
