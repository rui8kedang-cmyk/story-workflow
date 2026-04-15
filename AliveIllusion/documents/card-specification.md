# 🃏 Alive Illusion 卡牌数据规格

**版本：** v2 (基于 AK-card-table-v2.md)  
**卡牌总数：** 20张（🟢基础6 + 🔵维护6 + 🔴应急4 + 🟣特殊4）  
**最后更新：** 2026-03-27

---

## 📊 卡牌数据结构

### 基础属性
```typescript
interface CardBase {
  id: number;           // 1-20
  name: string;         // 卡牌名称（中文）
  type: CardType;       // "basic" | "maintenance" | "emergency" | "special"
  color: string;        // "#78e08f" (🟢), "#3498db" (🔵), "#e74c3c" (🔴), "#9b59b6" (🟣)
  description: string;  // AI系统描述文本
  quality?: "standard" | "upgraded";  // 品质（标准/升级+）
}
```

### 数值效果
```typescript
interface CardEffects {
  // 主要效果（正值表示增加）
  food?: number;       // 饱食度变化
  water?: number;      // 水分变化
  mood?: number;       // 精神状态变化
  stamina?: number;    // 体力变化
  health?: number;     // 健康度直接变化（仅急救协议）
  
  // 特殊效果
  buffs?: {
    nextDayBasicBuff?: number;    // 下一天基础牌效果加成（如+30%）
    memorySlots?: number;         // 下一天内存增加（如+2）
    specialFlags?: string[];      // 特殊标记
  };
  
  // 清除效果
  clears?: {
    moodDebuffs?: boolean;        // 清除所有精神debuff
    physicalDebuffs?: string[];   // 清除特定体力debuff
    all?: boolean;                // 清除所有buff/debuff
  };
}
```

### 消耗代价
```typescript
interface CardCosts {
  // 基本消耗（负值表示减少）
  food?: number;       // 饱食度消耗
  water?: number;      // 水分消耗
  mood?: number;       // 精神状态消耗
  stamina?: number;    // 体力消耗
  
  // 特殊代价
  special?: {
    skipOtherActions?: boolean;   // 本回合不能再打其他牌
    discardAllHand?: boolean;     // 丢弃所有手牌
    endTurn?: boolean;            // 立即结束回合
    nextDayPenalty?: {            // 次日惩罚
      memorySlots?: number;       // 内存减少
      stamina?: number;           // 体力减少
    };
  };
}
```

### 条件效果
```typescript
interface CardConditions {
  // 触发条件
  triggers?: {
    moodDebuffActive?: boolean;   // 当有精神debuff时
    moodLow?: number;             // 精神状态≤某个值
    healthLow?: number;           // 健康度<某个值
    waterZero?: boolean;          // 水分=0时
  };
  
  // 概率效果
  chances?: {
    memoryFragment?: number;      // 获得记忆碎片概率
    emergencyCard?: number;       // 获得应急牌概率
  };
}
```

---

## 📋 20张卡牌完整数据表

### 🟢 基础指令 (6张)

| ID | 名称 | 类型 | 效果 | 消耗 | 特殊/条件 |
|----|------|------|------|------|-----------|
| 1 | 进食指令 | basic | 饱食+25,体力+5 | 体力-3 | - |
| 2 | 饮水指令 | basic | 水分+30 | 体力-2 | - |
| 3 | 休眠模式 | basic | 体力+35,精神+5 | 饱食-5,水分-5 | 占满行动,本回合不能再打其他牌 |
| 4 | 高压氧气 | basic | 精神+10,体力+5 | 无 | - |
| 5 | 幻想 | basic | 精神+15 | 体力-2 | 若有精神debuff,额外+5 |
| 6 | 健胃消食 | basic | 饱食+10 | 水分-3 | 下一天进食指令效果+30% |

### 🔵 维护指令 (6张)

| ID | 名称 | 类型 | 效果 | 消耗 | 特殊/条件 |
|----|------|------|------|------|-----------|
| 7 | 机械指压 | maintenance | 体力+15,精神+10 | 饱食-8,水分-10 | 连续3天未用维护指令触发"肌肉萎缩" |
| 8 | 清洁程序 | maintenance | 精神+15 | 体力-5,水分-8 | 清除"卫生恶化"debuff |
| 9 | 全身扫描 | maintenance | 显示隐藏信息 | 无 | 健康度<50时获得1张应急牌 |
| 10 | 空间整理 | maintenance | 精神+10 | 体力-8 | 下一天基础牌效果+20% |
| 11 | 记忆回放 | maintenance | 精神+20 | 体力-5 | 20%概率获记忆碎片;精神≤20时额外+10 |
| 12 | 急冻箱 | maintenance | 体力+10 | 饱食-3 | 可解除"轻伤"debuff剩余天数-1 |

### 🔴 应急指令 (4张)

| ID | 名称 | 类型 | 效果 | 消耗 | 特殊/条件 |
|----|------|------|------|------|-----------|
| 13 | 强制进食 | emergency | 饱食+40 | 精神-15,体力-5 | 无视"拒食"debuff |
| 14 | 紧急补水 | emergency | 水分+45 | 精神-10 | 水分=0时额外健康+10 |
| 15 | 急救协议 | emergency | 健康+20 | 体力-15,精神-10 | 次日体力-20;可解除重伤debuff |
| 16 | 强制休眠 | emergency | 体力+50,清精神debuff | 饱食-10,水分-10 | 使用后本回合立即结束 |

### 🟣 特殊指令 (4张)

| ID | 名称 | 类型 | 效果 | 消耗 | 特殊/条件 |
|----|------|------|------|------|-----------|
| 17 | 超频运算 | special | 下一天内存+2,算力+1 | 无 | 后天内存-1,算力仅1 |
| 18 | 灵光一闪 | special | 随机+2张牌 | 精神-5 | 完全随机(可能任何类型) |
| 19 | 系统重启 | special | 全数值归50,清所有状态 | 丢弃所有手牌 | 下一天从0手牌开始 |
| 20 | 机械的碰撞 | special | 精神+40,清精神debuff | 体力-30,水分-25 | 使用时体力<35或水分<30可能死亡 |

---

## 🎯 卡牌品质系统

### 品质级别
- **标准 (standard)** - 默认状态，无标记
- **升级+ (upgraded)** - 名称后加"+"，效果提升20-30%

### 升级规则
1. **每张卡只能升级一次**
2. **升级后名称加"+"** (如"进食指令 → 进食指令+")
3. **消耗数值不变**，只提升正面效果
4. **精神类卡牌不可升级**（幻想、记忆回放、机械的碰撞等）

### 可升级卡牌对应关系
| 品级 | 可升级卡牌类型 |
|------|----------------|
| 🟢普通 | 基础指令 |
| 🔵加密 | 基础+维护+应急 |
| 🟣机密 | 全部卡牌 |

---

## 🔢 数值平衡参考

### 每日衰减基准
- **饱食度：** -12/天
- **水分：** -18/天
- **精神状态：** 0/天（事件驱动）
- **体力：** 0/天（行为驱动，健康时回满）

### 卡牌效果设计原则
1. **基础牌 ≈ 1.5天需求**（饮水指令+30覆盖-18/天）
2. **维护牌 ≈ 投资回报**（今天付出，明天收益）
3. **应急牌 ≈ 2天需求**（紧急补水+45）
4. **特殊牌 ≈ 高风险高回报**

### 体力消耗参考
- **轻度：** 2-5 (高压氧气、幻想)
- **中度：** 5-10 (机械指压、清洁程序)
- **重度：** 10-15 (急救协议)
- **极重：** 30+ (机械的碰撞)

---

## 📝 开发实现建议

### 数据结构示例 (JSON)
```json
{
  "id": 1,
  "name": "进食指令",
  "type": "basic",
  "color": "#78e08f",
  "description": "[指令] 启动进食程序。张嘴。咀嚼。吞咽。",
  "effects": {
    "food": 25,
    "stamina": 5
  },
  "costs": {
    "stamina": 3
  },
  "quality": "standard"
}
```

### TypeScript 类型定义
```typescript
type CardType = "basic" | "maintenance" | "emergency" | "special";
type CardQuality = "standard" | "upgraded";

interface Card {
  id: number;
  name: string;
  type: CardType;
  color: string;
  description: string;
  quality: CardQuality;
  
  effects: {
    food?: number;
    water?: number;
    mood?: number;
    stamina?: number;
    health?: number;
    buffs?: {
      nextDayBasicBuff?: number;
      memorySlots?: number;
    };
    clears?: {
      moodDebuffs?: boolean;
      physicalDebuffs?: string[];
    };
  };
  
  costs: {
    food?: number;
    water?: number;
    mood?: number;
    stamina?: number;
    special?: {
      skipOtherActions?: boolean;
      discardAllHand?: boolean;
      endTurn?: boolean;
      nextDayPenalty?: {
        memorySlots?: number;
        stamina?: number;
      };
    };
  };
  
  conditions?: {
    triggers?: {
      moodDebuffActive?: boolean;
      moodLow?: number;
      healthLow?: number;
      waterZero?: boolean;
    };
    chances?: {
      memoryFragment?: number;
      emergencyCard?: number;
    };
  };
}
```

### 实现优先级
1. **M1阶段：** 基础数据结构 + 20张卡牌数据
2. **M1阶段：** 简单的效果应用系统
3. **M2阶段：** 条件效果和概率系统
4. **M2阶段：** 品质升级系统
5. **M3阶段：** 完整的特殊效果处理

---

## 🧩 相关设计文档

- **[AK-card-table-v2.md](file:///C:/Users/xurui01/.openclaw/workspace/memory/X-future/AK-card-table-v2.md)** - 完整卡牌设计（含描述和设计意图）
- **[AK-card-quality-v1.md](file:///C:/Users/xurui01/.openclaw/workspace/memory/X-future/AK-card-quality-v1.md)** - 品质分级系统
- **[AK-deck-rules-v1.md](file:///C:/Users/xurui01/.openclaw/workspace/memory/X-future/AK-deck-rules-v1.md)** - 牌库管理规则
- **[AK-daily-reward-v3.md](file:///C:/Users/xurui01/.openclaw/workspace/memory/X-future/AK-daily-reward-v3.md)** - 奖励系统（影响卡牌获取）

---

*文档维护：OpenClaw AI 助手*  
*创建时间：2026-04-01*  