import subprocess
from pathlib import Path
from random import randrange

import mido

from data.escalas import dici_alt
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


def gera_midi(
    notas: list[str],
    duracoes: list[float],
    clave: str,
    diretorio: str,
    tempo_bpm: int = 120,
) -> str:
    """
    Gera arquivo MIDI a partir das notas e durações musicais.

    Args:
        notas: Lista de notas no formato LilyPond (ex: "c'", "d''", "r")
        duracoes: Lista de durações correspondentes em unidades de semicolcheia
        clave: Clave musical ("Sol", "Fá", "Dó")
        diretorio: Diretório onde salvar o arquivo MIDI
        tempo_bpm: Batidas por minuto (padrão: 120)

    Returns:
        Caminho do arquivo MIDI gerado
    """
    # Cria um novo arquivo MIDI
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)

    # Define o tempo (microssegundos por batida)
    # Uma batida = uma semicolcheia no nosso sistema (16 unidades = 1 seminima)
    # 120 BPM = 2 batidas por segundo = 500.000 microssegundos por batida
    tempo_micros = int(60_000_000 / tempo_bpm)
    track.append(mido.MetaMessage("set_tempo", tempo=tempo_micros))

    # Define o instrumento (piano acústico)
    track.append(mido.Message("program_change", program=0, time=0))

    # Mapeamento de oitavas baseado na clave
    octave_offset = {
        "Sol": 4,  # Clave de Sol: oitava central
        "Fá": 3,  # Clave de Fá: oitava abaixo
        "Dó": 4,  # Clave de Dó: oitava central
    }.get(clave, 4)

    current_time = 0

    for nota, dur in zip(notas, duracoes, strict=False):
        # Converte duração: 1 unidade = 1 semicolcheia
        # Em MIDI, tempo é em ticks (usaremos resolução padrão de 480 ticks por batida)
        # Uma semicolcheia = 120 ticks (480/4)
        duration_ticks = int(dur * 120)

        if nota == "r":
            # Pausa - apenas avança o tempo
            current_time += duration_ticks
        else:
            # Nota musical
            # Remove aspas e números de oitava do formato LilyPond
            clean_nota = (
                nota.replace("'", "")
                .replace(",", "")
                .replace("''", "")
                .replace(",,", "")
            )

            # Converte para número MIDI (C4 = 60)
            if clean_nota in dici_alt:
                midi_note = dici_alt[clean_nota]

                # Ajusta oitava baseada na clave e modificadores
                octave = octave_offset
                if "'" in nota:
                    octave += nota.count("'")
                elif "," in nota:
                    octave -= nota.count(",")

                midi_note += (octave - 4) * 12  # 4 é a oitava central

                # Garante que a nota esteja no range MIDI válido (0-127)
                midi_note = max(0, min(127, midi_note))

                # Adiciona mensagens note_on e note_off
                track.append(
                    mido.Message(
                        "note_on", note=midi_note, velocity=64, time=current_time
                    )
                )
                track.append(
                    mido.Message(
                        "note_off", note=midi_note, velocity=64, time=duration_ticks
                    )
                )
                current_time = 0
            else:
                # Se não conseguir mapear a nota, apenas avança o tempo
                current_time += duration_ticks

    # Salva o arquivo MIDI
    base_path = Path(diretorio)
    base_path.mkdir(parents=True, exist_ok=True)

    midi_filename = f"sight_reading_{randrange(0, 10000)}.mid"
    midi_path = base_path / midi_filename

    mid.save(str(midi_path))
    return str(midi_path)
