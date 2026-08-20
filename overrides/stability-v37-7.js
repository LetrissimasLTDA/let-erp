/* LET ERP v37.7 - finalização robusta + sincronização de atrasos */
(()=>{
  const page=(location.pathname.split('/').pop()||'').toLowerCase();
  if(page!=='painel_producao.html')return;

  const sleep=ms=>new Promise(r=>setTimeout(r,ms));
  async function getDb(){
    for(let i=0;i<80&&!window.letErpSupabase;i++)await sleep(75);
    return window.letErpSupabase||null;
  }

  async function finalizeOrderV377(id,delivered){
    const db=await getDb();
    if(!db){
      if(typeof showNotice==='function')showNotice('Não foi possível conectar ao banco para finalizar o pedido.');
      return;
    }
    try{
      const {data,error}=await db.rpc('finalizar_pedido_erp',{
        p_pedido_id:String(id),
        p_entregue_marketplace:!!delivered
      });
      if(error)throw error;

      if(typeof showNotice==='function')showNotice('✓ Pedido #'+id+' finalizado e enviado para PEDIDOS PRONTOS.');
      try{if(typeof closeModal==='function')closeModal('analysisModal')}catch(e){}
      try{if(typeof closeModal==='function')closeModal('qualityGateModal')}catch(e){}

      // Recarrega a fonte real do Supabase. Isso impede que um pedido atrasado
      // seja reaberto por algum estado antigo mantido no navegador.
      setTimeout(()=>location.reload(),220);
      return data;
    }catch(e){
      console.error('Finalização v37.7:',e);
      if(typeof showNotice==='function')showNotice('Erro ao finalizar pedido: '+(e?.message||e));
      else alert('Erro ao finalizar pedido: '+(e?.message||e));
    }
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
