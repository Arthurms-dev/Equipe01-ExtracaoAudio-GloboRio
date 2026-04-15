import librosa
import noisereduce as nr
import soundfile as sf
import os as os


def remover_ruido(input_path, output_path):
    print(f"Transformando o audio em dados numéricos")
    data, rate=librosa.load(input_path,sr=None)

    print(f"Reduzindo ruido")
    audio_limpo=nr.reduce_noise(y=data, sr=rate)

    sf.write(output_path, audio_limpo, rate)
    print(f"Processamento concluído. Áudio salvo na pasta 's_ruido'")


if __name__=="__main__":
    remover_ruido("audios_extraidos/video1.mp3", "s_ruido/audio_limpo_video1.wav")