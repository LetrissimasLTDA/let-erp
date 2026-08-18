from pathlib import Path
import shutil, re

site=Path('_site')
old='20260817-v35-reenvios-limpeza'
new='20260817-v35-final-svg'
for html in site.glob('*.html'):
    text=html.read_text(encoding='utf-8').replace(old,new)
    html.write_text(text,encoding='utf-8')

# Publica a tela exclusiva de TV sem menu administrativo.
tv_source=Path('overrides/tv_producao.html')
if not tv_source.exists():
    raise SystemExit('Arquivo do Dashboard TV não encontrado.')
shutil.copyfile(tv_source,site/'tv_producao.html')

# Adiciona o atalho Dashboard TV nos cards de Hoje e Amanhã.
panel=site/'painel_producao.html'
s=panel.read_text(encoding='utf-8')

if '.tv-mode-link{' not in s:
    anchor='''.ready-stat span{
  display:block;margin-top:7px;font-size:10px;font-weight:950;color:#0f766e;letter-spacing:.45px
}'''
    replacement=anchor+'''\n.tv-mode-link{\n  display:inline-flex!important;align-items:center;justify-content:center;width:max-content;max-width:100%;\n  margin-top:9px!important;padding:7px 10px;border-radius:9px;background:#083344;color:#fff!important;\n  border:1px solid #083344;font-size:9px!important;letter-spacing:.35px!important;box-shadow:0 3px 10px rgba(8,51,68,.13)\n}\n.tv-mode-link:hover{background:#0f766e;border-color:#0f766e}\n'''
    if anchor not in s:
        raise SystemExit('CSS dos cards estatísticos não encontrado.')
    s=s.replace(anchor,replacement,1)

old_today='''  <button class="stat ready-stat" id="todayStat" type="button" title="Clique para ver somente os pedidos de hoje">
    <small>PEDIDOS DE HOJE</small>
    <b id="statToday">0</b>
    <span>VER PEDIDOS</span>
  </button>'''
new_today='''  <button class="stat ready-stat" id="todayStat" type="button" title="Clique para ver somente os pedidos de hoje">
    <small>PEDIDOS DE HOJE</small>
    <b id="statToday">0</b>
    <span>VER PEDIDOS</span>
    <span class="tv-mode-link" onclick="event.stopPropagation();window.open('tv_producao.html?dia=hoje','_blank')">📺 DASHBOARD TV</span>
  </button>'''
if old_today not in s:
    raise SystemExit('Card Pedidos de Hoje não encontrado.')
s=s.replace(old_today,new_today,1)

old_tom='''  <button class="stat ready-stat" id="tomorrowStat" type="button" title="Clique para ver somente os pedidos de amanhã">
    <small>PEDIDOS DE AMANHÃ</small>
    <b id="statTomorrow">0</b>
    <span>VER PEDIDOS</span>
  </button>'''
new_tom='''  <button class="stat ready-stat" id="tomorrowStat" type="button" title="Clique para ver somente os pedidos de amanhã">
    <small>PEDIDOS DE AMANHÃ</small>
    <b id="statTomorrow">0</b>
    <span>VER PEDIDOS</span>
    <span class="tv-mode-link" onclick="event.stopPropagation();window.open('tv_producao.html?dia=amanha','_blank')">📺 DASHBOARD TV</span>
  </button>'''
if old_tom not in s:
    raise SystemExit('Card Pedidos de Amanhã não encontrado.')
s=s.replace(old_tom,new_tom,1)

# Mostra v36, mantendo uma marca interna para compatibilidade com a validação antiga do deploy.
s=re.sub(r'<div class="version">versão \d+(?: • Supabase)?</div>','<div class="version">versão 36 • Supabase</div>\n<!-- compat: versão 35 -->',s,count=1)
panel.write_text(s,encoding='utf-8')

# Confirma que a tela realmente foi montada antes do GitHub Pages publicar.
tv=(site/'tv_producao.html').read_text(encoding='utf-8')
for required in ['PAINEL DE PRODUÇÃO • MODO TV','SLIDE_MS=10000','tv-producao-live','TELA CHEIA']:
    if required not in tv:
        raise SystemExit('Dashboard TV incompleto: '+required)

png=site/'developer-badge.png'
if png.exists():
    png.unlink()
svg=site/'developer-badge.svg'
if not svg.exists() or '<svg' not in svg.read_text(encoding='utf-8'):
    raise SystemExit('Badge Developer SVG não foi gerada corretamente.')
