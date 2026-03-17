import os
from sklearn.model_selection import train_test_split

AUG_DIR  = "./Answer-Sheet-Data-Augmented"
IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp"}

all_images = [
    f for f in os.listdir(AUG_DIR)
    if os.path.splitext(f)[1].lower() in IMG_EXTS
]

train_files, val_files = train_test_split(all_images, test_size=0.2, random_state=42)

print(f"数据集总数：{len(all_images)}")
print(f"训练集数量：{len(train_files)}")
print(f"验证集数量：{len(val_files)}")

# 保存划分结果
with open("train_list.txt", "w") as f:
    f.write("\n".join(train_files))

with open("val_list.txt", "w") as f:
    f.write("\n".join(val_files))

print("学号：your_student_id")   # 将 your_student_id 替换为你的真实学号
