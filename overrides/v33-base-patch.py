from pathlib import Path
import re

theme=Path('_site/theme.js')
s=theme.read_text(encoding='utf-8')

nav_old='''    {href:"atividades.html", icon:"🧾", label:"Atividades", sub:"Quem alterou cada módulo"},
    {href:"perfil.html", icon:"👤", label:"Meu Perfil", sub:"Nome, setor e foto"}'''
nav_new='''    {href:"atividades.html", icon:"🧾", label:"Atividades", sub:"Quem alterou cada módulo"},
    {href:"acessos.html", icon:"🔐", label:"Gerenciar Acessos", sub:"Criar usuários e redefinir senhas", adminOnly:true},
    {href:"perfil.html", icon:"👤", label:"Meu Perfil", sub:"Nome, setor e foto"}'''
if nav_old in s:
    s=s.replace(nav_old,nav_new,1)

needle='  function ensureNavigation(){\n    if(document.querySelector(".let-erp-menu-button"))return;'
replacement='  function ensureNavigation(){\n    const routePage=(location.pathname.split("/").pop()||"").toLowerCase();\n    if(routePage==="login.html"||routePage==="index.html"||routePage==="")return;\n    if(document.querySelector(".let-erp-menu-button"))return;'
if needle in s:
    s=s.replace(needle,replacement,1)

old_map='''    const links=NAV_ITEMS.map(item=>{
      const active=page===item.href.toLowerCase();
      return '<a class="let-erp-drawer-link '+(active?'active':'')+'" href="'+item.href+'">'+'''
new_map='''    const links=NAV_ITEMS.map(item=>{
      const active=page===item.href.toLowerCase();
      const adminAttrs=item.adminOnly?' data-admin-only="true" style="display:none"':'';
      return '<a class="let-erp-drawer-link '+(active?'active':'')+'" href="'+item.href+'"'+adminAttrs+'>'+'''
if old_map in s:
    s=s.replace(old_map,new_map,1)

if 'async function hydrateAdminNavigation()' not in s:
    admin_func='''  async function hydrateAdminNavigation(){
    let tries=0;
    while(!window.letErpSupabase && tries<50){
      await new Promise(r=>setTimeout(r,100));
      tries++;
    }
    if(!window.letErpSupabase)return;
    try{
      const {data}=await window.letErpSupabase.auth.getSession();
      const uid=data?.session?.user?.id;
      if(!uid)return;
      const {data:adminRow}=await window.letErpSupabase.from("erp_admins").select("user_id").eq("user_id",uid).maybeSingle();
      if(adminRow){
        document.querySelectorAll('[data-admin-only="true"]').forEach(el=>el.style.display="");
      }
    }catch(e){console.warn("Não foi possível validar menu administrativo:",e)}
  }

'''
    s=s.replace('  function ensureNavigation(){',admin_func+'  function ensureNavigation(){',1)

if 'hydrateDrawerProfile();\n    hydrateAdminNavigation();' not in s:
    s=s.replace('    document.body.appendChild(drawer);\n    hydrateDrawerProfile();','    document.body.appendChild(drawer);\n    hydrateDrawerProfile();\n    hydrateAdminNavigation();',1)

s=s.replace(
    'position:fixed;left:0;top:0;bottom:0;width:min(330px,88vw);z-index:9998;\n      background:#fff;box-shadow:18px 0 50px rgba(15,23,42,.22);\n      transform:translateX(-105%);transition:transform .24s ease;',
    'position:fixed;right:0;left:auto;top:0;bottom:0;width:min(330px,88vw);z-index:9998;\n      background:#fff;box-shadow:-18px 0 50px rgba(15,23,42,.22);\n      transform:translateX(105%);transition:transform .24s ease;',
    1
)
theme.write_text(s,encoding='utf-8')

login=Path('_site/login.html')
t=login.read_text(encoding='utf-8')
t=t.replace('''        <button class="signup" id="signupBtn" type="button">CRIAR ACESSO</button>
        <button class="signup" id="resendBtn" type="button">REENVIAR CONFIRMAÇÃO</button>
''','')
t=t.replace('''    <div class="note">Depois de criar os usuários da equipe, recomendamos desativar novos cadastros públicos no Supabase para deixar o sistema restrito à fábrica.</div>''','''    <div class="note">Os acessos são criados pela administração do LET ERP. Se você não consegue entrar, peça para um administrador redefinir sua senha.</div>''')
t=t.replace("if(error){if(error.code==='email_not_confirmed'||String(error.message).toLowerCase().includes('email not confirmed'))showError('Seu e-mail ainda não foi confirmado. Abra o e-mail do Supabase ou clique em REENVIAR CONFIRMAÇÃO.');else showError('Não foi possível entrar: '+error.message);return}","if(error){if(error.code==='email_not_confirmed'||String(error.message).toLowerCase().includes('email not confirmed'))showError('Seu e-mail ainda não foi liberado. Peça para um administrador do LET ERP redefinir seu acesso.');else showError('Não foi possível entrar. Confira o e-mail e a senha ou peça para um administrador redefinir seu acesso.');return}")
t=re.sub(r"document\.getElementById\('resendBtn'\)[\s\S]*?document\.getElementById\('signupBtn'\)[\s\S]*?\n\}\);\n",'',t,count=1)
login.write_text(t,encoding='utf-8')

cache_tag='20260817-v33-access-admin'
for html in Path('_site').glob('*.html'):
    text=html.read_text(encoding='utf-8')
    text=text.replace('src="theme.js"',f'src="theme.js?v={cache_tag}"')
    text=text.replace('src="supabase-config.js"',f'src="supabase-config.js?v={cache_tag}"')
    html.write_text(text,encoding='utf-8')
