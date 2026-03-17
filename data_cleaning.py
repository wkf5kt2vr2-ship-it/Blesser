import os
import hashlib
from PIL import Image

# ====== 配置区（填入你自己的信息）======
ACCESS_KEY    = "your_access_key"             # 替换为真实密钥
SECRET_KEY    = "your_secret_key"             # 替换为真实密钥
DATA_DIR      = "./Answer-Sheet-Data-Truth"   # 数据集根目录
OUTPUT_LIST   = "./clean_file_list.txt"       # 清洗后文件列表输出路径
IMG_EXTS      = {".jpg", ".jpeg", ".png", ".bmp"}
LABEL_EXT     = ".txt"                        # 标注文件后缀（根据实际调整）
# =========================================

def get_md5(filepath):
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def is_valid_image(filepath):
    try:
        with Image.open(filepath) as img:
            img.verify()
        return True
    except Exception:
        return False

# 1. 收集所有图片文件
all_images = []
for root, _, files in os.walk(DATA_DIR):
    for fname in files:
        if os.path.splitext(fname)[1].lower() in IMG_EXTS:
            all_images.append(os.path.join(root, fname))

total_before = len(all_images)
print(f"清洗前图片总数：{total_before}")

# 2. 过滤损坏图片
valid_images = [p for p in all_images if is_valid_image(p)]
removed_corrupt = total_before - len(valid_images)
print(f"损坏/无法读取图片数：{removed_corrupt}")

# 3. 检查标注文件完整性
missing_label = []
for img_path in valid_images:
    base = os.path.splitext(img_path)[0]
    label_path = base + LABEL_EXT
    if not os.path.exists(label_path):
        missing_label.append(img_path)

print(f"缺少标注文件的图片数：{len(missing_label)}")
valid_images = [p for p in valid_images if p not in missing_label]

# 4. 去除重复文件（MD5校验）
seen_md5 = {}
dedup_images = []
for img_path in valid_images:
    md5 = get_md5(img_path)
    if md5 not in seen_md5:
        seen_md5[md5] = img_path
        dedup_images.append(img_path)
    else:
        print(f"重复文件跳过：{img_path}（与 {seen_md5[md5]} 相同）")

total_after = len(dedup_images)
print(f"\n====== 清洗结果 ======")
print(f"清洗前：{total_before} 张")
print(f"清洗后：{total_after} 张（移除损坏 {removed_corrupt}、缺标注 {len(missing_label)}、重复 {total_before - removed_corrupt - len(missing_label) - total_after}）")

# 5. 保存清洗后文件列表
with open(OUTPUT_LIST, "w") as f:
    for p in dedup_images:
        f.write(p + "\n")
print(f"已保存清洗后文件列表至：{OUTPUT_LIST}")
