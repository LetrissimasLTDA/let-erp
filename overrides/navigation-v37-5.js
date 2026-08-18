/* LET ERP v37.5 - menu agrupado, favoritos e topbar compacta */
(()=>{
  const page=(location.pathname.split('/').pop()||'').toLowerCase();
  if(!page || ['login.html','index.html','tv_producao.html','tv_setor.html','tv_geral.html'].includes(page)) return;

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
    .let-erp-home-clover{top:9px!important;width:40px!important;height:40px!important}
    .let-erp-home-clover img{width:36px!important;height:36px!important}
    .let-erp-menu-button{top:10px!important;width:40px!important;height:40px!important}
    .let-erp-drawer-body.let-erp-grouped-menu{padding:9px 10px 12px!important}
    .let-erp-menu-favorites{border:1px solid #fde68a;background:#fffdf4;border-radius:12px;padding:5px;margin-bottom:8px}
    .let-erp-menu-favorites:empty{display:none}
    .let-erp-menu-fav-title{padding:6px 7px 5px;color:#92400e;font:950 9px Arial,sans-serif;letter-spacing:.45px}
    .let-erp-menu-group{border:1px solid #e8eef2;border-radius:12px;overflow:hidden;margin-bottom:7px;background:#fff}
    .let-erp-menu-group[hidden]{display:none!important}
    .let-erp-menu-group-btn{width:100%;min-height:38px;padding:0 10px;border:0;background:#f8fafc;color:#334155;display:flex;align-items:center;gap:8px;text-align:left;cursor:pointer;font:950 9px Arial,sans-serif;letter-spacing:.35px}
    .let-erp-menu-group-btn:hover{background:#f0fdfa;color:#0f766e}
    .let-erp-menu-group-btn .group-icon{font-size:14px}.let-erp-menu-group-btn .group-name{flex:1}.let-erp-menu-group-btn .group-chevron{font-size:14px;transition:transform .15s ease}
    .let-erp-menu-group.closed .group-chevron{transform:rotate(-90deg)}.let-erp-menu-group.closed .let-erp-menu-group-links{display:none}
    .let-erp-menu-group-links{padding:5px}
    .let-erp-menu-group-links .let-erp-drawer-link{grid-template-columns:36px 1fr 25px 14px!important;padding:8px!important;margin-bottom:2px!important;gap:7px!important}
    .let-erp-menu-group-links .let-erp-drawer-icon{width:34px!important;height:34px!important;font-size:15px!important}
    .let-erp-menu-group-links .let-erp-drawer-text strong{font-size:11px!important}.let-erp-menu-group-links .let-erp-drawer-text small{font-size:8px!important}
    .let-erp-menu-star{width:24px;height:24px;border:0;background:transparent;border-radius:7px;display:grid;place-items:center;color:#cbd5e1;font-size:15px;cursor:pointer;padding:0}
    .let-erp-menu-star:hover{background:#fffbeb;color:#f59e0b}.let-erp-menu-star.on{color:#f59e0b}
    .let-erp-menu-favorites .let-erp-drawer-link{grid-template-columns:36px 1fr 14px!important;padding:8px!important;margin-bottom:2px!important}
    .let-erp-menu-favorites .let-erp-drawer-icon{width:34px!important;height:34px!important;font-size:15px!important}
    @media(max-width:700px){body>.topbar{min-height:58px!important;padding-top:7px!important;padding-bottom:7px!important}.let-erp-home-clover{top:8px!important}.let-erp-menu-button{top:8px!important}}
  `;
  document.head.appendChild(style);

  const sleep=ms=>new Promise(r=>setTimeout(r,ms));
  const hrefName=h=>String(h||'').split('?')[0].split('#')[0].split('/').pop().toLowerCase();
  let favorites=[],userId=null,body=null;
  async function getDb(){for(let i=0;i<60&&!window.letErpSupabase;i++)await sleep(100);return window.letErpSupabase||null}
  async function loadFavorites(){const db=await getDb();if(!db)return;try{const {data:s}=await db.auth.getSession();userId=s?.session?.user?.id||null;if(!userId)return;const {data,error}=await db.from('perfis').select('menu_favoritos').eq('id',userId).maybeSingle();if(error)throw error;favorites=Array.isArray(data?.menu_favoritos)?data.menu_favoritos.map(hrefName):[]}catch(e){console.warn('Favoritos do menu:',e);favorites=[]}}
  async function saveFavorites(){const db=await getDb();if(!db||!userId)return;try{const {error}=await db.from('perfis').update({menu_favoritos:favorites}).eq('id',userId);if(error)throw error}catch(e){console.warn('Não foi possível salvar favoritos:',e)}}
  function originalLinks(){return[...document.querySelectorAll('.let-erp-menu-group-links .let-erp-drawer-link')]}
  function syncStars(){document.querySelectorAll('.let-erp-menu-star').forEach(btn=>{const a=btn.closest('.let-erp-drawer-link'),h=hrefName(a?.getAttribute('href')),on=favorites.includes(h);btn.classList.toggle('on',on);btn.textContent=on?'★':'☆';btn.title=on?'Remover dos favoritos':'Adicionar aos favoritos';btn.setAttribute('aria-label',btn.title)})}
  function visibleLink(a){return!!a&&getComputedStyle(a).display!=='none'&&!a.hidden}
  function renderFavorites(){const box=document.querySelector('.let-erp-menu-favorites');if(!box)return;box.innerHTML='';const links=originalLinks().filter(a=>favorites.includes(hrefName(a.getAttribute('href')))&&visibleLink(a));if(!links.length)return;const title=document.createElement('div');title.className='let-erp-menu-fav-title';title.textContent='⭐ FAVORITOS';box.appendChild(title);links.forEach(a=>{const c=a.cloneNode(true);c.querySelector('.let-erp-menu-star')?.remove();c.addEventListener('click',()=>window.letErpCloseMenu?.());box.appendChild(c)})}
  function refreshGroupVisibility(){document.querySelectorAll('.let-erp-menu-group').forEach(group=>{group.hidden=![...group.querySelectorAll('.let-erp-menu-group-links .let-erp-drawer-link')].some(visibleLink)});renderFavorites()}
  function addStar(a){if(a.querySelector('.let-erp-menu-star'))return;const btn=document.createElement('button');btn.type='button';btn.className='let-erp-menu-star';btn.addEventListener('click',async e=>{e.preventDefault();e.stopPropagation();const h=hrefName(a.getAttribute('href'));favorites=favorites.includes(h)?favorites.filter(x=>x!==h):[...new Set([...favorites,h])];syncStars();renderFavorites();await saveFavorites()});const arrow=a.querySelector('.let-erp-drawer-arrow');arrow?a.insertBefore(btn,arrow):a.appendChild(btn)}
  function storedClosed(name){try{return localStorage.getItem('letErpGroup:'+name)==='closed'}catch(e){return false}}
  function setStoredClosed(name,closed){try{localStorage.setItem('letErpGroup:'+name,closed?'closed':'open')}catch(e){}}
  async function buildGroupedMenu(){for(let i=0;i<70&&!body;i++){body=document.querySelector('.let-erp-drawer-body');if(!body)await sleep(80)}if(!body||body.classList.contains('let-erp-grouped-menu'))return;await loadFavorites();const all=[...body.querySelectorAll('.let-erp-drawer-link')],map=new Map(all.map(a=>[hrefName(a.getAttribute('href')),a]));body.innerHTML='';body.classList.add('let-erp-grouped-menu');const favBox=document.createElement('div');favBox.className='let-erp-menu-favorites';body.appendChild(favBox);const used=new Set();GROUPS.forEach(g=>{const links=g.items.map(h=>map.get(h)).filter(Boolean);if(!links.length)return;links.forEach(a=>used.add(hrefName(a.getAttribute('href'))));const group=document.createElement('section');group.className='let-erp-menu-group';group.dataset.group=g.name;group.innerHTML='<button class="let-erp-menu-group-btn" type="button"><span class="group-icon">'+g.icon+'</span><span class="group-name">'+g.name+'</span><span class="group-chevron">⌄</span></button><div class="let-erp-menu-group-links"></div>';const linksBox=group.querySelector('.let-erp-menu-group-links');links.forEach(a=>{addStar(a);linksBox.appendChild(a)});const containsCurrent=links.some(a=>hrefName(a.getAttribute('href'))===page);group.classList.toggle('closed',!containsCurrent&&storedClosed(g.name));group.querySelector('.let-erp-menu-group-btn').addEventListener('click',()=>{group.classList.toggle('closed');setStoredClosed(g.name,group.classList.contains('closed'))});body.appendChild(group)});const extras=[...map.entries()].filter(([h])=>!used.has(h)).map(([,a])=>a);if(extras.length){const group=document.createElement('section');group.className='let-erp-menu-group';group.dataset.group='OUTROS';group.innerHTML='<button class="let-erp-menu-group-btn" type="button"><span class="group-icon">🧩</span><span class="group-name">OUTROS</span><span class="group-chevron">⌄</span></button><div class="let-erp-menu-group-links"></div>';extras.forEach(a=>{addStar(a);group.querySelector('.let-erp-menu-group-links').appendChild(a)});const containsCurrent=extras.some(a=>hrefName(a.getAttribute('href'))===page);group.classList.toggle('closed',!containsCurrent&&storedClosed('OUTROS'));group.querySelector('.let-erp-menu-group-btn').addEventListener('click',()=>{group.classList.toggle('closed');setStoredClosed('OUTROS',group.classList.contains('closed'))});body.appendChild(group)}syncStars();refreshGroupVisibility();setTimeout(refreshGroupVisibility,500);setTimeout(refreshGroupVisibility,1500);setTimeout(refreshGroupVisibility,3000)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',buildGroupedMenu);else buildGroupedMenu();
})();
