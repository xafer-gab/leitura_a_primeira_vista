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
                    midi = gr.Checkbox(
                        label="Gerar MIDI? (Apenas se disponível)", value=True
                    )

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

        # Controles de reprodução MIDI
        with gr.Row():
            play_btn = gr.Button("▶️ Play", variant="secondary")
            pause_btn = gr.Button("⏸️ Pause", variant="secondary")
            stop_btn = gr.Button("⏹️ Stop", variant="secondary")

        midi_audio = gr.Audio(label="Reprodução MIDI", visible=False)

        # Estado para controlar a reprodução
        playback_state = gr.State({"playing": False, "midi_path": None})

        def generate_exercise(*args):
            """Gera o exercício e retorna imagem e áudio se MIDI estiver habilitado."""
            png_path, midi_path = func(*args)

            # Se MIDI foi gerado, mostra o componente de áudio e inicia autoplay
            if midi_path:
                return (
                    png_path,
                    gr.Audio(visible=True, value=midi_path, autoplay=True),
                    {"playing": True, "midi_path": midi_path},
                )
            else:
                return (
                    png_path,
                    gr.Audio(visible=False),
                    {"playing": False, "midi_path": None},
                )

        def play_midi(state):
            """Inicia a reprodução do MIDI."""
            if state["midi_path"]:
                return gr.Audio(
                    value=state["midi_path"], visible=True, autoplay=True
                ), {
                    "playing": True,
                    "midi_path": state["midi_path"],
                }
            return gr.Audio(visible=False), state

        def pause_midi(state):
            """Pausa a reprodução do MIDI."""
            return gr.Audio(visible=True), {
                "playing": False,
                "midi_path": state["midi_path"],
            }

        def stop_midi(state):
            """Para a reprodução do MIDI."""
            return gr.Audio(visible=False), {"playing": False, "midi_path": None}

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
                midi,
                tempo_bpm,
            ],
            outputs=[output_image, midi_audio, playback_state],
        )

        play_btn.click(
            fn=play_midi,
            inputs=playback_state,
            outputs=[midi_audio, playback_state],
        )

        pause_btn.click(
            fn=pause_midi,
            inputs=playback_state,
            outputs=[midi_audio, playback_state],
        )

        stop_btn.click(
            fn=stop_midi,
            inputs=playback_state,
            outputs=[midi_audio, playback_state],
        )

    demo.launch()
