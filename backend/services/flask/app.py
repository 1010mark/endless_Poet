import eventlet
eventlet.monkey_patch()

from flask import Flask, make_response
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from io import BytesIO
from tools import getAudio
import json, time, os

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", transports=["websocket"])

@app.route('/', methods=['GET'])
def index():
    try:
        audio = getAudio.get_audio()
        with BytesIO() as buf:
            audio["AudioSegment"].export(buf, format="mp3")
            response = make_response(buf.getvalue())
        response.headers["Content-Type"] = 'audio/mp3'
        response.headers["Content-Disposition"] = 'attachment; filename=audio.mp3'
        response.headers["Content-Script"] = json.dumps(audio["script"])
        response.headers["Content-Updated-At"] = audio["updated_at"]
        return response
    except Exception:
        import traceback
        traceback.print_exc()
        return "Something went wrong", 500

@socketio.on('request_audio')
def stream_audio():
    print("socket request_audio")
    audio = getAudio.get_audio()
    with BytesIO() as buf:
        audio["AudioSegment"].export(buf, format="mp3")
        audio_data = buf.getvalue()
        
    print("emit script_data")
    emit("script_data", audio["script"])
    socketio.emit("audio", audio_data)

if __name__ == "__main__":
    # app.debug = True
    # app.run(host='0.0.0.0', port=5001)
    socketio.run(app,host='0.0.0.0', debug=True, port=5001)