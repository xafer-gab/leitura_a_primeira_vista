import data.duracoes as duracoes
import src.gera as gera

def acomoda_decimais(altura, duracao, lig):
    if duracao in duracoes.lilydur.keys():
        return f"{altura}{duracoes.lilydur[duracao]}{lig}"
    elif altura == "\\break":
        return "\\break"
    else:
        d = duracao
        res = 0
        figs = ""
        while d > 0:
            d -= 0.25; res += 0.25
            if d in list(duracoes.lilydur.keys()):
                primeira = duracoes.lilydur[d]
                segunda = duracoes.lilydur[res]
                figs += f"{altura}{primeira}~{altura}{segunda}{lig}"
                break
        return figs

def dur_formata(lis_dur, lis_alt, tempos, uni_temp):
    
    #Variáveis gerais
    f_comp = f"{tempos}/{uni_temp}"
    quebra_sistema = duracoes.quebras[f_comp]
    agrup = duracoes.agrupamento[f_comp]
    dur_min = 0.25
    
    #Contadores iniciais
    t_total = sum(lis_dur)/dur_min  #Tempo total
    qsis = 0                        #Valor do sistema
    comp = sum(agrup)               #Valor do compasso
    n_agrup = len(agrup)            #Elementos do agrupamento
    i_agrup = 0                     #Índice do agrupamento
    c_agrup = agrup[i_agrup]        #Valor do agrupamento

    
    #Iteração
    i = 0
    lis_notas_form = []
    lis_comp = []
    altura = lis_alt[i]
    duracao = lis_dur[i]
    d = 0
    
    for j in range(int(t_total)):
        #Realiza quebra de sistema
        if qsis == quebra_sistema:
            lis_comp.append(["\\break", 0, ""])
            qsis = 0
        if comp == 0:
            comp = sum(agrup)
        if c_agrup == 0:
            i_agrup = (i_agrup + 1) % n_agrup
            c_agrup = agrup[i_agrup]
       
        #FIXME: Necessário, porém verboso.
        #Agrupamentos comuns e exceções. 
        #Atenção para os detalhes numéricos dos blocos!
        
        #Compasso inteiro
        if duracao == sum(agrup):
            lis_comp.append([altura, duracao, ""])
            d = 0; i_agrup = 0; c_agrup = agrup[i_agrup]; comp = 0; qsis += sum(agrup)
            if i >= len(lis_alt) - 1: break
            i += 1; altura = lis_alt[i]; duracao = lis_dur[i]
            continue
        
        #Meio compasso em 4/4
        if duracao == 8 and sum(agrup) in [16] and comp in [8, 16]:
            lis_comp.append([altura, duracao, ""])
            i_agrup = (i_agrup + 2) % n_agrup; 
            d = 0; c_agrup = agrup[i_agrup]; comp -= 8; qsis += 8
            if i >= len(lis_alt) - 1: break
            i += 1; altura = lis_alt[i]; duracao = lis_dur[i]
            continue
            
        #Meio compasso em 6/4
        meio_comp = sum(agrup) / 2
        if duracao == 12 and sum(agrup) in [24] and comp in [24, 12]:
            lis_comp.append([altura, duracao, ""])
            i_agrup = (i_agrup + 3) % n_agrup; 
            d = 0; c_agrup = agrup[i_agrup]; comp -= 12; qsis += 12
            if i >= len(lis_alt) - 1: break
            i += 1; altura = lis_alt[i]; duracao = lis_dur[i]
            continue
        
        #1/3 de compasso em 6/4    
        terco_comp = sum(agrup) / 3
        if duracao == terco_comp and sum(agrup) in [24] and comp in [24, 16, 8]:
            lis_comp.append([altura, duracao, ""])
            i_agrup = (i_agrup + 2) % n_agrup; 
            d = 0; c_agrup = agrup[i_agrup]; comp -= terco_comp; qsis += terco_comp
            if i >= len(lis_alt) - 1: break
            i += 1; altura = lis_alt[i]; duracao = lis_dur[i]
            continue
        
        #Mínima pontuada em 4/4
        if duracao == 12 and sum(agrup) in [16] and comp in [16, 12] and d == 0:
            lis_comp.append([altura, duracao, ""])
            i_agrup = (i_agrup + 3) % n_agrup; 
            d = 0; c_agrup = agrup[i_agrup]; comp -= 12; qsis += 12
            if i >= len(lis_alt) - 1: break
            i += 1; altura = lis_alt[i]; duracao = lis_dur[i]
            continue
    
        #Mínima pontuada em 5/4
        if duracao == 12 and sum(agrup) in [20] and comp in [20, 16, 12] and d == 0:
            lis_comp.append([altura, duracao, ""])
            i_agrup = (i_agrup + 3) % n_agrup; 
            d = 0; c_agrup = agrup[i_agrup]; comp -= 12; qsis += 12
            if i >= len(lis_alt) - 1: break
            i += 1; altura = lis_alt[i]; duracao = lis_dur[i]
            continue
        
        #Mínima pontuada em 6/4
        if duracao == 12 and sum(agrup) in [24] and comp in [24, 20, 16, 12] and d == 0:
            lis_comp.append([altura, duracao, ""])
            i_agrup = (i_agrup + 3) % n_agrup; 
            d = 0; c_agrup = agrup[i_agrup]; comp -= 12; qsis += 12
            if i >= len(lis_alt) - 1: break
            i += 1; altura = lis_alt[i]; duracao = lis_dur[i]
            continue
            
        #Mínima pontuada em 7/4
        if duracao == 12 and sum(agrup) in [28] and comp in [28, 24, 20, 16, 12] and d == 0:
            lis_comp.append([altura, duracao, ""])
            i_agrup = (i_agrup + 3) % n_agrup; 
            d = 0; c_agrup = agrup[i_agrup]; comp -= 12; qsis += 12
            if i >= len(lis_alt) - 1: break
            i += 1; altura = lis_alt[i]; duracao = lis_dur[i]
            continue
        
        #Síncopa de seminima em 7/8 até 2/4
        dur_comp = sum(agrup)
        if duracao == 4 and d == 0:
            if dur_comp == 28:
                if comp in [26, 18, 10]:
                    lis_comp.append([altura, duracao, ""])
                    i_agrup = (i_agrup + 1) % n_agrup
                    d = 0; c_agrup = agrup[i_agrup] - 2; comp -= 4; qsis += 4
                    if i >= len(lis_alt) - 1: break
                    i += 1; altura = lis_alt[i]; duracao = lis_dur[i]
                    continue
            elif dur_comp == 24:
                if comp in [22, 14, 6]:
                    lis_comp.append([altura, duracao, ""])
                    i_agrup = (i_agrup + 1) % n_agrup
                    d = 0; c_agrup = agrup[i_agrup] - 2; comp -= 4; qsis += 4
                    if i >= len(lis_alt) - 1: break
                    i += 1; altura = lis_alt[i]; duracao = lis_dur[i]
                    continue
            elif dur_comp == 20:
                if comp in [18, 10]:
                    lis_comp.append([altura, duracao, ""])
                    i_agrup = (i_agrup + 1) % n_agrup
                    d = 0; c_agrup = agrup[i_agrup] - 2; comp -= 4; qsis += 4
                    if i >= len(lis_alt) - 1: break
                    i += 1; altura = lis_alt[i]; duracao = lis_dur[i]
                    continue
            elif  dur_comp == 16:
                if comp in [14, 6]:
                    lis_comp.append([altura, duracao, ""])
                    i_agrup = (i_agrup + 1) % n_agrup
                    d = 0; c_agrup = agrup[i_agrup] - 2; comp -= 4; qsis += 4
                    if i >= len(lis_alt) - 1: break
                    i += 1; altura = lis_alt[i]; duracao = lis_dur[i]
                    continue
            elif  dur_comp == 12:
                if comp == 10:
                    lis_comp.append([altura, duracao, ""])
                    i_agrup = (i_agrup + 1) % n_agrup
                    d = 0; c_agrup = agrup[i_agrup] - 2; comp -= 4; qsis += 4
                    if i >= len(lis_alt) - 1: break
                    i += 1; altura = lis_alt[i]; duracao = lis_dur[i]
                    continue
            elif  dur_comp == 8:
                if comp == 6:
                    lis_comp.append([altura, duracao, ""])
                    i_agrup = (i_agrup + 1) % n_agrup
                    d = 0; c_agrup = agrup[i_agrup] - 2; comp -= 4; qsis += 4
                    if i >= len(lis_alt) - 1: break
                    i += 1; altura = lis_alt[i]; duracao = lis_dur[i]
                    continue
    
        #Atualiza contadores
        duracao -= dur_min 
        d += dur_min
        qsis += dur_min
        comp -= dur_min
        c_agrup -= dur_min
        
        #Agrupa durações
        if duracao != 0 and c_agrup == 0:
            lis_comp.append([altura, d, "~"])
            d = 0
        elif duracao == 0:
            lis_comp.append([altura, d, ""])
            d = 0
        
            #Condição de parada
            if i >= len(lis_alt) - 1:
                break
            
            #Atualiza índices de altura e duração
            i += 1
            altura = lis_alt[i]
            duracao = lis_dur[i]
     
    #Converte para formato lilypond   
    for ele in lis_comp:
        lis_notas_form.append(acomoda_decimais(ele[0], ele[1], ele[2]))
    return lis_notas_form
