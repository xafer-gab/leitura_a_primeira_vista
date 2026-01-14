#Dicionário de notas -> classes de alturas
dici_alt = {
    "Dó": 0,
    "Dó#": 1,
    "Réb": 1,
    "Ré": 2,
    "Ré#": 3,
    "Mib": 3,
    "Mi": 4,
    "Fá": 5,
    "Fá#": 6,
    "Solb": 6,
    "Sol": 7,
    "Sol#": 8,
    "Láb": 8,
    "Lá": 9,
    "Lá#": 10,
    "Sib": 10,
    "Si": 11
    }

#Dicionário de notas -> lilypond
dici_alt_lily = {
    "Dó": "c",
    "Dó#": "cis",
    "Réb": "des",
    "Ré": "d",
    "Ré#": "dis",
    "Mib": "ees",
    "Mi": "e",
    "Fá": "f",
    "Fá#": "fis",
    "Solb": "ges",
    "Sol": "g",
    "Sol#": "gis",
    "Láb": "aes",
    "Lá": "a",
    "Lá#": "ais",
    "Sib": "bes",
    "Si": "b"
    }

#Lista de notas
c_alt_sus = ["c", "cis", "d", "dis", "e", "eis", "fis", "g", "gis", "a", "ais", "b"]  
c_alt_bem = ["c", "des", "d", "ees", "e", "f", "ges", "g", "aes", "a", "bes", "ces"]
c_alt_dodec = ["!c", "!cis", "!d", "!ees", "!e", "!f", "!fis", "!g", "!aes", "!a", "!bes", "!b"] 

#Escalas
cromatico = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
octofonico = [2, 1, 2, 1, 2, 1, 2]
maior = [2, 2, 1, 2, 2, 2]
hexafonico = [2, 2, 2, 2, 2]
pentatonico = [2, 2, 3, 2]

dici_escalas = {
    "Cromática": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "Octofônica": [2, 1, 2, 1, 2, 1, 2],
    "Maior/Menor": [2, 2, 1, 2, 2, 2],
    "Hexafônica": [2, 2, 2, 2, 2],
    "Pentatônica": [2, 2, 3, 2]
    }

def escala(fund, escala):
    fundamental = dici_alt[fund]
    escala_inter = dici_escalas[escala]
    if escala == "Cromático":
        c_lis = c_alt_dodec[:]
    else:
        if fund[2:3] == "b" or fund in ["Fá", "Solb"]:
            c_lis = c_alt_bem[:]
        elif fund == "Dó":
            c_lis = c_alt_sus[:]
            c_lis[5] = "f"
        elif fund in ["Dó#", "Ré#", "Sol#", "Lá#"]:
            c_lis = ["bis", "cis", "cisis", "dis", "e", "eis", "fis", "fisis", "gis", "a", "ais", "b"]
            if fund == "Lá#":
                c_lis[9] = "gisis"
        else:
            c_lis = c_alt_sus[:]
    
    escala_final = []
    escala_final.append(c_lis[fundamental])
    for i in range(len(escala_inter)):
        prox_alt = (fundamental + escala_inter[i]) % 12
        escala_final.append(c_lis[prox_alt])
        fundamental = prox_alt
    return escala_final

#Modelos harmônicos probabilísticos
''' 
Cada modelo fora treinado por aprendizado de máquina a partir de uma obra específica.
Os pesos correspondem à preponderância nota a nota disposta nos graus da escala natural.
Ex: Dórico na escala de dó, é ordenado em [[dó], [ré], [mi], etc.], sendo ré a finalis.
A seguir, listamos as composiçẽs:
    1. Jônio - Ave Regina coelorum, Giovanni Pierluigi da Palestrina
    2. Dórico - Sederunt Principes, Pérotin
    3. Frígio - Mille Regrez, Josquin Desprez
    4. Lídio - Mikrokosmos nº 37 e 61, Béla Bártok
    5. Mixolídio - O Ovo, Hermeto Pascoal
    6. Eólio - Für Alina, Arvo Pärt
    7. Lócrio - Can vei la lauzeta mover (adaptado), Bernart de Ventadorn
    8. Tonal - Sonata em Fá Maior (VII), temas A e B - W. A. Mozart
'''


modelos_probabilisticos = {
    "Jônio": [
        [0.047703, 0.381166, 0.047497, 0.0, 0.142687, 0.143065, 0.237883],
        [0.42946, 0.0, 0.498468, 0.0, 0.072071, 0.0, 0.0],
        [0.165542, 0.416244, 0.0, 0.418214, 0.0, 0.0, 0.0],
        [0.125002, 0.125046, 0.374284, 0.0, 0.375669, 0.0, 0.0],
        [0.334843, 0.0, 0.083037, 0.250377, 0.0, 0.331743, 0.0],
        [0.180709, 0.0, 0.0, 0.091163, 0.273249, 0.0, 0.454879],
        [0.499453, 0.0, 0.0, 0.0, 0.10019, 0.400357, 0.0]
        ],
    "Dórico": [
        [0.0, 0.714945, 0.0, 0.0, 0.0, 0.285055, 0.0], #Dó
        [0.109234, 0.0, 0.222779, 0.221588, 0.11165, 0.111473, 0.223276], #Ré
        [0.495655, 0.504345, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.140897, 0.0, 0.571071, 0.288032, 0.0],
        [0.072395, 0.0, 0.071057, 0.213446, 0.0, 0.643102, 0.0],
        [0.0, 0.090412, 0.0, 0.090624, 0.272915, 0.135523, 0.410527],
        [0.272249, 0.0, 0.0, 0.0, 0.272639, 0.455112, 0.0],
        ],
    "Frígio": [
        [0.0, 0.167409, 0.08313, 0.083235, 0.082924, 0.082413, 0.500888],
        [0.557071, 0.0, 0.222194, 0.0, 0.0, 0.220736, 0.0],
        [0.181751, 0.227382, 0.136171, 0.182179, 0.045736, 0.18113, 0.04565],
        [0.099534, 0.200492, 0.502221, 0.0, 0.197753, 0.0, 0.0],
        [0.0, 0.0, 0.299898, 0.498502, 0.0, 0.2016, 0.0],
        [0.065264, 0.0, 0.333249, 0.0, 0.333617, 0.066755, 0.201115],
        [0.100772, 0.0, 0.301024, 0.0, 0.1006, 0.497604, 0.0],
        ],
    "Lídio": [
        [0.0, 0.124114, 0.0, 0.0, 0.0, 0.250869, 0.625017],
        [0.091145, 0.0, 0.181419, 0.091199, 0.180677, 0.45556, 0.0],
        [0.251673, 0.501056, 0.0, 0.0, 0.247272, 0.0, 0.0],
        [0.180535, 0.273221, 0.0, 0.0, 0.364473, 0.181771, 0.0],
        [0.058907, 0.117046, 0.0, 0.352043, 0.0, 0.472004, 0.0],
        [0.083044, 0.08272, 0.083185, 0.125062, 0.25078, 0.041616, 0.333594],
        [0.15411, 0.0, 0.0, 0.0, 0.385257, 0.460634, 0.0]
        ],
    "Mixolídio": [
        [0.0, 0.250382, 0.0, 0.0, 0.0, 0.0, 0.749618],
        [0.498114, 0.0, 0.167623, 0.0, 0.168286, 0.0, 0.165978],
        [0.0, 0.499021, 0.0, 0.0, 0.500979, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.056043, 0.111596, 0.221947, 0.056253, 0.220432, 0.333728],
        [0.0, 0.0, 0.0, 0.0, 0.749624, 0.0, 0.250376],
        [0.125396, 0.311754, 0.0, 0.0, 0.312885, 0.249965, 0.0]
        ],
    "Eólio": [
        [0.0, 0.399679, 0.065526, 0.066947, 0.0, 0.268637, 0.199211],
        [0.374352, 0.0, 0.4979, 0.0, 0.0, 0.127747, 0.0],
        [0.501329, 0.199515, 0.0, 0.200131, 0.0, 0.099025, 0.0],
        [0.251454, 0.0, 0.0, 0.0, 0.4986, 0.249946, 0.0],
        [0.333211, 0.0, 0.0, 0.333061, 0.0, 0.333727, 0.0],
        [0.230858, 0.0, 0.230518, 0.0, 0.077707, 0.0, 0.460917],
        [0.224394, 0.0, 0.219788, 0.0, 0.0, 0.555818, 0.0]
        ],
    "Lócrio": [
        [0.0, 0.398595, 0.200118, 0.0, 0.0, 0.10008, 0.301207],
        [0.363587, 0.0, 0.636413, 0.0, 0.0, 0.0, 0.0],
        [0.149574, 0.200996, 0.0, 0.64943, 0.0, 0.0, 0.0],
        [0.0, 0.10563, 0.421761, 0.0, 0.315483, 0.157126, 0.0],
        [0.0, 0.0, 0.181222, 0.272241, 0.0, 0.546537, 0.0],
        [0.0, 0.0, 0.0, 0.271997, 0.456015, 0.0, 0.271988],
        [0.500891, 0.167906, 0.165358, 0.0, 0.0, 0.165846, 0.0]
        ],
    "Tonal": [
        [0.0, 0.400973, 0.265045, 0.0, 0.199888, 0.0, 0.134094],
        [0.444382, 0.0, 0.333055, 0.111048, 0.055795, 0.0, 0.055721],
        [0.052918, 0.263707, 0.0, 0.315856, 0.314586, 0.052934, 0.0],
        [0.0, 0.352508, 0.353848, 0.0, 0.117742, 0.058204, 0.117697],
        [0.117114, 0.0, 0.175387, 0.531048, 0.0, 0.176451, 0.0],
        [0.0, 0.165472, 0.0, 0.0, 0.834528, 0.0, 0.0],
        [0.800391, 0.0, 0.0, 0.0, 0.0, 0.199609, 0.0]
        ]
}

finalis = {
    "Jônio": 0,
    "Dórico": 1,
    "Frígio": 2,
    "Lídio": 3,
    "Mixolídio": 4,
    "Eólio": 5,
    "Lócrio": 6,
    "Tonal": 0
}
    
#Lista de instrumentos MIDI
instrumentos = {
    # Sopros
    "Flauta": "flute",
    "Oboé": "oboe",
    "Clarinete": "clarinet",
    "Fagote": "bassoon",

    # Metais
    "Trompete": "trumpet",
    "Trombone": "trombone",
    "Trompa": "french horn",
    "Tuba": "tuba",
    
    # Teclados
    "Piano": "acoustic grand",
    "Vibrafone": "vibraphone",
    "Marimba": "marimba",

    # Percussão
    "Tom-Tom": "melodic tom",
    "Agogô": "agogo",
        
    # Cordas dedilhadas
    "Violão": "acoustic guitar (nylon)",
    "Bandolim": "banjo",
    "Harpa": "orchestral harp",

    # Cordas friccionadas
    "Violino": "violin",
    "Viola": "viola",
    "Violoncelo": "cello",
    "Contrabaixo": "contrabass",
}
