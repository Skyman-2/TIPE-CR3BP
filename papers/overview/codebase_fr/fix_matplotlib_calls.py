from pathlib import Path
import re
root = Path('c:/Users/yanni/Desktop/Personal Docs/Classes/translation_new')
for path in root.rglob('*.py'):
    text = path.read_text(encoding='utf-8')
    updated = re.sub(r'\.tracer\(', '.plot(', text)
    updated = re.sub(r'\.grille\(', '.grid(', updated)
    if updated != text:
        path.write_text(updated, encoding='utf-8')
