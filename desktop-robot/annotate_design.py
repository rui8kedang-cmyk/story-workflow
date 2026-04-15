from PIL import Image, ImageDraw, ImageFont
import os

img = Image.open(r'C:\Users\xurui01\.openclaw\workspace\desktop-robot\design-v1.png')
print(f"Image size: {img.size}")

draw = ImageDraw.Draw(img)

# Try to use a visible font
try:
    font_large = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 28)
    font_medium = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 22)
    font_small = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 18)
except:
    font_large = ImageFont.load_default()
    font_medium = font_large
    font_small = font_large

w, h = img.size

# Colors
RED = (255, 50, 50)
BLUE = (50, 100, 255)
GREEN = (50, 200, 50)
ORANGE = (255, 160, 0)
PURPLE = (180, 50, 220)
WHITE = (255, 255, 255)
YELLOW = (255, 220, 0)

def draw_label(draw, x, y, text, color, font, anchor_x=None, anchor_y=None):
    """Draw text with background box and optional leader line"""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    padding = 6
    # Background
    draw.rectangle([x - padding, y - padding, x + tw + padding, y + th + padding], 
                   fill=(0, 0, 0, 200), outline=color, width=2)
    draw.text((x, y), text, fill=color, font=font)
    # Leader line
    if anchor_x is not None and anchor_y is not None:
        cx = x + tw // 2
        cy = y + th // 2
        draw.line([(cx, cy), (anchor_x, anchor_y)], fill=color, width=2)
        draw.ellipse([anchor_x-4, anchor_y-4, anchor_x+4, anchor_y+4], fill=color)

# The image appears to be a front view of a cute yellow robot
# Based on the screenshot I saw earlier, approximate positions:
# Head is roughly top 60% of image, body is bottom 40%
# Eyes are two dark circles in the head area

cx = w // 2  # center x

# === ANNOTATIONS ===

# 1. Head / PCB area
draw_label(draw, int(w*0.65), int(h*0.15), "PCB开发板", RED, font_large,
           int(w*0.5), int(h*0.28))
draw_label(draw, int(w*0.65), int(h*0.20), "93.5×36.5mm", RED, font_medium)
draw_label(draw, int(w*0.65), int(h*0.25), "从背面推入安装", RED, font_small)

# 2. Left eye
draw_label(draw, int(w*0.05), int(h*0.22), "左眼 Ø33mm", BLUE, font_medium,
           int(w*0.35), int(h*0.30))

# 3. Right eye  
draw_label(draw, int(w*0.62), int(h*0.30), "右眼 Ø33mm", BLUE, font_medium,
           int(w*0.58), int(h*0.30))

# 4. Mic hole
draw_label(draw, int(w*0.05), int(h*0.10), "⚠️ 需加：麦克风孔", ORANGE, font_medium,
           int(w*0.45), int(h*0.18))
draw_label(draw, int(w*0.05), int(h*0.15), "头顶 Ø2mm×2", ORANGE, font_small)

# 5. Speaker holes
draw_label(draw, int(w*0.05), int(h*0.38), "⚠️ 需加：喇叭声孔", ORANGE, font_medium,
           int(w*0.30), int(h*0.42))
draw_label(draw, int(w*0.05), int(h*0.43), "侧面/背面 1.5mm孔阵列", ORANGE, font_small)

# 6. Servo #2 (pitch) - neck area
draw_label(draw, int(w*0.65), int(h*0.48), "舵机#2（俯仰）", GREEN, font_large,
           int(w*0.50), int(h*0.50))
draw_label(draw, int(w*0.65), int(h*0.53), "控制点头/抬头", GREEN, font_medium)
draw_label(draw, int(w*0.65), int(h*0.57), "23×12×29mm", GREEN, font_small)

# 7. Servo #1 (yaw) - body top
draw_label(draw, int(w*0.65), int(h*0.65), "舵机#1（水平）", GREEN, font_large,
           int(w*0.50), int(h*0.62))
draw_label(draw, int(w*0.65), int(h*0.70), "控制左右转头", GREEN, font_medium)
draw_label(draw, int(w*0.65), int(h*0.74), "固定在身体内", GREEN, font_small)

# 8. Battery
draw_label(draw, int(w*0.05), int(h*0.68), "锂电池 3.7V", PURPLE, font_large,
           int(w*0.40), int(h*0.75))
draw_label(draw, int(w*0.05), int(h*0.73), "50×34×8mm", PURPLE, font_medium)
draw_label(draw, int(w*0.05), int(h*0.77), "MX1.25 正向接口", PURPLE, font_small)

# 9. USB-C
draw_label(draw, int(w*0.05), int(h*0.55), "USB-C 充电口", YELLOW, font_medium,
           int(w*0.45), int(h*0.88))
draw_label(draw, int(w*0.05), int(h*0.60), "背面开口 12×7mm", YELLOW, font_small)

# 10. PCA9685
draw_label(draw, int(w*0.05), int(h*0.83), "PCA9685 驱动板", PURPLE, font_medium,
           int(w*0.35), int(h*0.82))
draw_label(draw, int(w*0.05), int(h*0.88), "62×25mm 竖放", PURPLE, font_small)

# 11. Separation line hint
draw_label(draw, int(w*0.30), int(h*0.47), "← 头身分离线（旋转接缝）→", YELLOW, font_medium)

# 12. Title
draw_label(draw, int(w*0.25), int(h*0.02), "桌面机器人 零件布局标注", WHITE, font_large)

# Save
output_path = r'C:\Users\xurui01\.openclaw\workspace\desktop-robot\design-v1-annotated.png'
img.save(output_path)
print(f"Saved to: {output_path}")
