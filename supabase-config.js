// Configuração pública do LET ERP para o Supabase.
// A publishable key pode ficar no frontend; a segurança real é feita por Auth + RLS no Supabase.
window.LET_ERP_SUPABASE_URL = "https://iruyaokicgbwduczxkfi.supabase.co";
window.LET_ERP_SUPABASE_KEY = "sb_publishable_zozFctu93z4GmeDsvDIaZQ_WncpBHmJ";

window.letErpSupabase = window.supabase.createClient(
  window.LET_ERP_SUPABASE_URL,
  window.LET_ERP_SUPABASE_KEY,
  {
    auth: {
      persistSession: true,
      autoRefreshToken: true,
      detectSessionInUrl: true
    }
  }
);

window.letErpGetCurrentProfile = async function() {
  const { data: userData, error: userError } = await window.letErpSupabase.auth.getUser();
  if (userError || !userData || !userData.user) return null;

  const user = userData.user;
  let { data: profile, error } = await window.letErpSupabase
    .from('perfis')
    .select('*')
    .eq('id', user.id)
    .maybeSingle();

  if (error) {
    console.error('Erro ao carregar perfil:', error);
    return { id:user.id, email:user.email || '', nome:'', setor:'', foto_url:'' };
  }

  if (!profile) {
    const payload = { id:user.id, email:user.email || '' };
    const created = await window.letErpSupabase
      .from('perfis')
      .upsert(payload)
      .select('*')
      .single();
    profile = created.data || payload;
  }

  profile.email = profile.email || user.email || '';
  window.LET_ERP_CURRENT_PROFILE = profile;
  return profile;
};

window.letErpProfileComplete = function(profile) {
  return !!(profile && String(profile.nome || '').trim() && String(profile.setor || '').trim());
};

window.letErpRequireAuth = async function() {
  const { data, error } = await window.letErpSupabase.auth.getSession();
  if (error) console.error('Erro ao verificar sessão:', error);

  if (!data || !data.session) {
    const next = encodeURIComponent(location.pathname.split('/').pop() || 'painel_producao.html');
    location.replace('login.html?next=' + next);
    return null;
  }

  const profile = await window.letErpGetCurrentProfile();
  const page = (location.pathname.split('/').pop() || 'painel_producao.html').toLowerCase();

  if (page !== 'perfil.html' && !window.letErpProfileComplete(profile)) {
    const next = encodeURIComponent(page + location.search);
    location.replace('perfil.html?next=' + next);
    return null;
  }

  return data.session;
};

window.letErpLogout = async function() {
  await window.letErpSupabase.auth.signOut();
  window.LET_ERP_CURRENT_PROFILE = null;
  location.replace('login.html');
};
