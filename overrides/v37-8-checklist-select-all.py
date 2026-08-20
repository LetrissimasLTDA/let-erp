from pathlib import Path
import re, shutil

site=Path('_site')
root=Path('overrides')
panel=site/'painel_producao.html'
text=panel.read_text(encoding='utf-8')

# ------------------------------------------------------------
# Botão "Marcar todos": instalação idempotente.
# O JavaScript também recria o controle em tempo de execução caso
# o modal seja redesenhado e remova o botão.
# ------------------------------------------------------------
old='<div class="quality-grid-v37" id="qualityGateGrid"></div>'
new='''<label id="qualityGateSelectAllWrap" data-let-erp-sticky-select-all="1" style="display:flex;align-items:center;gap:9px;border:1px solid #99f6e4;background:#f0fdfa;border-radius:10px;padding:10px 12px;margin:0 0 9px;font-size:10px;font-weight:950;color:#0f766e;cursor:pointer;flex:0 0 auto;visibility:visible;opacity:1"><input type="checkbox" id="qualityGateSelectAll" style="width:18px;height:18px;accent-color:#14b8a6;flex:0 0 auto"> MARCAR TODOS OS ITENS</label><div class="quality-grid-v37" id="qualityGateGrid"></div>'''

if 'id="qualityGateSelectAllWrap"' not in text:
    if old in text:
        text=text.replace(old,new,1)
    else:
        # Compatibilidade caso a classe/atributos do grid tenham mudado.
        pat=re.compile(r'(<div[^>]*id=["\']qualityGateGrid["\'][^>]*>)',re.I)
        m=pat.search(text)
        if not m:
            raise SystemExit('Checklist de qualidade não encontrado para adicionar Marcar Todos.')
        label=new.split('<div class="quality-grid-v37" id="qualityGateGrid"></div>',1)[0]
        text=text[:m.start()]+label+text[m.start():]

src=root/'checklist-select-all-v37-8.js'
if not src.exists():
    raise SystemExit('checklist-select-all-v37-8.js não encontrado')
shutil.copyfile(src,site/'checklist-select-all-v37-8.js')

cache='20260820-v37-8-1-sticky-select-all'
tag=f'<script src="checklist-select-all-v37-8.js?v={cache}"></script>'
if 'checklist-select-all-v37-8.js' not in text:
    pos=text.rfind('</body>')
    if pos<0:
        raise SystemExit('Fechamento do body não encontrado no painel.')
    text=text[:pos]+tag+'\n'+text[pos:]
else:
    text=re.sub(
        r'<script\s+src="checklist-select-all-v37-8\.js(?:\?v=[^"]*)?"\s*></script>',
        tag,
        text,
        count=1,
        flags=re.I
    )

if 'checklist-select-all-ready' not in text:
    text+='\n<!-- checklist-select-all-ready -->\n'
if 'checklist-select-all-sticky-v37-8-1' not in text:
    text+='\n<!-- checklist-select-all-sticky-v37-8-1 -->\n'
panel.write_text(text,encoding='utf-8')

js=(site/'checklist-select-all-v37-8.js').read_text(encoding='utf-8')
for token in ['qualityGateSelectAll','data-qv37','MutationObserver','createWrap','setInterval']:
    if token not in js:
        raise SystemExit('Checklist Marcar Todos incompleto: '+token)
