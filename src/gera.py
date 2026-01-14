import random
import data.duracoes as duracoes
import data.escalas as escalas

#Função para permutar ou selecionar
def permuta(lista, tipo="permuta"):
    if tipo == "permuta":
        copia = lista[:]
        random.shuffle(copia)
        return copia
    elif tipo == "seleciona":
        return random.choice(lista)
    else:
        raise ValueError("Tipos: 'permuta' e 'seleciona'")

def gera_lista_dur(duracoes_lis):
	dur_sele = []
	for dur in duracoes_lis:
		dur_sele.append(duracoes.dur_dic[dur])
	return dur_sele

#Deduz número de semicolcheias da fórmula de compasso
def deduz_semicol(tempos, uni_tempo):
    f_comp = f"{tempos}/{uni_tempo}"
    return sum(duracoes.agrupamento[f_comp])

#Gera uma série rítmica com a duração de um compasso
def adiciona_valores(lista_dur, tempos, uni_tempo, num_comp, ligadura=False):
    duracoes = []
    duracao_total_compasso = deduz_semicol(tempos, uni_tempo)
    
    if not ligadura:
        #Itera sobre cada compasso até esvaziar duração total
        for i in range(num_comp):
            tempo_restante_no_compasso = duracao_total_compasso
        
            #Gera lista de durações possíveis para o tempo restante
            while tempo_restante_no_compasso > 0:
                duracoes_possiveis = [dur for dur in lista_dur if dur <= tempo_restante_no_compasso]
            
                #Garante que não falte durações no compasso (adiciona resto)
                if not duracoes_possiveis:
                    duracoes.append(tempo_restante_no_compasso) 
                    break
            
                #Sorteia e adiciona figura na lista do compasso
                duracao_escolhida = random.choice(duracoes_possiveis)
                duracoes.append(duracao_escolhida)
                tempo_restante_no_compasso -= duracao_escolhida
    
    else:
        t_total = num_comp * duracao_total_compasso
        while t_total > 0:
            duracoes_possiveis = [dur for dur in lista_dur if dur <= t_total]
            
            #Garante que não falte durações no compasso (adiciona resto)
            if not duracoes_possiveis:
                duracoes.append(t_total) 
                break
            #Sorteia e adiciona figura na lista do compasso
            duracao_escolhida = random.choice(duracoes_possiveis)
            duracoes.append(duracao_escolhida)
            t_total -= duracao_escolhida
            
    return duracoes

#Define a lista de oitavas a partir da fundamental
def oitava(fund, clave, oitavas, escala, alt_adc_modo):
    
    #Dicionário de oitavas para cada
    oit_simb = [",,", ",", "", "'", "''", "'''", "''''"]
    oitavas_brutas =[]
    for i, simb in enumerate(oit_simb):
        oitavas_brutas.extend([oit_simb[i] for oit in range(12)])
    
    #Incremendo de fundamental em cada clave
    fund_num = escalas.dici_alt[fund]
    do_central = 36 #Índice do dó central
    if clave == "Sol" or clave == "Fá":
        ref = do_central + fund_num
    else:
        ref = (do_central - 12) + fund_num
    
    #Seleciona oitava a depender da clave
    oit_semi = 12 
    oit_escalada = oitavas * oit_semi
    if clave == "Sol" or clave == "Dó":
        oits = oitavas_brutas[ref:]
    else:
        oits = oitavas_brutas[:(ref + 1)]
    
    #Gera sequência de símbolos a partir de intervalos da escala
    inter = escalas.dici_escalas[escala]
    itv = 0
    oit_final = [oits[itv]]

    for i in range(oitavas):
        for j in range(len(inter)):
            itv += inter[j]
            oit_final.append(oits[itv])
        itv = (i + 1) * 12
        oit_final.append(oits[itv])
    for i in range(alt_adc_modo):
        itv += inter[j]
        oit_final.append(oits[itv])
    return oit_final
    

def seleciona_oitava(
    nota_idx, tamanho_escala, escala_oitavada, oits, 
    oitavas, modelo, tam_esc_total, ultima_oitava=None, 
    ultima_nota_idx=None, prob_manter_oitava=0.66):
    
    otv = oitavas

    # Define limites de oitava para finalis
    if modelo in escalas.finalis.keys():
        verif = escalas.finalis[modelo]
        oitavadas = [i for i in range(verif)]
    else:
        oitavadas = []

    #Ajuste para finalis
    if nota_idx == 0 and modelo not in escalas.finalis.keys():
        otv += 1
    elif modelo in escalas.finalis.keys():
        if nota_idx == escalas.finalis[modelo] and modelo != "Lócrio":
            otv += 1

    # Se houver última nota, aplica ponderação
    if ultima_nota_idx is not None:
        distancia = abs(nota_idx - ultima_nota_idx)
        prob_oitavacao = random.random() < prob_manter_oitava
        if prob_oitavacao:
            r = random.randrange(0, otv)
        else:
           r = ultima_oitava 
    else:
        r = random.randrange(0, otv)

    # Calcula índice final na escala escalonada
    n_oit = nota_idx + (tamanho_escala * r)
        
    # Ajuste para finalis
    if n_oit in oitavadas:
        n_oit += tamanho_escala
    
    #Garante aderência à escala
    while n_oit > (tam_esc_total - 1):
        n_oit -= tamanho_escala
    while n_oit < 0:
        n_oit += tamanho_escala
    return f"{escala_oitavada[n_oit]}{oits[n_oit]}", r
    
    

#Seleciona uma altura randômica em certa oitava aleatória
def nota_randomica(fund, modo, modelo, n_notas, clave, oitavas, pausa_probab=20, dispersao=0.66):
    
    #1. Gera escala e oitavas
    #Escala
    escala = escalas.escala(fund, modo)
    tamanho_escala = len(escala)
    
    #Escala escalonada para oitavas
    escala_oitavada = escala * oitavas
    escala_oitavada.append(escala[0])
    if modelo in escalas.finalis.keys():
        oits = oitava(fund, clave, oitavas, modo, escalas.finalis[modelo])
        for i in range(escalas.finalis[modelo]):
            escala_oitavada.append(escala[i+1])
    else:
        oits = oitava(fund, clave, oitavas, modo, 0)
    tam_esc_total = len(escala_oitavada)
    
    #2. Modelos harmônicos
    modelo_harm = []
    #Se for serial/dodecafônico, gera série de x alturas
    if modelo == "Serial/Dodecafônico":
        serie = []
        c_rand = 0
        while c_rand < tamanho_escala:
            r = random.randrange(0, tamanho_escala)
            if not r in serie:
                serie.append(r)
                c_rand += 1
    
    #Se não for distribuição igual, adiciona pesos nulos, trunca ou mantém modelo
    elif not modelo == "Igual":
        modelo_harm = escalas.modelos_probabilisticos[modelo]
        tamanho_modelo = len(modelo_harm)
        
        #Adiciona pesos nulos
        if tamanho_escala > tamanho_modelo:
            diferenca = tamanho_escala-tamanho_modelo
            for i in range(len(modelo_harm)):
                modelo_harm[i].extend([(n*0) for n in range(diferenca)]) #Esse trecho do código precisa ser refatorado após inserir modelos probabilísticos
            for i in range(diferenca):
                modelo_harm.append([(n*0) for n in range(tamanho_escala)])
        
        #Faz truncamento
        elif tamanho_escala < tamanho_modelo:
            modelo_harm = modelo_harm[0:tamanho_escala]
            for i in range(len(modelo_harm)):
                modelo_harm[i] = modelo_harm[i][0:tamanho_escala]
    
    #Gera distribuição igual
    else:
        modelo_harm = [(n*0)+1 for n in range(tamanho_escala)] 

    #3. Geração de alturas
    #Variáveis gerais
    alturas = []
    notas_idx = []
    notas_oit = []
    c = 0
    
    #Variáveis Série de Markov
    if modelo != "Serial/Dodecafônico" and modelo != "Igual":
        idx_mark = [alt for alt in range(tamanho_escala)]
        idx = escalas.finalis[modelo]
        #Garante índice válido em escalas menores
        if idx >= tamanho_escala:
            idx = 0
        final = idx
    
    #Algoritmo de geração
    for n in range(n_notas):
        nota = ""
        
        #Decide se é pausa
        if pausa_probab != 0:
            p = random.randrange(1, 101)
            if p <= pausa_probab:
                nota = "r"
                alturas.append(nota)
                notas_idx.append(0)
                notas_oit.append(0)
        
        #Decide altura a depender do modelo
        if nota != "r":
            
            #Produz série circular
            if modelo == "Serial/Dodecafônico":
                nota = serie[c]
                notas_idx.append(nota)
                c += 1
                if c == tamanho_escala:
                    c = 0
            
            #Produz distribuição igual
            elif modelo == "Igual":
                if n == 0 or n == (n_notas - 1):
                    nota = 0
                    notas_idx.append(nota)
                    
                else:
                    nota = random.randrange(0, tamanho_escala)
                    notas_idx.append(nota)
            
            #Produz Série de Markov (1ª ordem)
            else:
                if n == 0 or n == (n_notas - 1):
                    nota = final
                    notas_idx.append(nota)
                else:
                    idx = random.choices(idx_mark, modelo_harm[idx])
                    idx = idx[0]
                    nota = idx
                    notas_idx.append(nota)
                    
                    
            #Determina oitava
            if n == 0:
                nota_oitavada, ultima_oitava = seleciona_oitava(
                    nota, tamanho_escala, escala_oitavada, 
                    oits, oitavas, modelo, tam_esc_total
                    )
                notas_oit.append(ultima_oitava)
            elif notas_idx[n-1] != "r":
                nota_oitavada, ultima_oitava = seleciona_oitava(
                    nota, tamanho_escala, escala_oitavada, oits, 
                    oitavas, modelo, tam_esc_total, ultima_oitava=notas_oit[n-1],
                    ultima_nota_idx=notas_idx[n-1], prob_manter_oitava=dispersao
                    )
                notas_oit.append(ultima_oitava)
            
            #Adiciona altura e oitava na lista de alturas
            alturas.append(nota_oitavada)
            
    return alturas

def nota_percussao(n_notas, pausa_probab=20):
    alturas = []
    pausa = "r"
    terc_linha = "c'" #Região central clave perc.
    for n in range(n_notas):
        #Decide se é pausa
        if pausa_probab != 0:
            p = random.randrange(1, 101)
            if p <= pausa_probab:
                alturas.append(pausa)
            else:
                alturas.append(terc_linha)
        else:
            alturas.append(terc_linha)
    return alturas
    
