import os
import random
import matplotlib.pyplot as plt
from PIL import Image

AUG_DIR  = "./Answer-Sheet-Data-Augmented"
IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp"}

all_images = [
    os.path.join(AUG_DIR, f) for f in os.listdir(AUG_DIR)
    if os.path.splitext(f)[1].lower() in IMG_EXTS
]

# 1. 随机展示9张样本图片
sample = random.sample(all_images, min(9, len(all_images)))
fig, axes = plt.subplots(3, 3, figsize=(10, 10))
for ax, img_path in zip(axes.flatten(), sample):
    img = Image.open(img_path).convert("RGB")
    ax.imshow(img)
    ax.set_title(os.path.basename(img_path)[:15], fontsize=8)
    ax.axis("off")
plt.suptitle("数据集样本展示", fontsize=14)
plt.tight_layout()
plt.savefig("sample_visualization.png", dpi=150)
plt.show()
print("样本图已保存：sample_visualization.png")

# 2. 训练集/验证集数量柱状图
with open("train_list.txt") as f:
    n_train = len(f.read().splitlines())
with open("val_list.txt") as f:
    n_val = len(f.read().splitlines())

fig2, ax2 = plt.subplots(figsize=(5, 4))
ax2.bar(["训练集", "验证集"], [n_train, n_val], color=["steelblue", "coral"])
ax2.set_ylabel("图片数量")
ax2.set_title("训练集与验证集数量分布")
for i, v in enumerate([n_train, n_val]):
    ax2.text(i, v + 5, str(v), ha="center", fontsize=12)
plt.tight_layout()
plt.savefig("split_distribution.png", dpi=150)
plt.show()
print("分布图已保存：split_distribution.png")
