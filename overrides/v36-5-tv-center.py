from pathlib import Path
import re

site=Path('_site')
tv=site/'tv_producao.html'
s=tv.read_text(encoding='utf-8')

css=r'''
<style id="tvCenterV365">
/* v36.5 - conteúdo do Dashboard TV realmente centralizado */
@media (min-width:901px){
  .slide{
    grid-template-columns:minmax(360px,41%) minmax(0,59%)!important;
  }
  .info-zone{
    display:flex!important;
    flex-direction:column!important;
    justify-content:center!important;
    align-items:center!important;
    text-align:center!important;
    padding:clamp(32px,3.2vw,56px)!important;
    gap:clamp(14px,1.7vh,22px)!important;
  }
  .info-zone > *{
    width:min(100%,900px)!important;
    margin-left:auto!important;
    margin-right:auto!important;
  }
  .order-row{
    width:100%!important;
    display:flex!important;
    flex-direction:column!important;
    align-items:center!important;
    justify-content:center!important;
    gap:12px!important;
    text-align:center!important;
  }
  .order-id{
    width:100%!important;
    min-width:0!important;
    text-align:center!important;
  }
  .order-id .label{
    display:block!important;
    text-align:center!important;
  }
  .order-id h2{
    width:100%!important;
    margin:4px auto 0!important;
    text-align:center!important;
    font-size:clamp(34px,4vw,60px)!important;
    line-height:1!important;
    letter-spacing:-.035em!important;
    overflow-wrap:anywhere!important;
    word-break:break-word!important;
  }
  .reenvio{
    margin-left:auto!important;
    margin-right:auto!important;
  }
  .deadline{
    position:static!important;
    transform:none!important;
    margin:0 auto!important;
    min-width:190px!important;
    text-align:center!important;
  }
  .client{
    width:100%!important;
    text-align:center!important;
    font-size:clamp(30px,3.3vw,50px)!important;
  }
  .chips{
    width:100%!important;
    justify-content:center!important;
  }
  .details{
    width:100%!important;
    max-width:900px!important;
    margin-left:auto!important;
    margin-right:auto!important;
  }
  .detail{
    text-align:center!important;
  }
  .obs{
    width:100%!important;
    max-width:900px!important;
    margin-left:auto!important;
    margin-right:auto!important;
    text-align:left!important;
  }
  .logo-zone{
    justify-content:center!important;
  }
  .logo-box{
    display:grid!important;
    place-items:center!important;
  }
}
</style>
'''

if 'id="tvCenterV365"' not in s:
    s=s.replace('</head>',css+'\n</head>',1)

# Marca de versão no HTML para facilitar conferência de cache.
if 'data-tv-version="36.5"' not in s:
    s=s.replace('<div class="tv-shell">','<div class="tv-shell" data-tv-version="36.5">',1)

tv.write_text(s,encoding='utf-8')

# Painel principal passa a indicar v36.5.
panel=site/'painel_producao.html'
p=panel.read_text(encoding='utf-8')
p=re.sub(r'<div class="version">versão \d+(?:\.\d+)?(?: • Supabase)?</div>',
         '<div class="version">versão 36.5 • Supabase</div>',p,count=1)
panel.write_text(p,encoding='utf-8')

final=tv.read_text(encoding='utf-8')
for required in ['tvCenterV365','align-items:center!important','text-align:center!important','data-tv-version="36.5"']:
    if required not in final:
        raise SystemExit('Centralização do Dashboard TV incompleta: '+required)
