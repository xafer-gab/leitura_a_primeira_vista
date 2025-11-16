import subprocess
from random import randrange
from data.escalas import dici_alt_lily as a_lily


def comp_lily(notas, clave, fundamental, escala, form_comp):
    #Define armadura de clave:
    fund = a_lily[fundamental]
    if escala == "Maior":
        a_clave = f"\\key {fund} \\major"
    else:
        a_clave = "\\key c \\major"
    
    #Cria strings para LilyPond
    string_lily = ""
    for nota in notas:
        string_lily += f"{nota} "

    #Criar conteúdo LilyPond
    if clave == "Sol":
        clef = "\\clef G"
    elif clave == "Fá":
        clef = "\\clef F"
    else:
        clef = "\\clef C"

    #Gera script lilypond
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
    
    return f"{r_dir}.{formato}"
