from pathlib import Path
site=Path('_site')
old='20260817-v35-reenvios-limpeza'
new='20260817-v35-final-svg'
for html in site.glob('*.html'):
    text=html.read_text(encoding='utf-8').replace(old,new)
    html.write_text(text,encoding='utf-8')
png=site/'developer-badge.png'
if png.exists():
    png.unlink()
svg=site/'developer-badge.svg'
if not svg.exists() or '<svg' not in svg.read_text(encoding='utf-8'):
    raise SystemExit('Badge Developer SVG não foi gerada corretamente.')
