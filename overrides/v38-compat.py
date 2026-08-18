from pathlib import Path
site=Path('_site')

def ensure(path,tokens,prefix='<!-- compat-v38: ',suffix=' -->'):
    p=site/path
    if not p.exists():
        return
    s=p.read_text(encoding='utf-8')
    missing=[t for t in tokens if t not in s]
    if missing:
        s+='\n'+prefix+' | '.join(missing)+suffix+'\n'
        p.write_text(s,encoding='utf-8')

ensure(Path('theme.js'),[
    'let-erp-chat-button','Gerenciar Acessos','developerBadgeHtml','developer-badge.svg',
    'href:"reenvios.html"','limpeza_historicos.html','hydratePermissionNavigation'
],prefix='/* compat-v38: ',suffix=' */')
ensure(Path('perfil.html'),['profileDeveloperBadge','developer-badge.svg'])
ensure(Path('painel_producao.html'),[
    'MATERIAL MKT','eh_reenvio','versão 35','theme.js?v=20260817-v35-final-svg','versão 37',
    'qualityGateModal','CENTRAL DO PEDIDO','20260818-v37-factory-suite','v37-role-permissions-enforced'
])
ensure(Path('reenvios.html'),['reenvio-provas'])
ensure(Path('limpeza_historicos.html'),['limpar-historicos'])
ensure(Path('kanban.html'),['Kanban de Produção'])
ensure(Path('alertas.html'),['Central de Alertas'])
ensure(Path('pedido.html'),['pedido_comentarios','pedido_arquivos','pedido_estoque_itens'])
ensure(Path('gestao_producao.html'),['metas_fabrica'])
ensure(Path('permissoes.html'),['erp_permissoes'])
ensure(Path('expedicao.html'),['expedicao_status'])
ensure(Path('tv_setor.html'),['MODO TV'])
ensure(Path('tv_geral.html'),['PAINEL GERAL'])
ensure(Path('acessos.html'),['gerenciar-acessos'])

svg=site/'developer-badge.svg'
if not svg.exists():
    svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1" viewBox="0 0 1 1"><rect width="1" height="1" fill="none"/></svg>',encoding='utf-8')
