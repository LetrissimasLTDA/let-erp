from pathlib import Path
import re

site=Path('_site')
panel=site/'painel_producao.html'
s=panel.read_text(encoding='utf-8')

# CSS de camada máxima para o menu flutuante.
css='''
<style id="moreMenuPortalFix">
  .let-erp-more-portal{
    position:fixed!important;
    z-index:2147483000!important;
    min-width:190px;
    background:#fff;
    border:1px solid #dbe4ea;
    border-radius:12px;
    box-shadow:0 18px 45px rgba(15,23,42,.28);
    padding:7px;
    display:flex;
    flex-direction:column;
    gap:2px;
    pointer-events:auto!important;
  }
  .let-erp-more-portal button{
    width:100%;
    border:0;
    background:#fff;
    text-align:left;
    padding:11px 12px;
    border-radius:8px;
    font:inherit;
    font-size:10px;
    font-weight:950;
    cursor:pointer;
    pointer-events:auto!important;
  }
  .let-erp-more-portal button:hover{background:#f1f5f9}
  .let-erp-more-portal .danger-option{color:#b91c1c}
  .let-erp-more-portal .warning-option{color:#b45309}
  .let-erp-more-portal .purple-option{color:#6d28d9}
  .let-erp-more-portal .mkt-option{color:#0f766e}
</style>
'''
if 'id="moreMenuPortalFix"' not in s:
    s=s.replace('</head>',css+'\n</head>',1)

script=r'''
<script id="moreMenuPortalFixScript">
(function(){
  function removePortal(){
    document.querySelectorAll('.let-erp-more-portal').forEach(el=>el.remove());
  }

  function openPortal(button){
    removePortal();

    const wrap=button.closest('.more-wrap');
    if(!wrap)return;
    const source=wrap.querySelector('.more-menu');
    if(!source)return;

    const portal=document.createElement('div');
    portal.className='let-erp-more-portal';
    portal.innerHTML=source.innerHTML;
    document.body.appendChild(portal);

    const r=button.getBoundingClientRect();
    const pr=portal.getBoundingClientRect();
    const margin=10;

    let left=r.right-pr.width;
    left=Math.max(margin,Math.min(left,window.innerWidth-pr.width-margin));

    let top=r.bottom+7;
    if(top+pr.height>window.innerHeight-margin){
      top=r.top-pr.height-7;
    }
    top=Math.max(margin,Math.min(top,window.innerHeight-pr.height-margin));

    portal.style.left=left+'px';
    portal.style.top=top+'px';
  }

  // Captura antes do onclick antigo para impedir que o menu original seja aberto.
  document.addEventListener('click',function(e){
    const btn=e.target.closest && e.target.closest('.more-btn');
    if(!btn)return;

    e.preventDefault();
    e.stopPropagation();
    if(e.stopImmediatePropagation)e.stopImmediatePropagation();

    const already=document.querySelector('.let-erp-more-portal');
    if(already){
      removePortal();
      return;
    }
    openPortal(btn);
  },true);

  // Fecha ao clicar fora; cliques nos botões do portal continuam funcionando.
  document.addEventListener('click',function(e){
    const portal=e.target.closest && e.target.closest('.let-erp-more-portal');
    if(portal)return;
    removePortal();
  });

  window.addEventListener('resize',removePortal);
  window.addEventListener('scroll',removePortal,true);
  document.addEventListener('keydown',function(e){if(e.key==='Escape')removePortal();});
})();
</script>
'''
if 'id="moreMenuPortalFixScript"' not in s:
    s=s.replace('</body>',script+'\n</body>',1)

# Versão/cache desta correção.
s=re.sub(r'<div class="version">versão \d+(?:\.\d+)?(?: • Supabase)?</div>',
         '<div class="version">versão 36.3 • Supabase</div>',s,count=1)
s=s.replace('20260818-v36-2-code-badge','20260818-v36-3-menu-portal')
s=s.replace('20260818-v36-1-badge-menu-fix','20260818-v36-3-menu-portal')

panel.write_text(s,encoding='utf-8')

# Validação mínima da correção.
final=panel.read_text(encoding='utf-8')
for required in ['let-erp-more-portal','2147483000','moreMenuPortalFixScript','versão 36.3']:
    if required not in final:
        raise SystemExit('Correção do menu incompleta: '+required)

# v36.4: melhora definitiva da apresentação da badge Developer.
exec(compile(Path('overrides/v36-4-badge-fix.py').read_text(encoding='utf-8'),'overrides/v36-4-badge-fix.py','exec'))
