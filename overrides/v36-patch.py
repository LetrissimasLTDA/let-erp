from pathlib import Path
import re
site=Path('_site')
panel=site/'painel_producao.html'
s=panel.read_text(encoding='utf-8')

# Visual do atalho de Dashboard TV dentro dos cards Hoje/Amanhã
if '.tv-mode-link{' not in s:
    anchor='''.ready-stat span{
  display:block;margin-top:7px;font-size:10px;font-weight:950;color:#0f766e;letter-spacing:.45px
}'''
    replacement=anchor+'''\n.tv-mode-link{\n  display:inline-flex!important;align-items:center;justify-content:center;width:max-content;max-width:100%;\n  margin-top:9px!important;padding:7px 10px;border-radius:9px;background:#083344;color:#fff!important;\n  border:1px solid #083344;font-size:9px!important;letter-spacing:.35px!important;box-shadow:0 3px 10px rgba(8,51,68,.13)\n}\n.tv-mode-link:hover{background:#0f766e;border-color:#0f766e}\n'''
    if anchor not in s:
        raise SystemExit('CSS dos cards estatísticos não encontrado')
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
    raise SystemExit('Card Pedidos de Hoje não encontrado')
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
    raise SystemExit('Card Pedidos de Amanhã não encontrado')
s=s.replace(old_tom,new_tom,1)

s=re.sub(r'<div class="version">versão \d+(?: • Supabase)?</div>','<div class="version">versão 36 • Supabase</div>',s,count=1)
panel.write_text(s,encoding='utf-8')

# Novo cache para forçar todos os computadores a receberem a v36
cache='20260818-v36-tv-dashboard'
for html in site.glob('*.html'):
    text=html.read_text(encoding='utf-8')
    text=re.sub(r'src="theme\.js(?:\?v=[^"]+)?"',f'src="theme.js?v={cache}"',text)
    text=re.sub(r'src="supabase-config\.js(?:\?v=[^"]+)?"',f'src="supabase-config.js?v={cache}"',text)
    html.write_text(text,encoding='utf-8')
