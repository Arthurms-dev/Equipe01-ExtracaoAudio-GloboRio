import os
import subprocess
import imageio_ffmpeg as ffmpeg
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extrair_e_limpar_audio(video_input, output):
    filtro_audio = (
        "afftdn=nf=-24:nr=5,"
        "highpass=f=70,"
        "equalizer=f=160:width_type=q:width=0.9:g=1.5,"
        "equalizer=f=3200:width_type=q:width=1.0:g=2,"
        "equalizer=f=5200:width_type=q:width=0.8:g=1.2,"
        "acompressor=threshold=-21dB:ratio=1.8:attack=25:release=220:makeup=1,"
        "loudnorm=I=-16:LRA=10:TP=-1.5"
    )
    ffmpeg_path = ffmpeg.get_ffmpeg_exe()   
    comando = [
        ffmpeg_path, "-i", video_input, "-vn",
        "-af", filtro_audio,
        "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "1",
        output, "-y"
    ]
    subprocess.run(comando, check=True)

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
    audio_final_name = f"{base_name}_final.wav"
    audio_final_path = os.path.join(UPLOAD_FOLDER, audio_final_name)

    video_file.save(video_path)
    
    try:
        extrair_e_limpar_audio(video_path, audio_final_path)
        
        if os.path.exists(video_path): os.remove(video_path)

        return render_template('index.html', download_ready=True, filename=audio_final_name)
    
    except Exception as e:
        return f"Erro no processamento: {e}", 500

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)