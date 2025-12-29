import subprocess
from pathlib import Path
from random import randrange

from data.escalas import dici_alt_lily as a_lily


def comp_lily(
    notas: list[str],
    clave: str,
    fundamental: str,
    escala: str,
    form_comp: str,
    midi: bool = False,
) -> str:
    """Gera o script LilyPond para as notas fornecidas."""
    # Define armadura de clave:
    fund = a_lily[fundamental]
    if escala == "Maior":
        a_clave = f"\\key {fund} \\major"
    else:
        a_clave = "\\key c \\major"

    # Cria strings para LilyPond
    string_lily = " ".join(notas)

    # Criar conteúdo LilyPond
    if clave == "Sol":
        clef = "\\clef G"
    elif clave == "Fá":
        clef = "\\clef F"
    else:
        clef = "\\clef C"

    # Se quiser MIDI, adiciona bloco \midi
    midi_block = "\\midi { }" if midi else ""

    # Gera script lilypond
    lilypond_codigo = f"""
    \\version "2.24.4"
    #(set-global-staff-size 17)
    \\paper {{
        #(set-paper-size "a6")
        page-breaking = #ly:one-page-breaking
    }}
    \\header {{tagline = ##f}}
    \\layout {{indent = 0}}
    {{
        \\time {form_comp}
        {clef}
        {a_clave}
        {string_lily} \\bar "|."
    }}
    {midi_block}
    """
    return lilypond_codigo


def exporta(lily_codigo: str, diretorio: str, formato: str = "png") -> str:
    """Executa o LilyPond para gerar o arquivo de saída."""
    # Verifica se lilypond está instalado
    try:
        subprocess.run(["lilypond", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise RuntimeError(
            "LilyPond não encontrado. Certifique-se de que está instalado e no PATH."
        ) from None

    # Gera arquivo temporário .ly
    base_path = Path(diretorio)
    base_path.mkdir(parents=True, exist_ok=True)

    tmp_name = f"sight_reading_{randrange(0, 10000)}"
    ly_file = base_path / f"{tmp_name}.ly"
    output_base = base_path / tmp_name

    with open(ly_file, "w") as f:
        f.write(lily_codigo)

    # Executa lilypond por CLI
    cli = [
        "lilypond",
        "--silent",
        f"--format={formato}",
        f"--output={output_base}",
        str(ly_file),
    ]

    result = subprocess.run(cli, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Erro LilyPond: {result.stderr}")

    # Remove script Lily
    if ly_file.exists():
        ly_file.unlink()

    return f"{output_base}.{formato}"
