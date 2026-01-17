import json
import random
import datetime
import textwrap
import os
from PIL import Image, ImageDraw, ImageFont

# config
QUOTES_FILE = 'quotes.json'
OUTPUT_FILE = 'wallpaper.png'
WIDTH = 1080
HEIGHT = 1920
BG_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 60
AUTHOR_FONT_SIZE = 40
MARGIN = 100

def get_quote_of_the_day():
    with open(QUOTES_FILE, 'r') as f:
        quotes = json.load(f)
    
    # Seeding with the date ensures the same quote is picked for the entire day
    # even if the script runs multiple times.
    today = datetime.date.today().isoformat()
    random.seed(today) 
    
    return random.choice(quotes)

def create_wallpaper(quote):
    # Create image
    img = Image.new('RGB', (WIDTH, HEIGHT), color=BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Load fonts (using a default font if custom isn't available, but try to find a nice one)
    # On Linux systems, DejaVuSans is usually available.
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", FONT_SIZE)
        author_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", AUTHOR_FONT_SIZE)
    except IOError:
         # Fallback to default if system fonts aren't found
        print("Warning: Custom fonts not found, using default.")
        font = ImageFont.load_default()
        author_font = ImageFont.load_default()

    text = quote['text']
    author = "- " + quote['author']

    # WRAPPING TEXT
    # This is a rudimentary wrap. For precise pixel-width wrapping, we'd measure text size.
    # standard avg char width approx FONT_SIZE/2? 
    # (WIDTH - 2*MARGIN) / (FONT_SIZE / 2)
    chars_per_line = int((WIDTH - 2 * MARGIN) / (FONT_SIZE * 0.5))
    
    lines = textwrap.wrap(text, width=chars_per_line)
    
    # Calculate total text height to center it vertically
    # Ascent/Descent issues aside, simply multiplying lines is a good heuristic
    line_height = font.getbbox("Ay")[3] + 15 # + padding
    total_height = len(lines) * line_height + author_font.getbbox("Ay")[3] + 50 # + gap for author
    
    current_y = (HEIGHT - total_height) / 2
    
    # Draw Quote
    for line in lines:
        # Center align each line
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x_pos = (WIDTH - text_width) / 2
        draw.text((x_pos, current_y), line, font=font, fill=TEXT_COLOR)
        current_y += line_height
        
    # Draw Author
    current_y += 30 # Gap
    bbox = draw.textbbox((0, 0), author, font=author_font)
    text_width = bbox[2] - bbox[0]
    x_pos = (WIDTH - text_width) / 2
    draw.text((x_pos, current_y), author, font=author_font, fill=TEXT_COLOR)
    
    img.save(OUTPUT_FILE)
    print(f"Generated {OUTPUT_FILE} with quote: {text[:30]}...")

if __name__ == "__main__":
    q = get_quote_of_the_day()
    create_wallpaper(q)
