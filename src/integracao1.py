import subprocess
from moviepy.audio.io.AudioFileClip import AudioFileClip

def segmentacao(audio_bruto, tempo_inicio, tempo_fim, saida):
    try:
        audio=AudioFileClip(audio_bruto)
        segmento=audio.subclipped(tempo_inicio, tempo_fim)
        segmento.write_audiofile(saida)
        print("Segmento salvo com sucesso na pasta 'audios_segmentados'")
        
    except Exception as e:
        print(f"Erro {e} ao tentar segmentar o áudio")

def extrair_audio(video_bruto, audio_extraido):
    comando=['ffmpeg', '-i', video_bruto, '-vn', '-acodec', 'libmp3lame', audio_extraido]
    
    try:
        subprocess.run(comando, check=True)
        print(f"Sucesso! O audio foi extraído e já se encontra na pasta audios_extraídos")
    except Exception as e:
        print(f"Erro {e}")


if __name__ == "__main__":
    video_original="videos_teste/video4.mp4"
    audio_bruto="audios_extraidos/video4.mp3"
    segmento_final="audios_segmentados/segmento1_video4.mp3"
    extrair_audio(video_original, audio_bruto)
    segmentacao(audio_bruto, '0:02', '0:15', segmento_final)

    print("\nIntegração entre extração e segmentação realizada bem sucedida")