from pathlib import Path
import re
site=Path('_site')

# ------------------------------------------------------------
# Menu: módulos antigos também passam a respeitar permissões.
# ------------------------------------------------------------
theme=site/'theme.js'
s=theme.read_text(encoding='utf-8')

def add_perm(href,key):
    global s
    pattern=r'(\{href:"'+re.escape(href)+r'"[^\n\}]*?)(\})'
    m=re.search(pattern,s)
    if not m: return
    if 'perm:' in m.group(0) or 'adminOnly:' in m.group(0): return
    s=s[:m.start()]+m.group(1)+', perm:"'+key+'"'+m.group(2)+s[m.end():]

add_perm('novo_pedido.html','pedidos_criar')
add_perm('reenvios.html','pedidos_criar')
add_perm('analises.html','gestao')
add_perm('financeiro.html','financeiro')
add_perm('programacoes.html','gestao')
add_perm('estoque.html','estoque_gerenciar')
add_perm('atividades.html','gestao')
add_perm('expedicao.html','expedicao_gerenciar')

# v37.1: remove do menu os três módulos marcados pelo usuário.
for href in ('alertas.html','produtividade.html','gestao_producao.html'):
    s=re.sub(r'\n?\s*\{href:"'+re.escape(href)+r'"[^\n]*\},?', '', s)
for href in ('alertas.html','produtividade.html','gestao_producao.html'):
    if 'href:"'+href+'"' in s:
        raise SystemExit('Não foi possível remover do menu: '+href)

# v37.2: Expedição simples, somente retiradas e histórico.
s=re.sub(
    r'(\{href:"expedicao\.html"[^\n]*?sub:")[^"]*(")',
    r'\1Retiradas e histórico\2',
    s,
    count=1
)

theme.write_text(s,encoding='utf-8')

# ------------------------------------------------------------
# Central do Pedido: bloqueia os controles sem permissão.
# ------------------------------------------------------------
pedido=site/'pedido.html'
p=pedido.read_text(encoding='utf-8')
if 'function applyPermissionUIV37' not in p:
    marker='function pName(uid)'
    helper=r'''function applyPermissionUIV37(){
  const canEdit=!!perms.pedidos_editar;
  const canComment=!!perms.comentarios;
  const canFiles=!!perms.arquivos;
  const canQuality=!!perms.qualidade_aprovar;
  const canStock=!!(perms.estoque_gerenciar||perms.pedidos_editar);
  const setDisabled=(sel,disabled)=>document.querySelectorAll(sel).forEach(el=>{el.disabled=disabled;if(disabled)el.title='Sem permissão para esta ação';});
  setDisabled('#priority,#responsible,#pinned,#newTag,#saveSummary,#addTag,[data-rm-tag]',!canEdit);
  setDisabled('#commentText,#sendComment',!canComment);
  setDisabled('#fileInput,#fileDesc,#uploadFiles,[data-del-file]',!canFiles);
  setDisabled('[data-quality],#saveQuality',!canQuality);
  setDisabled('#stockItem,#stockQty,#addStock,#deductStock,[data-rm-stock]',!canStock);
  const undo=document.getElementById('undoBtn');if(undo)undo.style.display=perms.desfazer?'inline-flex':'none';
}
const permissionObserverV37=new MutationObserver(()=>applyPermissionUIV37());
permissionObserverV37.observe(document.body,{childList:true,subtree:true});
'''
    if marker not in p: raise SystemExit('Central do Pedido: marcador de funções não encontrado')
    p=p.replace(marker,helper+'\n'+marker,1)
    p=p.replace("await loadAll();await Promise.all([loadComments(),loadFiles(),loadStock(),loadHistory()]);", "await loadAll();await Promise.all([loadComments(),loadFiles(),loadStock(),loadHistory()]);applyPermissionUIV37();",1)
pedido.write_text(p,encoding='utf-8')

# ------------------------------------------------------------
# Painel: exclusão respeita a permissão visualmente.
# ------------------------------------------------------------
panel=site/'painel_producao.html'
pp=panel.read_text(encoding='utf-8')
if 'v37-permission-ui' not in pp:
    snippet=r'''
<script id="v37-permission-ui">
(function(){
  async function apply(){
    let tries=0;while(!window.letErpSupabase&&tries++<60)await new Promise(r=>setTimeout(r,100));
    if(!window.letErpSupabase)return;
    try{
      const {data:s}=await window.letErpSupabase.auth.getSession();const uid=s?.session?.user?.id;if(!uid)return;
      const {data}=await window.letErpSupabase.from('erp_permissoes').select('permissoes').eq('user_id',uid).maybeSingle();
      const pm=data?.permissoes||{};window.LET_ERP_PERMISSIONS=pm;
      const update=()=>{
        document.querySelectorAll('.delete-btn').forEach(b=>{b.style.display=pm.pedidos_excluir?'':'none'});
        document.querySelectorAll('.edit-btn').forEach(b=>{b.style.display=pm.pedidos_editar?'':'none'});
      };
      update();new MutationObserver(update).observe(document.body,{childList:true,subtree:true});
    }catch(e){console.warn('Permissões do painel:',e)}
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',apply);else apply();
})();
</script>
'''
    pp=pp.replace('</body>',snippet+'\n</body>',1)

pp=re.sub(r'<div class="version">versão \d+(?:\.\d+)?(?: • Supabase)?</div>','<div class="version">versão 37.3 • Supabase</div>',pp,count=1)
panel.write_text(pp,encoding='utf-8')

cache='20260818-v37-3-ficha-modelo'
for html in site.glob('*.html'):
    text=html.read_text(encoding='utf-8')
    text=re.sub(r'src="theme\.js(?:\?v=[^"]+)?"',f'src="theme.js?v={cache}"',text)
    text=re.sub(r'src="supabase-config\.js(?:\?v=[^"]+)?"',f'src="supabase-config.js?v={cache}"',text)
    html.write_text(text,encoding='utf-8')

with (site/'painel_producao.html').open('a',encoding='utf-8') as f:
    f.write('\n<!-- v37-role-permissions-enforced | compat-cache: 20260818-v37-factory-suite | v37.3-ficha-modelo -->\n')
