"""AK v6b final verification run — decay -15/-20, debuffs -10/-15/-8/-12"""
import random, statistics, sys
sys.path.insert(0, r"C:\Users\xurui01\.openclaw\workspace\memory\X-future")
from ak_simulation_v6b_reward import GameV6B, run_v6b, run_v5c_baseline

N = 3000

# Verify decay
g = GameV6B()
of, ow = g.food, g.water
g.daily_decay()
print(f"Decay: food -{of - g.food:.0f}/day, water -{ow - g.water:.0f}/day")
print(f"Debuffs: D1=-10, D2=-15, D3=-8, D4=-12 (total if all: -45/day)")
print()

random.seed(42)
print("Running v5c baseline...")
r5c, c5c = run_v5c_baseline(N)

random.seed(42)
print("Running v6b...")
r6b, c6b, e6b, m6b, s6b, rw6b, p6b, u6b = run_v6b(N)

a5 = statistics.mean(r5c); a6 = statistics.mean(r6b)
m5 = statistics.median(r5c); m6 = statistics.median(r6b)

print()
print("=" * 70)
print("  AK v6b Final — Decay -15/-20, Debuffs -10/-15/-8/-12")
print("  Rewards: daily, green50%/blue28%/purple15%/gold7%")
print("  Emergency: G+20 single/B+40 single/P=food+water full/Gold=all full")
print("=" * 70)

rows = [
    ("Avg days",    f"{a5:.1f}", f"{a6:.1f}", f"{a6-a5:+.1f}"),
    ("Median",      f"{m5:.1f}", f"{m6:.1f}", f"{m6-m5:+.1f}"),
    ("Stdev",       f"{statistics.stdev(r5c):.1f}", f"{statistics.stdev(r6b):.1f}", ""),
    (">7d survive", f"{sum(1 for r in r5c if r>7)/N*100:.1f}%", f"{sum(1 for r in r6b if r>7)/N*100:.1f}%", ""),
    (">14d survive",f"{sum(1 for r in r5c if r>14)/N*100:.1f}%",f"{sum(1 for r in r6b if r>14)/N*100:.1f}%",""),
    (">21d survive",f"{sum(1 for r in r5c if r>21)/N*100:.1f}%",f"{sum(1 for r in r6b if r>21)/N*100:.1f}%",""),
    (">30d survive",f"{sum(1 for r in r5c if r>30)/N*100:.1f}%",f"{sum(1 for r in r6b if r>30)/N*100:.1f}%",""),
]
print(f"  {'Metric':<35} {'v5c':>12} {'v6b':>12} {'Delta':>10}")
print(f"  {'-'*69}")
for label, v1, v2, d in rows:
    print(f"  {label:<35} {v1:>12} {v2:>12} {d:>10}")

print(f"\n  Death Causes:")
print(f"    {'Cause':<12} {'v5c':>12} {'v6b':>12}")
for cause in sorted(c6b.keys(), key=lambda c: -c6b[c]):
    print(f"    {cause:<12} {c5c.get(cause,0)/N*100:>11.1f}% {c6b[cause]/N*100:>11.1f}%")

print(f"\n  Distribution:")
for lo, hi in [(1,3),(4,7),(8,14),(15,21),(22,30),(31,50),(51,100),(101,200)]:
    cnt = sum(1 for r in r6b if lo <= r <= hi)
    bar = chr(9608) * (cnt * 40 // N)
    print(f"    {lo:>3}-{hi:<3}d: {cnt:>4} ({cnt/N*100:>5.1f}%) {bar}")

print(f"\n  Rewards (avg/run):")
labels = {"card_upgrade":"Card upgrades","spirit_card":"Spirit cards",
          "buff":"Short buffs","emergency":"Emergency heals","permanent":"Permanents"}
for k, v in rw6b.items():
    print(f"    {labels[k]:<25} {v/N:>8.2f}")
print(f"    {'Avg upgrade levels':<25} {statistics.mean(u6b):>8.2f}")
print(f"    {'Avg permanents':<25} {statistics.mean(p6b):>8.2f}")
print(f"    {'Avg spirit cards':<25} {s6b/N:>8.2f}")

if 16 <= a6 <= 22:
    print(f"\n  >>> PASS: avg {a6:.1f} days (target 16-22)")
elif a6 > 22:
    print(f"\n  >>> TOO STRONG: avg {a6:.1f} days")
else:
    print(f"\n  >>> TOO WEAK: avg {a6:.1f} days")
print("=" * 70)
