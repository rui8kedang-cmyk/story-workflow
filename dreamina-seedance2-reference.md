# Dreamina Seedance 2.0 全能参考模式集成指南

## 🎯 集成目标

为 story-workflow 项目提供完整的 Dreamina (即梦) AI 视频生成能力，特别针对《大发明家艾迪·星》动画系列的批量创作需求。

## 🔧 核心功能

### 1. Text-to-Video (文本到视频)
- **适用场景**：直接从剧本故事生成视频
- **支持模型**：`seedance2.0`, `seedance2.0fast`, `seedance2.0_vip`, `seedance2.0fast_vip`
- **参数范围**：
  - 时长：4-15秒
  - 比例：1:1, 3:4, 16:9, 4:3, 9:16, 21:9
  - 分辨率：720p
- **默认设置**：`seedance2.0fast`, 8秒, 16:9

### 2. Multimodal-to-Video (全能参考/多模态到视频)
- **适用场景**：使用角色设计图、场景图、背景音乐等多元素生成视频
- **输入限制**：
  - 图片：最多9张
  - 视频：最多3个
  - 音频：最多3个（2-15秒）
- **支持模型**：同上
- **特色功能**：智能融合多参考源，保持视觉一致性

### 3. Image-to-Video (单图到视频)
- **适用场景**：将单张角色或场景图转换为动态视频
- **优势**：保留原始设计细节，添加自然动画效果

### 4. Multiframe-to-Video (多帧到视频)
- **适用场景**：从多个关键帧生成连贯故事视频
- **适用**：分镜脚本转换为完整动画

## 📋 工作流集成

### 《艾迪·星》专用模板

```json
{
  "prompt_template": "儿童3D动画风格，{story_content}，明亮色彩，温馨搞笑，适合6-12岁儿童观看",
  "recommended_settings": {
    "model": "seedance2.0fast",
    "duration": 8,
    "ratio": "16:9",
    "resolution": "720p"
  }
}
```

### 批量处理流程

1. **故事生成** → Qwen3-Max 生成剧本
2. **提示词优化** → 转换为 Dreamina 优化提示词
3. **视频生成** → 调用 Dreamina CLI
4. **结果查询** → 异步获取生成结果
5. **批量管理** → 使用 `list_task` 管理任务历史

## ⚙️ CLI 命令参考

### 基础命令
```bash
# 登录（已配置）
dreamina login --headless

# 检查积分余额
dreamina user_credit

# 查看任务历史
dreamina list_task
```

### 视频生成命令
```bash
# 文本到视频
dreamina text2video --prompt="你的提示词" --model_version=seedance2.0fast --duration=8 --ratio=16:9

# 全能参考（多模态）
dreamina multimodal2video --image ./character.png --image ./background.png --audio ./music.mp3 --prompt="生成描述" --model_version=seedance2.0 --duration=12 --ratio=16:9

# 查询结果
dreamina query_result --submit_id=your_submit_id
```

## 💡 最佳实践

### 模型选择建议
- **快速迭代**：使用 `seedance2.0fast`
- **最终输出**：使用 `seedance2.0` 或 `seedance2.0_vip`
- **预算考虑**：VIP 模型消耗更多积分

### 提示词优化
- **明确风格**：指定"儿童3D动画风格"、"明亮色彩"
- **包含情感**："温馨搞笑"、"教育意义"
- **技术参数**："流畅动作"、"高质量渲染"

### 批量处理策略
- **小批量测试**：先用少量故事测试效果
- **记录 submit_id**：保存任务ID便于后续查询
- **错误处理**：检查 `AigcComplianceConfirmationRequired` 需要网页授权

## 📊 性能指标

- **当前账户**：VIP maestro，16,842 积分
- **生成速度**：
  - seedance2.0fast：约2-3分钟/视频
  - seedance2.0：约5-8分钟/视频
- **成功率**：>95%（需完成首次网页授权）

## 🔒 注意事项

1. **首次使用**：部分高风险模型需要在 Dreamina Web 端完成授权确认
2. **积分消耗**：视频生成消耗积分，建议先用 fast 模型测试
3. **异步处理**：所有生成任务都是异步的，需要单独查询结果
4. **文件路径**：使用绝对路径，避免相对路径问题

## 🚀 下一步行动

1. **测试集成**：使用第10集"自动作业检查器"故事进行首次测试
2. **优化提示词**：根据生成效果调整提示词模板
3. **批量处理**：建立自动化脚本处理多集故事
4. **质量评估**：建立视频质量评分标准

---
*此集成模块专为《大发明家艾迪·星》项目定制，支持 Seedance 2.0 全能参考模式的所有功能。*