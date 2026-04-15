"""
AK Simulation v6b - Daily Reward v3.1 (balanced)
Changes:
- Rewards daily, but lower high-rarity odds (green 50%, purple 15%, gold 7%)
- Emergency heals tiered:
  green: +20 single | blue: +40 single | purple: food+water full | gold: all full
- Buffs don't stack (same type replaces)
- Spirit cards: cap at 1 copy each (no duplicates in deck)
- Mood debuffs strengthened: D1 -10, D2 -15, D3 -8, D4 -12 (was -8,-12,-6,-10)
- Post-day-14 events amplified: hard 1.3x, hell 1.5x negative effects
"""
import random
import statistics
import sys

sys.path.insert(0, r"C:\Users\xurui01\.openclaw\workspace\memory\X-future")
from ak_simulation_v5c import (
    GameV5C, CARDS_V2, CARD_POOLS_V2, PHYSICAL_ACTION_CARDS_V2,
)
from ak_simulation_v6_reward import (
    UPGRADE_TABLE, UPGRADE_ACCESS,
    SPIRIT_CARDS_BLUE, SPIRIT_CARDS_PURPLE,
    BUFFS_GREEN, BUFFS_BLUE, BUFFS_PURPLE, PERMANENTS,
    run_v5c_baseline,
)

# Adjusted rarity: lower purple/gold
RARITY_WEIGHTS_V2 = {
    "green":  0.50,   # was 0.45
    "blue":   0.28,   # unchanged
    "purple": 0.15,   # was 0.18
    "gold":   0.07,   # was 0.09
}

REWARD_TYPE_WEIGHTS = {
    "green":  (40, 35, 25),
    "blue":   (50, 25, 25),
    "purple": (50, 25, 25),
    "gold":   (100, 0, 0),
}


def roll_rarity():
    r = random.random()
    cumul = 0
    for rarity, w in RARITY_WEIGHTS_V2.items():
        cumul += w
        if r < cumul:
            return rarity
    return "green"


def roll_reward_type(rarity):
    if rarity == "gold":
        return "permanent"
    weights = REWARD_TYPE_WEIGHTS[rarity]
    r = random.randint(1, sum(weights))
    if r <= weights[0]:
        return "card"
    elif r <= weights[0] + weights[1]:
        return "buff"
    else:
        return "emergency"


class GameV6B(GameV5C):
    def __init__(self):
        super().__init__()
        self.card_levels = {name: 1 for name in UPGRADE_TABLE}
        self.spirit_cards_obtained = set()  # set, no duplicates
        self.active_buffs = []
        self.permanents_obtained = set()
        self.perm_draw_bonus = 0
        self.perm_play_bonus = 0
        self.perm_hand_limit_bonus = 0
        self.perm_energy_cap_bonus = 0
        self.rewards_given = {"card_upgrade": 0, "spirit_card": 0,
                              "buff": 0, "emergency": 0, "permanent": 0}
        self.spirit_card_count = 0

    # --- Strengthened mood debuffs ---
    def check_mood_debuffs(self):
        """Override: increase mood debuff damage"""
        # D1: Hunger anxiety: food <= 20 for 2 days -> mood -10/day (was -8)
        if self.food <= 20:
            self.food_low_days += 1
        else:
            self.food_low_days = 0
        if self.food_low_days >= 2 and not self.hunger_anxiety:
            self.hunger_anxiety = True
        if self.food >= 35:
            self.hunger_anxiety = False
            self.food_low_days = 0

        # D2: Dehydration irritation: water <= 15 for 1 day -> mood -15/day (was -12)
        if self.water <= 15:
            self.water_low_days_mood += 1
        else:
            self.water_low_days_mood = 0
        if self.water_low_days_mood >= 1 and not self.dehydration_irritation:
            self.dehydration_irritation = True
        if self.water >= 30:
            self.dehydration_irritation = False
            self.water_low_days_mood = 0

        # D3: Fatigue depression: energy <= 15 for 2 days -> mood -8/day (was -6)
        if self.energy <= 15:
            self.energy_low_days += 1
        else:
            self.energy_low_days = 0
        if self.energy_low_days >= 2 and not self.fatigue_depression:
            self.fatigue_depression = True
        if self.energy >= 30:
            self.fatigue_depression = False
            self.energy_low_days = 0

        # D4: Illness suffering: health <= 40 -> mood -12/day (was -10)
        if self.health <= 40 and not self.illness_suffering:
            self.illness_suffering = True
        if self.health >= 50:
            self.illness_suffering = False

        # Apply strengthened mood debuffs
        if self.hunger_anxiety: self.mood -= 10      # was -8
        if self.dehydration_irritation: self.mood -= 15  # was -12
        if self.fatigue_depression: self.mood -= 8    # was -6
        if self.illness_suffering: self.mood -= 12    # was -10

        # Mood DoT from events
        if self.mood_dot_turns > 0:
            self.mood += self.mood_dot_val
            self.mood_dot_turns -= 1

        self.clamp()

    # --- Post-day-14 event amplification ---
    def apply_event(self, evt):
        """Override: amplify negative event effects after day 14"""
        if self.day > 14:
            # Determine multiplier: hard phase 1.3x, hell phase 1.5x
            if self.day <= 30:
                mult = 1.3
            else:
                mult = 1.5

            # Create amplified copy for negative values only
            amp_evt = dict(evt)
            for stat in ["food", "water", "mood", "energy", "health"]:
                val = amp_evt.get(stat, 0)
                if val < 0:
                    amp_evt[stat] = int(val * mult)
            # Amplify mood DoT
            if "mood_dot" in amp_evt and amp_evt["mood_dot"] < 0:
                amp_evt["mood_dot"] = int(amp_evt["mood_dot"] * mult)
            # Amplify water extra decay
            if "water_extra_decay" in amp_evt and amp_evt["water_extra_decay"] < 0:
                amp_evt["water_extra_decay"] = int(amp_evt["water_extra_decay"] * mult)
            # Amplify energy extra decay
            if "energy_extra_decay" in amp_evt and amp_evt["energy_extra_decay"] < 0:
                amp_evt["energy_extra_decay"] = int(amp_evt["energy_extra_decay"] * mult)

            super().apply_event(amp_evt)
        else:
            super().apply_event(evt)

    # --- Draw / play with permanent bonuses ---
    def draw_cards(self):
        draw = 3 + self.draw_bonus + self.draw_penalty_val + self.perm_draw_bonus
        self.draw_bonus = 0
        for b in self.active_buffs:
            if b[1] == "draw_bonus":
                draw += int(b[2])
            elif b[1] == "draw_play_bonus":
                draw += int(b[2])
        if self.overclock_day > 0:
            if self.day == self.overclock_day + 1: draw += 2
            elif self.day == self.overclock_day + 2: draw -= 1
        draw = max(1, draw)
        all_c = list(CARDS_V2.keys())
        for _ in range(draw):
            hand_limit = 5 + self.perm_hand_limit_bonus
            if len(self.hand) < hand_limit:
                self.hand.append(random.choice(all_c))
        hand_limit = 5 + self.perm_hand_limit_bonus
        while len(self.hand) > hand_limit:
            self.discard_worst()

    def get_play_limit(self):
        limit = 3 + self.perm_play_bonus
        for b in self.active_buffs:
            if b[1] == "play_bonus":
                limit += int(b[2])
            elif b[1] == "draw_play_bonus":
                limit += int(b[2])
        if self.play_limit_turns > 0:
            limit = min(limit, self.play_limit_val)
        return limit

    def get_energy_cap(self):
        return 100 + self.perm_energy_cap_bonus + getattr(self, 'energy_cap_event_mod', 0)

    # --- Play card with upgrades ---
    def play_card(self, name):
        if name in UPGRADE_TABLE and self.card_levels.get(name, 1) > 1:
            orig_card = CARDS_V2.get(name)
            if orig_card:
                saved = {}
                lvl = self.card_levels[name]
                for stat, values in UPGRADE_TABLE[name]:
                    if lvl <= len(values):
                        saved[stat] = orig_card.get(stat)
                        orig_card[stat] = values[lvl - 1]
                result = super().play_card(name)
                for stat, val in saved.items():
                    if val is not None:
                        orig_card[stat] = val
                    elif stat in orig_card:
                        del orig_card[stat]
                return result
        return super().play_card(name)

    # --- Buff management ---
    def apply_buff_effects_daily(self):
        for b in self.active_buffs:
            if b[1] == "mood_regen":
                self.mood += int(b[2])

    def tick_buffs(self):
        self.active_buffs = [(n, s, v, d-1) for n, s, v, d in self.active_buffs if d > 1]

    def has_buff(self, stat_name):
        return any(b[1] == stat_name for b in self.active_buffs)

    def add_buff(self, buff_tuple, duration):
        """Add buff, replacing same-type (no stacking)"""
        name, stat, value, _ = buff_tuple
        self.active_buffs = [b for b in self.active_buffs if b[1] != stat]
        self.active_buffs.append((name, stat, value, duration))

    # --- Daily reward ---
    def apply_daily_reward(self):
        rewards = []
        for _ in range(3):
            rarity = roll_rarity()
            rtype = roll_reward_type(rarity)
            rewards.append((rarity, rtype))

        # Milestone
        if self.day % 5 == 0:
            md = self.day
            if md <= 5:     rewards.append(("green", roll_reward_type("green")))
            elif md <= 10:  rewards.append(("blue", roll_reward_type("blue")))
            elif md <= 15:  rewards.append(("purple", roll_reward_type("purple")))
            elif md <= 20:  rewards.append(("gold", "permanent"))
            else:           rewards.append(("purple", roll_reward_type("purple")))

        best_score = -999
        best_idx = 0
        for i, (rarity, rtype) in enumerate(rewards):
            score = self.score_reward(rarity, rtype)
            if score > best_score:
                best_score = score
                best_idx = i

        self.apply_reward(*rewards[best_idx])

        if self.day % 5 == 0 and len(rewards) > 3 and best_idx != len(rewards) - 1:
            self.apply_reward(*rewards[-1])

    def score_reward(self, rarity, rtype):
        score = {"green": 0, "blue": 10, "purple": 25, "gold": 50}.get(rarity, 0)
        if rtype == "permanent":
            avail = [p for p in PERMANENTS if p[0] not in self.permanents_obtained]
            return 100 if avail else -10
        if rtype == "emergency":
            if self.food < 25 or self.water < 25 or self.mood < 25:
                score += 50
            else:
                score += 5
        if rtype == "card":
            score += 20
        if rtype == "buff":
            score += 15 if rarity == "purple" else 8
        return score

    def apply_reward(self, rarity, rtype):
        if rtype == "permanent":
            self.apply_permanent()
        elif rtype == "card":
            self.apply_card_reward(rarity)
        elif rtype == "buff":
            self.apply_buff_reward(rarity)
        elif rtype == "emergency":
            self.apply_emergency(rarity)

    def apply_card_reward(self, rarity):
        if rarity == "blue":
            if random.random() < 0.5:
                self.do_card_upgrade(rarity)
            else:
                self.do_spirit_card(SPIRIT_CARDS_BLUE)
        elif rarity == "purple":
            if random.random() < 0.5:
                self.do_card_upgrade(rarity)
            else:
                self.do_spirit_card(SPIRIT_CARDS_PURPLE)
        else:
            self.do_card_upgrade(rarity)

    def do_card_upgrade(self, rarity):
        accessible = UPGRADE_ACCESS.get(rarity, [])
        upgradeable = [c for c in accessible if self.card_levels.get(c, 1) < 4]
        if upgradeable:
            card = random.choice(upgradeable)
            self.card_levels[card] = min(4, self.card_levels[card] + 1)
            self.rewards_given["card_upgrade"] += 1

    def do_spirit_card(self, pool):
        available = [c for c in pool if c not in self.spirit_cards_obtained]
        if not available:
            return  # all obtained, wasted
        card = random.choice(available)
        self.spirit_cards_obtained.add(card)
        self.rewards_given["spirit_card"] += 1
        self.spirit_card_count += 1

    def apply_buff_reward(self, rarity):
        if rarity == "purple":
            pool = BUFFS_GREEN + BUFFS_BLUE + BUFFS_PURPLE
            chosen = random.choice(pool)
            self.add_buff(chosen, 3)
        elif rarity == "blue":
            pool = BUFFS_GREEN + BUFFS_BLUE
            chosen = random.choice(pool)
            self.add_buff(chosen, 1)
        else:
            pool = BUFFS_GREEN
            chosen = random.choice(pool)
            self.add_buff(chosen, 1)
        self.rewards_given["buff"] += 1

    def apply_emergency(self, rarity):
        if rarity == "green":
            # +20 single (food or water, whichever lower)
            if self.food < self.water:
                self.food = min(100, self.food + 20)
            else:
                self.water = min(100, self.water + 20)
        elif rarity == "blue":
            # +40 single (food or water, whichever lower)
            if self.food < self.water:
                self.food = min(100, self.food + 40)
            else:
                self.water = min(100, self.water + 40)
        elif rarity == "purple":
            # Food + water refill to 100
            self.food = 100
            self.water = 100
        elif rarity == "gold":
            # All four stats refill
            self.food = 100
            self.water = 100
            self.mood = 100
            cap = self.get_energy_cap()
            self.energy = min(cap, 100)
        self.rewards_given["emergency"] += 1

    def apply_permanent(self):
        available = [p for p in PERMANENTS if p[0] not in self.permanents_obtained]
        if not available:
            self.apply_reward("purple", roll_reward_type("purple"))
            return
        chosen = available[0]
        self.permanents_obtained.add(chosen[0])
        if chosen[1] == "draw_permanent":      self.perm_draw_bonus += chosen[2]
        elif chosen[1] == "play_permanent":    self.perm_play_bonus += chosen[2]
        elif chosen[1] == "hand_limit_plus":   self.perm_hand_limit_bonus += chosen[2]
        elif chosen[1] == "energy_cap_plus":   self.perm_energy_cap_bonus += chosen[2]
        self.rewards_given["permanent"] += 1

    # --- sim_day override ---
    def sim_day(self):
        if not self.alive:
            return
        self.day += 1
        self.apply_buff_effects_daily()
        # Undo day increment since parent will do it
        self.day -= 1
        super().sim_day()
        if self.alive:
            self.apply_daily_reward()
            self.tick_buffs()


def run_v6b(n=3000):
    results = []
    death_causes = {"water": 0, "food": 0, "mood": 0, "health": 0, "other": 0}
    energy_at_death = []
    mood_at_death = []
    spirit_cards_total = 0
    reward_totals = {"card_upgrade": 0, "spirit_card": 0,
                     "buff": 0, "emergency": 0, "permanent": 0}
    permanents_obtained = []
    upgrade_levels = []

    for _ in range(n):
        g = GameV6B()
        while g.alive and g.day < 200:
            g.sim_day()
        results.append(g.day)
        energy_at_death.append(g.energy)
        mood_at_death.append(g.mood)
        spirit_cards_total += g.spirit_card_count
        for k in reward_totals:
            reward_totals[k] += g.rewards_given[k]
        permanents_obtained.append(len(g.permanents_obtained))
        upgrade_levels.append(sum(v - 1 for v in g.card_levels.values()))

        if g.mood <= 0:       death_causes["mood"] += 1
        elif g.water <= 0:    death_causes["water"] += 1
        elif g.food <= 0:     death_causes["food"] += 1
        elif g.health <= 0:   death_causes["health"] += 1
        else:                 death_causes["other"] += 1

    return (results, death_causes, energy_at_death, mood_at_death,
            spirit_cards_total, reward_totals, permanents_obtained, upgrade_levels)


if __name__ == "__main__":
    N = 3000

    random.seed(42)
    print("Running v5c baseline...")
    r5c, causes5c = run_v5c_baseline(N)

    random.seed(42)
    print("Running v6b (reward v3.1 balanced)...")
    (r6b, causes6b, energy6b, mood6b, spirit6b,
     rewards6b, perms6b, upgrades6b) = run_v6b(N)

    avg5c = statistics.mean(r5c); avg6b = statistics.mean(r6b)
    med5c = statistics.median(r5c); med6b = statistics.median(r6b)

    print()
    print("=" * 70)
    print("  AK v6b Daily Reward v3.1 (Balanced)")
    print("  Nerfs: emergency=fixed heal, no buff stacking, spirit cap=1 each")
    print("=" * 70)
    print(f"  {'Metric':<35} {'v5c':>12} {'v6b':>12} {'Delta':>10}")
    print(f"  {'-'*69}")
    print(f"  {'Avg days':<35} {avg5c:>12.1f} {avg6b:>12.1f} {avg6b-avg5c:>+10.1f}")
    print(f"  {'Median':<35} {med5c:>12.1f} {med6b:>12.1f} {med6b-med5c:>+10.1f}")
    print(f"  {'Stdev':<35} {statistics.stdev(r5c):>12.1f} {statistics.stdev(r6b):>12.1f}")
    print(f"  {'>7d survive':<35} {sum(1 for r in r5c if r>7)/N*100:>11.1f}% {sum(1 for r in r6b if r>7)/N*100:>11.1f}%")
    print(f"  {'>14d survive':<35} {sum(1 for r in r5c if r>14)/N*100:>11.1f}% {sum(1 for r in r6b if r>14)/N*100:>11.1f}%")
    print(f"  {'>21d survive':<35} {sum(1 for r in r5c if r>21)/N*100:>11.1f}% {sum(1 for r in r6b if r>21)/N*100:>11.1f}%")
    print(f"  {'>30d survive':<35} {sum(1 for r in r5c if r>30)/N*100:>11.1f}% {sum(1 for r in r6b if r>30)/N*100:>11.1f}%")

    print(f"\n  Death Cause Comparison:")
    print(f"    {'Cause':<12} {'v5c':>12} {'v6b':>12}")
    for cause in sorted(causes6b.keys(), key=lambda c: -causes6b[c]):
        c5 = causes5c.get(cause, 0); c6 = causes6b.get(cause, 0)
        print(f"    {cause:<12} {c5/N*100:>11.1f}% {c6/N*100:>11.1f}%")

    print(f"\n  V6b Distribution:")
    for lo, hi in [(1,3),(4,7),(8,14),(15,21),(22,30),(31,50),(51,100),(101,200)]:
        cnt = sum(1 for r in r6b if lo <= r <= hi)
        bar = chr(9608) * (cnt * 40 // N)
        print(f"    {lo:>3}-{hi:<3}d: {cnt:>4} ({cnt/N*100:>5.1f}%) {bar}")

    print(f"\n  Reward Stats (avg/run):")
    for k, v in rewards6b.items():
        label = {"card_upgrade":"Card upgrades","spirit_card":"Spirit cards",
                 "buff":"Short buffs","emergency":"Emergency heals",
                 "permanent":"Permanents"}[k]
        print(f"    {label:<25} {v/N:>8.2f}")
    print(f"    {'Avg upgrade levels':<25} {statistics.mean(upgrades6b):>8.2f}")
    print(f"    {'Avg permanents':<25} {statistics.mean(perms6b):>8.2f}")

    target_lo, target_hi = 16, 22
    print(f"\n  Target: {target_lo}-{target_hi} days avg")
    if target_lo <= avg6b <= target_hi:
        print(f"    PASS - avg {avg6b:.1f} days")
    elif avg6b > target_hi:
        print(f"    TOO STRONG - avg {avg6b:.1f} days (+{avg6b-avg5c:.1f})")
    else:
        print(f"    WEAK - avg {avg6b:.1f} days (+{avg6b-avg5c:.1f})")
    print("=" * 70)
