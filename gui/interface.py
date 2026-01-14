import gradio as gr
from data.escalas import instrumentos as instrumentos

def interface(func):
    with gr.Blocks() as demo:

        # Título
        gr.Markdown("""
        # LEIA ♪
        ### *Leitura Musical Interativa e Algorítmica*
        """)

        # Tonalidade, escacala e modelo probabilístico
        with gr.Row():
            fundamental = gr.Dropdown(
                ["Dó", "Dó#", "Ré", "Ré#", "Mib", "Mi", "Fá", "Fá#", "Solb", "Sol", "Sol#", "Láb", "Lá", "Lá#", "Sib", "Si"], 
                label="Fundamental", value="Dó"
            )
            escala = gr.Dropdown(
                ["Pentatônica", "Hexafônica", "Maior/Menor", "Octofônica", "Cromática"],
                label="Escala", value="Maior/Menor"
            )
            modelo = gr.Dropdown(
                ["Jônio", "Dórico", "Frígio", "Lídio", "Mixolídio", "Eólio", "Lócrio", "Tonal", "Igual", "Serial/Dodecafônico"], 
                label="Modelo probabilístico", value="Igual"
            )
            clave = gr.Radio(["Sol", "Fá", "Dó", "Percussão"], label="Clave", value="Sol")
            oitavas = gr.Radio([1, 2, 3], label="Número de oitavas", value=1)

        #Definiçẽs de rítmica
        with gr.Row():
            n_compassos = gr.Slider(4, 128, value=8, step=1, label="Número de compassos")
            compasso = gr.Dropdown(
                ["7/4", "6/4", "5/4", "4/4", "3/4", "2/4", "7/8", "6/8", "5/8", "7/16", "5/16"], 
                label="Fórmula de compasso", value="4/4"
            )
            pausas = gr.Slider(0, 100, value=0, step=1, label="Probabilidade de pausas (%)")
            dispersao = gr.Slider(0, 100, value=20, step=1, label="Dispersão melódica (%)")
            ligadura = gr.Checkbox(label="Ligadura entre compassos")
        
        #Figuras rítmicas
        figuras = gr.CheckboxGroup(
            [
                'Semibreve pontuada','Semibreve','Mínima pontuada','Mínima',
                'Semínima pontuada','Semínima','Colcheia pontuada','Colcheia',
                'Semicolcheia pontuada','Semicolcheia','Fusa pontuada','Fusa','Semifusa'
            ],
            label="Figuras rítmicas", value='Semínima'
        )
            
        #Botões para gerar
        with gr.Row():
            gerar = gr.Button("Gerar")
            limpar = gr.Button("Limpar")

        #Saídas de imagem e áudio
        partitura = gr.Image(label="Partitura")
        audio = gr.Audio(type="filepath", label="Áudio (MIDI)")
        
        #Seção de opções midi
        with gr.Row():
            andamento = gr.Slider(50, 160, value=60, step=1, label="Andamento MIDI (BPM)")
            timbre = gr.Dropdown(choices=list(instrumentos.keys()), label="Timbre MIDI", value="Piano")

        # Conectar função
        gerar.click(
            fn=func,
            inputs=[fundamental, escala, modelo, clave, oitavas, n_compassos, compasso, pausas, dispersao, ligadura, figuras, andamento, timbre],
            outputs=[partitura, audio]
        )
        limpar.click(lambda: (None, None), inputs=[], outputs=[partitura, audio])

        # Rodapé
        gr.Markdown("""
        <hr>
        <div style="text-align:center; font-size:0.85em; color:gray;">
            Desenvolvido por <strong>Gabriel Xavier</strong> · 2025-2026
            <br>
            <a href="https://github.com/xafer-gab" target="_blank">GitHub</a> ·
            <a href="https://gabriel-xavier.com" target="_blank">Site</a>
        </div>
        """)

    demo.launch()
