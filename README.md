# 🎼 Leitura à Primeira Vista

**Interactive Sight-Reading Practice Tool**

A comprehensive web application for musicians and music students to practice sight-reading through randomly generated musical exercises. Features both **visual notation** and **audio playback** for complete musical training.

## ✨ Features

### 🎵 Musical Generation
- **Multiple Time Signatures**: 2/4, 3/4, 4/4, 5/4, 6/4, 7/4, 3/8, 5/8, 6/8, 7/8, 5/16, 7/16
- **Configurable Rhythms**: Whole notes, half notes, quarter notes, eighth notes, sixteenth notes, dotted notes
- **Scale Support**: Major, Minor, Chromatic, Octatonic, Hexatonic, Pentatonic
- **Harmonic Models**: Jônico, Dórico, Frígio, Lídio, Mixolídio, Eólio, Lócrio, and more
- **Multiple Clefs**: Treble (G), Bass (F), Alto (C)
- **Flexible Octave Range**: 1-3 octaves

### 🎧 Audio Features
- **MIDI Playback**: Hear your exercises with professional-quality audio
- **Adjustable Tempo**: 60-200 BPM for different skill levels
- **Interactive Controls**: Play, Pause, Stop buttons
- **Real-time Audio**: Instant feedback while reading

### 🎨 Visual Interface
- **Professional Notation**: High-quality sheet music rendered with LilyPond
- **Web-based UI**: No installation required - works in any browser
- **Responsive Design**: Optimized for desktop and mobile devices
- **Parameter Presets**: Quick access to common practice configurations

## 🚀 Quick Start

### Option 1: Google Colab (Recommended)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/xafer-gab/leitura_a_primeira_vista/blob/feat/first-refactor/Leitura_%C3%A0_primeira_vista_(LilyPond).ipynb)

1. Click the badge above to open in Google Colab
2. Run the setup cell (installs dependencies)
3. Run the application cell
4. Access the web interface via the generated link

### Option 2: Local Installation

#### Prerequisites
- Python 3.10+
- LilyPond (music notation software)
- Git

#### Installation
```bash
# Clone the repository
git clone https://github.com/xafer-gab/leitura_a_primeira_vista.git
cd leitura_a_primeira_vista

# Install Python dependencies
pip install -r requirements.txt

# Install LilyPond (macOS with Homebrew)
brew install lilypond

# Or download from https://lilypond.org/ for other platforms
```

#### Usage
```bash
python main.py
```

Open the generated URL in your browser (usually `http://127.0.0.1:7860`).

## 🎯 How to Use

1. **Configure Parameters**:
   - Select your clef (Treble, Bass, Alto)
   - Choose a scale and harmonic model
   - Set octave range (1-3 octaves)
   - Pick time signature
   - Select rhythmic values
   - Set number of measures (4, 8, or 16)

2. **Enable Audio** (Optional):
   - Check "Gerar MIDI?" for audio playback
   - Adjust tempo with the BPM slider (60-200)

3. **Generate & Practice**:
   - Click "Gerar Exercício"
   - View the sheet music
   - Use play/pause/stop controls to hear the music
   - Practice reading along with the audio

4. **Repeat**: Generate new exercises to build your sight-reading skills!

## 🛠️ Development

### Setup Development Environment
```bash
# Install development dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install

# Run linting and formatting
pre-commit run --all-files
```

### Project Structure
```
leitura_a_primeira_vista/
├── src/                    # Core application logic
│   ├── gera.py            # Music generation algorithms
│   ├── formata.py         # LilyPond formatting
│   └── renderiza.py       # File rendering (PNG, MIDI)
├── gui/                    # Web interface
│   └── interface.py       # Gradio UI components
├── data/                   # Musical data and constants
│   ├── escalas.py         # Scales and note mappings
│   └── duracoes.py        # Rhythms and time signatures
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Ruff configuration
└── .pre-commit-config.yaml # Code quality hooks
```

## 📚 Educational Value

This tool helps musicians develop essential sight-reading skills by:

- **Rhythmic Reading**: Practice complex rhythmic patterns
- **Pitch Recognition**: Improve note-reading speed and accuracy
- **Key Familiarity**: Exposure to different scales and keys
- **Tempo Flexibility**: Practice at various speeds
- **Multimodal Learning**: Combine visual and auditory learning

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure code passes pre-commit hooks
5. Submit a pull request

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Gradio](https://gradio.app/) for the web interface
- Music notation powered by [LilyPond](https://lilypond.org/)
- MIDI generation using [Mido](https://mido.readthedocs.io/)
- Code quality ensured by [Ruff](https://ruff.rs/)

---

**Happy Practicing! 🎵**
