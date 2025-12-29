import tempfile

from data import duracoes
from gui.interface import interface
from src import formata, gera, renderiza

# Configuração padrão usando diretório temporário do sistema
DEFAULT_DIR = tempfile.gettempdir()


def gera_formata_renderiza(
    fundamental: str,
    escala: str,
    modelo: str,
    clave: str,
    oitavas: int,
    form_comp: str,
    fig_selec: list[str],
    ligadura: bool,
    pausa_p: int,
    num_comp: int,
    diretorio: str,
    midi: bool = False,
) -> str:
    """Função principal que integra a geração, formatação e renderização musical."""

    if not diretorio:
        diretorio = DEFAULT_DIR

    # Processamento
    lis_dur_selec = gera.gera_lista_dur(fig_selec)
    f_c = duracoes.form_compasso[form_comp]

    duracoes_rand = gera.adiciona_valores(
        lis_dur_selec, f_c[0], f_c[1], num_comp, ligadura=ligadura
    )
    alturas_rand = gera.nota_randomica(
        fundamental,
        escala,
        modelo,
        len(duracoes_rand),
        clave,
        oitavas,
        pausa_probab=pausa_p,
    )

    notas = formata.dur_formata(duracoes_rand, alturas_rand, f_c[0], f_c[1])
    l_script = renderiza.comp_lily(
        notas, clave, fundamental, escala, form_comp, midi=midi
    )

    # Exportação (sempre em PNG para visualização na interface)
    caminho_arquivo = renderiza.exporta(l_script, diretorio, formato="png")

    return caminho_arquivo


if __name__ == "__main__":
    interface(gera_formata_renderiza)
