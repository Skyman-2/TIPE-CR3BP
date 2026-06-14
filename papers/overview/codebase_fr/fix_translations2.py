from pathlib import Path
import re
root = Path('c:/Users/yanni/Desktop/Personal Docs/Classes/translation_new')
replacements = {
    'barycentre': 'barycentre',
    'rayon_dans_le_temps': 'rayon_dans_le_temps',
    'energie1': 'energie1',
    'energie2': 'energie2',
    'energie3': 'energie3',
    'etiquettes_graph': 'etiquettes_graph',
    'energie_potentielle': 'energie_potentielle',
    'energie_cinetique': 'energie_cinetique',
    'resultat': 'resultat',
}

for path in root.rglob('*.py'):
    text = path.read_text(encoding='utf-8')
    updated = text
    for old, new in replacements.items():
        updated = re.sub(rf'\b{re.escape(old)}\b', new, updated)
    if updated != text:
        path.write_text(updated, encoding='utf-8')

systems = root / 'systems.json'
text = systems.read_text(encoding='utf-8')
new_text = re.sub(r'"barycentre"', '"barycentre"', text)
if new_text != text:
    systems.write_text(new_text, encoding='utf-8')
