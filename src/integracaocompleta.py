import os
import subprocess
import glob
import uuid
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = "/tmp/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extrair_e_limpar_audio(video_input, output):
    ffmpeg_path = "ffmpeg"
    filtro_audio = (
        "afftdn=nf=-20:nr=3,"
        "highpass=f=70,"
        "acompressor=threshold=-21dB:ratio=1.8:attack=25:release=220:makeup=1"
    )

    job_id = str(uuid.uuid4())
    segmentos_dir = os.path.join(UPLOAD_FOLDER, job_id, "segmentos")
    os.makedirs(segmentos_dir, exist_ok=True)
    segmento_pattern = os.path.join(segmentos_dir, "parte_%03d.mp4")

    comando_segmentar = [
        ffmpeg_path,
        "-i", video_input,
        "-f", "segment",
        "-segment_time", "60",
        "-c", "copy",
        segmento_pattern,
        "-y"
    ]

    subprocess.run(comando_segmentar, check=True)
    segmentos = sorted(glob.glob(os.path.join(segmentos_dir, "parte_*.mp4")))
    wavs_processados = []

    for i, segmento in enumerate(segmentos):
        wav_saida = os.path.join(segmentos_dir, f"audio_{i}.wav")
        comando_audio = [
            ffmpeg_path,
            "-threads", "1",
            "-i", segmento,
            "-vn",
            "-af", filtro_audio,
            "-acodec", "pcm_s16le",
            "-ar", "44100",
            "-ac", "1",
            wav_saida,
            "-y"
        ]

        subprocess.run(comando_audio, check=True)

        wavs_processados.append(wav_saida)
    lista_path = os.path.join(segmentos_dir, "lista.txt")

    with open(lista_path, "w", encoding="utf-8") as f:
        for wav in wavs_processados:
            f.write(f"file '{wav}'\n")
    
    comando_juntar = [
        ffmpeg_path,
        "-f", "concat",
        "-safe", "0",
        "-i", lista_path,
        "-c", "copy",
        output,
        "-y"
    ]

    subprocess.run(comando_juntar, check=True)
    for arquivo in glob.glob(os.path.join(segmentos_dir, "*")):
        os.remove(arquivo)
    

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