import gradio as gr


def interface(func):
    """Cria e lança a interface Gradio para a aplicação."""
    with gr.Blocks(title="Leitura à Primeira Vista") as demo:
        gr.Markdown("# 🎼 Leitura à Primeira Vista")
        gr.Markdown("Gerador randômico de exercícios musicais para estudo de leitura.")

        with gr.Row():
            with gr.Column():
                fundamental = gr.Dropdown(
                    [
                        "Dó",
                        "Dó#",
                        "Ré",
                        "Ré#",
                        "Mib",
                        "Mi",
                        "Fá",
                        "Fá#",
                        "Solb",
                        "Sol",
                        "Sol#",
                        "Láb",
                        "Lá",
                        "Lá#",
                        "Sib",
                        "Si",
                    ],
                    label="Fundamental",
                    value="Dó",
                )
                escala = gr.Dropdown(
                    ["Cromática", "Octofônica", "Maior", "Hexafônica", "Pentatônica"],
                    label="Escala",
                    value="Maior",
                )
                modelo = gr.Dropdown(
                    [
                        "Jônio",
                        "Dórico",
                        "Frígio",
                        "Lídio",
                        "Mixolídio",
                        "Eólio",
                        "Lócrio",
                        "Tétrade Maior",
                        "Tétrade Menor",
                        "Aumentado",
                        "Igual",
                        "Dodecafônico",
                    ],
                    label="Modelo probabilístico",
                    value="Igual",
                )
                clave = gr.Radio(["Sol", "Fá", "Dó"], label="Clave", value="Sol")
                oitavas = gr.Radio([1, 2, 3], label="Número de oitavas", value=1)

            with gr.Column():
                form_comp = gr.Dropdown(
                    [
                        "7/4",
                        "6/4",
                        "5/4",
                        "4/4",
                        "3/4",
                        "2/4",
                        "7/8",
                        "6/8",
                        "5/8",
                        "7/16",
                        "5/16",
                    ],
                    label="Fórmula de compasso",
                    value="4/4",
                )
                fig_selec = gr.CheckboxGroup(
                    [
                        "Semibreve pontuada",
                        "Semibreve",
                        "Mínima pontuada",
                        "Mínima",
                        "Semínima pontuada",
                        "Semínima",
                        "Colcheia pontuada",
                        "Colcheia",
                        "Semicolcheia pontuada",
                        "Semicolcheia",
                        "Fusa pontuada",
                        "Fusa",
                        "Semifusa",
                    ],
                    label="Figuras rítmicas",
                    value=["Semínima"],
                )
                with gr.Row():
                    ligadura = gr.Checkbox(label="Ligadura entre compassos?")

                pausa_p = gr.Slider(
                    minimum=0,
                    maximum=100,
                    value=0,
                    step=1,
                    label="Probabilidade de pausas (%)",
                )
                num_comp = gr.Dropdown([4, 8, 16], label="Número de compassos", value=8)
                tempo_bpm = gr.Slider(
                    minimum=60,
                    maximum=200,
                    value=120,
                    step=10,
                    label="Tempo (BPM)",
                )
                diretorio = gr.Textbox(
                    label="Diretório de saída (opcional)",
                    placeholder="Padrão: diretório temporário",
                )

        submit_btn = gr.Button("Gerar Exercício", variant="primary")
        output_image = gr.Image(label="Partitura Gerada")

        midi_audio = gr.Audio(label="Reprodução de Áudio", type="filepath")

        info_text = gr.Markdown(visible=False)

        def generate_exercise(*args):
            """Gera o exercício e retorna imagem e áudio se disponível."""
            png_path, audio_path = func(*args)

            if audio_path:
                return (
                    png_path,
                    gr.Audio(visible=True, value=audio_path, autoplay=True),
                    gr.Markdown(visible=False),
                )
            else:
                # Se não gerou áudio (provavelmente por falta de fluidsynth localmente)
                msg = (
                    "⚠️ Áudio indisponível. Para ouvir localmente, "
                    "instale `fluidsynth` e `fluid-soundfont-gm`."
                )
                return (
                    png_path,
                    gr.Audio(visible=False),
                    gr.Markdown(msg, visible=True),
                )

        submit_btn.click(
            fn=generate_exercise,
            inputs=[
                fundamental,
                escala,
                modelo,
                clave,
                oitavas,
                form_comp,
                fig_selec,
                ligadura,
                pausa_p,
                num_comp,
                diretorio,
                tempo_bpm,
            ],
            outputs=[output_image, midi_audio, info_text],
        )

    demo.launch(debug=True)
