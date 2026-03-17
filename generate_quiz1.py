import re
import random

QUIZ_FILE = r'c:\Users\Admin\My Drive (albanm1687@gmail.com)\Discord\MIGA TRADING\miga github\quiz1_intermediate.html'

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
    random.seed(42) # Seed for consistency but realistic chaos
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
        "q": "What is a Fair Value Gap (FVG)?",
        "diff": "Medium",
        "options": [
            "A gap between Monday's opening price and Friday's closing price.",
            "A 3-candle sequence where the tails of the 1st and 3rd candles do not overlap, leaving a void.",
            "An area where options premium is mispriced relative to volatility.",
            "The distance between a stock's bid and ask price."
        ],
        "ans": 1,
        "exp_c": "Correct! An FVG is an imbalance formed by a 3-candle sequence where the 1st and 3rd candles' wicks don't overlap, creating a liquidity void.",
        "exp_w": "Incorrect. An FVG is a 3-candle imbalance where the wicks of candle 1 and 3 do not overlap, indicating aggressive price displacement.",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        {generate_bg_candles(15, 10, 8, 80, -1, 3, 5)[0]}
        {draw_seq([
            (60, 40, 35, 65), # Up candle (c=40, <= 60 so Green)
            (40, 45, 30, 50), # Red
            (45, 80, 40, 85), # Massive Red
            (80, 105, 75, 110), # Red
            (105, 95, 90, 110), # Green
        ], 130, 15, 8)}
        {generate_bg_candles(8, 205, 8, 95, 1, 3, 5)[0]}
        
        <!-- FVG highlight Box -->
        <!-- Candle 1 low wick is at 50, Candle 3 high wick is at 75. Gap = 50 to 75 -->
        <rect x="130" y="50" width="160" height="25" class="lux-zone-red"/>
        <text x="210" y="65" text-anchor="middle" class="lux-text-red">BEARISH FVG (VOID)</text>
        <line x1="130" y1="50" x2="290" y2="50" class="lux-line-red"/>
        <line x1="130" y1="75" x2="290" y2="75" class="lux-line-red"/>
      </svg>
        '''
    },
    {
        "q": "What does a Call Option give the buyer the right to do?",
        "diff": "Easy",
        "options": [
            "The right to sell 100 shares of the underlying stock at the strike price.",
            "The obligation to buy 100 shares of the underlying stock at the strike price.",
            "The right specifically to collect dividends from the underlying stock.",
            "The right to buy 100 shares of the underlying stock at the strike price."
        ],
        "ans": 3,
        "exp_c": "Correct! Buying a call gives you the RIGHT, but not the obligation, to buy 100 shares of the underlying at the agreed strike price.",
        "exp_w": "Incorrect. A Call Option gives the buyer the RIGHT to buy 100 shares of the underlying asset at the strike price before expiration.",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        {generate_bg_candles(20, 10, 6, 80, 0, 4, 4)[0]}
        {draw_seq([
            (90, 80, 75, 95),
            (80, 60, 55, 85),
            (60, 40, 35, 65), # Stock rockets up
            (40, 10, 5, 45),
        ], 130, 20, 10)}
        {generate_bg_candles(10, 210, 6, 10, -1, 3, 4)[0]}
        <!-- Strike Price Box -->
        <rect x="20" y="80" width="270" height="12" class="lux-zone-blue"/>
        <text x="150" y="88" text-anchor="middle" class="lux-text">STRIKE PRICE (CALL BOUGHT HERE)</text>
        <line x1="20" y1="80" x2="290" y2="80" class="lux-line-white"/>
        <text x="150" y="40" class="lux-text-green">PRICE ROCKETS = CALL GAINS VALUE</text>
      </svg>
        '''
    },
    {
        "q": "In Smart Money Concepts, what is a Liquidity Sweep?",
        "diff": "Medium",
        "options": [
            "A sudden increase in overall market trading volume.",
            "When price momentarily breaks a significant high or low to trigger stop losses before reversing.",
            "The process of converting stock shares into options contracts.",
            "When Central Banks inject money into the financial system."
        ],
        "ans": 1,
        "exp_c": "Correct! A liquidity sweep occurs when price pierces a key high/low to grab resting stop-loss orders, then sharply reverses.",
        "exp_w": "Incorrect. A liquidity sweep is when Smart Money drives price above a high or below a low to take resting retail stop losses, providing them with liquidity to reverse the market.",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        <!-- Resistance level (Liquidity) -->
        <line x1="20" y1="40" x2="280" y2="40" class="lux-line-red"/>
        <text x="150" y="35" text-anchor="middle" class="lux-text-red">BUY-SIDE LIQUIDITY (BSL)</text>
        {generate_bg_candles(15, 10, 5, 60, -0.5, 4, 4)[0]}
        {draw_seq([
            (80, 60, 55, 85), # Green
            (60, 50, 45, 65), # Green
            (50, 65, 45, 70), # Red
            (65, 42, 40, 70), # Green touching BSL
            (42, 60, 38, 65), # Red
            (60, 50, 45, 65), # Green
            (50, 20, 15, 55), # MASSIVE GREEN SWEEP above BSL
            (20, 60, 15, 65), # INSTANT RED REVERSAL
            (60, 80, 55, 85), # Red Follow Through
            (80, 100, 75, 105), # Red Crash
        ], 90, 15, 8)}
        {generate_bg_candles(10, 240, 5, 100, 0, 3, 4)[0]}
        <!-- Sweep Highlight Box -->
        <rect x="170" y="10" width="35" height="40" class="lux-zone-red" rx="3"/>
        <text x="187" y="25" text-anchor="middle" class="lux-text">SWEEP + REVERSAL</text>
        
        <rect x="150" y="5" width="18" height="10" class="lux-signal-bg-down"/>
        <polygon points="159,13 155,7 163,7" class="lux-signal-arrow-down"/>
      </svg>
        '''
    },
    {
        "q": "What is a Break of Structure (BOS)?",
        "diff": "Medium",
        "options": [
            "When an options contract is exercised early.",
            "When a company announces a stock split.",
            "When price convincingly breaks and closes past a previous structural high (in an uptrend) or low (in a downtrend).",
            "A technical glitch in the trading platform."
        ],
        "ans": 2,
        "exp_c": "Correct! BOS confirms trend continuation. It happens when price breaks and closes beyond the previous major structural point.",
        "exp_w": "Incorrect. Break of Structure (BOS) refers to price closing past a previous structural high/low, confirming the continuation of the current trend.",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        {generate_bg_candles(12, 10, 6, 80, -2, 5, 4)[0]}
        {draw_seq([
            (90, 60, 55, 95),   # Green
            (60, 50, 45, 65),   # Green High
            (50, 70, 45, 75),   # Red Retrace
            (70, 65, 60, 75),   # Green start
            (65, 45, 40, 70),   # Green
            (45, 30, 25, 50),   # Green breaks previous high
            (30, 15, 10, 35),   # Green continues
        ], 80, 20, 10)}
        {generate_bg_candles(12, 220, 6, 15, -1, 3, 4)[0]}
        
        <!-- BOS Line -->
        <line x1="80" y1="50" x2="250" y2="50" class="lux-line-white"/>
        <rect x="140" y="44" width="30" height="12" fill="#1a2433" rx="2"/>
        <text x="155" y="52" text-anchor="middle" class="lux-text-green">BOS</text>

        <!-- LuxAlgo signal indicator -->
        <rect x="185" y="20" width="18" height="10" class="lux-signal-bg-up"/>
        <polygon points="194,22 190,28 198,28" class="lux-signal-arrow-up"/>
        <text x="194" y="38" text-anchor="middle" class="lux-text">BUY</text>
      </svg>
        '''
    },
    {
        "q": "What does 'Delta' measure in Options trading?",
        "diff": "Hard",
        "options": [
            "The daily time decay of an options contract.",
            "The expected change in the option's price for a $1 move in the underlying stock.",
            "The sensitivity of the option to changes in implied volatility.",
            "The percentage chance that the stock will payout a dividend."
        ],
        "ans": 1,
        "exp_c": "Correct! Delta measures how much the option's price will move for every $1 change in the underlying stock's price.",
        "exp_w": "Incorrect. Delta measures the rate of change of the option's premium given a $1 move in the underlying asset.",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        {generate_bg_candles(15, 10, 6, 90, -0.5, 3, 4)[0]}
        {draw_seq([
            (90, 50, 40, 95), # Massive +$1 move
        ], 100, 20, 12)}
        {generate_bg_candles(20, 125, 6, 50, -0.5, 3, 4)[0]}
        <rect x="130" y="10" width="150" height="60" class="lux-zone-blue" rx="5"/>
        <text x="205" y="30" text-anchor="middle" class="lux-text-green" font-size="12">DELTA = 0.50</text>
        <line x1="60" y1="40" x2="260" y2="40" class="lux-line-white"/>
        <text x="205" y="50" text-anchor="middle" class="lux-text">Underlying Stock Moves +$1.00</text>
        <text x="205" y="60" text-anchor="middle" class="lux-text-green">Option Gained +$0.50</text>
      </svg>
        '''
    },
    {
        "q": "What is a Change of Character (CHOCH)?",
        "diff": "Medium",
        "options": [
            "When an option goes from Out of The Money to In The Money.",
            "An early signal of a potential trend reversal, indicated by the breaking of the first counter-trend structural point.",
            "When implied volatility drops severely.",
            "When the CEO of a company resigns unexpectedly."
        ],
        "ans": 1,
        "exp_c": "Correct! CHOCH is the first break of structure in the opposite direction of the current trend, signaling a potential reversal.",
        "exp_w": "Incorrect. CHOCH (Change of Character) is the initial structural break that indicates a trend might be failing and ready to reverse.",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        {generate_bg_candles(10, 10, 5, 20, 2, 4, 3)[0]}
        {draw_seq([
            (30, 45, 25, 50), # Red
            (45, 60, 40, 65), # Red
            (60, 50, 45, 65), # Green retrace (Swing High)
            (50, 75, 45, 80), # Red
            (75, 95, 70, 100), # Red
            (95, 80, 75, 105), # Green
            (80, 60, 55, 90), # Green
            (60, 30, 25, 70), # Massive Green - Breaks swing high!
            (30, 10, 5, 40)   # Green follow thru
        ], 60, 15, 8)}
        {generate_bg_candles(15, 195, 6, 10, -0.5, 3, 4)[0]}
        
        <!-- CHOCH Line -->
        <!-- Swing high was at 50 -->
        <line x1="75" y1="50" x2="250" y2="50" class="lux-line-green"/>
        <rect x="200" y="44" width="35" height="12" fill="#1a2433" rx="2"/>
        <text x="217" y="52" text-anchor="middle" class="lux-text-green">CHoCH</text>
        
        <text x="150" y="30" class="lux-text">TREND REVERSAL SIGNAL</text>
      </svg>
        '''
    },
    {
        "q": "When buying a Put Option, what is the maximum risk?",
        "diff": "Easy",
        "options": [
            "Unlimited risk if the stock goes to infinity.",
            "Limited to the difference between the strike price and zero.",
            "100% of the premium paid for the option contract.",
            "There is no risk because options are protected by the exchange."
        ],
        "ans": 2,
        "exp_c": "Correct! As an options buyer (Call or Put), your absolute maximum risk is defined strictly as the premium you paid.",
        "exp_w": "Incorrect. Buying options has strictly defined risk. The maximum you can lose is the premium you paid to purchase the contract.",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        {generate_bg_candles(15, 10, 6, 40, 0, 4, 4)[0]}
        {draw_seq([
            (50, 80, 45, 85), # Red
            (80, 110, 75, 115), # Red
        ], 100, 30, 12)}
        {generate_bg_candles(20, 160, 6, 110, 0, 3, 4)[0]}
        <rect x="70" y="30" width="160" height="50" class="lux-zone-red" rx="5"/>
        <text x="150" y="45" text-anchor="middle" class="lux-text-red" font-size="10">MAX RISK = PREMIUM PAID</text>
        <line x1="80" y1="55" x2="210" y2="55" class="lux-line-white"/>
        <text x="150" y="65" text-anchor="middle" class="lux-text">You bought 1 Put Contract for $2.50.</text>
        <text x="150" y="75" text-anchor="middle" class="lux-text">Maximum Loss = $250</text>
      </svg>
        '''
    },
    {
        "q": "What is the Premium vs Discount relative to the dealing range?",
        "diff": "Medium",
        "options": [
            "Premium is buying calls; Discount is buying puts.",
            "The top 50% of a range is 'Premium' (where you look to sell/short), and the bottom 50% is 'Discount' (where you look to buy).",
            "The difference between the bid and the ask spread of an option.",
            "A fee brokerages charge for executing trades."
        ],
        "ans": 1,
        "exp_c": "Correct! In ICT, any level above the 50% equilibrium of a range is Premium (sell zone), and below is Discount (buy zone).",
        "exp_w": "Incorrect. The top half of a dealing range is the 'Premium' zone (optimal for shorting), while the bottom half is the 'Discount' zone (optimal for longing).",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        
        <rect x="60" y="10" width="180" height="50" class="lux-zone-red"/>
        <rect x="60" y="60" width="180" height="50" class="lux-zone-green"/>
        
        <line x1="50" y1="60" x2="250" y2="60" class="lux-line-white"/>
        <text x="260" y="63" class="lux-text">EQ (50%)</text>
        
        <text x="150" y="35" text-anchor="middle" class="lux-text-red">PREMIUM (SELL ZONE)</text>
        <text x="150" y="85" text-anchor="middle" class="lux-text-green">DISCOUNT (BUY ZONE)</text>
        
        <!-- Fibo lines -->
        <text x="45" y="13" class="lux-text">0.0</text>
        <text x="45" y="113" class="lux-text">1.0</text>
        
        {generate_bg_candles(40, 10, 6, 60, 0, 5, 4)[0]}
      </svg>
        '''
    },
    {
        "q": "What is 'Theta' decay in Options?",
        "diff": "Hard",
        "options": [
            "A measure of how much an option's value decreases each day as it approaches expiration.",
            "The speed at which implied volatility drops.",
            "An increase in premium due to high demand.",
            "The amount of shares an option represents."
        ],
        "ans": 0,
        "exp_c": "Correct! Theta represents time decay. It tells you how much value an option loses every single day as expiration draws nearer.",
        "exp_w": "Incorrect. Theta is the options Greek that measures time decay—the amount an option's theoretical value decreases with the passage of one day.",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        {generate_bg_candles(45, 10, 6, 60, 0, 4, 4)[0]}
        <path d="M 20 20 Q 180 30 250 100" fill="none" stroke="#ff3366" stroke-width="2"/>
        <text x="135" y="30" class="lux-text-red" font-size="8">THETA DECAY DRAINS VALUE OUT OF CHOPPY PRICE</text>
        <line x1="250" y1="20" x2="250" y2="105" class="lux-line-white"/>
        <rect x="230" y="105" width="40" height="12" fill="#1a2433" rx="2"/>
        <text x="250" y="113" text-anchor="middle" class="lux-text">0 DTE</text>
      </svg>
        '''
    },
    {
        "q": "What is an Implied Volatility (IV) crush?",
        "diff": "Medium",
        "options": [
            "When the stock price drops drastically.",
            "When trading volume hits a daily low.",
            "A rapid drop in implied volatility after a known event (like earnings), causing options premiums to deflate quickly.",
            "When an options order is canceled before filling."
        ],
        "ans": 2,
        "exp_c": "Correct! IV crush happens right after a major uncertainty (like earnings) passes. The volatility prediction drops quickly, sucking value out of options.",
        "exp_w": "Incorrect. IV Crush is the rapid decline of implied volatility immediately following a major event, resulting in a sharp drop in options premiums.",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        {generate_bg_candles(20, 10, 6, 80, -0.5, 3, 4)[0]}
        {draw_seq([
            (60, 10, 5, 65) # Earnings gap!
        ], 130, 20, 10)}
        {generate_bg_candles(20, 150, 6, 10, 0.5, 3, 4)[0]}
        <path d="M 30 100 L 90 40 L 120 20 L 130 90 L 270 95" fill="none" stroke="#0096ff" stroke-width="2"/>
        <line x1="120" y1="10" x2="120" y2="110" class="lux-line-white"/>
        <rect x="95" y="100" width="50" height="12" fill="#1a2433" rx="2"/>
        <text x="120" y="108" text-anchor="middle" class="lux-text">EARNINGS EVENT</text>
        
        <text x="70" y="20" class="lux-text-green">IV PUMP</text>
        <text x="150" y="70" class="lux-text-red">IV CRUSH</text>
      </svg>
        '''
    },
    {
        "q": "What is Buy-Side Liquidity (BSL)?",
        "diff": "Hard",
        "options": [
            "A pool of resting buy stop orders typically located above major resistance levels or old highs.",
            "The total number of Call options bought in a day.",
            "When retail traders are exclusively buying.",
            "A structural point that indicates a downtrend."
        ],
        "ans": 0,
        "exp_c": "Correct! BSL refers to the buy stops placed above previous high points by short-sellers to protect their positions.",
        "exp_w": "Incorrect. Buy-Side Liquidity (BSL) exists above old highs and resistance levels. It consists of buy stops from short sellers and breakout buyers.",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        <!-- Liquidity level -->
        <rect x="30" y="20" width="240" height="15" class="lux-zone-green"/>
        <line x1="30" y1="35" x2="270" y2="35" class="lux-line-green"/>
        <text x="150" y="30" text-anchor="middle" class="lux-text-green">BUY-SIDE LIQUIDITY (BUY STOPS ON TOP OF RANGE)</text>
        
        {generate_bg_candles(8, 10, 6, 80, -2, 5, 4)[0]}
        {draw_seq([
            (50, 70, 45, 75), # Down
            (70, 90, 65, 95), # Down
            (90, 55, 50, 95), # Up
            (55, 80, 50, 85), # Down
            (80, 40, 35, 85), # UP (Sweeps BSL)
        ], 58, 15, 8)}
        {generate_bg_candles(25, 133, 6, 40, 0.5, 4, 4)[0]}
        
        <text x="150" y="110" text-anchor="middle" class="lux-text">Equal Highs (Retail Resistance)</text>
      </svg>
        '''
    },
    {
        "q": "In ICT, what typically represents a valid Order Block?",
        "diff": "Medium",
        "options": [
            "Any randomly large green or red candle on the daily chart.",
            "The last down-candle before a strong upward displacement (bullish OB), or the last up-candle before a strong downward displacement (bearish OB).",
            "A period of tight consolidation stretching for days.",
            "The exact price where the most options Volume is resting."
        ],
        "ans": 1,
        "exp_c": "Correct! An Order Block is typically the last opposite-colored candle prior to a massive impulsive move that breaks structure.",
        "exp_w": "Incorrect. A valid ICT Order Block is the final down-candle before a bullish breakout, or the final up-candle before a bearish breakdown.",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        {generate_bg_candles(15, 10, 6, 40, 2, 4, 4)[0]}
        {draw_seq([
            (60, 80, 55, 85), # Down
            (80, 95, 75, 100), # Last down candle (Red)
            (95, 40, 35, 105), # Massive Green displacement
            (40, 20, 15, 45), # Green
            (20, 10, 5, 25), # Green
        ], 100, 15, 8)}
        {generate_bg_candles(15, 175, 6, 10, 0.5, 3, 4)[0]}
        <!-- Order Block Zone overlaying the last down candle -->
        <rect x="80" y="80" width="200" height="15" class="lux-zone-blue"/>
        <line x1="80" y1="80" x2="280" y2="80" class="lux-line-white"/>
        <text x="210" y="90" class="lux-text">BULLISH ORDER BLOCK</text>
      </svg>
        '''
    },
    {
        "q": "What does 'In the Money' (ITM) mean for a Call Option?",
        "diff": "Easy",
        "options": [
            "The option was purchased using margin.",
            "The strike price is above the current stock price.",
            "The options trade is currently at a 100% profit.",
            "The strike price is strictly below the current stock price."
        ],
        "ans": 3,
        "exp_c": "Correct! A call option is In The Money (ITM) when the stock is currently trading HIGHER than the established strike price.",
        "exp_w": "Incorrect. A Call option is ITM when the underlying asset's current price is greater than the strike price, giving the contract intrinsic value.",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        <line x1="40" y1="60" x2="260" y2="60" class="lux-line-white"/>
        <rect x="40" y="10" width="220" height="50" class="lux-zone-green"/>
        <text x="265" y="62" class="lux-text">STRIKE: $100</text>
        
        {generate_bg_candles(20, 20, 6, 100, -1, 4, 4)[0]}
        {draw_seq([
            (70, 50, 45, 75),
            (50, 20, 15, 55), # Stock goes up above strike
        ], 140, 15, 8)}
        {generate_bg_candles(15, 170, 6, 20, 0, 4, 4)[0]}
        
        <circle cx="205" cy="30" r="5" class="lux-zone-blue"/>
        <text x="165" y="30" text-anchor="middle" class="lux-text-green" font-size="12">ITM (IN THE MONEY)</text>
      </svg>
        '''
    },
    {
        "q": "What is Sell-Side Liquidity (SSL)?",
        "diff": "Hard",
        "options": [
            "Sell stop orders resting beneath previous lows, typically used as stop losses by long traders.",
            "When the options market has more Puts than Calls.",
            "An area where institutional algorithms start buying.",
            "The exact point where a stock goes bankrupt."
        ],
        "ans": 0,
        "exp_c": "Correct! SSL is the pool of resting sell-stop orders placed underneath old lows by retail traders who are currently long.",
        "exp_w": "Incorrect. Sell-Side Liquidity (SSL) consists of resting sell stop orders located beneath significant prior lows.",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        <rect x="30" y="90" width="240" height="15" class="lux-zone-red"/>
        <line x1="30" y1="90" x2="270" y2="90" class="lux-line-red"/>
        <text x="150" y="100" text-anchor="middle" class="lux-text-red">SELL-SIDE LIQUIDITY (SELL STOPS BELOW SUPPORT)</text>
        
        {generate_bg_candles(12, 10, 6, 30, 2, 4, 4)[0]}
        {draw_seq([
            (50, 30, 25, 55), # Green
            (30, 60, 25, 65), # Red down
            (60, 80, 55, 85), # Hits support again
            (80, 105, 75, 110), # Sweeps SSL!
        ], 82, 15, 8)}
        {generate_bg_candles(20, 142, 6, 105, 0, 5, 4)[0]}
      </svg>
        '''
    },
    {
        "q": "What is the primary purpose of taking partial profits at key Liquidity levels?",
        "diff": "Medium",
        "options": [
            "To trigger algorithmic high-frequency trading traps.",
            "To offset the commission costs of the trade.",
            "To secure realized gains and fund your stop-loss risk in case the market reverses at that liquidity pool.",
            "To manipulate the options greeks favorably."
        ],
        "ans": 2,
        "exp_c": "Correct! When price reaches a major liquidity pool, it often reverses aggressively. Taking partials there guarantees you pay yourself and mitigates risk.",
        "exp_w": "Incorrect. Liquidity pools act like magnets but frequently cause sharp reversals once swept. Taking partials secures your profit before a potential reversal.",
        "svg": lambda: f'''
      <svg class="q-chart" viewBox="0 0 300 120" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="120" class="lux-bg"/>
        {draw_grid()}
        
        <!-- Target BSL -->
        <line x1="20" y1="30" x2="280" y2="30" class="lux-line-green"/>
        <text x="60" y="25" class="lux-text-green">BUY-SIDE LIQUIDITY</text>
        
        <!-- Entry OB -->
        <rect x="20" y="90" width="80" height="20" class="lux-zone-blue"/>
        <text x="60" y="102" text-anchor="middle" class="lux-text">ENTRY OB</text>
        
        {generate_bg_candles(10, 20, 6, 90, -3, 6, 4)[0]}
        {draw_seq([
            (50, 20, 15, 55), # Reaches BSL and partials
            (20, 60, 15, 65), # Aggressive reversal!
        ], 80, 15, 8)}
        {generate_bg_candles(20, 110, 6, 60, 1, 4, 4)[0]}
        
        <!-- Partial icon box -->
        <rect x="170" y="10" width="40" height="15" class="lux-signal-bg-up"/>
        <text x="190" y="20" text-anchor="middle" class="lux-text-green">TAKE PROFIT</text>
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

# Inject JS correctly so that arrays are mapped dynamically (just replace the lines matching the JS const definitions)
content = re.sub(r'const ANSWERS=\[.*?\];', answers_js, content)
content = re.sub(r'const EXPLANATIONS=\[\n.*?\n\];', explanations_js, content, flags=re.DOTALL)

with open(QUIZ_FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Quiz 1 extensively upgraded with 40-CANDLE REALISTIC BACKGROUNDS: {QUIZ_FILE}")
