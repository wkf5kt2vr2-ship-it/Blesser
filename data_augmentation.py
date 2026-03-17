import os
import shutil
from PIL import Image, ImageEnhance, ImageFilter
import random

DATA_DIR   = "./Answer-Sheet-Data-Truth"
AUG_DIR    = "./Answer-Sheet-Data-Augmented"
os.makedirs(AUG_DIR, exist_ok=True)

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp"}

def augment_image(img):
    """对单张图片执行随机增强，返回增强后图片列表"""
    results = []

    # 水平翻转
    results.append(img.transpose(Image.FLIP_LEFT_RIGHT))

    # 随机旋转 ±15°
    angle = random.uniform(-15, 15)
    results.append(img.rotate(angle, expand=True))

    # 亮度调整
    enhancer = ImageEnhance.Brightness(img)
    results.append(enhancer.enhance(random.uniform(0.7, 1.3)))

    # 对比度调整
    enhancer = ImageEnhance.Contrast(img)
    results.append(enhancer.enhance(random.uniform(0.7, 1.3)))

    # 轻微模糊（模拟噪声）
    results.append(img.filter(ImageFilter.GaussianBlur(radius=1)))

    return results

all_files = []
for root, _, files in os.walk(DATA_DIR):
    for fname in files:
        if os.path.splitext(fname)[1].lower() in IMG_EXTS:
            all_files.append(os.path.join(root, fname))

count_before = len(all_files)
count_added  = 0

for img_path in all_files:
    # 复制原图
    dst = os.path.join(AUG_DIR, os.path.basename(img_path))
    shutil.copy2(img_path, dst)

    # 生成增强图
    with Image.open(img_path) as img:
        img = img.convert("RGB")
        for i, aug_img in enumerate(augment_image(img)):
            name, ext = os.path.splitext(os.path.basename(img_path))
            save_path = os.path.join(AUG_DIR, f"{name}_aug{i}{ext}")
            aug_img.save(save_path)
            count_added += 1

total_after = count_before + count_added
print(f"原始图片数量：{count_before}")
print(f"新增扩增图片：{count_added}")
print(f"扩增后总数量：{total_after}")
print(f"扩增结果保存至：{AUG_DIR}")
