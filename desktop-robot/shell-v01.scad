// 桌面机器人外壳 3D模型 v0.1
// 基于微雪 ESP32-S3-LCD-1.85 (55×55mm)
// 用 OpenSCAD 打开渲染：https://openscad.org/

/* ===== 全局参数（可调） ===== */

// 头部
head_diameter = 90;          // 球形头部外径
head_wall = 3;               // 壁厚
screen_window_dia = 40;      // 屏幕圆形窗口直径
screen_offset_up = 5;        // 屏幕窗口向上偏移（更拟人）

// PCB凹槽（头部背面）
pcb_w = 56;                  // 凹槽宽（PCB 55 + 0.5×2间隙）
pcb_h = 56;                  // 凹槽高
pcb_d = 14;                  // 凹槽深（PCB厚12 + 2余量）

// USB-C开口
usbc_w = 12;
usbc_h = 7;

// 颈部
neck_height = 30;            // 颈部高度
neck_diameter = 25;          // 颈部直径

// 底座
base_width = 80;             // 底座宽
base_depth = 80;             // 底座深
base_height = 50;            // 底座高
base_wall = 3;               // 底座壁厚
base_corner_r = 10;          // 底座圆角

// 舵机 SG90
servo_w = 23;
servo_d = 12.2;
servo_h = 29;

// 喇叭声孔
sound_hole_dia = 1.5;
sound_hole_spacing = 4;
sound_hole_rows = 4;
sound_hole_cols = 6;

// 麦克风拾音孔
mic_hole_dia = 2;

/* ===== 颜色 ===== */
head_color = [1, 0.92, 0.6, 0.85];     // 暖黄色（可爱风）
base_color = [0.95, 0.85, 0.55, 0.85];  // 稍深黄
neck_color = [0.8, 0.8, 0.8, 1];        // 灰色
screen_color = [0.1, 0.1, 0.1, 1];      // 黑色屏幕
servo_color = [0.2, 0.3, 0.8, 0.7];     // 蓝色舵机

$fn = 80;  // 圆形精度

/* ===== 模块定义 ===== */

// 球形头部（前半壳）
module head_front() {
    difference() {
        // 外球前半
        difference() {
            sphere(d=head_diameter);
            sphere(d=head_diameter - head_wall*2);
            // 切掉后半
            translate([0, 0, 0])
                rotate([0,0,0])
                translate([0, head_diameter/2, 0])
                cube([head_diameter+10, head_diameter, head_diameter+10], center=true);
        }
        // 屏幕圆形窗口
        translate([0, -head_diameter/2, screen_offset_up])
            rotate([90, 0, 0])
            cylinder(d=screen_window_dia, h=head_wall+2, center=true);
        
        // 麦克风拾音孔（屏幕上方）
        translate([-6, -head_diameter/2, screen_offset_up + screen_window_dia/2 + 5])
            rotate([90, 0, 0])
            cylinder(d=mic_hole_dia, h=head_wall+2, center=true);
        translate([6, -head_diameter/2, screen_offset_up + screen_window_dia/2 + 5])
            rotate([90, 0, 0])
            cylinder(d=mic_hole_dia, h=head_wall+2, center=true);
        
        // 侧面喇叭声孔阵列
        translate([head_diameter/2 - head_wall/2, 0, 0])
            rotate([0, 90, 0])
            for(r = [0 : sound_hole_rows-1])
                for(c = [0 : sound_hole_cols-1])
                    translate([
                        (c - (sound_hole_cols-1)/2) * sound_hole_spacing,
                        (r - (sound_hole_rows-1)/2) * sound_hole_spacing,
                        0
                    ])
                    cylinder(d=sound_hole_dia, h=head_wall+2, center=true);
    }
}

// 球形头部（后半壳 + PCB凹槽）
module head_back() {
    difference() {
        // 外球后半
        difference() {
            sphere(d=head_diameter);
            sphere(d=head_diameter - head_wall*2);
            // 切掉前半
            translate([0, -head_diameter/2, 0])
                cube([head_diameter+10, head_diameter, head_diameter+10], center=true);
        }
        // PCB凹槽
        translate([0, head_diameter/2 - pcb_d/2 - head_wall, 0])
            cube([pcb_w, pcb_d, pcb_h], center=true);
        
        // USB-C开口（底部）
        translate([0, head_diameter/2 - head_wall, -pcb_h/2 + usbc_h/2])
            cube([usbc_w, head_wall+5, usbc_h], center=true);
    }
}

// 屏幕示意（黑色圆盘）
module screen() {
    translate([0, -head_diameter/2 + head_wall/2, screen_offset_up])
        rotate([90, 0, 0])
        cylinder(d=screen_window_dia - 1, h=1, center=true);
}

// 颈部连接件
module neck() {
    cylinder(d=neck_diameter, h=neck_height);
}

// 舵机示意
module servo() {
    cube([servo_w, servo_d, servo_h], center=true);
    // 摇臂
    translate([0, 0, servo_h/2])
        cylinder(d=7, h=4, center=true);
}

// 底座（圆角方体）
module base_body() {
    difference() {
        // 外壳 - 圆角
        minkowski() {
            cube([
                base_width - base_corner_r*2,
                base_depth - base_corner_r*2,
                base_height - base_corner_r
            ], center=true);
            cylinder(r=base_corner_r, h=base_corner_r);
        }
        // 内腔
        translate([0, 0, base_wall])
            minkowski() {
                cube([
                    base_width - base_corner_r*2 - base_wall*2,
                    base_depth - base_corner_r*2 - base_wall*2,
                    base_height - base_corner_r
                ], center=true);
                cylinder(r=base_corner_r - base_wall, h=1);
            }
    }
}

/* ===== 组装 ===== */

// 底座
translate([0, 0, base_height/2])
    color(base_color)
    base_body();

// 水平旋转舵机（在底座内部顶端）
translate([0, 0, base_height - 5])
    color(servo_color)
    servo();

// 颈部
translate([0, 0, base_height])
    color(neck_color)
    neck();

// 俯仰舵机（颈部顶端）
translate([0, 0, base_height + neck_height])
    rotate([0, 90, 0])
    color(servo_color)
    servo();

// 头部前壳
translate([0, 0, base_height + neck_height + head_diameter/2])
    color(head_color)
    head_front();

// 头部后壳
translate([0, 0, base_height + neck_height + head_diameter/2])
    color(head_color, 0.5)
    head_back();

// 屏幕
translate([0, 0, base_height + neck_height + head_diameter/2])
    color(screen_color)
    screen();

/* ===== 标注线（辅助） ===== */

// 总高度标注
echo(str("=== 整机尺寸 ==="));
echo(str("头部直径: ", head_diameter, "mm"));
echo(str("底座: ", base_width, "×", base_depth, "×", base_height, "mm"));
echo(str("颈部高: ", neck_height, "mm"));
echo(str("总高度: ", base_height + neck_height + head_diameter, "mm (", 
    base_height + neck_height + head_diameter, ")"));
echo(str("PCB凹槽: ", pcb_w, "×", pcb_h, "×", pcb_d, "mm"));
echo(str("屏幕窗口: Ø", screen_window_dia, "mm"));
