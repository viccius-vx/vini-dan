import json
from bs4 import BeautifulSoup
import re
from deep_translator import GoogleTranslator
import time
import sys
from bs4 import BeautifulSoup, Comment, Doctype

# Load HTML
file_path = "c:/Users/rian9/Downloads/GLP1 - SITE/gentlemobility-modern-copy/index.html"
with open(file_path, "r", encoding="utf-8") as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, "lxml")

translator = GoogleTranslator(source='auto', target='es')

# We want to translate text nodes within these tags
# Exclude script, style, and comments
tags_with_text = soup.find_all(string=True)
count = 0
total_translated = 0

for text_node in tags_with_text:
    if isinstance(text_node, Comment) or isinstance(text_node, Doctype):
        continue
    parent = text_node.parent
    if parent.name in ['style', 'script', 'title', 'meta', 'link']:
        continue
    
    text = str(text_node).strip()
    if text and len(sys.argv) > 1 and sys.argv[1] == 'count':
        count += 1
        continue

    # simple heuristic: if it has alphabet characters in it
    if text and re.search(r'[a-zA-Z\u00C0-\u00FF]', text):
        try:
            # Check if text is just a placeholder or number
            if len(text) > 1:
                translated = translator.translate(text)
                if translated and translated != text:
                    text_node.replace_with(text_node.replace(text, translated))
                    total_translated += 1
                    sys.stdout.write(f"Translated: {text[:30]}... -> {translated[:30]}...\n")
                    # Sleep briefly to avoid rate limiting
                    time.sleep(0.1)
        except Exception as e:
            sys.stdout.write(f"Error on {text[:30]}: {e}\n")

if len(sys.argv) > 1 and sys.argv[1] == 'count':
    print(f"Total phrases found to translate: {count}")
    sys.exit(0)

# Write back
with open(file_path, "w", encoding="utf-8") as f:
    f.write(str(soup))
print(f"Finished translation. Total translated strings: {total_translated}")
