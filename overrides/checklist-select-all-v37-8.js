/* LET ERP v37.8 - Marcar todos no checklist de qualidade */
(()=>{
  function init(){
    const master=document.getElementById('qualityGateSelectAll');
    const grid=document.getElementById('qualityGateGrid');
    if(!master||!grid)return;

    const checks=()=>[...grid.querySelectorAll('[data-qv37]')];
    const sync=()=>{
      const list=checks();
      if(!list.length){master.checked=false;master.indeterminate=false;return;}
      const marked=list.filter(c=>c.checked).length;
      master.checked=marked===list.length;
      master.indeterminate=marked>0&&marked<list.length;
    };

    master.addEventListener('change',()=>{
      checks().forEach(c=>{c.checked=master.checked;});
      master.indeterminate=false;
    });

    grid.addEventListener('change',e=>{
      if(e.target&&e.target.matches('[data-qv37]'))sync();
    });

    new MutationObserver(sync).observe(grid,{childList:true,subtree:true});
    sync();
  }

  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);
  else init();
})();
