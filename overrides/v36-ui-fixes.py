from pathlib import Path
import shutil, re, hashlib

site=Path('_site')
source=Path('overrides/developer-badge.png')
expected='d4f28988b6b0b9dd2de5084a7f75e8afc77bd109802e49e7b0216b418a8c5223'
if not source.exists():
    raise SystemExit('Badge Developer original não encontrada.')
if hashlib.sha256(source.read_bytes()).hexdigest()!=expected:
    raise SystemExit('Badge Developer original não confere com o arquivo enviado.')
shutil.copyfile(source, site/'developer-badge.png')

# Badge Developer: usa o PNG original enviado e tooltip próprio.
theme=site/'theme.js'
s=theme.read_text(encoding='utf-8')
s=s.replace('developer-badge.svg','developer-badge.png')

css_old='''.let-erp-developer-badge{width:18px;height:18px;object-fit:contain;display:inline-block;vertical-align:middle;flex:0 0 auto;cursor:help;border-radius:4px;box-shadow:0 0 0 1px rgba(15,118,110,.18)}
    .let-erp-chat-author .let-erp-developer-badge{width:15px;height:15px}'''
css_new='''.let-erp-developer-badge-wrap{display:inline-flex;align-items:center;justify-content:center;flex:0 0 auto;vertical-align:middle;cursor:help}
    .let-erp-developer-badge{width:22px;height:22px;object-fit:contain;display:block;flex:0 0 auto;filter:drop-shadow(0 1px 2px rgba(15,23,42,.12))}
    .let-erp-chat-author .let-erp-developer-badge{width:18px;height:18px}
    .let-erp-developer-tooltip{position:fixed;z-index:40000;padding:6px 9px;border-radius:8px;background:#083344;color:#fff;font-size:10px;font-weight:950;letter-spacing:.2px;box-shadow:0 8px 24px rgba(15,23,42,.24);pointer-events:none;opacity:0;transform:translate(-50%,-5px);transition:opacity .12s ease,transform .12s ease;white-space:nowrap}
    .let-erp-developer-tooltip.show{opacity:1;transform:translate(-50%,0)}'''
if css_old in s:
    s=s.replace(css_old,css_new,1)
elif '.let-erp-developer-badge-wrap{' not in s:
    anchor='.let-erp-user-info #drawerUserName{display:flex;align-items:center;gap:5px;min-width:0}'
    if anchor not in s: raise SystemExit('CSS do drawer não encontrado.')
    s=s.replace(anchor,anchor+'\n    '+css_new,1)

helper_old='''  function developerBadgeHtml(userId){
    if(!letErpDeveloperIds.has(userId))return "";
    return '<img class="let-erp-developer-badge" src="developer-badge.png" alt="Developer" title="Developer" aria-label="Developer">';
  }'''
helper_new='''  function developerBadgeHtml(userId){
    if(!letErpDeveloperIds.has(userId))return "";
    return '<span class="let-erp-developer-badge-wrap" data-developer-badge="true" aria-label="Developer"><img class="let-erp-developer-badge" src="developer-badge.png?v=20260818-original" alt="Developer"></span>';
  }'''
if helper_old in s:
    s=s.replace(helper_old,helper_new,1)
elif 'data-developer-badge="true"' not in s:
    raise SystemExit('Helper da badge não encontrado.')

drawer_old='''          const badge=document.createElement("img");
          badge.className="let-erp-developer-badge";
          badge.src="developer-badge.png";
          badge.alt="Developer";
          badge.title="Developer";
          badge.setAttribute("aria-label","Developer");
          name.appendChild(badge);'''
drawer_new='''          const badgeWrap=document.createElement("span");
          badgeWrap.className="let-erp-developer-badge-wrap";
          badgeWrap.dataset.developerBadge="true";
          badgeWrap.setAttribute("aria-label","Developer");
          const badge=document.createElement("img");
          badge.className="let-erp-developer-badge";
          badge.src="developer-badge.png?v=20260818-original";
          badge.alt="Developer";
          badgeWrap.appendChild(badge);
          name.appendChild(badgeWrap);'''
if drawer_old in s:
    s=s.replace(drawer_old,drawer_new,1)

if 'function showDeveloperTooltip' not in s:
    insert_before='''  async function hydrateDrawerProfile(){'''
    tooltip_js='''  function getDeveloperTooltip(){
    let tip=document.getElementById("letErpDeveloperTooltip");
    if(!tip){
      tip=document.createElement("div");
      tip.id="letErpDeveloperTooltip";
      tip.className="let-erp-developer-tooltip";
      tip.textContent="Developer";
      document.body.appendChild(tip);
    }
    return tip;
  }

  function showDeveloperTooltip(el){
    const tip=getDeveloperTooltip();
    const r=el.getBoundingClientRect();
    tip.style.left=(r.left+r.width/2)+"px";
    tip.style.top=(Math.max(8,r.bottom+8))+"px";
    tip.classList.add("show");
  }

  function hideDeveloperTooltip(){
    document.getElementById("letErpDeveloperTooltip")?.classList.remove("show");
  }

  document.addEventListener("mouseover",e=>{
    const badge=e.target.closest?.('[data-developer-badge="true"]');
    if(badge)showDeveloperTooltip(badge);
  });
  document.addEventListener("mouseout",e=>{
    const badge=e.target.closest?.('[data-developer-badge="true"]');
    if(badge&&!badge.contains(e.relatedTarget))hideDeveloperTooltip();
  });
  document.addEventListener("focusin",e=>{
    const badge=e.target.closest?.('[data-developer-badge="true"]');
    if(badge)showDeveloperTooltip(badge);
  });
  document.addEventListener("focusout",e=>{
    const badge=e.target.closest?.('[data-developer-badge="true"]');
    if(badge)hideDeveloperTooltip();
  });

'''
    if insert_before not in s: raise SystemExit('Ponto de inserção do tooltip não encontrado.')
    s=s.replace(insert_before,tooltip_js+insert_before,1)

theme.write_text(s,encoding='utf-8')

# Tela Meu Perfil: badge maior e tooltip visível.
profile=site/'perfil.html'
t=profile.read_text(encoding='utf-8').replace('developer-badge.svg','developer-badge.png')
old_html='''<div class="profile-name-row"><h2 id="displayName">Perfil do funcionário</h2><img id="profileDeveloperBadge" class="profile-developer-badge" src="developer-badge.png" alt="Developer" title="Developer"></div>'''
new_html='''<div class="profile-name-row"><h2 id="displayName">Perfil do funcionário</h2><span id="profileDeveloperBadge" class="profile-developer-badge" data-developer-badge="true" aria-label="Developer"><img src="developer-badge.png?v=20260818-original" alt="Developer"><span class="profile-developer-tip">Developer</span></span></div>'''
if old_html in t:
    t=t.replace(old_html,new_html,1)

css_old='.profile-name-row{display:flex;align-items:center;gap:8px;flex-wrap:wrap}.profile-developer-badge{width:20px;height:20px;object-fit:contain;display:none;cursor:help}'
css_new='.profile-name-row{display:flex;align-items:center;gap:8px;flex-wrap:wrap}.profile-developer-badge{position:relative;display:none;align-items:center;justify-content:center;cursor:help}.profile-developer-badge img{width:28px;height:28px;object-fit:contain;display:block;filter:drop-shadow(0 1px 2px rgba(15,23,42,.12))}.profile-developer-tip{position:absolute;left:50%;top:calc(100% + 7px);transform:translateX(-50%) translateY(-3px);background:#083344;color:#fff;padding:6px 9px;border-radius:8px;font-size:10px;font-weight:950;white-space:nowrap;opacity:0;pointer-events:none;transition:.12s;z-index:50}.profile-developer-badge:hover .profile-developer-tip{opacity:1;transform:translateX(-50%) translateY(0)}'
if css_old in t:
    t=t.replace(css_old,css_new,1)
t=t.replace('style.display=isDeveloper?"inline-block":"none"','style.display=isDeveloper?"inline-flex":"none"')
profile.write_text(t,encoding='utf-8')

# Painel: menu dos 3 pontinhos vira um portal no body para nunca ficar atrás de modal.
panel=site/'painel_producao.html'
p=panel.read_text(encoding='utf-8')
p=p.replace('''  z-index:5000;
  display:none;''','''  z-index:30000;
  display:none;''',1)
if '.floating-more-menu{' not in p:
    p=p.replace('.more-menu.open{display:block}', '.more-menu.open{display:block}\n.floating-more-menu{z-index:30000!important;pointer-events:auto!important;position:fixed!important}',1)

old_close='''function closeAllMoreMenus(){
  document.querySelectorAll(".more-menu.open").forEach(m=>{
    m.classList.remove("open");
    m.style.left="";
    m.style.top="";
  });
}'''
new_close='''function closeAllMoreMenus(){
  document.querySelectorAll(".floating-more-menu").forEach(m=>m.remove());
  document.querySelectorAll(".more-menu.open").forEach(m=>{
    m.classList.remove("open");
    m.style.left="";
    m.style.top="";
  });
}'''
if old_close in p:
    p=p.replace(old_close,new_close,1)

start=p.find('function toggleMoreMenu(event,id){')
end=p.find('\n}\n\ndocument.addEventListener("click",closeAllMoreMenus);',start)
if start<0 or end<0:
    raise SystemExit('Função toggleMoreMenu não encontrada.')
new_toggle='''function toggleMoreMenu(event,id){
  event.stopPropagation();

  const button=event.currentTarget;
  const source=document.getElementById("moreMenu-"+id);
  if(!source)return;

  const existing=document.querySelector('.floating-more-menu[data-source-id="'+CSS.escape(String(id))+'"]');
  closeAllMoreMenus();
  if(existing)return;

  const target=document.createElement("div");
  target.className="more-menu open floating-more-menu";
  target.dataset.sourceId=String(id);
  target.innerHTML=source.innerHTML;
  document.body.appendChild(target);

  requestAnimationFrame(()=>{
    const buttonRect=button.getBoundingClientRect();
    const menuRect=target.getBoundingClientRect();
    const margin=10;
    const viewportW=window.innerWidth;
    const viewportH=window.innerHeight;

    let left=buttonRect.right-menuRect.width;
    left=Math.max(margin,Math.min(left,viewportW-menuRect.width-margin));

    let top=buttonRect.bottom+7;
    if(top+menuRect.height>viewportH-margin){
      top=buttonRect.top-menuRect.height-7;
    }
    top=Math.max(margin,Math.min(top,viewportH-menuRect.height-margin));

    target.style.left=left+"px";
    target.style.top=top+"px";
  });
}'''
p=p[:start]+new_toggle+p[end+2:]
p=re.sub(r'<div class="version">versão \d+(?:\.\d+)?(?: • Supabase)?</div>','<div class="version">versão 36.1 • Supabase</div>',p,count=1)
panel.write_text(p,encoding='utf-8')

cache='20260818-v36-1-badge-menu-fix'
for html in site.glob('*.html'):
    text=html.read_text(encoding='utf-8')
    text=re.sub(r'src="theme\.js(?:\?v=[^"]+)?"',f'src="theme.js?v={cache}"',text)
    text=re.sub(r'src="supabase-config\.js(?:\?v=[^"]+)?"',f'src="supabase-config.js?v={cache}"',text)
    html.write_text(text,encoding='utf-8')
