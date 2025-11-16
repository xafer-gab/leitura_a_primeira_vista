from src import gera, formata, renderiza
from data import duracoes, escalas
from gui.interface import interface

#Variáves globais (mudar a forma de selecionar)
fundamental = "Dó"
escala = "Maior" 
modelo = "Jônio"
clave = "Sol"
oitavas = 1 #[1, 2, 3]
form_comp = "4/4"
fig_selec = ["Colcheia", "Semicolcheia"]
ligadura = False
pausa_p = 0
num_comp = 12  
diretorio = "/tmp"

def gera_formata_renderiza(fundamental, escala, modelo, clave, oitavas, form_comp, fig_selec, ligadura, pausa_p, num_comp, diretorio):
    lis_dur_selec = gera.gera_lista_dur(fig_selec)
    f_c = duracoes.form_compasso[form_comp]
    duracoes_rand = gera.adiciona_valores(lis_dur_selec, f_c[0], f_c[1], num_comp, ligadura=ligadura)
    alturas_rand = gera.nota_randomica(fundamental, escala, modelo, len(duracoes_rand), clave, oitavas, pausa_probab=pausa_p)
    notas = formata.dur_formata(duracoes_rand, alturas_rand, f_c[0], f_c[1])
    l_script = renderiza.comp_lily(notas, clave, fundamental, escala, form_comp)
    exporta = renderiza.exporta(l_script, diretorio, formato="png")
    return exporta

interface(gera_formata_renderiza)
