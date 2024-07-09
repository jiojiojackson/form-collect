# app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
import os
from models import merge_images, new_uuid, save_photo, save_signature, uploud_folder_path

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
        token = new_uuid()
        return jsonify({'success': True, 'token': token})
    else:
        return jsonify({'success': False}), 401


@app.route('/submit', methods=['POST'])
def submit():
    text = request.form['text']
    username = request.form['username']
    photo = request.files['photo']
    signature = request.form['signature']

    # 保存文本
    print(f'Text: {text}')
    
    # 保存照片
    photo_uuid = new_uuid()
    save_photo(photo, photo_uuid)
    photo_path = os.path.join(uploud_folder_path, photo.filename)
    photo.save(photo_path)
    
    # 保存签名
    sign_uuid = new_uuid()
    save_signature(signature, sign_uuid)
    
    #合并签名
    signed_uuid = new_uuid()
    signature_path = os.path.join(uploud_folder_path, f'{sign_uuid}.png')
    signed_contract_path = os.path.join(uploud_folder_path, f'{signed_uuid}.png')
    blank_contract_path = os.path.join(uploud_folder_path, 'contract.png')
    merge_images(blank_contract_path, signature_path, signed_contract_path)
    
    cursor = db.cursor()
    cursor.execute("INSERT INTO submissions (text, username, photoUuid, signUuid) VALUES (%s, %s, %s, %s)",
                   (text, username, photo_uuid, signed_uuid))
    db.commit()
    cursor.close()
    
    return jsonify({'success': True})

@app.route('/records', methods=['GET'])
def get_records():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, text, photoUuid, signUuid FROM submissions")
    records = cursor.fetchall()
    cursor.close()

    return jsonify(records=records)

@app.route('/records/<int:id>', methods=['DELETE'])
def delete_record(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM submissions WHERE id = %s", (id,))
    db.commit()
    cursor.close()

    return jsonify(success=True)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    filename = filename + '.png'
    return send_from_directory(uploud_folder_path, filename)

if __name__ == '__main__':
    if not os.path.exists(uploud_folder_path): os.makedirs(uploud_folder_path)

    app.run(debug=True, host='0.0.0.0', port=5000)
