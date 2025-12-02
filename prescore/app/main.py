import sys
import os
import logging
from flask import Flask, render_template, send_from_directory

# Добавляем корень проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prescore.app.routes_upload import upload_bp

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# Папка загрузки
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Blueprint
app.register_blueprint(upload_bp, url_prefix='/upload')

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.logger.info("🚀 Prescore запускается...")
    app.run(host='127.0.0.1', port=8000, debug=True)
