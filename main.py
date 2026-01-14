import os
from src import gera, formata, renderiza, mid_aud
from data import duracoes, escalas
from gui.interface import interface

#Produz diretório de arquivos temporários
pasta_temp = "tmp_part"
def prepara_tmp():
    #Cria a pasta se não existir
    if not os.path.exists(pasta_temp):
        os.makedirs(pasta_temp)

    #Limpa arquivos temporários
    for arq in os.listdir(pasta_temp):
        arquivo = os.path.join(pasta_temp, arq)
        os.remove(arquivo)

def gera_formata_renderiza(
        fundamental, escala, modelo, clave, oitavas, 
        num_comp, form_comp, pausa_p, dispersao, ligadura,
        fig_selec,
        andamento_midi, inst_midi):
    
    #Gere arquivos temporários
    prepara_tmp()
    
    #Durações
    diretorio = "tmp_part"
    lis_dur_selec = gera.gera_lista_dur(fig_selec)
    f_c = duracoes.form_compasso[form_comp]
    duracoes_rand = gera.adiciona_valores(lis_dur_selec, f_c[0], f_c[1], num_comp, ligadura=ligadura)
    
    #Alturas
    if not clave == "Percussão":
        alturas_rand = gera.nota_randomica(
            fundamental, escala, modelo, len(duracoes_rand), 
            clave, oitavas, pausa_probab=pausa_p, dispersao=(dispersao/100)
            )
    else:
        alturas_rand = gera.nota_percussao(len(duracoes_rand), pausa_probab=pausa_p)
    
    #Formatação
    notas = formata.dur_formata(duracoes_rand, alturas_rand, f_c[0], f_c[1])
    l_script = renderiza.comp_lily(notas, clave, fundamental, escala, form_comp, andamento_midi, inst_midi)
    partitura, audio_dir = renderiza.exporta(l_script, diretorio, formato="png")
    
    #Gera arquivo de áudio
    mid_aud.midi_para_wav(f"{audio_dir}.midi", f"{audio_dir}.wav")
    
    #Retorna partitura (.png) e áudio (.wav)
    return partitura, f"{audio_dir}.wav"

interface(gera_formata_renderiza)
