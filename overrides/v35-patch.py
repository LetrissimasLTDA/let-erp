from pathlib import Path
import re
site=Path('_site')

# theme/navigation + badge visibility
theme=site/'theme.js'; s=theme.read_text(encoding='utf-8')
if 'href:"reenvios.html"' not in s:
    s=s.replace('    {href:"calendario_envios.html", icon:"🗓️", label:"Calendário de Envios", sub:"Agenda de saídas e quantidades"},\n    {href:"atividades.html", icon:"🧾", label:"Atividades", sub:"Quem alterou cada módulo"},',
'''    {href:"calendario_envios.html", icon:"🗓️", label:"Calendário de Envios", sub:"Agenda de saídas e quantidades"},
    {href:"reenvios.html", icon:"🔁", label:"Reenvios", sub:"Cadastrar e consultar reenvios"},
    {href:"atividades.html", icon:"🧾", label:"Atividades", sub:"Quem alterou cada módulo"},''',1)
if 'href:"limpeza_historicos.html"' not in s:
    s=s.replace('    {href:"acessos.html", icon:"🔐", label:"Gerenciar Acessos", sub:"Criar usuários e redefinir senhas", adminOnly:true},\n    {href:"perfil.html", icon:"👤", label:"Meu Perfil", sub:"Nome, setor e foto"}',
'''    {href:"acessos.html", icon:"🔐", label:"Gerenciar Acessos", sub:"Criar usuários e redefinir senhas", adminOnly:true},
    {href:"limpeza_historicos.html", icon:"🧹", label:"Limpeza de Históricos", sub:"Manutenção do banco de dados", adminOnly:true},
    {href:"perfil.html", icon:"👤", label:"Meu Perfil", sub:"Nome, setor e foto"}''',1)
s=s.replace('.let-erp-developer-badge{width:16px;height:16px;object-fit:contain;display:inline-block;vertical-align:middle;flex:0 0 auto;cursor:help}', '.let-erp-developer-badge{width:18px;height:18px;object-fit:contain;display:inline-block;vertical-align:middle;flex:0 0 auto;cursor:help;border-radius:4px;box-shadow:0 0 0 1px rgba(15,118,110,.18)}',1)
s=s.replace('.let-erp-chat-author .let-erp-developer-badge{width:13px;height:13px}', '.let-erp-chat-author .let-erp-developer-badge{width:15px;height:15px}',1)
theme.write_text(s,encoding='utf-8')

# painel - reenvio como pedido normal com etiqueta amarela
panel=site/'painel_producao.html'; s=panel.read_text(encoding='utf-8')
if '.reenvio-tag{' not in s:
    s=s.replace('.chip{background:#f1f5f9;border-radius:7px;padding:5px 8px;font-size:11px;font-weight:800}', '.chip{background:#f1f5f9;border-radius:7px;padding:5px 8px;font-size:11px;font-weight:800}\n.reenvio-tag{display:inline-flex;align-items:center;gap:4px;background:#fef08a;color:#854d0e;border:1px solid #fde047;border-radius:999px;padding:4px 8px;font-size:9px;font-weight:950;cursor:pointer;margin-left:6px;vertical-align:middle}.reenvio-tag:hover{background:#fde047}',1)
if 'typeof p.ehReenvio' not in s:
    s=s.replace('  if(!p.status)p.status="Aguardando";\n  return p;', '  if(!p.status)p.status="Aguardando";\n  if(typeof p.ehReenvio!=="boolean")p.ehReenvio=false;\n  p.reenvioId=p.reenvioId||null;\n  return p;',1)
if 'ehReenvio:!!r.eh_reenvio' not in s:
    s=s.replace('    producaoSegundosAcumulados:Number(r.producao_segundos_acumulados||0),producaoHistorico:r.producao_historico||[],\n    criadoEm:r.criado_em,atualizadoEm:r.atualizado_em', '    producaoSegundosAcumulados:Number(r.producao_segundos_acumulados||0),producaoHistorico:r.producao_historico||[],\n    ehReenvio:!!r.eh_reenvio,reenvioId:r.reenvio_id||null,\n    criadoEm:r.criado_em,atualizadoEm:r.atualizado_em',1)
if 'eh_reenvio:!!p.ehReenvio' not in s:
    s=s.replace('    producao_segundos_acumulados:Number(p.producaoSegundosAcumulados)||0,producao_historico:p.producaoHistorico||[],\n    criado_em:p.criadoEm||new Date().toISOString()', '    producao_segundos_acumulados:Number(p.producaoSegundosAcumulados)||0,producao_historico:p.producaoHistorico||[],\n    eh_reenvio:!!p.ehReenvio,reenvio_id:p.reenvioId||null,\n    criado_em:p.criadoEm||new Date().toISOString()',1)
if 'function reenvioTag(p)' not in s:
    s=s.replace('function cardStatus(p){','''function reenvioTag(p){
  if(!p?.ehReenvio||!p?.reenvioId)return "";
  return '<button class="reenvio-tag" type="button" onclick="event.stopPropagation();location.href=\\'reenvios.html?id='+encodeURIComponent(String(p.reenvioId))+'\\'">🔁 REENVIO</button>';
}

function cardStatus(p){''',1)
s=s.replace("      '<div class=\"order\">PEDIDO #'+escapeHtml(p.id||\"-\")+'</div>'+", "      '<div class=\"order\">PEDIDO #'+escapeHtml(p.id||\"-\")+reenvioTag(p)+'</div>'+",1)
patterns=[
("      '<strong>Pedido #'+escapeHtml(p.id)+' • '+escapeHtml(p.cliente||\"Sem cliente\")+'</strong>'+\n        '<span class=\"search-status ","      '<strong>Pedido #'+escapeHtml(p.id)+' • '+escapeHtml(p.cliente||\"Sem cliente\")+'</strong>'+reenvioTag(p)+\n        '<span class=\"search-status "),
("      '<strong>Pedido #'+escapeHtml(p.id)+' • '+escapeHtml(p.cliente||\"Sem cliente\")+'</strong>'+\n      '<small>Etapa atual:","      '<strong>Pedido #'+escapeHtml(p.id)+' • '+escapeHtml(p.cliente||\"Sem cliente\")+'</strong>'+reenvioTag(p)+\n      '<small>Etapa atual:"),
("      '<strong>Pedido #'+escapeHtml(p.id)+' • '+escapeHtml(p.cliente||\"Sem cliente\")+'</strong>'+\n      '<small>'+escapeHtml(finalText)","      '<strong>Pedido #'+escapeHtml(p.id)+' • '+escapeHtml(p.cliente||\"Sem cliente\")+'</strong>'+reenvioTag(p)+\n      '<small>'+escapeHtml(finalText)")]
for a,b in patterns:s=s.replace(a,b,1)
s=re.sub(r'<div class="version">versão \d+(?: • Supabase)?</div>','<div class="version">versão 35 • Supabase</div>',s,count=1)
panel.write_text(s,encoding='utf-8')

# edição de pedido preserva vínculo de reenvio
np=site/'novo_pedido.html'; s=np.read_text(encoding='utf-8')
if 'eh_reenvio:!!p.ehReenvio' not in s:
    s=s.replace('      producao_segundos_acumulados:Number(p.producaoSegundosAcumulados)||0,producao_historico:p.producaoHistorico||[],\n      criado_em:p.criadoEm||new Date().toISOString()', '      producao_segundos_acumulados:Number(p.producaoSegundosAcumulados)||0,producao_historico:p.producaoHistorico||[],\n      eh_reenvio:!!p.ehReenvio,reenvio_id:p.reenvioId||null,\n      criado_em:p.criadoEm||new Date().toISOString()',1)
if 'ehReenvio:!!pedidoOriginal.ehReenvio' not in s:
    s=s.replace('        entregueMarketplace:!!pedidoOriginal.entregueMarketplace,\n        criadoEm:pedidoOriginal.criadoEm||new Date().toISOString()', '        entregueMarketplace:!!pedidoOriginal.entregueMarketplace,\n        ehReenvio:!!pedidoOriginal.ehReenvio,reenvioId:pedidoOriginal.reenvioId||null,\n        criadoEm:pedidoOriginal.criadoEm||new Date().toISOString()',1)
old='''      if(modoEdicao&&idOriginal&&String(idOriginal)!==String(pedido.id)){
        const {error:deleteOldError}=await db.from("pedidos").delete().eq("id",String(idOriginal));
        if(deleteOldError)throw new Error(deleteOldError.message);
      }'''
if old in s:
    s=s.replace(old,'''      if(modoEdicao&&idOriginal&&String(idOriginal)!==String(pedido.id)){
        if(pedido.ehReenvio&&pedido.reenvioId){
          const {error:reLinkError}=await db.from("reenvios").update({pedido_id:String(pedido.id)}).eq("id",pedido.reenvioId);
          if(reLinkError)throw new Error(reLinkError.message);
        }
        const {error:deleteOldError}=await db.from("pedidos").delete().eq("id",String(idOriginal));
        if(deleteOldError)throw new Error(deleteOldError.message);
      }''',1)
np.write_text(s,encoding='utf-8')

# login: registra acesso bem sucedido
login=site/'login.html'; s=login.read_text(encoding='utf-8')
if "from('acessos_log')" not in s:
    old="  const p=await letErpGetCurrentProfile();\n  location.replace(letErpProfileComplete(p)?next:'perfil.html?next='+encodeURIComponent(next));"
    idx=s.rfind(old)
    if idx!=-1:
        new="  const {data:userData}=await letErpSupabase.auth.getUser();\n  if(userData?.user){try{await letErpSupabase.from('acessos_log').insert({usuario_id:userData.user.id,email:userData.user.email||email});}catch(e){}}\n  const p=await letErpGetCurrentProfile();\n  location.replace(letErpProfileComplete(p)?next:'perfil.html?next='+encodeURIComponent(next));"
        s=s[:idx]+new+s[idx+len(old):]
login.write_text(s,encoding='utf-8')

# atividades: novos módulos
act=site/'atividades.html'; s=act.read_text(encoding='utf-8')
s=s.replace('<option value="material_mkt">Material MKT</option><option value="perfis">Perfis</option>', '<option value="material_mkt">Material MKT</option><option value="reenvios">Reenvios</option><option value="reenvio_provas">Provas de Reenvio</option><option value="perfis">Perfis</option>',1)
s=s.replace('material_mkt:"Material MKT",perfis:"Perfis"','material_mkt:"Material MKT",reenvios:"Reenvios",reenvio_provas:"Provas de Reenvio",perfis:"Perfis"',1)
s=s.replace('if(log.tabela==="material_mkt")return "Material MKT • Pedido #"+(d.pedido_id||"-");if(log.tabela==="perfis")','if(log.tabela==="material_mkt")return "Material MKT • Pedido #"+(d.pedido_id||"-");if(log.tabela==="reenvios")return "Reenvio • Pedido #"+(d.pedido_id||"-");if(log.tabela==="reenvio_provas")return "Prova de Reenvio #"+(d.reenvio_id||"-");if(log.tabela==="perfis")',1)
act.write_text(s,encoding='utf-8')

cache='20260817-v35-reenvios-limpeza'
for html in site.glob('*.html'):
    text=html.read_text(encoding='utf-8')
    text=re.sub(r'src="theme\.js(?:\?v=[^"]+)?"',f'src="theme.js?v={cache}"',text)
    text=re.sub(r'src="supabase-config\.js(?:\?v=[^"]+)?"',f'src="supabase-config.js?v={cache}"',text)
    html.write_text(text,encoding='utf-8')
