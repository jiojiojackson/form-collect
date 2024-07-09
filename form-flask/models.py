from PIL import Image
import os
import uuid
import io
import base64
import re

# 获取当前文件的绝对路径
current_file_path = os.path.abspath(__file__)
# 获取当前文件所在的目录的绝对路径
current_file_dir = os.path.dirname(current_file_path)
uploud_folder_path = os.path.join(current_file_dir, 'uploads')

def merge_images(base_path, overlay_path, output_path, bottom_margin=150, right_margin=4):
  """
  将一张PNG图片合并到另一张PNG图片的右下角。

  Args:
      base_path (str): 基础图片路径。
      overlay_path (str): 覆盖图片路径。
      output_path (str): 输出图片路径。
      bottom_margin (int): 底部边距。
      right_margin (int): 右侧边距。
  """
  resize_factor = 0.6
  try:
    base_image = Image.open(base_path).convert("RGBA")
    overlay_image = Image.open(overlay_path).convert("RGBA")
    overlay_width = int(overlay_image.width * resize_factor)
    overlay_height = int(overlay_image.height * resize_factor)
    overlay_image = overlay_image.resize((overlay_width, overlay_height))

    base_width, base_height = base_image.size
    overlay_width, overlay_height = overlay_image.size

    # 计算粘贴位置
    position = (
      base_width - overlay_width - right_margin,
      base_height - overlay_height - bottom_margin,
    )

    # 粘贴图片
    base_image.paste(overlay_image, position, overlay_image)

    # 保存图片
    base_image.save(output_path, "PNG")

    print(f"图片已成功合并并保存到: {output_path}")

  except FileNotFoundError:
    print("图片未找到，请检查路径是否正确。")
  except Exception as e:
    print(f"发生错误: {e}")

def new_uuid():
  uuid_str = str(uuid.uuid4())
  return uuid_str

def save_photo(photo, myuuid):
  photo_dir = os.path.join(uploud_folder_path, f'{myuuid}.png')
  # 使用 Pillow 打开图片
  try:
      img = Image.open(photo)
  except IOError:
      print("Invalid image file")

  # 将图片转换为 RGB 模式（如果需要）
  if img.mode != 'RGB':
      img = img.convert('RGB')

  # 保存为 PNG 格式
  img.save(photo_dir, format='PNG')
  print('Image uploaded successfully!') 

def save_signature(signature, myuuid):
  # 移除 base64 头部信息
  signature_data = re.sub('^data:image/.+;base64,', '', signature)
  signature_data = base64.b64decode(signature_data)
  signature_image = Image.open(io.BytesIO(signature_data))
  signature_path = os.path.join(uploud_folder_path, f'{myuuid}.png')
  signature_image.save(signature_path)
   