from moviepy.audio.io.AudioFileClip import AudioFileClip

def segmentacao(audio_bruto, tempo_inicio, tempo_fim, saida):
    try:
        audio=AudioFileClip(audio_bruto)
        segmento=audio.subclipped(tempo_inicio, tempo_fim)
        segmento.write_audiofile(saida)
        print("Segmento salvo com sucesso na pasta 'audios_segmentados'")
        
    except Exception as e:
        print(f"Erro {e} ao tentar segmentar o áudio")

if __name__=="__main__":
    audio_bruto="audios_extraidos/video1.mp3"
    segmentacao(audio_bruto, '0:04', '0:19', "audios_segmentados/segmento2_video1.mp3")
