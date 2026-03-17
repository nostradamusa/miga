import re
import random

QUIZ_FILE = r'c:\Users\Admin\My Drive (albanm1687@gmail.com)\Discord\MIGA TRADING\miga github\quiz2_mastery.html'

with open(QUIZ_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

css_injection = """
  /* ── LUXALGO INSPIRED CHART STYLES ── */
  .beautiful-candle-up { fill: #00ff88; stroke: #00ff88; filter: drop-shadow(0 0 2px rgba(0,255,136,0.3)); stroke-width: 1; opacity: 0.9; }
  .beautiful-candle-down { fill: #ff3366; stroke: #ff3366; filter: drop-shadow(0 0 2px rgba(255,51,102,0.3)); stroke-width: 1; opacity: 0.9; }
  .beautiful-wick { stroke: #8a9bb1; stroke-width: 1; opacity: 0.6; }
  .lux-bg { fill: #0d131a; rx: 5; }
  .lux-grid { stroke: #1a2433; stroke-width: 0.5; stroke-dasharray: 2,2; }
  .lux-zone-red { fill: rgba(255, 51, 102, 0.15); stroke: #ff3366; stroke-width: 0.8; }
  .lux-zone-green { fill: rgba(0, 255, 136, 0.15); stroke: #00ff88; stroke-width: 0.8; }
  .lux-zone-blue { fill: rgba(0, 150, 255, 0.15); stroke: #0096ff; stroke-width: 0.8; }
  .lux-zone-yellow { fill: rgba(201, 168, 76, 0.15); stroke: #c9a84c; stroke-width: 0.8; }
  .lux-line-red { stroke: #ff3366; stroke-width: 1; stroke-dasharray: 3,2; }
  .lux-line-green { stroke: #00ff88; stroke-width: 1; stroke-dasharray: 3,2; }
  .lux-line-white { stroke: #ffffff; stroke-width: 1; stroke-dasharray: 4,4; }
  .lux-text { font-family: 'Barlow', sans-serif; font-size: 6px; fill: #8a9bb1; }
  .lux-text-red { font-family: 'Barlow', sans-serif; font-size: 6px; fill: #ff3366; font-weight: bold; }
  .lux-text-green { font-family: 'Barlow', sans-serif; font-size: 6px; fill: #00ff88; font-weight: bold; }
  .lux-signal-bg-down { fill: rgba(255, 51, 102, 0.2); stroke: #ff3366; stroke-width: 0.8; rx: 2; }
  .lux-signal-bg-up { fill: rgba(0, 255, 136, 0.2); stroke: #00ff88; stroke-width: 0.8; rx: 2; }
  .lux-signal-arrow-down { fill: #ff3366; }
  .lux-signal-arrow-up { fill: #00ff88; }
  
  .chart-container { margin-top: 15px; border-radius: 8px; overflow: hidden; border: 1px solid #1a2433; background: #0d131a; padding: 10px; text-align: center; }
  .q-chart { width: 100%; height: auto; max-width: 600px; display: inline-block; }
"""
if "LUXALGO INSPIRED CHART STYLES" not in content:
    content = re.sub(r'/\* ── BEAUTIFUL CANDLES ── \*/.*?\n\s*\.q-chart\s*\{.*?\}', '', content, flags=re.DOTALL)
    content = content.replace("</style>", css_injection + "\n</style>")

def draw_candle(x, o, c, h, l, w=6):
    is_up = c <= o
    cls = "beautiful-candle-up" if is_up else "beautiful-candle-down"
    ytop = min(o, c)
    ybot = max(o, c)
    body_h = max(ybot - ytop, 1)
    return f'''
        <line x1="{x+w/2}" y1="{h}" x2="{x+w/2}" y2="{l}" class="beautiful-wick"/>
        <rect x="{x}" y="{ytop}" width="{w}" height="{body_h}" class="{cls}"/>
    '''

def draw_grid():
    grid = ""
    for y in range(20, 120, 20):
        grid += f'<line x1="0" y1="{y}" x2="300" y2="{y}" class="lux-grid"/>'
    return grid

def draw_seq(data, start_x, spacing=10, w=6):
    svg = ""
    for i, (o, c, h, l) in enumerate(data):
        svg += draw_candle(start_x + i*spacing, o, c, h, l, w)
    return svg

def generate_bg_candles(num=30, start_x=10, spacing=6, start_y=60, trend=0, vol=5, w=4):
    random.seed(43) # Seed
    svg = ""
    y = start_y
    data = []
    for _ in range(num):
        move = random.uniform(-vol, vol) + trend
        o = y
        c = y + move
        if c < 10: c = 10; move = c - o
        if c > 110: c = 110; move = c - o
        h = min(o, c) - random.uniform(1, vol)
        l = max(o, c) + random.uniform(1, vol)
        data.append((o, c, h, l))
        y = c
    return draw_seq(data, start_x, spacing, w), start_x + (num)*spacing, y

questions = [
    {
        "q": "What does the acronym AMD stand for in the Power of 3 concept?",
        "diff": "Medium",
        "options": [
            "Average, Moving, Direction.",
            "Accumulation, Manipulation, Distribution.",
            "Algorithmic Market Delivery.",
            "Asymmetric Market Distribution."
        ],
        "ans": 1,
        "exp_c": "Correct! AMD stands for Accumulation (building positions), Manipulation (false breakout to grab liquidity), and Distribution (the true directional move).",
        "exp_w": "Incorrect. AMD refers to Accumulation, Manipulation, and Distribution. It describes the daily cycle where Smart Money accumulates, manipulates retail traders, and distributes in the intended direction.",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        {generate_bg_candles(8, 10, 6, 60, 0, 4, 3)[0]}
        {draw_seq([
            (60, 65, 55, 70), (62, 58, 50, 68), (58, 62, 55, 65), (62, 60, 58, 66), # Range
            (60, 40, 35, 65), # Manipulation UP (Green)
            (40, 65, 30, 70), # Red
            (65, 90, 60, 95), # Red
            (90, 110, 85, 115), # Red Distribution
        ], 60, 20, 10)}
        {generate_bg_candles(12, 220, 6, 110, 0, 3, 3)[0]}
        <rect x="55" y="50" width="70" height="25" class="lux-zone-yellow"/>
        <text x="90" y="45" text-anchor="middle" class="lux-text" style="fill:#c9a84c;">ACCUMULATION</text>
        <circle cx="150" cy="35" r="8" fill="rgba(255,51,102,0.2)" stroke="#ff3366"/>
        <text x="150" y="20" text-anchor="middle" class="lux-text-red">MANIPULATION</text>
        <rect x="160" y="70" width="70" height="40" class="lux-zone-red"/>
        <text x="195" y="65" text-anchor="middle" class="lux-text-red">DISTRIBUTION</text>
      </svg>
        '''
    },
    {
        "q": "What defines a valid Breaker Block?",
        "diff": "Hard",
        "options": [
            "A structural point that breaks the current trend line.",
            "A sequence of three identically sized candles.",
            "An Order Block that was violated or broken, which now acts as support or resistance.",
            "The exact price where market makers break up large equity block trades."
        ],
        "ans": 2,
        "exp_c": "Correct! A Breaker Block is a failed Order Block. Once price breaks through it and invalidates it, it swaps roles and becomes a highly reliable support/resistance zone.",
        "exp_w": "Incorrect. A Breaker Block occurs when an established Order Block is broken by price displacement. It then flips its role, acting as strong support or resistance from the other side.",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        {generate_bg_candles(10, 10, 6, 40, -1, 3, 3)[0]}
        {draw_seq([
            (60, 40, 35, 65), # OB up candle (Green)
            (40, 60, 35, 65), # Red
            (60, 80, 55, 85), # Red (forms bearish OB)
            (80, 95, 75, 100),
            (95, 60, 55, 100), # Green price rips UP THROUGH the OB
            (60, 30, 25, 65), # Green Breakout
            (30, 50, 25, 55), # Red retest drops back down
            (50, 45, 40, 55), # Green touches OB
            (45, 20, 15, 50), # Green Shoots up!
            (20, 10, 5, 25),
        ], 70, 15, 8)}
        {generate_bg_candles(12, 220, 6, 10, 0, 3, 3)[0]}
        
        <rect x="70" y="40" width="160" height="20" class="lux-zone-red"/>
        <text x="100" y="35" text-anchor="middle" class="lux-text-red">OLD BEARISH OB</text>
        <text x="185" y="32" text-anchor="middle" class="lux-text-green">BULLISH BREAKER</text>
        
        <!-- Signal Box -->
        <rect x="180" y="65" width="18" height="10" class="lux-signal-bg-up"/>
        <polygon points="189,67 185,73 193,73" class="lux-signal-arrow-up"/>
      </svg>
        '''
    },
    {
        "q": "In options trading, what happens to Gamma as an option tracking the underlying price approaches Expiration?",
        "diff": "Hard",
        "options": [
            "Gamma becomes exactly 1.0 for all options regardless of strike.",
            "Gamma decreases for At-The-Money (ATM) options and increases for Out-Of-The-Money (OTM) options.",
            "Gamma increases significantly for At-The-Money (ATM) options, creating massive 'Gamma Risk'.",
            "Gamma ceases to exist once there are fewer than 5 days to expiration (0DTE)."
        ],
        "ans": 2,
        "exp_c": "Correct! Gamma explodes for ATM options near expiration (0DTE), meaning Delta can flip rapidly between 0 and 1. This highly volatile behavior is known as Gamma Risk.",
        "exp_w": "Incorrect. As expiration approaches, Gamma for At-The-Money options spikes dramatically because the option's moneyness (Delta) becomes hyper-sensitive to small price moves.",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        <rect x="40" y="20" width="220" height="50" class="lux-zone-red" rx="5"/>
        <text x="150" y="35" text-anchor="middle" class="lux-text-red" font-size="10">GAMMA RISK BANDS (0 DTE)</text>
        <line x1="150" y1="40" x2="150" y2="70" class="lux-line-white"/>
        {generate_bg_candles(8, 20, 6, 60, -1, 3, 4)[0]}
        {draw_seq([
            (70, 60, 55, 75), (60, 45, 40, 65), (45, 30, 25, 50), # Wild swings in price shown via candles
            (30, 20, 15, 35), (20, 50, 15, 55), (50, 60, 45, 65),
            (60, 30, 25, 65), (30, 70, 25, 75)
        ], 70, 20, 10)}
        {generate_bg_candles(12, 230, 6, 70, 0.5, 3, 4)[0]}
        <text x="150" y="100" text-anchor="middle" class="lux-text-green">Near Expiration: ATM Options are volatile!</text>
      </svg>
        '''
    },
    {
        "q": "What is a Judas Swing?",
        "diff": "Medium",
        "options": [
            "A wild swing in IV prior to a company split.",
            "A false breakout initially moving opposite to the real daily trend, designed to stop out retail traders.",
            "An options strategy combining far OTM calls with near OTM puts.",
            "When the market consolidates into a completely flat range."
        ],
        "ans": 1,
        "exp_c": "Correct! The Judas Swing is the 'Manipulation' leg of the AMD profile, engineered to fake out retail and sweep early stops before proceeding to the true target.",
        "exp_w": "Incorrect. A Judas Swing is a deceptive, engineered move at the market open designed to intentionally trigger retail stop losses before changing direction.",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        {generate_bg_candles(15, 10, 6, 60, 0, 3, 3)[0]}
        {draw_seq([
            (60, 65, 55, 70), (65, 60, 50, 70), (60, 62, 50, 65), # Consolidation
            (62, 40, 35, 65), # Up Sweep (Judas)
            (40, 70, 35, 75), # Instant reversal Red
            (70, 90, 65, 95), # True direction Red
            (90, 110, 85, 115),
        ], 100, 20, 10)}
        {generate_bg_candles(15, 200, 6, 110, 0, 3, 3)[0]}
        
        <circle cx="163" cy="40" r="10" class="lux-zone-red"/>
        <text x="163" y="25" text-anchor="middle" class="lux-text-red">JUDAS SWING</text>
        
        <text x="215" y="60" text-anchor="middle" class="lux-text-red">TRUE DIRECTION</text>
        <line x1="185" y1="65" x2="250" y2="105" stroke="#ff3366" stroke-width="2" stroke-dasharray="3,3"/>
      </svg>
        '''
    },
    {
        "q": "How does Implied Volatility (IV) Rank typically impact option strategy selection?",
        "diff": "Medium",
        "options": [
            "IV Rank doesn't matter; historical volatility is the only metric that dictates option pricing.",
            "High IV Rank favors options buying strategies (debit), while low IV Rank favors options selling (credit).",
            "High IV Rank favors options selling/premium collection (credit), while low IV Rank favors options buying (debit)",
            "It strictly determines if the trader should buy a Call or a Put."
        ],
        "ans": 2,
        "exp_c": "Correct! High IV means options are expensive (great for sellers). Low IV means options are cheap (great for buyers). Always sell high premium and buy low premium.",
        "exp_w": "Incorrect. A high IV Rank indicates options are relatively expensive, favoring premium sellers (credit spreads). A low IV Rank indicates options are cheap, favoring premium buyers.",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        <rect x="25" y="20" width="115" height="80" class="lux-zone-red"/>
        <rect x="160" y="20" width="115" height="80" class="lux-zone-green"/>
        
        <text x="82" y="40" text-anchor="middle" class="lux-text-red" font-size="8">HIGH IV RANK</text>
        {generate_bg_candles(15, 30, 7, 50, 0, 12, 5)[0]}
        
        <text x="217" y="40" text-anchor="middle" class="lux-text-green" font-size="8">LOW IV RANK</text>
        {generate_bg_candles(15, 165, 7, 60, 0, 2, 5)[0]}
      </svg>
        '''
    },
    {
        "q": "What is a Mitigation Block?",
        "diff": "Hard",
        "options": [
            "An Order Block whose resulting move successfully displaced but FAILED to break structural highs/lows before retracing.",
            "An Order Block that was fully swept by stop losses.",
            "An alternative name for a Fair Value Gap.",
            "The exact price where the Daily Open overlaps with the Asian Session High."
        ],
        "ans": 0,
        "exp_c": "Correct! A Mitigation Block is an Order Block that resulted in a lower-high or higher-low. Because it failed to break the major structure, price returns to mitigate it.",
        "exp_w": "Incorrect. A Mitigation Block forms when an OB causes a move that FAILS to break structure (forming a lower high or higher low), and is subsequently broken and mitigated.",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        {generate_bg_candles(8, 10, 6, 70, -2, 4, 3)[0]}
        {draw_seq([
            (70, 50, 45, 75), # UP move
            (50, 20, 15, 55), # UP Peak
            (20, 40, 15, 45), # DOWN (Creates OB)
            (40, 30, 25, 45), # UP (Fails to break high of 20)
            (30, 60, 25, 65), # DOWN (Mitigation starts)
            (60, 90, 55, 95), # DOWN
            (90, 60, 55, 95), # UP to mitigate
            (60, 85, 55, 90), # DOWN response
            (85, 110, 80, 115) # further DOWN
        ], 60, 15, 8)}
        {generate_bg_candles(12, 195, 6, 110, 0, 3, 3)[0]}
        <line x1="60" y1="20" x2="200" y2="20" class="lux-line-white"/>
        <text x="135" y="15" text-anchor="middle" class="lux-text-red">FAILS TO BREAK HIGH</text>
        
        <rect x="100" y="30" width="80" height="15" class="lux-zone-blue"/>
        <text x="190" y="40" class="lux-text-red">MITIGATION BLOCK</text>
      </svg>
        '''
    },
    {
        "q": "What is 'Vega' in option Greeks?",
        "diff": "Easy",
        "options": [
            "The sensitivity of an option's premium to changes in the risk-free interest rate.",
            "The speed at which the option loses value on weekends.",
            "The measure of an option's intrinsic value.",
            "The sensitivity of an option's price to changes in Implied Volatility."
        ],
        "ans": 3,
        "exp_c": "Correct! Vega measures how much an option's premium shifts with every 1% change in implied volatility, making it highly critical around earnings.",
        "exp_w": "Incorrect. Vega measures the rate of change in an option's premium for every 1% change in Implied Volatility. If Vega is high, the option is highly sensitive to volatility swings.",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        {generate_bg_candles(10, 10, 6, 80, -2, 4, 4)[0]}
        {draw_seq([
            (40, 80, 35, 85), # Massive red candle showing high vol
        ], 70, 30, 15)}
        {generate_bg_candles(15, 110, 6, 80, 0, 8, 4)[0]}
        <rect x="70" y="30" width="160" height="60" class="lux-zone-green" rx="5"/>
        <text x="150" y="45" text-anchor="middle" class="lux-text-green" font-size="12">VEGA = $0.15</text>
        <line x1="90" y1="60" x2="210" y2="60" class="lux-line-white"/>
        <text x="150" y="70" text-anchor="middle" class="lux-text">Implied Volatility (IV) increases +1.0%</text>
        <text x="150" y="80" text-anchor="middle" class="lux-text-green">Option Gained +$0.15</text>
      </svg>
        '''
    },
    {
        "q": "What is a Liquidity Void?",
        "diff": "Medium",
        "options": [
            "A Fair Value Gap that is permanently ignored.",
            "A sudden halt in market trading due to SEC regulations.",
            "A very large, one-directional price move consisting of multiple consecutive large candles with minimal overlaps.",
            "When the options order book has no visible contracts available for trading."
        ],
        "ans": 2,
        "exp_c": "Correct! A Liquidity Void represents a sudden, massive burst of impulsive energy. This forms a fast track where price often snaps back aggressively to fill the void.",
        "exp_w": "Incorrect. A Liquidity Void is an area where price moved significantly fast in one direction via large-range candles. The market algorithm often draws price back to 'fill' this empty zone.",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        {generate_bg_candles(10, 10, 6, 20, 0, 3, 3)[0]}
        {draw_seq([
            (20, 50, 15, 55), # Red
            (50, 80, 45, 85), # Red
            (80, 110, 75, 115), # Red
        ], 70, 15, 8)}
        
        <rect x="65" y="15" width="40" height="100" class="lux-zone-red"/>
        <text x="110" y="60" class="lux-text-red" font-size="8">LIQUIDITY VOID</text>
        
        {generate_bg_candles(8, 115, 6, 110, -0.5, 3, 3)[0]}
        
        <!-- Pullback to fill -->
        {draw_seq([
            (110, 80, 75, 115), # Green
            (80, 50, 45, 85), # Green
            (50, 20, 15, 55), # Green
        ], 163, 15, 8)}
        {generate_bg_candles(15, 208, 6, 20, 0, 4, 3)[0]}
        
        <path d="M 105 105 Q 140 120 150 50 L 140 55 M 150 50 L 160 55" fill="none" stroke="#0096ff" stroke-width="1.5"/>
        <text x="175" y="55" class="lux-text">PRICE RETURNS</text>
      </svg>
        '''
    },
    {
        "q": "What does the term 'Killzone' refer to in ICT?",
        "diff": "Medium",
        "options": [
            "A price range where an option loses 100% of its value.",
            "A 30-minute block where high-frequency bots temporarily shut down.",
            "The specific time windows aligning with major market open volatilities, optimized for high probability entries.",
            "An arbitrary price target for a long-term swing trade."
        ],
        "ans": 2,
        "exp_c": "Correct! Killzones are time-based windows (London Open, NY Open, London Close) when volatility and institutional volume inject peak opportunity into the market.",
        "exp_w": "Incorrect. ICT Killzones are distinct intra-day time windows where substantial institutional volatility enters the market, making setups highly predictable.",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        <rect x="40" y="20" width="50" height="90" class="lux-zone-blue"/>
        <rect x="120" y="20" width="50" height="90" class="lux-zone-red"/>
        <rect x="200" y="20" width="50" height="90" class="lux-zone-green"/>
        
        <text x="65" y="15" text-anchor="middle" class="lux-text">LONDON KZ</text>
        <text x="145" y="15" text-anchor="middle" class="lux-text-red">NY KZ</text>
        <text x="225" y="15" text-anchor="middle" class="lux-text-green">LONDON CLOSE</text>
        
        {generate_bg_candles(10, 10, 4, 60, -1, 3, 2)[0]}
        {generate_bg_candles(8, 50, 6, 50, 1, 8, 4)[0]}
        {generate_bg_candles(6, 98, 4, 58, 0, 3, 2)[0]}
        {generate_bg_candles(8, 122, 6, 58, -2, 9, 4)[0]}
        {generate_bg_candles(6, 170, 4, 42, 0, 3, 2)[0]}
        {generate_bg_candles(8, 194, 6, 42, 1, 6, 4)[0]}
      </svg>
        '''
    },
    {
        "q": "In a bearish AMD (Power of 3) profile, when does the Manipulation essentially occur?",
        "diff": "Hard",
        "options": [
            "It drops below the Asian session low before continuing further down.",
            "It shoots above the Asian session high (typically in London or NY open) to grab buy-side liquidity before crashing into distribution.",
            "It consolidates aggressively exactly at the Daily Open mapping a tight doji.",
            "Manipulation does not occur in a bearish environment, only bullish."
        ],
        "ans": 1,
        "exp_c": "Correct! During a bearish AMD day, smart money runs price ABOVE the Asian high to clear out early retail shorts. Once liquidity is grabbed, the true bearish distribution occurs.",
        "exp_w": "Incorrect. In a bearish AMD model, the Manipulation stage always targets the liquidity resting ABOVE the Asian session, forcing price to spike upward temporarily before selling off.",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        <rect x="30" y="50" width="70" height="20" class="lux-zone-yellow"/>
        <text x="65" y="45" text-anchor="middle" class="lux-text">ASIAN RANGE</text>
        
        {generate_bg_candles(10, 10, 6, 60, 0, 3, 3)[0]}
        {draw_seq([
            (60, 55, 50, 65),
            (55, 30, 25, 60), # Shoots up! Manipulation (Green)
            (30, 50, 25, 55), # Red
            (50, 80, 45, 85), # Instantly collapses (Red)
            (80, 100, 75, 105), # Red
        ], 70, 20, 10)}
        {generate_bg_candles(15, 170, 6, 100, 1, 4, 3)[0]}
        
        <circle cx="110" cy="30" r="15" class="lux-zone-red"/>
        <text x="110" y="10" text-anchor="middle" class="lux-text-red">MANIPULATION</text>
      </svg>
        '''
    },
    {
        "q": "What is 'Rho' in options trading?",
        "diff": "Easy",
        "options": [
            "Sensitivity of an option's price to the passage of time.",
            "Sensitivity to the underlying stock's historical volume.",
            "Sensitivity of an option's expected contract to the risk-free interest rate.",
            "The probability of the underlying asset being halted."
        ],
        "ans": 2,
        "exp_c": "Correct! Rho measures an option contract's sensitivity to changes in the risk-free interest rate. For short-term options, Rho is barely noticeable.",
        "exp_w": "Incorrect. Rho is the Greek that measures the sensitivity of an option's premium to changing risk-free interest rates.",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        {generate_bg_candles(45, 10, 6, 70, -0.8, 4, 4)[0]}
        <rect x="80" y="30" width="160" height="60" class="lux-zone-blue" rx="5"/>
        <text x="160" y="50" text-anchor="middle" class="lux-text-green" font-size="10">RHO = INTEREST RATES</text>
        <line x1="90" y1="65" x2="230" y2="65" class="lux-line-white"/>
        <text x="160" y="76" text-anchor="middle" class="lux-text">Minimal impact for 0DTE.</text>
        <text x="160" y="86" text-anchor="middle" class="lux-text">Crucial for LEAPs (Long-term).</text>
      </svg>
        '''
    },
    {
        "q": "What does an Inversion Fair Value Gap (IFVG) represent?",
        "diff": "Hard",
        "options": [
            "An FVG that occurs precisely on the bottom of a V-shaped recovery.",
            "A Fair Value Gap that price completely disrespected and closed through, which now acts as the opposite support or resistance.",
            "When the options bid/ask spread completely inverts in a low liquidity stock.",
            "A gap on the daily chart created over a long weekend."
        ],
        "ans": 1,
        "exp_c": "Correct! If price impulsively blasts right through a bullish FVG without respecting it, it flips its role to become a bearish IFVG.",
        "exp_w": "Incorrect. An Inversion Fair Value Gap (IFVG) occurs when price strongly closes entirely through a traditional FVG, converting it into a potent support/resistance of the opposite directional bias.",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        {generate_bg_candles(10, 10, 6, 30, -1, 3, 3)[0]}
        
        <rect x="70" y="50" width="130" height="20" class="lux-zone-green"/>
        <text x="100" y="45" text-anchor="middle" class="lux-text-green">BULLISH FVG</text>
        
        {draw_seq([
            (30, 40, 25, 45), # Red 
            (40, 80, 35, 85), # Crash straight down over the FVG! (Red)
            (80, 100, 75, 105), # Red
            (100, 90, 85, 105), # Back up (Green)
            (90, 70, 65, 95), # Touch edge of old FVG (Green)
            (70, 90, 65, 95), # Bearish bounce off IFVG (Red)
            (90, 105, 80, 110)
        ], 70, 15, 8)}
        {generate_bg_candles(12, 175, 6, 105, 0, 3, 3)[0]}
        
        <rect x="200" y="50" width="80" height="20" class="lux-zone-red"/>
        <text x="240" y="45" text-anchor="middle" class="lux-text-red">BEARISH IFVG</text>
      </svg>
        '''
    },
    {
        "q": "How does the 'Options Pinning' phenomenon usually impact price action near OpEx?",
        "diff": "Medium",
        "options": [
            "It guarantees that all contracts expire worthless.",
            "The underlying stock price magnetically gravitates towards the strike price that has the absolute largest open interest.",
            "It forces the option premium to double temporarily.",
            "It permanently freezes trading on options contracts 3 hours before close."
        ],
        "ans": 1,
        "exp_c": "Correct! Market Makers inherently manage their risk exposure by buying/selling the underlying asset. Near OpEx, this hedging forces the stock to 'pin' near heavy open-interest levels.",
        "exp_w": "Incorrect. Options Pinning happens when the underlying stock price gets 'pinned' to a tightly concentrated specific strike price near expiration, primarily driven by market makers hedging their deltas.",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        <rect x="20" y="55" width="260" height="15" class="lux-zone-blue"/>
        <line x1="20" y1="60" x2="280" y2="60" class="lux-line-green"/>
        <text x="150" y="50" text-anchor="middle" class="lux-text-green">HEAVY OPEN INTEREST (STRIKE: $100)</text>
        
        {generate_bg_candles(10, 10, 6, 90, -3, 5, 4)[0]}
        {draw_seq([
            (90, 70, 65, 95),  (70, 90, 65, 95), (90, 60, 55, 95), (60, 80, 55, 85), 
            (80, 60, 55, 85), (60, 65, 55, 70)
        ], 70, 15, 8)}
        {generate_bg_candles(20, 160, 6, 65, 0, 8, 4)[0]}
        <text x="260" y="75" class="lux-text-red">PINNED</text>
      </svg>
        '''
    },
    {
        "q": "What is a Rejection Block?",
        "diff": "Hard",
        "options": [
            "When the CFTC rejects an options settlement.",
            "An area where institutional algorithms start accumulating short biases.",
            "A structural pivot where price abruptly fails to sweep the liquidity resting precisely at a major high/low, reversing instantly and forming an order block behind it.",
            "A series of five perfectly identical sized wicks."
        ],
        "ans": 2,
        "exp_c": "Correct! A Rejection Block functions when the price purposely leaves liquidity intact, failing to sweep, and immediately pivots using the most recent wicks as protection.",
        "exp_w": "Incorrect. A Rejection Block utilizes long wicks near significant liquidity pools. Price approaches the high/low, fails to push through it entirely, and immediately rejects in the opposite direction.",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        <line x1="20" y1="20" x2="280" y2="20" class="lux-line-red"/>
        <text x="150" y="15" text-anchor="middle" class="lux-text">BSL</text>
        
        {generate_bg_candles(15, 10, 6, 60, -1, 4, 3)[0]}
        {draw_seq([
            (60, 40, 35, 65), (40, 30, 25, 45),
            (30, 45, 25, 50), # Hits 25, fails to sweep 20!
            (45, 80, 40, 85), # Massive down (Red)
            (80, 100, 75, 105),
        ], 100, 20, 10)}
        {generate_bg_candles(15, 200, 6, 100, 0.5, 3, 3)[0]}
        
        <rect x="130" y="25" width="20" height="20" class="lux-zone-green"/>
        <text x="160" y="32" class="lux-text-green">REJECTION BLOCK</text>
      </svg>
        '''
    },
    {
        "q": "What essentially defines an 'Expected Move' or 'Standard Deviation' move in an options pricing model?",
        "diff": "Hard",
        "options": [
            "A manual prediction made by high-tier brokerage analysts.",
            "The statistical pricing derived strictly from historical data points over the last 10 years.",
            "The exact price where the underlying asset will close on expiration day.",
            "A statistical calculation based on current Implied Volatility showcasing the probable max range of the stock for a specific timeframe."
        ],
        "ans": 3,
        "exp_c": "Correct! Market Makers utilize IV to mathematically bracket a 1 Standard Deviation (approx ~68% probability) range on the stock for the expiration cycle.",
        "exp_w": "Incorrect. An expected move is entirely mathematically calculated based on the current Implied Volatility. It predicts the likely bounds the stock will be contained within.",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        <line x1="120" y1="20" x2="120" y2="100" class="lux-line-white"/>
        <text x="120" y="15" text-anchor="middle" class="lux-text">CURRENT STOCK PRICE ($100)</text>
        
        <rect x="75" y="30" width="150" height="80" fill="rgba(0,150,255,0.1)"/>
        
        <line x1="75" y1="30" x2="75" y2="100" class="lux-line-red"/>
        <text x="75" y="25" text-anchor="middle" class="lux-text-red">- 1SD ($95)</text>
        
        <line x1="225" y1="30" x2="225" y2="100" class="lux-line-green"/>
        <text x="225" y="25" text-anchor="middle" class="lux-text-green">+ 1SD ($105)</text>
        
        {generate_bg_candles(15, 10, 6, 60, 0, 4, 3)[0]}
        {draw_seq([ (60, 50, 45, 65), (50, 70, 45, 75), (70, 40, 35, 75), (40, 80, 35, 85) ], 100, 15, 8)}
        {generate_bg_candles(20, 160, 6, 80, -0.5, 4, 3)[0]}
        <text x="150" y="115" text-anchor="middle" class="lux-text" style="fill:#c9a84c;">EXPECTED MOVE (68% BANDS)</text>
      </svg>
        '''
    }
]

# Generate answers arrays
answers_js = "const ANSWERS=[" + ",".join([str(q['ans']) for q in questions]) + "];"
explanations_js = "const EXPLANATIONS=[\n"
for q in questions:
    c_escaped = q["exp_c"].replace('"', '\\"')
    w_escaped = q["exp_w"].replace('"', '\\"')
    explanations_js += f'  {{c:"{c_escaped}",w:"{w_escaped}"}},\n'
explanations_js += "];"

new_cards_html = ""
for i, q in enumerate(questions):
    diff_class = "diff-easy"
    if q['diff'] == "Medium":
        diff_class = "diff-medium"
    elif q['diff'] == "Hard":
        diff_class = "diff-hard"
        
    card_html = f'''
  <!-- ═══════════════ Q{i+1} ═══════════════ -->
  <div class="question-card" id="qcard-{i}">
    <div class="question-header">
      <div class="q-left">
        <div class="q-top-row">
          <div class="q-number">{(i+1):02d}</div>
          <div class="question-text">{q['q']}</div>
          <div class="q-difficulty {diff_class}">{q['diff']}</div>
        </div>
      </div>
    </div>
    <div class="options" id="opts-{i}">
      <button class="option-btn" onclick="answer({i},0)"><span class="option-letter">A</span>{q['options'][0]}</button>
      <button class="option-btn" onclick="answer({i},1)"><span class="option-letter">B</span>{q['options'][1]}</button>
      <button class="option-btn" onclick="answer({i},2)"><span class="option-letter">C</span>{q['options'][2]}</button>
      <button class="option-btn" onclick="answer({i},3)"><span class="option-letter">D</span>{q['options'][3]}</button>
    </div>
    <div class="explanation" id="exp-{i}"></div>
    <div id="chart-{i}" style="display:none">
      {q['svg']()}
    </div>
  </div>
'''
    new_cards_html += card_html

content = re.sub(r'<!-- ═══════════════ Q1 ═══════════════ -->.*?<!-- ── SCORE CARD ── -->', new_cards_html + '\n  <!-- ── SCORE CARD ── -->', content, flags=re.DOTALL)

# Inject JS strings correctly so they are never missed
content = re.sub(r'const ANSWERS=\[.*?\];', answers_js, content)
content = re.sub(r'const EXPLANATIONS=\[\n.*?\n\];', explanations_js, content, flags=re.DOTALL)

with open(QUIZ_FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Quiz 2 extensively upgraded with 40+ CANDLE REALISTIC BACKGROUNDS: {QUIZ_FILE}")
