from pathlib import Path
import re

site=Path('_site')

# ============================================================
# BADGE DEVELOPER SEM IMAGEM: símbolo </> feito só com HTML/CSS
# ============================================================
theme=site/'theme.js'
s=theme.read_text(encoding='utf-8')

# CSS visual da badge e tooltip global.
css='''
    .let-erp-developer-badge-wrap{
      display:inline-flex!important;align-items:center;justify-content:center;flex:0 0 auto;
      vertical-align:middle;cursor:help;position:relative;margin-left:4px;overflow:visible!important
    }
    .let-erp-developer-code{
      width:24px;height:24px;border-radius:7px;background:#083344;border:1px solid #2dd4cf;
      color:#5eead4;display:inline-flex;align-items:center;justify-content:center;
      font-family:Consolas,"Courier New",monospace;font-size:9px;font-weight:950;letter-spacing:-1.2px;
      line-height:1;box-shadow:0 2px 6px rgba(8,51,68,.20);box-sizing:border-box
    }
    .let-erp-chat-author .let-erp-developer-code{width:19px;height:19px;border-radius:5px;font-size:7px}
    .let-erp-developer-tooltip{
      position:fixed;z-index:50000;padding:7px 10px;border-radius:8px;background:#083344;color:#fff;
      font-size:10px;font-weight:950;letter-spacing:.25px;box-shadow:0 8px 24px rgba(15,23,42,.28);
      pointer-events:none;opacity:0;transform:translate(-50%,-5px);transition:opacity .12s ease,transform .12s ease;
      white-space:nowrap
    }
    .let-erp-developer-tooltip.show{opacity:1;transform:translate(-50%,0)}
'''
if '.let-erp-developer-code{' not in s:
    marker='    .let-erp-user-info span{display:block;font-size:9px;color:#0f766e;font-weight:900;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'
    if marker not in s:
        raise SystemExit('CSS do perfil lateral não encontrado.')
    s=s.replace(marker,css+'\n'+marker,1)

# Helper usado nas mensagens do chat.
pattern=r'''  function developerBadgeHtml\(userId\)\{[\s\S]*?\n  \}'''
replacement='''  function developerBadgeHtml(userId){
    if(!letErpDeveloperIds.has(userId))return "";
    return '<span class="let-erp-developer-badge-wrap" data-developer-badge="true" title="Developer" aria-label="Developer"><span class="let-erp-developer-code" aria-hidden="true">&lt;/&gt;</span></span>';
  }'''
s,n=re.subn(pattern,replacement,s,count=1)
if n!=1:
    raise SystemExit('Helper da badge Developer não encontrado.')

# Badge ao lado do nome no menu lateral.
old_drawer='''          const badge=document.createElement("img");
          badge.className="let-erp-developer-badge";
          badge.src="developer-badge.svg";
          badge.alt="Developer";
          badge.title="Developer";
          badge.setAttribute("aria-label","Developer");
          name.appendChild(badge);'''
new_drawer='''          const badgeWrap=document.createElement("span");
          badgeWrap.className="let-erp-developer-badge-wrap";
          badgeWrap.dataset.developerBadge="true";
          badgeWrap.title="Developer";
          badgeWrap.setAttribute("aria-label","Developer");
          const badgeCode=document.createElement("span");
          badgeCode.className="let-erp-developer-code";
          badgeCode.textContent="</>";
          badgeCode.setAttribute("aria-hidden","true");
          badgeWrap.appendChild(badgeCode);
          name.appendChild(badgeWrap);'''
if old_drawer in s:
    s=s.replace(old_drawer,new_drawer,1)
else:
    # aceita também versões intermediárias que já usavam um wrapper com imagem
    drawer_pattern=r'''          const badgeWrap=document\.createElement\("span"\);[\s\S]*?          name\.appendChild\(badgeWrap\);'''
    s,n=re.subn(drawer_pattern,new_drawer,s,count=1)
    if n!=1:
        raise SystemExit('Trecho da badge no menu lateral não encontrado.')

# Tooltip próprio, independente do tooltip padrão do navegador.
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
    let top=r.bottom+8;
    if(top+34>window.innerHeight)top=r.top-36;
    tip.style.top=Math.max(6,top)+"px";
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

'''
    if insert_before not in s:
        raise SystemExit('Ponto de inserção do tooltip não encontrado.')
    s=s.replace(insert_before,tooltip_js+insert_before,1)

theme.write_text(s,encoding='utf-8')

# ============================================================
# TELA MEU PERFIL: mesma badge </>
# ============================================================
profile=site/'perfil.html'
t=profile.read_text(encoding='utf-8')

# substitui qualquer img antiga da badge por elemento textual
profile_pattern=r'''<img id="profileDeveloperBadge" class="profile-developer-badge"[^>]*>'''
profile_badge='''<span id="profileDeveloperBadge" class="profile-developer-badge" data-developer-badge="true" title="Developer" aria-label="Developer"><span class="profile-developer-code" aria-hidden="true">&lt;/&gt;</span><span class="profile-developer-tip">Developer</span></span>'''
t,n=re.subn(profile_pattern,profile_badge,t,count=1)
if n!=1 and 'id="profileDeveloperBadge"' not in t:
    raise SystemExit('Badge da tela Meu Perfil não encontrada.')

# CSS específico do perfil. O seletor antigo pode variar; adicionamos override forte.
profile_css='''
.profile-developer-badge{position:relative!important;display:none;align-items:center!important;justify-content:center!important;cursor:help!important;width:auto!important;height:auto!important;overflow:visible!important}
.profile-developer-code{width:30px;height:30px;border-radius:8px;background:#083344;border:1px solid #2dd4cf;color:#5eead4;display:inline-flex;align-items:center;justify-content:center;font-family:Consolas,"Courier New",monospace;font-size:11px;font-weight:950;letter-spacing:-1.5px;line-height:1;box-shadow:0 3px 8px rgba(8,51,68,.18)}
.profile-developer-tip{position:absolute;left:50%;top:calc(100% + 7px);transform:translateX(-50%) translateY(-3px);background:#083344;color:#fff;padding:6px 9px;border-radius:8px;font-size:10px;font-weight:950;white-space:nowrap;opacity:0;pointer-events:none;transition:.12s;z-index:200}
.profile-developer-badge:hover .profile-developer-tip{opacity:1;transform:translateX(-50%) translateY(0)}
'''
if '.profile-developer-code{' not in t:
    t=t.replace('</style>',profile_css+'\n</style>',1)
t=t.replace('style.display=isDeveloper?"inline-block":"none"','style.display=isDeveloper?"inline-flex":"none"')
profile.write_text(t,encoding='utf-8')

# ============================================================
# PAINEL: 3 PONTINHOS DA PESQUISA SEM FICAR ATRÁS DO MODAL
# ============================================================
panel=site/'painel_producao.html'
p=panel.read_text(encoding='utf-8')

# reforça z-index do menu
p=p.replace('''  z-index:5000;
  display:none;''','''  z-index:50000;
  display:none;''',1)
if '.floating-more-menu{' not in p:
    p=p.replace('.more-menu.open{display:block}', '.more-menu.open{display:block}\n.floating-more-menu{z-index:50000!important;pointer-events:auto!important;position:fixed!important}',1)

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
    if(top+menuRect.height>viewportH-margin)top=buttonRect.top-menuRect.height-7;
    top=Math.max(margin,Math.min(top,viewportH-menuRect.height-margin));

    target.style.left=left+"px";
    target.style.top=top+"px";
  });
}'''
p=p[:start]+new_toggle+p[end+2:]
p=re.sub(r'<div class="version">versão \d+(?:\.\d+)?(?: • Supabase)?</div>','<div class="version">versão 36.2 • Supabase</div>',p,count=1)
panel.write_text(p,encoding='utf-8')

# ============================================================
# CACHE BUSTING
# ============================================================
cache='20260818-v36-2-code-developer'
for html in site.glob('*.html'):
    text=html.read_text(encoding='utf-8')
    text=re.sub(r'src="theme\.js(?:\?v=[^"]+)?"',f'src="theme.js?v={cache}"',text)
    text=re.sub(r'src="supabase-config\.js(?:\?v=[^"]+)?"',f'src="supabase-config.js?v={cache}"',text)
    html.write_text(text,encoding='utf-8')
