from pathlib import Path
import re

site=Path('_site')

theme=site/'theme.js'
s=theme.read_text(encoding='utf-8')

# Ajuste visual definitivo da badge Developer no drawer/chat.
css_patch = r'''
/* v36.4 - Developer badge legível */
.let-erp-user-info #drawerUserName{
  display:flex!important;
  align-items:center!important;
  gap:7px!important;
  overflow:visible!important;
  white-space:nowrap!important;
}
.let-erp-developer-badge-wrap{
  display:inline-flex!important;
  align-items:center!important;
  justify-content:center!important;
  flex:0 0 auto!important;
  position:relative!important;
  overflow:visible!important;
  margin-left:3px!important;
  cursor:help!important;
}
.let-erp-developer-code{
  width:31px!important;
  height:22px!important;
  min-width:31px!important;
  border-radius:7px!important;
  background:linear-gradient(135deg,#083344,#0f766e)!important;
  border:1px solid #2dd4cf!important;
  color:#ffffff!important;
  display:inline-flex!important;
  align-items:center!important;
  justify-content:center!important;
  padding:0!important;
  margin:0!important;
  overflow:visible!important;
  font-family:Consolas,'Courier New',monospace!important;
  font-size:10px!important;
  font-weight:900!important;
  letter-spacing:-.8px!important;
  line-height:22px!important;
  text-indent:0!important;
  text-shadow:0 1px 1px rgba(0,0,0,.22)!important;
  box-shadow:0 2px 7px rgba(8,51,68,.22)!important;
  box-sizing:border-box!important;
}
.let-erp-chat-author .let-erp-developer-code{
  width:27px!important;
  height:19px!important;
  min-width:27px!important;
  border-radius:6px!important;
  font-size:8px!important;
  line-height:19px!important;
}
'''
if 'v36.4 - Developer badge legível' not in s:
    # Insere o CSS antes do fechamento do bloco de estilo criado pelo theme.js.
    marker='    /* login não possui topbar */'
    if marker in s:
        s=s.replace(marker,css_patch+'\n'+marker,1)
    else:
        # fallback: injeta no começo do template CSS global
        marker2='  const style=document.createElement("style");'
        if marker2 not in s:
            raise SystemExit('Não foi possível localizar o CSS global do theme.js')
        s=s.replace(marker2,marker2+'\n  style.textContent += `'+css_patch.replace('`','\\`')+'`;\n',1)

# Garante texto exatamente </> na badge do drawer e do chat.
s=s.replace('badgeCode.textContent="</>";','badgeCode.textContent="</>";',1)
s=s.replace('&lt;/&gt;','&lt;/&gt;')

theme.write_text(s,encoding='utf-8')

# Meu Perfil: mesma identidade visual, maior.
profile=site/'perfil.html'
p=profile.read_text(encoding='utf-8')
profile_css=r'''
<style id="developerBadgeV364">
.profile-developer-badge{
  display:none;
  align-items:center;
  justify-content:center;
  position:relative;
  overflow:visible;
  cursor:help;
}
.profile-developer-badge .developer-code-profile{
  width:38px;height:26px;border-radius:8px;
  background:linear-gradient(135deg,#083344,#0f766e);
  border:1px solid #2dd4cf;color:#fff;
  display:inline-flex;align-items:center;justify-content:center;
  font-family:Consolas,'Courier New',monospace;font-size:12px;font-weight:900;
  letter-spacing:-.8px;line-height:26px;
  box-shadow:0 3px 9px rgba(8,51,68,.20)
}
.profile-developer-badge .profile-developer-tip{
  position:absolute;left:50%;top:calc(100% + 7px);transform:translateX(-50%) translateY(-3px);
  background:#083344;color:#fff;padding:6px 9px;border-radius:8px;font-size:10px;font-weight:950;
  white-space:nowrap;opacity:0;pointer-events:none;transition:.12s;z-index:50000
}
.profile-developer-badge:hover .profile-developer-tip{opacity:1;transform:translateX(-50%) translateY(0)}
</style>
'''
if 'developerBadgeV364' not in p:
    p=p.replace('</head>',profile_css+'\n</head>',1)

# Troca qualquer conteúdo visual antigo do span da badge do perfil por badge em CSS/texto.
pattern=r'(<span[^>]*id="profileDeveloperBadge"[^>]*>)[\s\S]*?(</span>)'
m=re.search(pattern,p)
if m:
    replacement=m.group(1)+'<span class="developer-code-profile" aria-hidden="true">&lt;/&gt;</span><span class="profile-developer-tip">Developer</span>'+m.group(2)
    p=p[:m.start()]+replacement+p[m.end():]

profile.write_text(p,encoding='utf-8')

# Cache/versionamento.
cache='20260818-v36-4-developer-badge'
for html in site.glob('*.html'):
    text=html.read_text(encoding='utf-8')
    text=re.sub(r'src="theme\.js(?:\?v=[^"]+)?"',f'src="theme.js?v={cache}"',text)
    text=re.sub(r'src="supabase-config\.js(?:\?v=[^"]+)?"',f'src="supabase-config.js?v={cache}"',text)
    html.write_text(text,encoding='utf-8')

panel=site/'painel_producao.html'
pt=panel.read_text(encoding='utf-8')
pt=re.sub(r'<div class="version">versão \d+(?:\.\d+)?(?: • Supabase)?</div>','<div class="version">versão 36.4 • Supabase</div>',pt,count=1)
panel.write_text(pt,encoding='utf-8')
