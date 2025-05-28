from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from utils import get_price
import requests
from load_data import import_excel_to_db
import os

# ✅ 初始化时导入数据（上线后可改为仅首次导入）
import_excel_to_db()

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/devis', methods=['POST'])
def api_devis():
    data = request.get_json()
    w = int(data.get('largeur', 0))
    h = int(data.get('hauteur', 0))
    type_name = data.get('type', 'FIXED_WINDOW_PRICING')
    color = data.get('color', 'blanc')
    vitrage = data.get('vitrage', '4-20-4')
    ob = data.get('ob', False)
    result = get_price(type_name, w, h, color, vitrage, ob)
    return jsonify(result)

@app.route('/api/feedback', methods=['POST'])
def api_feedback():
    data = request.get_json()
    script_url = "https://script.google.com/macros/s/AKfycbyfL22EVTvP_SrVuv5cYU2GEAz2InkQB31nahEWF7B3Afy27C7meqbZY2XrrPi3-4_t/exec"
    try:
        print("📨 正在转发到 Apps Script：", data)
        response = requests.post(script_url, json=data)
        print("📥 返回结果：", response.text)
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print("❌ 错误：", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500
        
@app.route('/ping')
def ping():
    return 'pong', 200

# ✅ 使用 Render 要求的端口绑定方式
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

