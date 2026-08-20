/* LET ERP v37.7 - finalização robusta + sincronização de atrasos */
(()=>{
  const page=(location.pathname.split('/').pop()||'').toLowerCase();
  if(page!=='painel_producao.html')return;

  const sleep=ms=>new Promise(r=>setTimeout(r,ms));
  async function getDb(){
    for(let i=0;i<80&&!window.letErpSupabase;i++)await sleep(75);
    return window.letErpSupabase||null;
  }

  async function ensureFinalized(db,id,delivered){
    let lastData=null;
    for(let attempt=0;attempt<3;attempt++){
      const {data,error}=await db.rpc('finalizar_pedido_erp',{
        p_pedido_id:String(id),
        p_entregue_marketplace:!!delivered
      });
      if(error)throw error;
      lastData=data;
      await sleep(attempt===0?180:320);
      const {data:check,error:checkError}=await db.from('pedidos').select('id,finalizado,status').eq('id',String(id)).maybeSingle();
      if(checkError)throw checkError;
      if(!check || check.finalizado===true)return lastData;
      console.warn('Pedido foi reaberto por gravação concorrente; reforçando finalização.',id);
    }
    throw new Error('O pedido recebeu uma gravação concorrente e não permaneceu finalizado.');
  }

  async function finalizeOrderV377(id,delivered){
    const db=await getDb();
    if(!db){
      if(typeof showNotice==='function')showNotice('Não foi possível conectar ao banco para finalizar o pedido.');
      return;
    }
    try{
      const data=await ensureFinalized(db,id,delivered);

      if(typeof showNotice==='function')showNotice('✓ Pedido #'+id+' finalizado e enviado para PEDIDOS PRONTOS.');
      try{if(typeof closeModal==='function')closeModal('analysisModal')}catch(e){}
      try{if(typeof closeModal==='function')closeModal('qualityGateModal')}catch(e){}

      // Dá tempo para qualquer realtime/estado antigo terminar e só então
      // recarrega a fonte real do Supabase.
      setTimeout(()=>location.reload(),260);
      return data;
    }catch(e){
      console.error('Finalização v37.7:',e);
      if(typeof showNotice==='function')showNotice('Erro ao finalizar pedido: '+(e?.message||e));
      else alert('Erro ao finalizar pedido: '+(e?.message||e));
    }
  }

  // Remove o listener antigo do checklist. Ele usava updateOrder() e disparava
  // uma gravação completa e antiga do pedido ao mesmo tempo que a RPC de
  // finalização, fazendo finalizado=true voltar para false.
  function installQualityFinalizeFix(){
    const oldBtn=document.getElementById('qualityGateConfirm');
    if(!oldBtn || oldBtn.dataset.finalizeFixV377==='1')return;
    const btn=oldBtn.cloneNode(true);
    btn.dataset.finalizeFixV377='1';
    oldBtn.replaceWith(btn);

    btn.addEventListener('click',async()=>{
      const checks=[...document.querySelectorAll('[data-qv37]')];
      const errorBox=document.getElementById('qualityGateError');
      if(!checks.length || !checks.every(c=>c.checked)){
        if(errorBox)errorBox.style.display='block';
        return;
      }
      if(errorBox)errorBox.style.display='none';

      let id=null,after=null;
      try{
        if(typeof qualityGateOrderId!=='undefined')id=qualityGateOrderId;
        if(typeof qualityGateAfter!=='undefined')after=qualityGateAfter;
      }catch(e){}
      if(!id)return;

      const db=await getDb();
      if(!db)return;
      const checklist={};
      checks.forEach(c=>checklist[c.dataset.qv37]=true);
      btn.disabled=true;
      try{
        const profileId=window.LET_ERP_CURRENT_PROFILE?.id||null;
        const {error}=await db.from('pedidos').update({
          qualidade_checklist:checklist,
          qualidade_aprovado:true,
          qualidade_aprovado_por:profileId,
          qualidade_aprovado_em:new Date().toISOString()
        }).eq('id',String(id)).eq('finalizado',false);
        if(error)throw error;

        // Só depois do checklist estar realmente salvo é que finalizamos.
        try{if(typeof closeModal==='function')closeModal('qualityGateModal')}catch(e){}
        try{qualityGateOrderId=null;qualityGateAfter=null}catch(e){}
        if(typeof after==='function')await after();
        else await finalizeOrderV377(id,false);
      }catch(e){
        console.error('Checklist/finalização:',e);
        btn.disabled=false;
        if(typeof showNotice==='function')showNotice('Erro ao salvar checklist: '+(e?.message||e));
      }
    });
  }

  // Substitui a finalização da v37 por uma RPC atômica no banco.
  window.completeOrderV37=finalizeOrderV377;
  window.finalizarPedido=function(encodedId){
    const id=decodeURIComponent(encodedId);
    let o=null;
    try{o=typeof getOrder==='function'?getOrder(id):null}catch(e){}
    if(!o)return;
    if(o.finalizado){
      if(typeof showNotice==='function')showNotice('Este pedido já está finalizado.');
      return;
    }
    if(typeof openQualityGate==='function'){
      openQualityGate(id,()=>finalizeOrderV377(id,false));
    }else{
      finalizeOrderV377(id,false);
    }
  };

  installQualityFinalizeFix();
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',installQualityFinalizeFix,{once:true});

  // Fallback além do pg_cron do Supabase: sempre que o painel estiver aberto,
  // sincroniza atrasos imediatamente e depois a cada 5 minutos.
  async function syncAutomaticDelays(){
    const db=await getDb();
    if(!db)return;
    try{
      const {error}=await db.rpc('marcar_atrasos_automaticos');
      if(error)console.warn('Atraso automático:',error.message);
    }catch(e){console.warn('Atraso automático:',e)}
  }
  syncAutomaticDelays();
  setInterval(syncAutomaticDelays,5*60*1000);
})();
