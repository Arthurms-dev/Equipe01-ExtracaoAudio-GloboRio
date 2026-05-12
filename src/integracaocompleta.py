import os
import subprocess
from flask import Flask, render_template, request, send_file
from pydub import AudioSegment
from pydub.silence import split_on_silence

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extrair_e_limpar_audio(video_input, output):
    filtro_audio = (
        "afftdn=nf=-45:nr=20:om=i,"
        "highpass=f=100," 
        "agate=threshold=-35dB," 
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
        "ffmpeg", "-i", video_input, "-vn",
        "-af", filtro_audio,
        "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "1",
        output, "-y"
    ]
    subprocess.run(comando, check=True)

def remover_silencios(input_audio, output_audio):
    audio = AudioSegment.from_wav(input_audio)
    chunks = split_on_silence(
        audio, min_silence_len=300, silence_thresh=-30, keep_silence=250      
    )
    
    if not chunks:
        audio.export(output_audio, format="mp3") 
        return
    
    audio_final = AudioSegment.empty()
    for chunk in chunks:
        audio_final += chunk
    audio_final.export(output_audio, format="mp3")

@app.route('/')
def index():
    return render_template('index.html', download_ready=False)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "Nenhum arquivo enviado", 400
    
    video_file = request.files['file']
    if video_file.filename == '':
        return "Nenhum arquivo selecionado", 400

    base_name = os.path.splitext(video_file.filename)[0]
    video_path = os.path.join(UPLOAD_FOLDER, video_file.filename)
    audio_temp = os.path.join(UPLOAD_FOLDER, f"{base_name}_temp.wav")
    audio_final_name = f"{base_name}_final.mp3"
    audio_final_path = os.path.join(UPLOAD_FOLDER, audio_final_name)

    video_file.save(video_path)
    
    try:
        extrair_e_limpar_audio(video_path, audio_temp)
        remover_silencios(audio_temp, audio_final_path)
        
        if os.path.exists(video_path): os.remove(video_path)
        if os.path.exists(audio_temp): os.remove(audio_temp)

        return render_template('index.html', download_ready=True, filename=audio_final_name)
    
    except Exception as e:
        return f"Erro no processamento: {e}", 500

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)