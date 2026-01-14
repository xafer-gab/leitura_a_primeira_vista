import subprocess
from random import randrange
from data.escalas import dici_alt_lily as a_lily
from data.escalas import instrumentos as instrumentos 
from data.duracoes import div_lily

def comp_lily(notas, clave, fundamental, escala, form_comp, andamento_midi, inst_midi):
    #Define armadura de clave:
    fund = a_lily[fundamental]
    if escala == "Maior/Menor":
        a_clave = f"\\key {fund} \\major"
    else:
        a_clave = "\\key c \\major"
    
    #Cria strings para LilyPond
    string_lily = ""
    for nota in notas:
        string_lily += f"{nota} "

    #Criar conteúdo LilyPond
    n_linhas = ""
    if clave == "Sol":
        clef = "\\clef G"
    elif clave == "Fá":
        clef = "\\clef F"
    elif clave == "Dó":
        clef = "\\clef C"
    else:
        a_clave = "\\key c \\major" #Sem armadura de clave
        clef = "\\clef percussion"
        n_linhas = "\\override Staff.StaffSymbol.line-count = #1"
    
    andamento = andamento_midi
    instrumento = instrumentos[inst_midi]
    
    #Gera script lilypond
    lilypond_codigo = f"""
    \\version "2.24.4"
    #(set-global-staff-size 17)
    \\paper {{
        #(set-paper-size "a4") 
        page-breaking = #ly:one-page-breaking
    }}
    \\header {{tagline = ##f}}
    \\score {{
        {{  \\tempo 4 = {andamento}
            \\set Staff.midiInstrument = #"{instrumento}"
            \\time {div_lily[form_comp]} {form_comp}
            {n_linhas}
            {clef}
            {a_clave}
            {string_lily} \\bar "|."
        }}
        \\layout {{indent = 0}}
        \\midi {{ \\tempo 4 = 60 }}
    }}
    """
    return lilypond_codigo

def exporta(lily_codigo, diretorio, formato="pdf"):
    
    #Gera arquivo temporário .ly
    tmp_n = str(randrange(0, 10000))
    r_dir = f"{diretorio}/{tmp_n}"
    with open(f"{r_dir}.ly", "w") as lily:
        lily.write(lily_codigo)
    
    #Executa lilypond por CLI
    out_dir = f"--output={r_dir}"
    in_dir = f"{r_dir}.ly"
    form = f"--format={formato}"
    cli = ["lilypond", "--silent", form, out_dir, in_dir]
    subprocess.run(cli)
    
    #Remove script Lily
    subprocess.run(["rm", f"{r_dir}.ly"]) 
    
    #Saída partitura, áudio MIDI
    return f"{r_dir}.{formato}", r_dir
