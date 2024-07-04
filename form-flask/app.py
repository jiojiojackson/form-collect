# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os
from models import merge_images

app = Flask(__name__)
CORS(app)


# 配置数据库连接
db = mysql.connector.connect(
    host="192.168.20.170",
    user="webapp",
    password="Ab147258*",
    database="form"
)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        # 生成一个 token，实际应用中应该使用更安全的方式生成
        token = "some-generated-token"
        return jsonify({'success': True, 'token': token})
    else:
        return jsonify({'success': False}), 401


@app.route('/submit', methods=['POST'])
def submit():
    text = request.form['text']
    photo = request.files['photo']
    signature = request.form['signature']

    # 保存文本
    print(f'Text: {text}')
    
    # 保存照片
    if photo:
        photo_path = os.path.join(uploud_folder_path, photo.filename)
        photo.save(photo_path)
    
    # 保存签名
    if signature:
        import base64
        import re
        from io import BytesIO
        from PIL import Image

        # 移除 base64 头部信息
        signature_data = re.sub('^data:image/.+;base64,', '', signature)
        signature_data = base64.b64decode(signature_data)
        signature_image = Image.open(BytesIO(signature_data))
        signature_path = os.path.join(uploud_folder_path, 'signature.png')
        signature_image.save(signature_path)
    
    signed_contract_path = os.path.join(uploud_folder_path, 'signed.png')
    blank_contract_path = os.path.join(uploud_folder_path, 'contract.png')
    merge_images(blank_contract_path, signature_path, signed_contract_path)
    
    cursor = db.cursor()
    cursor.execute("INSERT INTO submissions (text, photo_path, signature_path) VALUES (%s, %s, %s)",
                   (text, photo_path, signature_path))
    db.commit()
    cursor.close()
    
    return jsonify({'success': True})

if __name__ == '__main__':
    # 获取当前文件的绝对路径
    current_file_path = os.path.abspath(__file__)
    # 获取当前文件所在的目录的绝对路径
    current_file_dir = os.path.dirname(current_file_path)
    uploud_folder_path = os.path.join(current_file_dir, 'uploads')
    if not os.path.exists(uploud_folder_path): os.makedirs(uploud_folder_path)

    app.run(debug=True, host='0.0.0.0', port=5000)
