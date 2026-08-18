from pathlib import Path
import shutil,re

site=Path('_site')
src=Path('overrides/navigation-v37-5.js')
if not src.exists():
    raise SystemExit('navigation-v37-5.js não encontrado')

shutil.copyfile(src,site/'navigation-v37-5.js')

exclude={'login.html','index.html','tv_producao.html','tv_setor.html','tv_geral.html'}
tag='<script src="navigation-v37-5.js?v=20260818-v37-5-menu-favoritos"></script>'
for html in site.glob('*.html'):
    if html.name in exclude:
        continue
    text=html.read_text(encoding='utf-8')
    if 'navigation-v37-5.js' not in text:
        text=text.replace('</body>',tag+'\n</body>',1)
    html.write_text(text,encoding='utf-8')

panel=site/'painel_producao.html'
if panel.exists():
    text=panel.read_text(encoding='utf-8')
    text=re.sub(r'<div class="version">versão \d+(?:\.\d+)?(?: • Supabase)?</div>','<div class="version">versão 37.5 • Supabase</div>',text,count=1)
    if 'v37.5-menu-favoritos-compacto' not in text:
        text+='\n<!-- v37.5-menu-favoritos-compacto -->\n'
    panel.write_text(text,encoding='utf-8')

js=(site/'navigation-v37-5.js').read_text(encoding='utf-8')
for token in ['let-erp-menu-group','let-erp-menu-star','menu_favoritos','body>.topbar']:
    if token not in js:
        raise SystemExit('Patch v37.5 incompleto: '+token)

# v37.6: acabamento visual, progresso e dashboard personalizável.
patch=Path('overrides/v37-6-design-patch.py')
if not patch.exists():
    raise SystemExit('Patch v37.6 não encontrado.')
exec(compile(patch.read_text(encoding='utf-8'),'overrides/v37-6-design-patch.py','exec'))
