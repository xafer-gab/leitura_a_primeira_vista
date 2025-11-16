import data.duracoes as duracoes
import src.gera as gera

def dur_formata(lis_dur, lis_alt, tempos, uni_temp):
    
    #Variáveis gerais
    f_comp = f"{tempos}/{uni_temp}"
    quebra_sistema = duracoes.quebras[f_comp]
    agrup = duracoes.agrupamento[f_comp]
    c_agrup = sum(agrup)
    n_agrup = len(agrup)
    
    #Contadores iniciais
    qsis = 0
    c = agrup[0]
    j = 0
    
    #Iteração
    lis_notas_form = []
    for i, dur in enumerate(lis_dur):
        altura = lis_alt[i]
        fig = 0
        d = dur
        while d > 0:
            
            #Realiza quebra de sistema
            if qsis == quebra_sistema:
                lis_notas_form.append("\\break")
                qsis = 0
                
            #Preenche com figuras longas, se possível
            if d in [8, 12, 16] and d <= c_agrup and c == agrup[j % n_agrup]:
                lis_notas_form.append(altura+duracoes.lilydur[d])
                for v in range(d):
                    print (d, c, fig)
                    c -= 1; qsis += 1
                    if c == 0:
                        idx = j % n_agrup
                        c = agrup[idx]
                        j += 1
                break
            
            #Quebra em figuras menores com ligadura
            else:
                d -= 1; c -= 1; fig += 1; qsis += 1
                if d == 0:
                    lis_notas_form.append(altura+duracoes.lilydur[fig])
                if c == 0:
                    j += 1
                    idx = j % n_agrup
                    c = agrup[idx]
                    if d > 0:
                        lis_notas_form.append(altura+duracoes.lilydur[fig]+"~")
                        fig = 0
    
    #Retorna lista de elementos                
    return lis_notas_form
