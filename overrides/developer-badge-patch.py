from pathlib import Path
import shutil, re

site=Path("_site")

badge_source=Path("overrides/developer-badge.png")
if not badge_source.exists() or badge_source.stat().st_size < 100:
    raise SystemExit("Insígnia Developer PNG inválida.")
shutil.copyfile(badge_source, site/"developer-badge.png")

theme=site/"theme.js"
s=theme.read_text(encoding="utf-8")

anchor='''    .let-erp-user-info strong{display:block;font-size:11px;font-weight:950;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
    .let-erp-user-info span{display:block;font-size:9px;color:#0f766e;font-weight:900;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'''
replacement='''    .let-erp-user-info strong{display:block;font-size:11px;font-weight:950;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
    .let-erp-user-info #drawerUserName{display:flex;align-items:center;gap:5px;min-width:0}
    .let-erp-developer-badge{width:16px;height:16px;object-fit:contain;display:inline-block;vertical-align:middle;flex:0 0 auto;cursor:help}
    .let-erp-chat-author .let-erp-developer-badge{width:13px;height:13px}
    .let-erp-user-info span{display:block;font-size:9px;color:#0f766e;font-weight:900;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'''
if anchor not in s:
    raise SystemExit("CSS do perfil lateral não encontrado.")
s=s.replace(anchor,replacement,1)

anchor='''  let letErpChatProfiles=[];
  let letErpChatSelectedFile=null;'''
replacement='''  let letErpChatProfiles=[];
  let letErpDeveloperIds=new Set();
  let letErpChatSelectedFile=null;'''
if anchor not in s:
    raise SystemExit("Estado de perfis do chat não encontrado.")
s=s.replace(anchor,replacement,1)

anchor='''  function chatProfileFor(id){
    return letErpChatProfiles.find(p=>p.id===id)||null;
  }'''
replacement='''  function chatProfileFor(id){
    return letErpChatProfiles.find(p=>p.id===id)||null;
  }

  function developerBadgeHtml(userId){
    if(!letErpDeveloperIds.has(userId))return "";
    return '<img class="let-erp-developer-badge" src="developer-badge.png" alt="Developer" title="Developer" aria-label="Developer">';
  }'''
if anchor not in s:
    raise SystemExit("Helper de perfil do chat não encontrado.")
s=s.replace(anchor,replacement,1)

anchor='''    const [{data:msgs,error:msgErr},{data:profiles,error:profileErr}]=await Promise.all([
      window.letErpSupabase.from("chat_mensagens").select("*").order("criado_em",{ascending:false}).limit(120),
      window.letErpSupabase.from("perfis").select("id,nome,setor,foto_url")
    ]);'''
replacement='''    const [{data:msgs,error:msgErr},{data:profiles,error:profileErr},{data:developers,error:developerErr}]=await Promise.all([
      window.letErpSupabase.from("chat_mensagens").select("*").order("criado_em",{ascending:false}).limit(120),
      window.letErpSupabase.from("perfis").select("id,nome,setor,foto_url"),
      window.letErpSupabase.from("developer_badges").select("user_id,label")
    ]);'''
if anchor not in s:
    raise SystemExit("Consulta do chat não encontrada.")
s=s.replace(anchor,replacement,1)

anchor='''    letErpChatProfiles=profiles||[];
    letErpChatMessages=(msgs||[]).reverse();'''
replacement='''    letErpChatProfiles=profiles||[];
    letErpDeveloperIds=new Set((developers||[]).map(x=>x.user_id));
    letErpChatMessages=(msgs||[]).reverse();'''
if anchor not in s:
    raise SystemExit("Carga de perfis do chat não encontrada.")
s=s.replace(anchor,replacement,1)

anchor='''          '<div class="let-erp-chat-author"><strong>'+(mine?"Você":chatEscape(p.nome||"Funcionário"))+'</strong><span>'+chatEscape(p.setor||"")+'</span></div>'+'''
replacement='''          '<div class="let-erp-chat-author"><strong>'+(mine?"Você":chatEscape(p.nome||"Funcionário"))+'</strong>'+developerBadgeHtml(m.usuario_id)+'<span>'+chatEscape(p.setor||"")+'</span></div>'+'''
if anchor not in s:
    raise SystemExit("Autor da mensagem não encontrado.")
s=s.replace(anchor,replacement,1)

anchor='''      if(name)name.textContent=(p.nome||"Complete seu perfil");
      if(sector)sector.textContent=(p.setor||"Setor não informado");'''
replacement='''      if(name){
        name.textContent=(p.nome||"Complete seu perfil");
        const {data:developerRow}=await window.letErpSupabase.from("developer_badges").select("label").eq("user_id",p.id).maybeSingle();
        if(developerRow){
          const badge=document.createElement("img");
          badge.className="let-erp-developer-badge";
          badge.src="developer-badge.png";
          badge.alt="Developer";
          badge.title="Developer";
          badge.setAttribute("aria-label","Developer");
          name.appendChild(badge);
        }
      }
      if(sector)sector.textContent=(p.setor||"Setor não informado");'''
if anchor not in s:
    raise SystemExit("Nome do perfil lateral não encontrado.")
s=s.replace(anchor,replacement,1)

theme.write_text(s,encoding="utf-8")

profile=site/"perfil.html"
t=profile.read_text(encoding="utf-8")

anchor='''.profile-head h2{margin:0;font-size:22px}.profile-head p{margin:6px 0 0;color:#64748b;font-size:11px;font-weight:800}'''
replacement='''.profile-head h2{margin:0;font-size:22px}.profile-head p{margin:6px 0 0;color:#64748b;font-size:11px;font-weight:800}
.profile-name-row{display:flex;align-items:center;gap:8px;flex-wrap:wrap}.profile-developer-badge{width:20px;height:20px;object-fit:contain;display:none;cursor:help}'''
if anchor not in t:
    raise SystemExit("Cabeçalho do perfil não encontrado.")
t=t.replace(anchor,replacement,1)

anchor='''      <div><h2 id="displayName">Perfil do funcionário</h2><p id="displaySector">Preencha seus dados abaixo.</p><p id="displayEmail"></p></div>'''
replacement='''      <div><div class="profile-name-row"><h2 id="displayName">Perfil do funcionário</h2><img id="profileDeveloperBadge" class="profile-developer-badge" src="developer-badge.png" alt="Developer" title="Developer"></div><p id="displaySector">Preencha seus dados abaixo.</p><p id="displayEmail"></p></div>'''
if anchor not in t:
    raise SystemExit("Nome do perfil não encontrado.")
t=t.replace(anchor,replacement,1)

if "let profile=null,user=null;" not in t:
    raise SystemExit("Estado do perfil não encontrado.")
t=t.replace("let profile=null,user=null;","let profile=null,user=null,isDeveloper=false;",1)

anchor='''  document.getElementById("avatar").innerHTML=profile?.foto_url?'<img src="'+profile.foto_url+'" alt="Foto do funcionário">':"👤";
  document.getElementById("incomplete").style.display=letErpProfileComplete(profile)?"none":"block";'''
replacement='''  document.getElementById("avatar").innerHTML=profile?.foto_url?'<img src="'+profile.foto_url+'" alt="Foto do funcionário">':"👤";
  document.getElementById("profileDeveloperBadge").style.display=isDeveloper?"inline-block":"none";
  document.getElementById("incomplete").style.display=letErpProfileComplete(profile)?"none":"block";'''
if anchor not in t:
    raise SystemExit("Renderização do perfil não encontrada.")
t=t.replace(anchor,replacement,1)

anchor='''  const {data}=await db.auth.getUser();user=data.user;
  profile=await letErpGetCurrentProfile();render();'''
replacement='''  const {data}=await db.auth.getUser();user=data.user;
  const {data:developerRow}=await db.from("developer_badges").select("label").eq("user_id",user.id).maybeSingle();
  isDeveloper=!!developerRow;
  profile=await letErpGetCurrentProfile();render();'''
if anchor not in t:
    raise SystemExit("Carregamento do perfil não encontrado.")
t=t.replace(anchor,replacement,1)

profile.write_text(t,encoding="utf-8")

for html in site.glob("*.html"):
    text=html.read_text(encoding="utf-8")
    text=text.replace("20260817-v33-access-admin","20260817-v34-developer-badge")
    html.write_text(text,encoding="utf-8")

panel=site/"painel_producao.html"
pt=panel.read_text(encoding="utf-8")
pt=pt.replace("versão 33 • Supabase","versão 34 • Supabase",1)
panel.write_text(pt,encoding="utf-8")
