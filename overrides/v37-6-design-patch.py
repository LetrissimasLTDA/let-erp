from pathlib import Path
import shutil,re

site=Path('_site')
src=Path('overrides/design-v37-6.js')
if not src.exists():
    raise SystemExit('design-v37-6.js não encontrado')

shutil.copyfile(src,site/'design-v37-6.js')
exclude={'login.html','index.html','tv_producao.html','tv_setor.html','tv_geral.html'}
tag='<script src="design-v37-6.js?v=20260818-v37-6-design-ux"></script>'
for html in site.glob('*.html'):
    if html.name in exclude:
        continue
    text=html.read_text(encoding='utf-8')
    if 'design-v37-6.js' not in text:
        text=text.replace('</body>',tag+'\n</body>',1)
    html.write_text(text,encoding='utf-8')

panel=site/'painel_producao.html'
if panel.exists():
    text=panel.read_text(encoding='utf-8')
    text=re.sub(r'<div class="version">versão \d+(?:\.\d+)?(?: • Supabase)?</div>','<div class="version">versão 37.6 • Supabase</div>',text,count=1)
    if 'v37.6-design-ux' not in text:
        text+='\n<!-- v37.6-design-ux -->\n'
    panel.write_text(text,encoding='utf-8')

js=(site/'design-v37-6.js').read_text(encoding='utf-8')
for token in ['erp-order-progress','erp-customize-btn','dashboard_preferencias','erpFadeUp','--erp-aqua','erp-ui-icon']:
    if token not in js:
        raise SystemExit('Patch v37.6 incompleto: '+token)
