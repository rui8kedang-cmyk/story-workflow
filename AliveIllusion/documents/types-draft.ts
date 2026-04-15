// Alive Illusion (AI) - TypeScript 类型定义草案
// 版本: v1.0
// 基于 AK-card-table-v2.md, AK-health-formula.md, AK-day-night-v1.md 等设计文档
// 创建: 2026-04-01

// ==================== 核心枚举 ====================

/** 卡牌类型 */
export enum CardType {
  BASIC = "basic",        // 🟢 基础指令
  MAINTENANCE = "maintenance", // 🔵 维护指令
  EMERGENCY = "emergency",     // 🔴 应急指令
  SPECIAL = "special"          // 🟣 特殊指令
}

/** 卡牌品质 */
export enum CardQuality {
  STANDARD = "standard",  // 标准
  UPGRADED = "upgraded"   // 升级+
}

/** 四维数值类型 */
export enum StatType {
  FOOD = "food",          // 饱食度
  WATER = "water",        // 水分
  MOOD = "mood",          // 精神状态
  STAMINA = "stamina"     // 体力
}

/** Debuff 类型 */
export enum DebuffType {
  // 精神类 debuff (D系列)
  D1_HUNGER_ANXIETY = "d1",    // D1 饥饿焦虑
  D2_DEHYDRATION_IRRITATION = "d2", // D2 脱水烦躁
  D3_FATIGUE_DEPRESSION = "d3",    // D3 疲劳抑郁
  D4_DISEASE_PAIN = "d4",          // D4 疾病痛苦
  
  // 体力类 debuff (E系列)
  E1_MILD_FATIGUE = "e1",      // E1 轻度疲劳
  E2_MINOR_INJURY = "e2",      // E2 轻伤
  E3_SERIOUS_INJURY = "e3",    // E3 重伤
  // ... 其他E系列
}

/** 游戏阶段 */
export enum GamePhase {
  MORNING = "morning",    // 早晨：数值衰减
  DAYTIME = "daytime",    // 白天：事件触发
  ACTION = "action",      // 行动：摸牌出牌
  EVENING = "evening",    // 晚间：事件+弃牌
  NIGHT = "night",        // 夜晚：体力回满
  NEXT_DAY = "nextDay"    // 次日：天数推进
}

// ==================== 核心接口 ====================

/** 四维数值对象 */
export interface Stats {
  food: number;       // 饱食度 (0-100)
  water: number;      // 水分 (0-100)
  mood: number;       // 精神状态 (0-100)
  stamina: number;    // 体力 (0-100)
}

/** 健康度计算结果 */
export interface HealthStatus {
  value: number;               // 健康度 (0-100)
  isLow: boolean;              // 是否低于50
  lowestStat: StatType | null; // 最低的数值类型
  warning: string | null;      // 警告信息
}

/** Debuff 实例 */
export interface Debuff {
  type: DebuffType;
  name: string;
  description: string;
  dailyEffect: number;         // 每日效果值（负值）
  duration: number;            // 剩余天数
  statAffected?: StatType;     // 影响的数值类型
}

/** 卡牌效果 */
export interface CardEffects {
  // 直接数值变化
  food?: number;
  water?: number;
  mood?: number;
  stamina?: number;
  health?: number;  // 直接健康度变化（仅急救协议）
  
  // 特殊效果
  buffs?: {
    nextDayBasicBuff?: number;  // 下一天基础牌效果加成
    memorySlots?: number;       // 内存增加
    specialFlags?: string[];    // 特殊标记
  };
  
  // 清除效果
  clears?: {
    moodDebuffs?: boolean;      // 清除所有精神debuff
    physicalDebuffs?: string[]; // 清除特定体力debuff
    all?: boolean;              // 清除所有buff/debuff
  };
}

/** 卡牌消耗 */
export interface CardCosts {
  // 基本消耗
  food?: number;
  water?: number;
  mood?: number;
  stamina?: number;
  
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

/** 触发条件 */
export interface TriggerConditions {
  moodDebuffActive?: boolean;   // 当有精神debuff时
  moodLow?: number;             // 精神状态≤某个值
  healthLow?: number;           // 健康度<某个值
  waterZero?: boolean;          // 水分=0时
}

/** 概率效果 */
export interface ChanceEffects {
  memoryFragment?: number;      // 获得记忆碎片概率 (0-1)
  emergencyCard?: number;       // 获得应急牌概率 (0-1)
}

/** 卡牌定义 */
export interface CardDefinition {
  id: number;                   // 1-20
  name: string;                 // 卡牌名称
  type: CardType;
  color: string;                // 边框颜色
  description: string;          // AI系统描述
  quality: CardQuality;
  
  effects: CardEffects;
  costs: CardCosts;
  
  conditions?: {
    triggers?: TriggerConditions;
    chances?: ChanceEffects;
  };
  
  // 升级版效果（如果存在）
  upgradedEffects?: CardEffects;
}

/** 游戏中的卡牌实例 */
export interface CardInstance {
  definition: CardDefinition;
  instanceId: string;           // 唯一实例ID
  isUpgraded: boolean;          // 是否已升级
  isUsed: boolean;              // 是否已使用
}

// ==================== 游戏状态 ====================

/** 游戏状态 */
export interface GameState {
  // 基本状态
  day: number;                  // 当前天数
  phase: GamePhase;             // 当前阶段
  isAlive: boolean;             // 是否存活
  deathReason?: string;         // 死亡原因
  
  // 数值状态
  stats: Stats;
  health: HealthStatus;
  
  // 卡牌状态
  deck: CardInstance[];         // 牌库
  hand: CardInstance[];         // 手牌
  discardPile: CardInstance[];  // 弃牌堆
  
  // 系统状态
  memorySlots: number;          // 内存（每日摸牌数，默认4）
  actionPoints: number;         // 算力（每日出牌数，默认3）
  cardsToKeep: number;          // 回合保留数（默认1）
  
  // 状态效果
  debuffs: Debuff[];
  buffs: {
    nextDayBasicBuff?: number;  // 下一天基础牌加成
    // 其他buff...
  };
  
  // 奖励系统
  rewardAvailable: boolean;     // 是否有每日奖励
  rewardTier?: "common" | "encrypted" | "confidential" | "core"; // 奖励品级
  
  // 事件系统
  dailyEvent?: DailyEvent;      // 当日事件
  eveningEvent?: EveningEvent;  // 晚间事件
}

/** 每日事件 */
export interface DailyEvent {
  id: string;
  title: string;
  description: string;
  effects: CardEffects;         // 事件效果
  pool: "easy" | "normal" | "hard" | "hell"; // 事件池
}

/** 晚间事件 */
export interface EveningEvent {
  id: string;
  title: string;
  description: string;
  isPositive: boolean;          // 是否正面事件
  effects: CardEffects;
}

// ==================== 游戏配置 ====================

/** 数值衰减配置 */
export interface DecayConfig {
  food: number;    // 饱食度每日衰减 (-12)
  water: number;   // 水分每日衰减 (-18)
  mood: number;    // 精神状态每日衰减 (0)
  stamina: number; // 体力每日衰减 (0)
}

/** 游戏规则配置 */
export interface GameRules {
  // 牌库规则
  initialDeckSize: number;      // 初始牌库大小 (12)
  maxHandSize: number;          // 手牌上限 (9)
  memorySlots: number;          // 每日内存 (4)
  actionPoints: number;         // 每日算力 (3)
  cardsToKeep: number;          // 回合保留数 (1)
  
  // 数值规则
  decay: DecayConfig;
  healthFormula: {
    foodWeight: number;         // 饱食度权重
    waterWeight: number;        // 水分权重
    moodWeight: number;         // 精神状态权重
    staminaWeight: number;      // 体力权重
    minValuePenalty: number;    // 最低值惩罚
  };
  
  // 事件规则
  eveningEventChance: number;   // 晚间事件触发概率 (0.5)
  positiveEventRatio: number;   // 正面事件比例 (0.6)
  eventAmplification: {
    hardPhase: number;          // 困难阶段放大 (1.3, day 15-30)
    hellPhase: number;          // 地狱阶段放大 (1.5, day 31+)
  };
  
  // 奖励系统
  rewardProbabilities: {
    common: number;      // 🟢普通 (0.5)
    encrypted: number;   // 🔵加密 (0.28)
    confidential: number; // 🟣机密 (0.15)
    core: number;        // 🟡核心 (0.07)
  };
}

// ==================== 函数类型 ====================

/** 健康度计算函数 */
export type HealthCalculator = (stats: Stats) => HealthStatus;

/** 卡牌效果应用函数 */
export type CardEffectApplier = (
  card: CardInstance,
  state: GameState
) => GameState;

/** 事件触发函数 */
export type EventTrigger = (state: GameState) => {
  newState: GameState;
  event?: DailyEvent | EveningEvent;
};

// ==================== 工具类型 ====================

/** 卡牌数据集合 */
export type CardLibrary = Record<number, CardDefinition>;

/** 游戏存档 */
export interface GameSave {
  version: string;
  timestamp: number;
  state: GameState;
  rules: GameRules;
  seed?: number;  // 随机种子
}

// ==================== 默认配置 ====================

/** 默认游戏规则 (v7终版) */
export const DEFAULT_RULES: GameRules = {
  // 牌库规则
  initialDeckSize: 12,
  maxHandSize: 9,
  memorySlots: 4,
  actionPoints: 3,
  cardsToKeep: 1,
  
  // 数值衰减
  decay: {
    food: -12,
    water: -18,
    mood: 0,
    stamina: 0
  },
  
  // 健康度公式 (v1.1)
  healthFormula: {
    foodWeight: 0.25,
    waterWeight: 0.35,
    moodWeight: 0.25,
    staminaWeight: 0.15,
    minValuePenalty: 0.5
  },
  
  // 事件规则
  eveningEventChance: 0.5,
  positiveEventRatio: 0.6,
  eventAmplification: {
    hardPhase: 1.3,  // day 15-30
    hellPhase: 1.5   // day 31+
  },
  
  // 奖励系统 (v3.1)
  rewardProbabilities: {
    common: 0.5,      // 🟢普通 50%
    encrypted: 0.28,  // 🔵加密 28%
    confidential: 0.15, // 🟣机密 15%
    core: 0.07        // 🟡核心 7%
  }
};

/** 默认初始状态 */
export const INITIAL_STATE: Partial<GameState> = {
  day: 1,
  phase: GamePhase.MORNING,
  isAlive: true,
  stats: {
    food: 100,
    water: 100,
    mood: 100,
    stamina: 100
  },
  memorySlots: 4,
  actionPoints: 3,
  cardsToKeep: 1,
  debuffs: [],
  buffs: {},
  rewardAvailable: false
};

// ==================== 导出 ====================

export default {
  CardType,
  CardQuality,
  StatType,
  DebuffType,
  GamePhase,
  
  DEFAULT_RULES,
  INITIAL_STATE
};