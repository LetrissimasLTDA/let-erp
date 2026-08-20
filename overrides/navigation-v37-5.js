/* LET ERP v37.5.2 - menu agrupado robusto, favoritos e perfil */
(()=>{
  const page=(location.pathname.split('/').pop()||'').toLowerCase();
  if(!page || ['login.html','index.html','tv_producao.html','tv_setor.html','tv_geral.html'].includes(page))return;

  const ITEMS={
    'painel_producao.html':{icon:'🏠',label:'Painel de Produção',sub:'Pedidos e prazos'},
    'novo_pedido.html':{icon:'＋',label:'Novo Pedido',sub:'Cadastrar pedido',perm:'pedidos_criar'},
    'setores.html':{icon:'⚙️',label:'Setores',sub:'Etapas da produção'},
    'kanban.html':{icon:'📋',label:'Kanban de Produção',sub:'Fila visual por etapa'},
    'reenvios.html':{icon:'🔁',label:'Reenvios',sub:'Cadastrar e consultar reenvios',perm:'pedidos_criar'},
    'calendario_envios.html':{icon:'📅',label:'Calendário de Envios',sub:'Agenda de saídas e quantidades'},
    'analises.html':{icon:'📊',label:'Análises',sub:'Indicadores e relatórios',perm:'gestao'},
    'atrasos.html':{icon:'⚠️',label:'Pedidos Atrasados',sub:'Histórico e motivos'},
    'financeiro.html':{icon:'💰',label:'Financeiro',sub:'Pagamentos e histórico',perm:'financeiro'},
    'programacoes.html':{icon:'🗓️',label:'Programações',sub:'Cupons, ofertas e promoções',perm:'gestao'},
    'estoque.html':{icon:'📦',label:'Estoque',sub:'Materiais e quantidades',perm:'estoque_gerenciar'},
    'expedicao.html':{icon:'🚚',label:'Expedição',sub:'Retiradas e histórico',perm:'expedicao_gerenciar'},
    'atividades.html':{icon:'🧾',label:'Atividades',sub:'Quem alterou cada módulo',perm:'gestao'},
    'permissoes.html':{icon:'🛡️',label:'Permissões',sub:'Acessos por função',perm:'permissoes'},
    'acessos.html':{icon:'🔐',label:'Gerenciar Acessos',sub:'Criar usuários e redefinir senhas',perm:'usuarios'},
    'limpeza_historicos.html':{icon:'🧹',label:'Limpeza de Históricos',sub:'Limpar registros antigos',perm:'limpeza'},
    'perfil.html':{icon:'👤',label:'Meu Perfil',sub:'Nome, setor e foto'}
  };
  const GROUPS=[
    {icon:'🏭',name:'PRODUÇÃO',items:['painel_producao.html','novo_pedido.html','setores.html','kanban.html','reenvios.html','calendario_envios.html']},
    {icon:'📊',name:'GESTÃO',items:['analises.html','atrasos.html','financeiro.html','programacoes.html']},
    {icon:'📦',name:'ESTOQUE',items:['estoque.html']},
    {icon:'🚚',name:'EXPEDIÇÃO',items:['expedicao.html']},
    {icon:'🔐',name:'ADMINISTRAÇÃO',items:['atividades.html','permissoes.html','acessos.html','limpeza_historicos.html']},
    {icon:'👤',name:'PERFIL',items:['perfil.html']}
  ];

  const style=document.createElement('style');
  style.textContent=`
    body>.topbar{min-height:62px!important;padding-top:8px!important;padding-bottom:8px!important}
    body>.topbar h1{font-size:clamp(18px,1.75vw,25px)!important;line-height:1.05!important;margin-top:0!important;margin-bottom:2px!important}
    body>.topbar p{font-size:9px!important;line-height:1.15!important;margin-top:2px!important;margin-bottom:0!important}
    .let-erp-home-clover{top:9px!important;width:40px!important;height:40px!important}.let-erp-home-clover img{width:36px!important;height:36px!important}
    .let-erp-menu-button{top:10px!important;width:40px!important;height:40px!important}
    .let-erp-drawer-body.let-erp-grouped-menu{padding:9px 10px 12px!important}
    .let-erp-menu-favorites{border:1px solid #fde68a;background:#fffdf4;border-radius:12px;padding:5px;margin-bottom:8px}.let-erp-menu-favorites:empty{display:none}
    .let-erp-menu-fav-title{padding:6px 7px 5px;color:#92400e;font:950 9px Arial,sans-serif;letter-spacing:.45px}
    .let-erp-menu-group{border:1px solid #e8eef2;border-radius:12px;overflow:hidden;margin-bottom:7px;background:#fff}.let-erp-menu-group[hidden]{display:none!important}
    .let-erp-menu-group-btn{width:100%;min-height:38px;padding:0 10px;border:0;background:#f8fafc;color:#334155;display:flex;align-items:center;gap:8px;text-align:left;cursor:pointer;font:950 9px Arial,sans-serif;letter-spacing:.35px}
    .let-erp-menu-group-btn:hover{background:#f0fdfa;color:#0f766e}.let-erp-menu-group-btn .group-icon{font-size:14px}.let-erp-menu-group-btn .group-name{flex:1}.let-erp-menu-group-btn .group-chevron{font-size:14px;transition:transform .15s ease}
    .let-erp-menu-group.closed .group-chevron{transform:rotate(-90deg)}.let-erp-menu-group.closed .let-erp-menu-group-links{display:none}.let-erp-menu-group-links{padding:5px}
    .let-erp-menu-group-links .let-erp-drawer-link{display:grid!important;grid-template-columns:36px 1fr 25px 14px!important;padding:8px!important;margin-bottom:2px!important;gap:7px!important;align-items:center!important;text-decoration:none!important}
    .let-erp-menu-group-links .let-erp-drawer-icon{width:34px!important;height:34px!important;font-size:15px!important;display:grid!important;place-items:center!important}
    .let-erp-menu-group-links .let-erp-drawer-text strong{font-size:11px!important}.let-erp-menu-group-links .let-erp-drawer-text small{font-size:8px!important}
    .let-erp-menu-star{width:24px;height:24px;border:0;background:transparent;border-radius:7px;display:grid;place-items:center;color:#cbd5e1;font-size:15px;cursor:pointer;padding:0}.let-erp-menu-star:hover{background:#fffbeb;color:#f59e0b}.let-erp-menu-star.on{color:#f59e0b}
    .let-erp-menu-favorites .let-erp-drawer-link{display:grid!important;grid-template-columns:36px 1fr 14px!important;padding:8px!important;margin-bottom:2px!important;gap:7px!important;align-items:center!important;text-decoration:none!important}.let-erp-menu-favorites .let-erp-drawer-icon{width:34px!important;height:34px!important;font-size:15px!important;display:grid!important;place-items:center!important}
    .let-erp-dev-inline{display:inline-grid;place-items:center;width:16px;height:16px;margin-left:5px;border-radius:5px;background:#083344;color:#2dd4cf;font:900 8px monospace;cursor:help;vertical-align:middle;flex:0 0 auto}
    @media(max-width:700px){body>.topbar{min-height:58px!important;padding-top:7px!important;padding-bottom:7px!important}.let-erp-home-clover{top:8px!important}.let-erp-menu-button{top:8px!important}}
  `;
  document.head.appendChild(style);

  const sleep=ms=>new Promise(r=>setTimeout(r,ms));
  let body=null,db=null,userId=null,permissions=null,profile=null,favorites=[];
  async function getDb(){for(let i=0;i<80&&!window.letErpSupabase;i++)await sleep(75);return window.letErpSupabase||null}
  function allowed(item){if(!item.perm)return true;if(!permissions)return true;return !!permissions[item.perm]}
  function storedClosed(name){try{return localStorage.getItem('letErpGroup:'+name)==='closed'}catch{return false}}
  function setStoredClosed(name,closed){try{localStorage.setItem('letErpGroup:'+name,closed?'closed':'open')}catch{}}
  function linkHtml(h,withStar=true){const i=ITEMS[h],active=page===h;return '<a class="let-erp-drawer-link '+(active?'active':'')+'" href="'+h+'"><span class="let-erp-drawer-icon">'+i.icon+'</span><span class="let-erp-drawer-text"><strong>'+i.label+'</strong><small>'+i.sub+'</small></span>'+(withStar?'<button type="button" class="let-erp-menu-star '+(favorites.includes(h)?'on':'')+'" data-fav="'+h+'" title="'+(favorites.includes(h)?'Remover dos favoritos':'Adicionar aos favoritos')+'">'+(favorites.includes(h)?'★':'☆')+'</button>':'')+'<span class="let-erp-drawer-arrow">›</span></a>'}
  function renderFavorites(){const box=document.querySelector('.let-erp-menu-favorites');if(!box)return;const list=favorites.filter(h=>ITEMS[h]&&allowed(ITEMS[h]));box.innerHTML=list.length?'<div class="let-erp-menu-fav-title">⭐ FAVORITOS</div>'+list.map(h=>linkHtml(h,false)).join(''):''}
  function bindStars(){document.querySelectorAll('.let-erp-menu-star').forEach(btn=>btn.onclick=async e=>{e.preventDefault();e.stopPropagation();const h=btn.dataset.fav;favorites=favorites.includes(h)?favorites.filter(x=>x!==h):[...new Set([...favorites,h])];renderMenu();try{if(db&&userId)await db.from('perfis').update({menu_favoritos:favorites}).eq('id',userId)}catch(err){console.warn('Favoritos:',err)}})}
  function renderMenu(){if(!body)return;body.innerHTML='<div class="let-erp-menu-favorites"></div>';body.classList.add('let-erp-grouped-menu');GROUPS.forEach(g=>{const items=g.items.filter(h=>ITEMS[h]&&allowed(ITEMS[h]));if(!items.length)return;const sec=document.createElement('section');sec.className='let-erp-menu-group';const contains=items.includes(page);sec.classList.toggle('closed',!contains&&storedClosed(g.name));sec.innerHTML='<button class="let-erp-menu-group-btn" type="button"><span class="group-icon">'+g.icon+'</span><span class="group-name">'+g.name+'</span><span class="group-chevron">⌄</span></button><div class="let-erp-menu-group-links">'+items.map(h=>linkHtml(h,true)).join('')+'</div>';sec.querySelector('.let-erp-menu-group-btn').onclick=()=>{sec.classList.toggle('closed');setStoredClosed(g.name,sec.classList.contains('closed'))};body.appendChild(sec)});renderFavorites();bindStars();body.querySelectorAll('a.let-erp-drawer-link').forEach(a=>a.addEventListener('click',()=>window.letErpCloseMenu?.()))}
  async function hydrateProfile(){if(!db||!userId)return;try{const [{data:p},{data:d}]=await Promise.all([db.from('perfis').select('id,nome,setor,email,foto_url,menu_favoritos').eq('id',userId).maybeSingle(),db.from('developer_badges').select('label').eq('user_id',userId).maybeSingle()]);profile=p||null;favorites=Array.isArray(p?.menu_favoritos)?p.menu_favoritos:[];const name=document.getElementById('drawerUserName'),sector=document.getElementById('drawerUserSector'),email=document.getElementById('drawerUserEmail'),avatar=document.getElementById('drawerUserAvatar');if(name){name.textContent=p?.nome||'Complete seu perfil';if(d){const b=document.createElement('span');b.className='let-erp-dev-inline';b.title='Developer';b.textContent='</>';name.appendChild(b)}}if(sector)sector.textContent=p?.setor||'Setor não informado';if(email)email.textContent=p?.email||'';if(avatar&&p?.foto_url)avatar.innerHTML='<img src="'+String(p.foto_url).replace(/"/g,'&quot;')+'" alt="Foto do funcionário">';renderMenu()}catch(err){console.warn('Perfil lateral:',err)}}
  async function init(){for(let i=0;i<80&&!body;i++){body=document.querySelector('.let-erp-drawer-body');if(!body)await sleep(75)}if(!body)return;db=await getDb();renderMenu();if(!db)return;try{const {data:s}=await db.auth.getSession();userId=s?.session?.user?.id||null;if(!userId)return;const {data:r}=await db.from('erp_permissoes').select('permissoes').eq('user_id',userId).maybeSingle();permissions=r?.permissoes||null;window.LET_ERP_PERMISSIONS=permissions||window.LET_ERP_PERMISSIONS;await hydrateProfile();renderMenu()}catch(err){console.warn('Navegação/permissões:',err);renderMenu()}}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
