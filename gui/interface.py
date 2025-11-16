import gradio as gr

def interface(func):
    interface = gr.Interface(
        fn=func,
        inputs=[
            gr.Dropdown(
                ["Dó", "Dó#", "Ré", "Ré#", "Mib", "Mi", "Fá", "Fá#", "Solb", "Sol", "Sol#", "Láb", "Lá", "Lá#", "Sib", "Si"], 
                label="Fundamental", 
                value="Dó"
                ),
            gr.Dropdown(["Cromática", "Octofônica", "Maior", "Hexafônica", "Pentatônica"], label="Escala", value="Maior"),
            gr.Dropdown(
                ["Jônio", "Dórico", "Frígio", "Lídio", "Mixolídio", "Eólio", "Lócrio", "Tétrade Maior", "Tétrade Menor", "Aumentado", "Igual", "Dodecafônico"], 
                label="Modelo probabilístico",
                value="Igual"
                ),
            gr.Radio(["Sol", "Fá", "Dó"], label="Clave", value="Sol"),
            gr.Radio([1, 2, 3], label="Número de oitavas", value=1),
            gr.Dropdown(
                ["7/4", "6/4", "5/4", "4/4", "3/4", "2/4", "7/8", "6/8", "5/8", "7/16", "5/16"], 
                label="Fórmula de compasso",
                value="4/4"
                ),
            gr.CheckboxGroup(
                ['Semibreve pontuada', 
                'Semibreve', 
                'Mínima pontuada', 
                'Mínima', 
                'Semínima pontuada', 
                'Semínima', 
                'Colcheia pontuada', 
                'Colcheia', 
                'Semicolcheia pontuada', 
                'Semicolcheia', 
                'Fusa pontuada', 
                'Fusa', 
                'Semifusa'],
                 label="Figuras rítmicas",
                 value='Semínima'),
            gr.Checkbox(label="Ligadura entre compassos?"),
            gr.Slider(minimum=0, maximum=100, value=0, step=1, label="Probabilidade de pausas (%)"),
            gr.Dropdown([4, 8, 16], label="Número de compassos", value=8),
            gr.Textbox(label="Diretório")
        ],
        outputs=[
        gr.Image()
        ],
        submit_btn="Gerar",
        clear_btn="Limpar",
        title="Leitura à Primeira Vista"
        )

    interface.launch()
