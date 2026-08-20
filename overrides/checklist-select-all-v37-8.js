/* LET ERP v37.8.1 - Marcar todos no checklist de qualidade (auto-reparo) */
(()=>{
  let queued=false;

  function getGrid(){
    return document.getElementById('qualityGateGrid');
  }

  function getChecks(grid){
    return grid ? [...grid.querySelectorAll('[data-qv37]')] : [];
  }

  function sync(){
    const grid=getGrid();
    const master=document.getElementById('qualityGateSelectAll');
    if(!grid||!master)return;
    const list=getChecks(grid);
    if(!list.length){
      master.checked=false;
      master.indeterminate=false;
      return;
    }
    const marked=list.filter(c=>c.checked).length;
    master.checked=marked===list.length;
    master.indeterminate=marked>0&&marked<list.length;
  }

  function createWrap(grid){
    const wrap=document.createElement('label');
    wrap.id='qualityGateSelectAllWrap';
    wrap.setAttribute('data-let-erp-sticky-select-all','1');
    wrap.style.cssText='display:flex;align-items:center;gap:9px;border:1px solid #99f6e4;background:#f0fdfa;border-radius:10px;padding:10px 12px;margin:0 0 9px;font-size:10px;font-weight:950;color:#0f766e;cursor:pointer;flex:0 0 auto;visibility:visible;opacity:1';
    wrap.innerHTML='<input type="checkbox" id="qualityGateSelectAll" style="width:18px;height:18px;accent-color:#14b8a6;flex:0 0 auto"> <span>MARCAR TODOS OS ITENS</span>';
    grid.parentNode.insertBefore(wrap,grid);
    return wrap;
  }

  function ensure(){
    const grid=getGrid();
    if(!grid||!grid.parentNode)return;

    let wrap=document.getElementById('qualityGateSelectAllWrap');
    let master=document.getElementById('qualityGateSelectAll');

    if(!wrap||!master){
      if(wrap)wrap.remove();
      wrap=createWrap(grid);
      master=document.getElementById('qualityGateSelectAll');
    }else if(wrap.parentNode!==grid.parentNode||wrap.nextElementSibling!==grid){
      grid.parentNode.insertBefore(wrap,grid);
    }

    // Se alguma renderização do modal esconder o controle, restaura imediatamente.
    wrap.style.display='flex';
    wrap.style.visibility='visible';
    wrap.style.opacity='1';
    wrap.hidden=false;
    if(master)master.hidden=false;
    sync();
  }

  function scheduleEnsure(){
    if(queued)return;
    queued=true;
    const run=()=>{queued=false;ensure();};
    if(typeof queueMicrotask==='function')queueMicrotask(run);
    else setTimeout(run,0);
  }

  document.addEventListener('change',e=>{
    const target=e.target;
    const grid=getGrid();
    if(!grid||!target)return;

    if(target.id==='qualityGateSelectAll'){
      getChecks(grid).forEach(c=>{c.checked=target.checked;});
      target.indeterminate=false;
      sync();
      return;
    }

    if(target.matches&&target.matches('[data-qv37]'))sync();
  });

  function start(){
    ensure();
    const root=document.body||document.documentElement;
    if(root){
      new MutationObserver(scheduleEnsure).observe(root,{childList:true,subtree:true});
    }
    // Fallback para renderizações que alterem somente atributos/estilos.
    setInterval(ensure,1200);
  }

  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start,{once:true});
  else start();
})();
