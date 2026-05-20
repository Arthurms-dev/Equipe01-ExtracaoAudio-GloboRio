import os
import subprocess
from flask import Flask, jsonify, render_template, request, send_file

app = Flask(__name__)

UPLOAD_FOLDER = "/tmp/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def run_ffmpeg(cmd):
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=600
    )
    if result.returncode != 0:
        print("FFMPEG ERROR:", result.stderr)
        raise Exception(result.stderr)
    return result

def extrair_e_limpar_audio(video_input, output):
    filtro_audio = (
        "afftdn=nf=-20:nr=3,"
        "highpass=f=70,"
        "acompressor=threshold=-21dB:ratio=1.8:attack=25:release=220:makeup=1"
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-i", video_input,
        "-vn",
        "-af", filtro_audio,
        "-acodec", "pcm_s16le",
        "-ar", "44100",
        "-ac", "1",
        output,
    ]

    run_ffmpeg(cmd)

@app.route('/')
def index():
    return render_template('index.html', download_ready=False)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400

    video_file = request.files['file']

    if video_file.filename == '':
        return jsonify({"erro": "Nenhum arquivo selecionado"}), 400

    try:
        import uuid

        job_id = str(uuid.uuid4())
        workdir = os.path.join(UPLOAD_FOLDER, job_id)
        os.makedirs(workdir, exist_ok=True)

        video_path = os.path.join(workdir, video_file.filename)
        video_file.save(video_path)

        base_name = os.path.splitext(video_file.filename)[0]
        output_wav = os.path.join(workdir, f"{base_name}_processado.wav")

        extrair_e_limpar_audio(video_path, output_wav)

        return jsonify({
            "status": "ok",
            "job_id": job_id,
            "download_url": f"/download/{job_id}"
        })

    except Exception as e:
        print("ERRO:", str(e))
        return jsonify({"erro": str(e)}), 500
    
@app.route('/download/<job_id>')
def download(job_id):
    workdir = os.path.join(UPLOAD_FOLDER, job_id)
    files = os.listdir(workdir)
    wav_file = next((f for f in files if f.endswith(".wav")), None)
    if not wav_file:
        return jsonify({"erro": "Arquivo não encontrado"}), 404
    file_path = os.path.join(workdir, wav_file)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)