from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return "hello?"

if __name__ == "__main__":
    app.debug = True
    app.run(host='flask', port=5000)