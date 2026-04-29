import subprocess
from pydub import AudioSegment
from pydub.silence import split_on_silence


def selecionar_video():
    comando = [
        "powershell",
        "-command",
        "Add-Type -AssemblyName System.Windows.Forms; "
        "$f = New-Object System.Windows.Forms.OpenFileDialog; "
        "$f.Filter = 'Videos (*.mp4;*.mkv;*.avi;*.mov)|*.mp4;*.mkv;*.avi;*.mov'; "
        "if ($f.ShowDialog() -eq 'OK') { $f.FileName }"
    ]

    resultado = subprocess.run(comando, capture_output=True, text=True)
    return resultado.stdout.strip()


def extrair_e_limpar_audio(video_input, output="audio_limpo.wav"):
    print("Extraindo e limpando áudio...")

    filtro_audio = (
        # O arnndn é um filtro de redução de ruído baseado em redes neurais, mas pode ser pesado para processar, utilizando IA.
        
        #f"arnndn=model='models/bd.rnnn'," 
        "afftdn=nf=-45:nr=20:om=i,"
        "highpass=f=100," 
        "agate=threshold=35dB" 
        "equalizer=f=350:width_type=h:width=150:g=-10,"
        "equalizer=f=1500:width_type=h:width=200:g=3," 
        "equalizer=f=4500:width_type=h:width=200:g=6," 
        "equalizer=f=12000:width_type=h:width=200:g=4," 
        "acompressor=threshold=-16dB:ratio=3:attack=5:release=100,"
        "deesser,"
        "anequalizer=c0 f=1000 w=200 g=-10|c0 f=2000 w=200 g=-5,"
        "loudnorm=I=-13:LRA=5:TP=-1.0"
    )

    comando = [
        "ffmpeg",
        "-i", video_input,
        "-vn",
        "-af", filtro_audio,
        "-acodec", "pcm_s16le",
        "-ar", "44100",
        "-ac", "1",
        output,
        "-y"
    ]

    subprocess.run(comando, check=True)
    print("Áudio tratado!")


def remover_silencios(input_audio, output_audio):
    print("Removendo silêncios automaticamente")

    audio = AudioSegment.from_wav(input_audio)

    chunks = split_on_silence(
        audio,
        min_silence_len=300, 
        silence_thresh=-30, 
        keep_silence=250      
    )

    if not chunks:
        print("Nenhum silêncio detectado, mantendo o audio original")
        audio.export(output_audio, format="wav")
        return
    audio_final = AudioSegment.empty()

    for chunk in chunks:
        audio_final += chunk
    audio_final.export(output_audio, format="wav")

    print("Silêncios removidos")


if __name__ == "__main__":
    video = selecionar_video()

    if not video:
        print("Nenhum vídeo selecionado.")
        exit()

    try:
        extrair_e_limpar_audio(video, "audio_tratado.wav")
        remover_silencios("audio_tratado.wav", "audio_final.wav")

        print("\nÁUDIO FINAL LIMPO GERADO")

    except Exception as e:
        print(f"\n[ERRO] {e}")