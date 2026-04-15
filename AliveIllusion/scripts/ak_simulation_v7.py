# AK Simulation v7
# Full system: deck cycling, draw 3 play 2, retain 1, night events, rewards v3.1
import random, statistics, sys, copy
sys.path.insert(0, r'C:\Users\xurui01\.openclaw\workspace\memory\X-future')
from ak_simulation_v5c import CARDS_V2, CARD_POOLS_V2, PHYSICAL_ACTION_CARDS_V2
from ak_simulation_v5b import NORMAL_EVENTS_V5B, HARD_EVENTS_V5B, HELL_EVENTS_V5B, SIMPLE_EVENTS
