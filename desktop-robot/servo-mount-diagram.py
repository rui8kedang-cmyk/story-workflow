"""
桌面机器人 — 舵机摆臂与头部固定 截面示意图
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Arc
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(10, 14))
ax.set_xlim(-60, 60)
ax.set_ylim(-10, 130)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('桌面机器人 舵机安装截面图（正面剖视）', fontsize=16, fontweight='bold', 
             fontfamily='Microsoft YaHei', pad=20)

# ============ 底座 ============
base = FancyBboxPatch((-40, 0), 80, 40, boxstyle="round,pad=3", 
                       facecolor='#E8E0D4', edgecolor='#333', linewidth=2)
ax.add_patch(base)
ax.text(0, 5, '底座', ha='center', va='center', fontsize=11, fontfamily='Microsoft YaHei', color='#666')

# 电池
battery = FancyBboxPatch((-30, 3), 25, 8, boxstyle="round,pad=1",
                          facecolor='#90EE90', edgecolor='#333', linewidth=1.5)
ax.add_patch(battery)
ax.text(-17.5, 7, '锂电池', ha='center', va='center', fontsize=8, fontfamily='Microsoft YaHei')

# PCA9685
pca = FancyBboxPatch((5, 3), 25, 12, boxstyle="round,pad=1",
                      facecolor='#87CEEB', edgecolor='#333', linewidth=1.5)
ax.add_patch(pca)
ax.text(17.5, 9, 'PCA9685', ha='center', va='center', fontsize=7, fontfamily='Microsoft YaHei')

# 升压模块
boost = FancyBboxPatch((-30, 14), 15, 8, boxstyle="round,pad=1",
                        facecolor='#FFD700', edgecolor='#333', linewidth=1.5)
ax.add_patch(boost)
ax.text(-22.5, 18, '升压5V', ha='center', va='center', fontsize=7, fontfamily='Microsoft YaHei')

# ============ 水平舵机（底座内上方）============
# 舵机体
servo_h_body = patches.Rectangle((-11, 25), 22, 12, facecolor='#4169E1', edgecolor='#222', linewidth=2)
ax.add_patch(servo_h_body)
ax.text(0, 31, '水平舵机', ha='center', va='center', fontsize=8, fontfamily='Microsoft YaHei', color='white', fontweight='bold')

# 舵机耳朵（固定翼）
ear_l = patches.Rectangle((-16, 31), 5, 3, facecolor='#4169E1', edgecolor='#222', linewidth=1.5)
ear_r = patches.Rectangle((11, 31), 5, 3, facecolor='#4169E1', edgecolor='#222', linewidth=1.5)
ax.add_patch(ear_l)
ax.add_patch(ear_r)
# 耳朵螺丝
ax.plot(-13.5, 32.5, 'o', color='#333', markersize=4)
ax.plot(13.5, 32.5, 'o', color='#333', markersize=4)

# 舵机输出轴
ax.plot(0, 37, 'o', color='#FFD700', markersize=8, zorder=5)
ax.plot(0, 37, '+', color='#222', markersize=10, markeredgewidth=2, zorder=6)

# 水平摆臂（连接颈部）
arm_h = patches.Rectangle((-14, 37), 28, 3, facecolor='#FF6347', edgecolor='#222', linewidth=1.5)
ax.add_patch(arm_h)
ax.text(20, 38.5, '← 水平摆臂', ha='left', va='center', fontsize=8, fontfamily='Microsoft YaHei', color='#FF6347', fontweight='bold')

# 摆臂螺丝孔
for x in [-10, -6, 0, 6, 10]:
    ax.plot(x, 38.5, 'o', color='#222', markersize=2.5)

# 固定标注
ax.annotate('螺丝固定到底座壁', xy=(-13.5, 32.5), xytext=(-45, 28),
            fontsize=7, fontfamily='Microsoft YaHei', color='#666',
            arrowprops=dict(arrowstyle='->', color='#999', lw=0.8))

# ============ 颈部连接件 ============
neck = FancyBboxPatch((-10, 40), 20, 30, boxstyle="round,pad=2",
                       facecolor='#DDA0DD', edgecolor='#333', linewidth=2)
ax.add_patch(neck)
ax.text(0, 48, '颈部\n连接件', ha='center', va='center', fontsize=9, fontfamily='Microsoft YaHei', linespacing=1.5)

# 颈部走线通道
wire_channel = patches.Circle((0, 55), 4, facecolor='#FFF', edgecolor='#999', linewidth=1, linestyle='--')
ax.add_patch(wire_channel)
ax.text(0, 55, '走线', ha='center', va='center', fontsize=6, fontfamily='Microsoft YaHei', color='#999')

# 走线标注
ax.annotate('Ø17.5mm\n走线通道', xy=(4, 55), xytext=(25, 52),
            fontsize=7, fontfamily='Microsoft YaHei', color='#999',
            arrowprops=dict(arrowstyle='->', color='#999', lw=0.8))

# ============ 俯仰舵机（颈部顶端）============
servo_p_body = patches.Rectangle((-11, 65), 22, 12, facecolor='#4169E1', edgecolor='#222', linewidth=2)
ax.add_patch(servo_p_body)
ax.text(0, 71, '俯仰舵机', ha='center', va='center', fontsize=8, fontfamily='Microsoft YaHei', color='white', fontweight='bold')

# 舵机耳朵
ear_pl = patches.Rectangle((-16, 71), 5, 3, facecolor='#4169E1', edgecolor='#222', linewidth=1.5)
ear_pr = patches.Rectangle((11, 71), 5, 3, facecolor='#4169E1', edgecolor='#222', linewidth=1.5)
ax.add_patch(ear_pl)
ax.add_patch(ear_pr)
ax.plot(-13.5, 72.5, 'o', color='#333', markersize=4)
ax.plot(13.5, 72.5, 'o', color='#333', markersize=4)

# 舵机输出轴
ax.plot(0, 77, 'o', color='#FFD700', markersize=8, zorder=5)
ax.plot(0, 77, '+', color='#222', markersize=10, markeredgewidth=2, zorder=6)

# 俯仰摆臂（连接头部）
arm_p = patches.Rectangle((-14, 77), 28, 3, facecolor='#FF6347', edgecolor='#222', linewidth=1.5)
ax.add_patch(arm_p)
ax.text(20, 78.5, '← 俯仰摆臂', ha='left', va='center', fontsize=8, fontfamily='Microsoft YaHei', color='#FF6347', fontweight='bold')

# 摆臂螺丝孔
for x in [-10, -6, 0, 6, 10]:
    ax.plot(x, 78.5, 'o', color='#222', markersize=2.5)

# 标注
ax.annotate('舵机体固定在\n颈部连接件上', xy=(13.5, 72.5), xytext=(25, 67),
            fontsize=7, fontfamily='Microsoft YaHei', color='#666',
            arrowprops=dict(arrowstyle='->', color='#999', lw=0.8))

# ============ 头部 ============
# 头部外壳（椭圆胶囊形）
head = FancyBboxPatch((-50, 82), 100, 42, boxstyle="round,pad=5",
                       facecolor='#FFF8DC', edgecolor='#333', linewidth=2.5)
ax.add_patch(head)

# 头部底面安装座（关键！）
mount_plate = patches.Rectangle((-15, 82), 30, 4, facecolor='#FF6347', edgecolor='#222', linewidth=2, alpha=0.7)
ax.add_patch(mount_plate)
ax.text(0, 84, '摆臂安装座', ha='center', va='center', fontsize=7, fontfamily='Microsoft YaHei', color='white', fontweight='bold')

# M2 安装孔标注
ax.plot(-8, 84, 'o', color='#222', markersize=5)
ax.plot(8, 84, 'o', color='#222', markersize=5)
ax.plot(0, 84, 'o', color='#FFD700', markersize=5)
ax.annotate('M2螺丝孔', xy=(-8, 84), xytext=(-40, 80),
            fontsize=7, fontfamily='Microsoft YaHei', color='#FF6347',
            arrowprops=dict(arrowstyle='->', color='#FF6347', lw=1))

# PCB 双眼屏
pcb = patches.Rectangle((-46, 95), 92, 6, facecolor='#228B22', edgecolor='#222', linewidth=1.5)
ax.add_patch(pcb)
ax.text(0, 98, 'ESP32-S3 DualEye PCB (93.5mm)', ha='center', va='center', fontsize=7, fontfamily='Microsoft YaHei', color='white')

# 左眼
eye_l = patches.Circle((-27, 101), 8, facecolor='#1a1a2e', edgecolor='#333', linewidth=2)
ax.add_patch(eye_l)
ax.text(-27, 101, 'L', ha='center', va='center', fontsize=14, fontweight='bold', color='#00BFFF')

# 右眼
eye_r = patches.Circle((27, 101), 8, facecolor='#1a1a2e', edgecolor='#333', linewidth=2)
ax.add_patch(eye_r)
ax.text(27, 101, 'R', ha='center', va='center', fontsize=14, fontweight='bold', color='#00BFFF')

# 喇叭（头顶）
speaker = patches.Rectangle((-15, 112), 30, 6, facecolor='#D2691E', edgecolor='#222', linewidth=1.5)
ax.add_patch(speaker)
ax.text(0, 115, '喇叭 20x30mm', ha='center', va='center', fontsize=7, fontfamily='Microsoft YaHei', color='white')

# 声孔标注
for x in [-8, -4, 0, 4, 8]:
    ax.plot(x, 121, 'v', color='#666', markersize=4)
ax.text(0, 124, '头顶声孔 ↑', ha='center', va='center', fontsize=7, fontfamily='Microsoft YaHei', color='#666')

# ============ 尺寸标注 ============
# 总高
ax.annotate('', xy=(55, 0), xytext=(55, 125),
            arrowprops=dict(arrowstyle='<->', color='#E74C3C', lw=1.5))
ax.text(57, 62, '总高\n~116mm', ha='left', va='center', fontsize=9, fontfamily='Microsoft YaHei', color='#E74C3C', fontweight='bold')

# 头部高
ax.annotate('', xy=(-55, 82), xytext=(-55, 124),
            arrowprops=dict(arrowstyle='<->', color='#3498DB', lw=1.2))
ax.text(-57, 103, '头部\n46mm', ha='right', va='center', fontsize=8, fontfamily='Microsoft YaHei', color='#3498DB')

# 底座高
ax.annotate('', xy=(-55, 0), xytext=(-55, 40),
            arrowprops=dict(arrowstyle='<->', color='#3498DB', lw=1.2))
ax.text(-57, 20, '底座\n45mm', ha='right', va='center', fontsize=8, fontfamily='Microsoft YaHei', color='#3498DB')

# ============ 图例 ============
legend_y = -5
ax.text(-50, legend_y, '图例：', fontsize=8, fontfamily='Microsoft YaHei', fontweight='bold')
ax.add_patch(patches.Rectangle((-35, legend_y-1.5), 6, 3, facecolor='#4169E1', edgecolor='#222', linewidth=1))
ax.text(-27, legend_y, 'SG90舵机', fontsize=7, fontfamily='Microsoft YaHei')
ax.add_patch(patches.Rectangle((-10, legend_y-1.5), 6, 3, facecolor='#FF6347', edgecolor='#222', linewidth=1))
ax.text(-2, legend_y, '摆臂/安装座', fontsize=7, fontfamily='Microsoft YaHei')
ax.plot(18, legend_y, 'o', color='#FFD700', markersize=6)
ax.text(22, legend_y, '输出轴', fontsize=7, fontfamily='Microsoft YaHei')

plt.tight_layout()
plt.savefig('C:/Users/xurui01/.openclaw/workspace/desktop-robot/servo-mount-cross-section.png', 
            dpi=150, bbox_inches='tight', facecolor='white')
print("Done: servo-mount-cross-section.png")
