# 项目全景交接文档

> 给新 AI 助手的快速学习手册
> 生成日期：2026-04-09
> 工作区根目录：C:\Users\xurui01\.openclaw\workspace

---

## 👤 用户信息

- 邮箱/ID：xurui01@corp.netease.com
- 时区：GMT+8（Asia/Shanghai）
- 工作环境：办公电脑 (GIH-D-32220)，Windows 10
- 方向：游戏美术/开发（本职）、私人创作（动画剧本）、投资、生活
- 偏好：记忆按主题分类、所有内容都要记录、注意隐私（办公环境）

---

## 📂 记忆体系

记忆按主题分目录存储，索引文件：`memory/README.md`

| 代号 | 目录 | 方向 | 说明 |
|------|------|------|------|
| A | memory/A-work/ | 工作 | 游戏美术、画面对比、数据产出 |
| B | memory/B-creative/ | 私人创作 | 剧本、分镜，《艾迪·星》《土松嘟嘟》 |
| C | memory/C-investment/ | 投资 | 金融、利息、股票 |
| D | memory/D-life/ | 生活 | 旅游、美食 |
| X | memory/X-future/ | 未来发展 | 新兴领域、创业展望、游戏开发 |

每日工作日志：`memory/2026-MM-DD.md`（从 2026-03-05 开始）

---

## 🚀 活跃项目一览

### 项目1：桌面AI伴侣机器人（X-future）

**状态：** 设计阶段（未采购）
**简介：** 基于 ESP32-S3 的桌面 AI 对话机器人，搭载 xiaozhi-esp32 开源固件，双眼圆屏显示表情，头部可转动。

**关键文件：**
- 项目主文档：`memory/X-future/desktop-robot.md`（完整选型/架构/待办）
- 外壳规格 v0.1（旧，单屏）：`memory/X-future/desktop-robot-shell-spec.md`
- 外壳规格 v0.2（新，双眼屏）：`memory/X-future/desktop-robot-shell-spec-v02.md`
- 旧开发板技术档案：`memory/X-future/waveshare-esp32s3-lcd185-spec.md`
- 3D模型文件（旧）：`desktop-robot/shell-v01.scad`
- 新屏幕结构图纸：`desktop-robot/ESP32-S3-DualEye-LCD-1.28.pdf`
- 外形设计参考：`desktop-robot/design-reference.md`

**当前状态（2026-04-09）：**
- 原方案：微雪 ESP32-S3-LCD-1.85 单屏（¥151）+ 球形头部 Ø90mm
- 新方案：微雪 ESP32-S3-DualEye-Touch-LCD-1.28 双眼屏（¥99）+ 椭圆头部 100×46mm
- 新方案外壳规格已出（v0.2），尚未生成新3D模型
- 采购清单需根据新屏幕更新
- 开源基座：xiaozhi-esp32（GitHub 25.5k⭐，MIT）

**技术要点：**
- 主控：ESP32-S3R8
- 双屏：2× 1.28寸圆形LCD（240×240）
- 音频：ES8311 + ES7210 + MIC + 喇叭
- 舵机：2× SG90（水平+俯仰），PCA9685驱动板（I2C 0x40）
- 电池：3.7V MX1.25 2PIN 正向

---

### 项目2：Alive Illusion / 26号宇宙（X-future → AliveIllusion/）

**状态：** M0完成 → M1灰盒原型（搁置中）
**简介：** 生存卡牌策略微信小程序游戏，AI监控下的密闭空间生存。

**关键文件：**
- 项目总览：`AliveIllusion/README.md`
- 设计文档索引：`AliveIllusion/documents/design-index.md`
- 卡牌规格：`AliveIllusion/documents/card-specification.md`
- TypeScript类型定义：`AliveIllusion/documents/types-draft.ts`
- 游戏设计文档（GDD）：`memory/X-future/GDD-card-survival.md`
- 数值模拟脚本（最终版）：`AliveIllusion/scripts/ak_simulation_v6b_reward.py`

**设计文档（29个，均在 memory/X-future/AK-*.md）：**
- 世界观：AK-worldbuilding-v3.md
- 卡牌表：AK-card-table-v2.md
- 事件系统：AK-events-master-v3.md
- 房间设计：AK-room-design-v1.md
- UI布局：AK-ui-layout-v1.md
- 教程系统：AK-tutorial-v1.md
- 美术风格：AK-art-style-v1.md
- 其他：体力/精神/衰减/debuff/奖励/叙事/科技研究等

**数值要点：** 摸4打3，牌库14张，平均生存16.5天，3000局验证通过

**技术栈：** Cocos Creator 3.8.8 LTS + TypeScript，目标微信/抖音小程序

**注意：** 2026-04-08 用户表示此项目正式搁置，除非用户主动提起不再推进。

---

### 项目3：《大发明家艾迪·星》动画创作（B-creative）

**状态：** 创作中
**简介：** 3D动画短片系列，搞笑温馨风格，主角艾迪用废旧零件发明各种装置。

**关键文件：**
- 角色/世界观设定：`memory/B-creative/projects.md`
- 项目设定：`艾迪小发明家/项目设定.md`
- 创作笔记：`艾迪小发明家/创作笔记.md`
- 备选故事：`艾迪小发明家/备选故事.md`
- 已完成故事：`艾迪小发明家/已完成故事.md`
- 工作流设定：`memory/B-creative/eddie-workflow.md`
- 剧本收录：`memory/B-creative/eddie-scripts.md`

**已完成故事：**
- 第07集：防雨书包罩（故事 + 分镜脚本）
- 第08集：完美发型器（故事）
- 第09集：成绩报告单美化器（故事）
- 故事文件：`艾迪小发明家/故事/` 目录
- 分镜脚本：`艾迪小发明家/分镜脚本/` 目录

**核心角色：**
- 艾迪：小学生发明家，聪明邋遢，鬼点子多
- 爷爷：知名发明家，古怪老顽童
- 机械狗：爷爷送的礼物，装错了发声装置会猫叫

---

### 项目4：story-workflow 创作工具（story-workflow/）

**状态：** 已部署，可迭代
**简介：** 基于 AI 的小故事批量创作工具，服务于《艾迪·星》系列的 剧本→分镜→Seedance提示词 全流程。

**关键文件：**
- 项目文档：`story-workflow/PROJECT.md`
- 桌面端：`story-workflow/index.html`
- 手机端：`story-workflow/mobile.html`
- 偏好工具：`story-workflow/preference-tool.html`
- 预设配置：`story-workflow/presets/`
- 技能配置：`story-workflow/skills/`
- 清单文件：`story-workflow/manifest.json`

**部署地址：**
- GitHub: https://github.com/rui8kedang-cmyk/story-workflow
- Cloudflare Pages: https://story-workflow.pages.dev
- 手机版: https://story-workflow.pages.dev/mobile.html

---

## 🛠️ 已安装工具

- **即梦 CLI (dreamina)**：`~/.dreamina_cli/dreamina.exe`
  - 已登录，UID: 3370452299295072，VIP: maestro
  - 支持：text2video, image2video, multiframe2video, multimodal2video
  - Seedance 2.0 系列模型可用
  - 积分余额：~10097（2026-04-06 消耗15测试）

---

## 📋 工作习惯备忘

- 所有讨论内容都需要记录到对应记忆文件
- 不确定分类时要确认
- 注意隐私：办公环境，敏感内容留意
- edit 工具在大中文文件上匹配容易失败 → 用 write + exec 组合更可靠
- 子代理生成大文件容易超时 → 自己分块写入
- GitHub Pages 国内手机访问不了 → 用 Cloudflare Pages
- POPO 不支持 markdown 表格 → 用列表格式
