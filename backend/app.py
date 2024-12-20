from flask import Flask, make_response
from flask_cors import CORS
from io import BytesIO
from tools import getAudio
import json

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    try:
        audio = getAudio.get_audio()
        with BytesIO() as buf:
            audio["AudioSegment"].export(buf, format="wav")
            response = make_response(buf.getvalue())
        response.headers["Content-Type"] = 'audio/wav'
        response.headers["Content-Disposition"] = 'attachment; filename=audio.wav'
        response.headers["Content-Script"] = json.dumps(audio["script"])
        response.headers["Content-Updated-At"] = audio["updated_at"]
        return response
    except Exception as e:
        import traceback
        traceback.print_exc()
        return "Something went wrong", 500

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5001)