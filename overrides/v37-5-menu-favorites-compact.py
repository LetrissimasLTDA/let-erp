from pathlib import Path
import shutil,re

site=Path('_site')
src=Path('overrides/navigation-v37-5.js')
if not src.exists():
    raise SystemExit('navigation-v37-5.js não encontrado')

shutil.copyfile(src,site/'navigation-v37-5.js')

exclude={'login.html','index.html','tv_producao.html','tv_setor.html','tv_geral.html'}
tag='<script src="navigation-v37-5.js?v=20260820-v37-5-2-menu-restaurado"></script>'
for html in site.glob('*.html'):
    if html.name in exclude:
        continue
    text=html.read_text(encoding='utf-8')
    if 'navigation-v37-5.js' not in text:
        pos=text.rfind('</body>')
        if pos<0:
            raise SystemExit('Fechamento </body> não encontrado em '+html.name)
        text=text[:pos]+tag+'\n'+text[pos:]
    else:
        text=re.sub(r'<script\s+src="navigation-v37-5\.js(?:\?v=[^"]*)?"\s*></script>',tag,text,count=1,flags=re.I)
    html.write_text(text,encoding='utf-8')

panel=site/'painel_producao.html'
if panel.exists():
    text=panel.read_text(encoding='utf-8')
    if 'v37.5.2-menu-restaurado' not in text:
        text+='\n<!-- v37.5.2-menu-restaurado -->\n'
    panel.write_text(text,encoding='utf-8')

js=(site/'navigation-v37-5.js').read_text(encoding='utf-8')
for token in ['let-erp-menu-group','let-erp-menu-star','menu_favoritos','body>.topbar','Gerenciar Acessos','Expedição','Reenvios','hydrateProfile']:
    if token not in js:
        raise SystemExit('Patch v37.5.2 incompleto: '+token)
