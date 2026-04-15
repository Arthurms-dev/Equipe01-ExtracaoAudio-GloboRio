import librosa
import noisereduce as nr
import soundfile as sf
import os
import moviepy.editor as mp

def remover_ruido(input_path, output_path):
    print(f"Processando o vídeo:")
    video = mp.VideoFileClip(input_path)
    audio_temp_path = "temp_audio.wav"
    video.audio.write_audiofile(audio_temp_path, codec='pcm_s16le')

    print(f"Lendo audio com librosa")
    audio_data, samplerate = librosa.load(audio_temp_path, sr=None)

    print(f"Reduzindo ruido")
    reduced_noise = nr.reduce_noise(y=audio_data, sr=samplerate)

    cleaned_audio_path = "cleaned_audio.wav"
    sf.write(cleaned_audio_path, reduced_noise, samplerate)

    print(f"Mesclando")
    cleaned_audio_path = mp.AudioFileClip(cleaned_audio_path)
    final_video = video.set_audio(cleaned_audio_path)

    final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')

    os.remove(audio_temp_path)
    os.remove(cleaned_audio_path)
    print(f"Processamento concluído. Vídeo salvo em {output_path}")

remover_ruido_video = ("videos_teste/video1.mp4", "video_limpo.mp4")