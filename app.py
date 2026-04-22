"""
HODGE EXPLORER v2.0 - PRODUCT EDITION
Compare Mode | Auto Animation | Question Mode | Shareable
"""

from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS
from functools import lru_cache
import numpy as np
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# ============================================================================
# STORY MODE (Non-technical, engaging)
# ============================================================================

def get_story(rho):
    """Get story for given rho"""
    if rho == 1:
        return {
            'title': '🌿 The Blank Canvas',
            'story': 'This surface is like a blank canvas - almost no predetermined patterns exist. Only 1 out of 20 possible geometric patterns actually appear as real curves.',
            'analogy': 'Like a fresh sheet of paper - anything is possible, but nothing is fixed yet.',
            'emoji': '🌿'
        }
    elif rho == 20:
        return {
            'title': '✨ The Masterpiece',
            'story': 'This is the Fermat Quintic - a mathematical masterpiece! EVERY possible geometric pattern (all 20) actually exists as real curves on this surface.',
            'analogy': 'Like a perfectly cut diamond - every facet exists in reality.',
            'emoji': '✨'
        }
    elif rho <= 5:
        return {
            'title': '🌱 Emerging Patterns',
            'story': f'This surface has {rho} geometric patterns that actually exist. Most theoretical possibilities are still just possibilities.',
            'analogy': f'Like a garden with {rho} types of flowers starting to bloom.',
            'emoji': '🌱'
        }
    elif rho <= 12:
        return {
            'title': '🌳 Organized Structure',
            'story': f'This surface has {rho} real geometric patterns. It has enough structure to be interesting, but still room for surprises.',
            'analogy': f'Like a city with {rho} major roads - organized but not overwhelming.',
            'emoji': '🌳'
        }
    else:
        return {
            'title': '🏔️ Highly Organized',
            'story': f'This surface has {rho} real geometric patterns! Only {20-rho} possibilities remain unrealized.',
            'analogy': f'Like a master-planned community with {rho} completed buildings.',
            'emoji': '🏔️'
        }

# ============================================================================
# COMPARE MODE
# ============================================================================

def compare_surfaces(rho1, rho2):
    """Compare two surfaces side by side"""
    story1 = get_story(rho1)
    story2 = get_story(rho2)
    
    diff = rho2 - rho1
    if diff > 0:
        comparison_text = f"Surface 2 has {diff} MORE real patterns than Surface 1. It is more organized and constrained."
    elif diff < 0:
        comparison_text = f"Surface 1 has {abs(diff)} MORE real patterns than Surface 2. It is more organized."
    else:
        comparison_text = "Both surfaces have the same number of real patterns!"
    
    evolution = f"As we move from ρ={rho1} to ρ={rho2}, {abs(diff)} new geometric patterns become real."
    
    return {
        'surface1': {'rho': rho1, 'story': story1, 'algebraic': rho1, 'ratio': (rho1/20)*100},
        'surface2': {'rho': rho2, 'story': story2, 'algebraic': rho2, 'ratio': (rho2/20)*100},
        'difference': diff,
        'comparison': comparison_text,
        'evolution': evolution
    }

# ============================================================================
# QUESTION MODE (AI Tutor)
# ============================================================================

def answer_question(question, rho):
    """Simple AI tutor answers"""
    q_lower = question.lower()
    
    if 'ghost' in q_lower or 'transcendental' in q_lower:
        return f"Ghost patterns are mathematical possibilities that don't correspond to real curves. At ρ={rho}, {20-rho} out of 20 patterns are ghosts. Think of them as theoretical shapes that could exist but don't actually appear on this surface."
    
    elif 'algebraic' in q_lower or 'real' in q_lower:
        return f"Real patterns (algebraic cycles) are actual curves that exist on the surface. At ρ={rho}, {rho} out of 20 patterns are real. These are like the 'built' structures in our city analogy."
    
    elif 'increase' in q_lower or 'jump' in q_lower:
        return f"At special points (ρ=2,4,7,10,12,15,17,18,20), new patterns suddenly appear. These are called Noether–Lefschetz loci - moments in shape-space where new geometric structures emerge!"
    
    elif 'max' in q_lower or '20' in q_lower:
        return f"At ρ=20 (Fermat quintic), EVERY possible pattern becomes real! This is the most organized possible K3 surface. It's like a perfectly designed city where every possible building has been constructed."
    
    elif 'min' in q_lower or 'generic' in q_lower or '1' in q_lower:
        return f"At ρ=1 (generic surface), almost no patterns are real. Only 1 out of 20 possibilities actually exists. This is like a blank canvas - maximum freedom, minimum structure."
    
    else:
        return f"Great question! At ρ={rho}, we have {rho} real patterns and {20-rho} ghost patterns. The ratio of reality is {(rho/20)*100:.1f}%. Want to know more about a specific number? Try asking about ρ=1 (generic) or ρ=20 (maximal)!"

# ============================================================================
# SHAREABLE OUTPUT
# ============================================================================

def generate_shareable(rho):
    """Generate shareable text and stats"""
    story = get_story(rho)
    ratio = (rho/20)*100
    
    share_text = f"""
📐 HODGE EXPLORER

{story['emoji']} {story['title']}

{story['story']}

📊 Reality: {rho}/20 patterns ({ratio:.0f}%)
👻 Ghosts: {20-rho}/20 patterns ({100-ratio:.0f}%)

💡 {story['analogy']}

Explore yourself at: [Your URL]
    """
    
    return {
        'text': share_text,
        'hashtags': '#HodgeExplorer #MathVisualization #Geometry #Patterns',
        'rho': rho,
        'ratio': ratio
    }

# ============================================================================
# CACHED API DATA
# ============================================================================

@lru_cache(maxsize=128)
def get_cached_analysis(rho):
    """Cached analysis"""
    story = get_story(rho)
    ratio = (rho/20)*100
    return {
        'rho': rho,
        'algebraic': rho,
        'transcendental': 20 - rho,
        'ratio': round(ratio, 1),
        'story': story,
        'algebraic_signal': round(ratio, 1),
        'transcendental_component': round(100 - ratio, 1)
    }

@lru_cache(maxsize=32)
def get_nl_data():
    """NL loci data"""
    return [
        {"t": 0.12, "rho": 2, "name": "First Jump"},
        {"t": 0.23, "rho": 4, "name": "Second Jump"},
        {"t": 0.35, "rho": 7, "name": "Third Jump"},
        {"t": 0.48, "rho": 10, "name": "Fermat Point"},
        {"t": 0.58, "rho": 12, "name": "Shioda–Inose"},
        {"t": 0.69, "rho": 15, "name": "Mid Jump"},
        {"t": 0.79, "rho": 17, "name": "Kummer Point"},
        {"t": 0.88, "rho": 18, "name": "Barth–Nieto"},
        {"t": 0.95, "rho": 20, "name": "Fermat Max"}
    ]

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/')
def index():
    return render_template('dashboard_v2.html')

@app.route('/api/analyze')
def analyze():
    rho = int(request.args.get('rho', 10))
    data = get_cached_analysis(rho)
    
    nl_loci = get_nl_data()
    t_vals = np.linspace(0, 1, 200)
    nl_curve = []
    for t in t_vals:
        r = 1.0
        for locus in nl_loci:
            r += (locus['rho'] - 1) * np.exp(-((t - locus['t']) / 0.08)**4)
        nl_curve.append(min(20, max(1, r)))
    
    return jsonify({
        'analysis': data,
        'nl_loci': nl_loci,
        'nl_curve': {'t': t_vals.tolist(), 'rho': nl_curve}
    })

@app.route('/api/compare')
def compare():
    rho1 = int(request.args.get('rho1', 1))
    rho2 = int(request.args.get('rho2', 20))
    comparison = compare_surfaces(rho1, rho2)
    return jsonify(comparison)

@app.route('/api/ask')
def ask():
    question = request.args.get('q', '')
    rho = int(request.args.get('rho', 10))
    answer = answer_question(question, rho)
    return jsonify({'question': question, 'answer': answer, 'rho': rho})

@app.route('/api/share')
def share():
    rho = int(request.args.get('rho', 10))
    shareable = generate_shareable(rho)
    return jsonify(shareable)

@app.route('/api/export')
def export():
    rho = int(request.args.get('rho', 10))
    data = get_cached_analysis(rho)
    nl_loci = get_nl_data()
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    fig.suptitle(f'Hodge Explorer | {data["story"]["title"]}', fontsize=14, fontweight='bold')
    
    # Bar chart
    ax1 = axes[0, 0]
    ax1.bar(['Real Patterns', 'Ghost Patterns'], [rho, 20-rho], color=['#2ecc71', '#e74c3c'])
    ax1.set_ylim(0, 22)
    ax1.set_title(f'Reality: {rho}/20 patterns ({data["ratio"]}%)')
    
    # Ratio curve
    ax2 = axes[0, 1]
    rhos = list(range(1, 21))
    ratios = [(r/20)*100 for r in rhos]
    ax2.plot(rhos, ratios, 'b-', linewidth=2)
    ax2.plot(rho, data['ratio'], 'ro', markersize=10)
    ax2.set_xlabel('Organization Level (ρ)')
    ax2.set_ylabel('Reality Percentage (%)')
    ax2.set_title('How Reality Grows')
    
    # NL curve
    ax3 = axes[1, 0]
    t_vals = np.linspace(0, 1, 200)
    r_vals = []
    for t in t_vals:
        r = 1.0
        for locus in nl_loci:
            r += (locus['rho'] - 1) * np.exp(-((t - locus['t']) / 0.08)**4)
        r_vals.append(min(20, max(1, r)))
    ax3.plot(t_vals, r_vals, 'b-')
    for locus in nl_loci:
        ax3.axvline(x=locus['t'], color='red', linestyle='--', alpha=0.5)
    ax3.set_xlabel('Shape Space →')
    ax3.set_ylabel('Real Patterns (ρ)')
    ax3.set_title('Where New Patterns Emerge')
    
    # Story panel
    ax4 = axes[1, 1]
    ax4.axis('off')
    story_text = f"""{data['story']['emoji']} {data['story']['title']}

{data['story']['story']}

💡 {data['story']['analogy']}

📊 Reality: {data['ratio']}%
🎯 Real Patterns: {rho}/20
👻 Ghosts: {20-rho}/20

Generated by Hodge Explorer"""
    ax4.text(0.05, 0.95, story_text, transform=ax4.transAxes, 
             fontsize=9, verticalalignment='top', fontfamily='sans-serif')
    
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close()
    
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 HODGE EXPLORER v2.0 - PRODUCT EDITION")
    print("   Compare | Auto Animation | Question Mode | Shareable")
    print("="*60)
    print("\n✅ WOW Features:")
    print("   • Compare Two Surfaces (ρ=1 vs ρ=20)")
    print("   • Auto Animation Mode")
    print("   • Question Mode (AI Tutor)")
    print("   • Shareable Output")
    print("\n🌐 http://localhost:5007")
    print("\n💰 Ready for deployment!")
    print("="*60)
    app.run(debug=True, host='127.0.0.1', port=5007)