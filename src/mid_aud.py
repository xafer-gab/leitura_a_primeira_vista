import subprocess

def midi_para_wav(
    midi_path,
    wav_path,
    soundfont="/usr/share/sounds/sf2/FluidR3_GM.sf2"
):
    subprocess.run(
        [
            "fluidsynth",
            "-ni",
            "-o", "audio.driver=null",
            "-F", wav_path,
            "-r", "44100",
            soundfont,
            midi_path
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )
