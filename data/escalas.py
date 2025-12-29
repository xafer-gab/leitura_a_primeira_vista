# Listas de oitavas para cada clave
c_sol = ["'", "''", "'''"]
c_do = ["", "'", "''"]
c_fa = ["", ",", ",,"]

# Dicionário de notas -> classes de alturas
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
    "Si": 11,
}

# Dicionário de notas -> lilypond
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
    "Si": "b",
}

# Lista de notas
c_alt_sus = ["c", "cis", "d", "dis", "e", "eis", "fis", "g", "gis", "a", "ais", "b"]
c_alt_bem = ["c", "des", "d", "ees", "e", "f", "ges", "g", "aes", "a", "bes", "ces"]
c_alt_dodec = [
    "!c",
    "!cis",
    "!d",
    "!ees",
    "!e",
    "!f",
    "!fis",
    "!g",
    "!aes",
    "!a",
    "!bes",
    "!b",
]

# Escalas
cromatico = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
octofonico = [2, 1, 2, 1, 2, 1, 2]
maior = [2, 2, 1, 2, 2, 2]
hexafonico = [2, 2, 2, 2, 2]
pentatonico = [2, 2, 3, 2]

dici_escalas = {
    "Cromática": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "Octofônica": [2, 1, 2, 1, 2, 1, 2],
    "Maior": [2, 2, 1, 2, 2, 2],
    "Hexafônica": [2, 2, 2, 2, 2],
    "Pentatônica": [2, 2, 3, 2],
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
            c_lis = [
                "bis",
                "cis",
                "cisis",
                "dis",
                "e",
                "eis",
                "fis",
                "fisis",
                "gis",
                "a",
                "ais",
                "b",
            ]
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


# Modelos harmônicos probabilísticos
modelos_probabilisticos = {
    "Jônio": [0.217, 0.086, 0.173, 0.152, 0.195, 0.108, 0.065],
    "Dórico": [0.065, 0.217, 0.086, 0.173, 0.152, 0.195, 0.108],
    "Frígio": [0.108, 0.065, 0.217, 0.086, 0.173, 0.152, 0.195],
    "Lídio": [0.195, 0.108, 0.065, 0.217, 0.086, 0.173, 0.152],
    "Mixolídio": [0.152, 0.195, 0.108, 0.065, 0.217, 0.086, 0.173],
    "Eólio": [0.173, 0.152, 0.195, 0.108, 0.065, 0.217, 0.086],
    "Lócrio": [0.086, 0.173, 0.152, 0.195, 0.108, 0.065, 0.217],
    "Tétrade Maior": [0.181, 0.090, 0.181, 0.090, 0.181, 0.090, 0.181],
    "Tétrade Menor": [0.181, 0.090, 0.181, 0.090, 0.181, 0.181, 0.090],
    "Aumentado": [0.222, 0.111, 0.222, 0.111, 0.222, 0.111],
}

# Mapeamento de notas LilyPond para semitons MIDI (relativo a C)
lily_to_midi = {
    "c": 0,
    "cis": 1,
    "cisis": 2,
    "ces": 11,
    "ceses": 10,
    "d": 2,
    "dis": 3,
    "disis": 4,
    "des": 1,
    "deses": 0,
    "e": 4,
    "eis": 5,
    "eisis": 6,
    "ees": 3,
    "eeses": 2,
    "f": 5,
    "fis": 6,
    "fisis": 7,
    "fes": 4,
    "feses": 3,
    "g": 7,
    "gis": 8,
    "gisis": 9,
    "ges": 6,
    "geses": 5,
    "a": 9,
    "ais": 10,
    "aisis": 11,
    "aes": 8,
    "aeses": 7,
    "b": 11,
    "bis": 0,
    "bisis": 1,
    "bes": 10,
    "beses": 9,
}
