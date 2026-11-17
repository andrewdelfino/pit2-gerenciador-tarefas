import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from flask import Flask
from controllers.tarefa_controller import tarefa_bp

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "views"))
app.secret_key = "chave_secreta_pit2"
app.register_blueprint(tarefa_bp)

if __name__ == "__main__":
    app.run(debug=True)
