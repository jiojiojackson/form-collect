from PIL import Image
import os

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

# # 设置图片路径
# current_file_path = os.path.abspath(__file__)
# # 获取当前文件所在的目录的绝对路径
# current_file_dir = os.path.dirname(current_file_path)
# uploud_folder_path = os.path.join(current_file_dir, 'uploads')
# base_image_path = os.path.join(uploud_folder_path, 'contract.png')
# overlay_image_path = os.path.join(uploud_folder_path, 'signature.png')
# output_image_path = os.path.join(uploud_folder_path, 'merged.png')

# # 合并图片
# merge_images(base_image_path, overlay_image_path, output_image_path)