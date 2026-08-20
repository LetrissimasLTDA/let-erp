from pathlib import Path
import re, shutil

site=Path('_site')
root=Path('overrides')

# ------------------------------------------------------------
# 1) Central do Pedido: move o JavaScript inline para arquivo externo.
# Isso evita que qualquer conteúdo HTML usado nas funções de impressão
# seja interpretado pelo navegador como parte da própria página.
# ------------------------------------------------------------
pedido=site/'pedido.html'
text=pedido.read_text(encoding='utf-8')
pat=re.compile(r'<script>\s*(const db=letErpSupabase;[\s\S]*?init\(\);)\s*</script>',re.S)
m=pat.search(text)
if not m:
    raise SystemExit('Não foi possível localizar o JavaScript inline da Central do Pedido.')
js=m.group(1).strip()+"\n"
(site/'pedido-central.js').write_text(js,encoding='utf-8')
external='<script src="pedido-central.js?v=20260820-v37-7-central-fix"></script>'
text=text[:m.start()]+external+text[m.end():]
pedido.write_text(text,encoding='utf-8')

# ------------------------------------------------------------
# 2) Painel: finalização robusta e sincronização de atrasos.
# ------------------------------------------------------------
src=root/'stability-v37-7.js'
if not src.exists():
    raise SystemExit('stability-v37-7.js não encontrado')
shutil.copyfile(src,site/'stability-v37-7.js')
panel=site/'painel_producao.html'
p=panel.read_text(encoding='utf-8')
tag='<script src="stability-v37-7.js?v=20260820-v37-9-finalize-race-fix"></script>'
if 'stability-v37-7.js' not in p:
    pos=p.rfind('</body>')
    if pos<0: raise SystemExit('Fechamento do body não encontrado no painel.')
    p=p[:pos]+tag+'\n'+p[pos:]
p=re.sub(r'<div class="version">versão \d+(?:\.\d+)?(?: • Supabase)?</div>','<div class="version">versão 37.7 • Supabase</div>',p,count=1)
if 'v37.7-stability-fixes' not in p:
    p+='\n<!-- v37.7-stability-fixes -->\n'
panel.write_text(p,encoding='utf-8')

# Validações mínimas.
central=(site/'pedido-central.js').read_text(encoding='utf-8')
for token in ['function printSheet()','function printLabel()','async function loadAll()','init();']:
    if token not in central:
        raise SystemExit('Central externa incompleta: '+token)
for token in ['finalizar_pedido_erp','marcar_atrasos_automaticos','window.finalizarPedido','installQualityFinalizeFix','ensureFinalized']:
    if token not in (site/'stability-v37-7.js').read_text(encoding='utf-8'):
        raise SystemExit('Correção v37.7 incompleta: '+token)
