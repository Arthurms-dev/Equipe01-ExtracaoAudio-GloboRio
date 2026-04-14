import subprocess

def extrair_audio(video_bruto, audio_extraido):
    comando=['ffmpeg', '-i', video_bruto, '-vn', '-acodec', 'libmp3lame', audio_extraido]
    
    try:
        subprocess.run(comando, check=True)
        print(f"Sucesso! O audio foi extraído como {audio_extraido}")
    except Exception as e:
        print(f"Erro {e}")
    


if __name__=="__main__":
    video_bruto="videos_teste/video1.mp4"
    audio_extraido="audios_extraidos/video1.mp3"

    extrair_audio(video_bruto, audio_extraido)