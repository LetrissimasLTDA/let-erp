from pathlib import Path
import shutil

site=Path('_site')
root=Path('overrides')
panel=site/'painel_producao.html'
text=panel.read_text(encoding='utf-8')

old='<div class="quality-grid-v37" id="qualityGateGrid"></div>'
new='''<label id="qualityGateSelectAllWrap" style="display:flex;align-items:center;gap:9px;border:1px solid #99f6e4;background:#f0fdfa;border-radius:10px;padding:10px 12px;margin:0 0 9px;font-size:10px;font-weight:950;color:#0f766e;cursor:pointer"><input type="checkbox" id="qualityGateSelectAll" style="width:18px;height:18px;accent-color:#14b8a6"> MARCAR TODOS OS ITENS</label><div class="quality-grid-v37" id="qualityGateGrid"></div>'''
if old not in text:
    raise SystemExit('Checklist de qualidade não encontrado para adicionar Marcar Todos.')
text=text.replace(old,new,1)

src=root/'checklist-select-all-v37-8.js'
if not src.exists():
    raise SystemExit('checklist-select-all-v37-8.js não encontrado')
shutil.copyfile(src,site/'checklist-select-all-v37-8.js')
tag='<script src="checklist-select-all-v37-8.js?v=20260820-checklist-select-all"></script>'
if 'checklist-select-all-v37-8.js' not in text:
    pos=text.rfind('</body>')
    if pos<0: raise SystemExit('Fechamento do body não encontrado no painel.')
    text=text[:pos]+tag+'\n'+text[pos:]

if 'checklist-select-all-ready' not in text:
    text+='\n<!-- checklist-select-all-ready -->\n'
panel.write_text(text,encoding='utf-8')

js=(site/'checklist-select-all-v37-8.js').read_text(encoding='utf-8')
for token in ['qualityGateSelectAll','data-qv37','MutationObserver']:
    if token not in js:
        raise SystemExit('Checklist Marcar Todos incompleto: '+token)
