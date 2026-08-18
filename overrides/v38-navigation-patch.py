from pathlib import Path
import shutil,re,subprocess

site=Path('_site')
src=Path('overrides/navigation-v38.js')
if not src.exists():
    raise SystemExit('navigation-v38.js não encontrado.')

nav=site/'navigation-v38.js'
shutil.copyfile(src,nav)

r=subprocess.run(['node','--check',str(nav)],capture_output=True,text=True)
if r.returncode:
    raise SystemExit('navigation-v38.js inválido: '+r.stderr)

tag='<script src="navigation-v38.js?v=20260818-v38-navigation-ux"></script>'
skip={'login.html','index.html','tv_producao.html','tv_setor.html','tv_geral.html'}
for html in site.glob('*.html'):
    if html.name in skip:
        continue
    txt=html.read_text(encoding='utf-8')
    if tag not in txt:
        txt=txt.replace('</body>',tag+'\n</body>',1)
    html.write_text(txt,encoding='utf-8')

panel=site/'painel_producao.html'
if panel.exists():
    p=panel.read_text(encoding='utf-8')
    p=re.sub(
        r'<div class="version">versão \d+(?:\.\d+)?(?: • Supabase)?</div>',
        '<div class="version">versão 38 • Supabase</div>\n<!-- compat: versão 37 -->',
        p,count=1
    )
    if 'v38-navigation-ux' not in p:
        p+='\n<!-- v38-navigation-ux -->\n'
    panel.write_text(p,encoding='utf-8')

cache='20260818-v38-navigation-ux'
for html in site.glob('*.html'):
    txt=html.read_text(encoding='utf-8')
    txt=re.sub(r'src="theme\.js(?:\?v=[^"]+)?"',f'src="theme.js?v={cache}"',txt)
    txt=re.sub(r'src="supabase-config\.js(?:\?v=[^"]+)?"',f'src="supabase-config.js?v={cache}"',txt)
    html.write_text(txt,encoding='utf-8')

js=nav.read_text(encoding='utf-8')
for token in ['LET_ERP_V38_NAVIGATION_UX','v38-search','v38-crumbwrap','menu_favoritos','v38-group']:
    if token not in js:
        raise SystemExit('v38 incompleta: '+token)
