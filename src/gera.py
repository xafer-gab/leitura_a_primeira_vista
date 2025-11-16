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
        raise ValueError("Tipo inválido.")

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

#Seleciona uma altura randômica em certa oitava aleatória
def nota_randomica(fund, modo, modelo, n_notas, clave, oitavas, pausa_probab=20):
    escala = escalas.escala(fund, modo) 
    tamanho_escala = len(escala)
    
    modelo_harm = []
    #Se for dodecafônico, gera série de x alturas
    if modelo == "Dodecafônico":
        serie = []
        c_rand = 0
        while c_rand < tamanho_escala:
            r = random.randrange(0, tamanho_escala)
            if not r in serie:
                serie.append(r)
                c_rand += 1
    
    #Se não for distribuição igual, adiciona, trunca ou mantém modelo
    elif not modelo == "Igual":
        modelo_harm = escalas.modelos_probabilisticos[modelo]
        tamanho_modelo = len(modelo_harm)
        if tamanho_escala > tamanho_modelo:
            #Adiciona pesos nulos
            for i in range(tamanho_escala-tamanho_modelo):
                modelo_harm.append(0)
        elif tamanho_escala < tamanho_modelo:
            #Faz truncamento
            modelo_harm = modelo_harm[0:len(escala)]
    
    #Gera distribuição igual
    else:
        modelo_harm = [(n*0)+1 for n in range(len(escala))] 

    alturas = []
    c = 0
    limite = len(escala)
    for n in range(n_notas):
        
        #Decide se é pausa
        if pausa_probab != 0:
            p = random.randrange(0, 101)
            if p <= pausa_probab:
                nota = "r"
                alturas.append(nota)
        
        #Decide altura a depender do modelo
        else:
            if not modelo == "Dodecafônico":
                nota_sele = random.choices(escala, modelo_harm)
                nota = nota_sele[0]
            else:
                nota = escala[serie[c]]
                c += 1
                if c == tamanho_escala:
                    c = 0
            
            #Determina oitava    
            if clave == "Sol":
                oit = permuta(escalas.c_sol[0:oitavas], tipo="seleciona")
            elif clave == "Fá":
                oit = permuta(escalas.c_fa[0:oitavas], tipo="seleciona")
            else:
                oit = permuta(escalas.c_do[0:oitavas], tipo="seleciona")
            
            #Adiciona altura e oitava na lista de alturas
            alturas.append(nota+oit)
            
    return alturas
