from PIL import Image
import glob
import os

# Define color thresholds for typical Google Maps traffic colors
def color_distance(c1, c2):
    return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5

def classify_pixel(r, g, b):
    # Base colors
    colors = {
        'green': (99, 214, 104),
        'orange': (255, 151, 77),
        'red': (242, 60, 50),
        'dark_red': (129, 31, 31),
        'bg': (240, 240, 240) # just an ignore threshold
    }
    
    # We only care if it's very close to one of the traffic colors
    # Traffic lines are quite pure
    min_dist = float('inf')
    best_color = None
    for name, color in colors.items():
        if name == 'bg': continue
        d = color_distance((r,g,b), color)
        if d < 40: # threshold for being a traffic line
            if d < min_dist:
                min_dist = d
                best_color = name
    return best_color

def analyze_image(path):
    try:
        img = Image.open(path).convert('RGB')
        # Crop the center to avoid UI elements (Live traffic bar at bottom, search bar at top)
        w, h = img.size
        # Crop middle 50%
        left = w * 0.25
        top = h * 0.25
        right = w * 0.75
        bottom = h * 0.75
        img = img.crop((left, top, right, bottom))
        
        counts = {'green': 0, 'orange': 0, 'red': 0, 'dark_red': 0}
        
        for pixel in img.getdata():
            c = classify_pixel(*pixel)
            if c:
                counts[c] += 1
                
        total = sum(counts.values())
        if total == 0:
            return 0.0, counts
            
        heavy = counts['orange'] + counts['red'] + counts['dark_red']
        return heavy / total, counts
    except Exception as e:
        print(f"Error analyzing {path}: {e}")
        return 0.0, {}

print("Analyzing Top 10...")
top_scores = []
for i in range(1, 11):
    path = f"screenshots/top_{i}.png"
    if os.path.exists(path):
        ratio, counts = analyze_image(path)
        top_scores.append(ratio)
        print(f"Top {i}: {ratio:.1%} heavy traffic {counts}")

print("\nAnalyzing Bottom 10...")
bot_scores = []
for i in range(1, 11):
    path = f"screenshots/bottom_{i}.png"
    if os.path.exists(path):
        ratio, counts = analyze_image(path)
        bot_scores.append(ratio)
        print(f"Bottom {i}: {ratio:.1%} heavy traffic {counts}")

if top_scores and bot_scores:
    avg_top = sum(top_scores) / len(top_scores)
    avg_bot = sum(bot_scores) / len(bot_scores)
    print(f"\nAverage Heavy Traffic Ratio - Top 10: {avg_top:.1%}")
    print(f"Average Heavy Traffic Ratio - Bottom 10: {avg_bot:.1%}")
