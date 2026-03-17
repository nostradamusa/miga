import os
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix encoding garbage
html = html.replace('ΓÇö', '—')
html = html.replace('ΓöÇ', '─')
html = html.replace('ΓåÆ', '→')
html = html.replace('≡ƒÄ»', '🎯')
html = html.replace('<strong>23</strong> QUESTIONS', '<strong>15</strong> QUESTIONS')
html = html.replace('<strong>25</strong> QUESTIONS', '<strong>15</strong> QUESTIONS')

# Increase elegance of hero.
html = html.replace('.hero-backdrop-logo {', '.hero-backdrop-logo {\n    opacity: 0.15;\n    width: 800px;\n    mix-blend-mode: screen;\n')

# Add quotes banner
quotes_html = '''
<!-- ── QUOTES BANNER ── -->
<div class="quotes-banner">
  <div class="quote-track">
    <span>"The goal of a successful trader is to make the best trades. Money is secondary." — Alexander Elder</span>
    <span class="separator">♦</span>
    <span>"Risk comes from not knowing what you're doing." — Warren Buffett</span>
    <span class="separator">♦</span>
    <span>"In trading, what is comfortable is rarely profitable." — Robert Arnott</span>
    <span class="separator">♦</span>
    <span>"Amateurs think about how much money they can make. Professionals think about how much money they could lose." — Jack Schwager</span>
  </div>
</div>
'''

quotes_css = '''
  /* ── QUOTES BANNER ── */
  .quotes-banner {
    background: var(--dark);
    border-bottom: 1px solid var(--dark4);
    padding: 12px 0;
    overflow: hidden;
    position: relative;
    white-space: nowrap;
  }
  .quote-track {
    display: inline-block;
    padding-left: 100%;
    animation: marquee 30s linear infinite;
    font-size: 0.85rem;
    color: var(--muted);
    font-family: 'Barlow', sans-serif;
    letter-spacing: 1px;
    text-transform: uppercase;
  }
  .quote-track span {
    margin: 0 15px;
  }
  .quote-track .separator {
    color: var(--red);
    font-size: 0.7rem;
  }
  @keyframes marquee {
    0%   { transform: translate(0, 0); }
    100% { transform: translate(-100%, 0); }
  }
  /* ── RULES BAR ── */
'''

if 'quotes-banner' not in html:
    html = html.replace('/* ── RULES BAR ── */', quotes_css)
    html = html.replace('<!-- ── RULES BAR ── -->', quotes_html + '\n<!-- ── RULES BAR ── -->')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Fixed encodings, question counts, and added quotes banner.')
