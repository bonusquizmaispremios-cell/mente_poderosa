import streamlit as st
from groq import Groq
from datetime import datetime
import json

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="MENTE PODEROSA", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp { background-color:#F6FBF4; font-family:'Inter',sans-serif; }
    [data-testid="stSidebar"] { display:none; }

    .stTextInput>div>div>input, .stTextArea>div>textarea,
    .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color:#FFFFFF !important; color:#1A1A2E !important;
        border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    }

    .stButton>button {
        width:100%; border-radius:10px; height:3.2em;
        background:linear-gradient(135deg,#16A34A,#15803D) !important; color:white !important;
        font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
        font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
    }
    .stButton>button:hover { background:linear-gradient(135deg,#15803D,#166534) !important; transform:translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

    .stApp h1, .stApp h2, .stApp h3 { color:#14532D !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }

    .card { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color:#14532D !important; }

    .card-dark { background:linear-gradient(135deg,#DCFCE7,#D1FAE5); padding:20px; border-radius:14px; border:1px solid #6EE7B7; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong { color:#14532D !important; }

    .card-green { background:linear-gradient(135deg,#DCFCE7,#BBF7D0); padding:20px; border-radius:14px; border:1px solid #4ADE80; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div { color:#14532D !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; white-space:normal; word-wrap:break-word; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow span, .stApp .card-yellow div { color:#78350F !important; }

    .stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #86EFAC; }
    .stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#14532D !important; }
    .stApp .stat-numero, .stat-numero { font-size:2em; font-weight:700; color:#166534 !important; }

    .hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #86EFAC; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div, .stApp .hist-item small { color:#14532D !important; }

    .badge { background:#166534; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-azul { background:#1D4ED8; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#86EFAC,transparent); margin:18px 0; }

    .chat-user { background:#FFFFFF; border:1px solid #86EFAC; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#14532D !important; }

    .chat-persona { background:#F6FBF4; border:1px solid #86EFAC; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona span, .stApp .chat-persona div { color:#14532D !important; }

    .questao-box { background:#FFFFFF; border:2px solid #86EFAC; border-radius:12px; padding:18px; margin-bottom:14px; }
    .stApp .questao-box, .stApp .questao-box p, .stApp .questao-box span, .stApp .questao-box div { color:#14532D !important; }

    .avaliacao-box { background:#FFFFFF; border:2px solid #86EFAC; border-radius:14px; padding:18px; margin-bottom:12px; }
    .stApp .avaliacao-box, .stApp .avaliacao-box p, .stApp .avaliacao-box span, .stApp .avaliacao-box div { color:#14532D !important; }

    .meta-box { background:#FFFFFF; border:2px solid #86EFAC; border-radius:12px; padding:16px; text-align:center; margin:10px 0; }
    .stApp .meta-box, .stApp .meta-box div, .stApp .meta-box span { color:#14532D !important; }
    .stApp .meta-numero { font-size:2em; font-weight:700; color:#166534 !important; }

    .chat-scroll-container { max-height:40vh; overflow-y:auto; display:flex; flex-direction:column; scroll-behavior:smooth; padding-bottom:4px; }
    .chat-scroll-container > * { flex-shrink:0; }
    

    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CACHE
# ─────────────────────────────────────────────
@st.cache_resource
def get_cache_mente():
    return {"perfis": {}}

_cache = get_cache_mente()

# ─────────────────────────────────────────────
# PERSISTÊNCIA LOCAL (JSON)
# ─────────────────────────────────────────────
CHAVES_SALVAR = [
    'usuario', 'historico_sessoes', 'conteudos_salvos',
    'maior_bloqueio', 'objetivo_mental', 'estado_emocional',
    'crencas_limitantes', 'sessoes_meditacao', 'diario_entradas',
]

def gerar_json_sessao() -> str:
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados['salvo_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados):
    _bloq = {'api_key','etapa','nome_login','chave_login','upload_login','btn_entrar_login'}
    _pref = (
        'btn_','sel_','ul_','dl_','cad_','_sub','_sm','_tab','_bsc',
        'ativo_','rem_','sel_pet_','ev_','prof_','hig_','prev_',
        'vac_','sint_','comp_','trad_','subs_','amb_','viag_','chat_',
        'duvida_','emerg_','peso_','data_','obs_','tipo_','vet_','desc_',
        'local_','prox_','alim','sit_emerg_','tc_','oraf','siau','agmag',
        'lv','mv','pt','pi','sh','wc','rv','rp','rc',
    )
    import re as _re
    for k, v in dados.items():
        if k in _bloq: continue
        if any(k.startswith(p) for p in _pref): continue
        if _re.match(r'.+_\d+$', k): continue
        st.session_state[k] = v

def salvar_perfil_cache(usuario: str):
    _cache["perfis"][usuario] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos() -> list:
    return list(_cache["perfis"].keys())

def carregar_perfil_cache(usuario: str) -> dict | None:
    return _cache["perfis"].get(usuario)

def salvar_sessao(tipo: str, tema: str, conteudo: str):
    st.session_state.historico_sessoes.append({
        'data':    datetime.now().strftime('%d/%m %H:%M'),
        'tipo':    tipo,
        'tema':    tema,
        'conteudo': conteudo,
    })

# --- INICIALIZAÇÃO DE ESTADO ---
defaults = {
    'etapa':             "Login",
    'usuario':           "",
    'api_key':           "",
    'pagina':            "Home",
    'historico_sessoes': [],
    'conteudos_salvos':  [],
    'maior_bloqueio':    "",
    'objetivo_mental':   "",
    'estado_emocional':  "Neutro",
    'crencas_limitantes':"",
    'sessoes_meditacao': 0,
    'diario_entradas':   [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- MOTOR DE IA ---
def mente_ia(prompt: str, system_extra: str = "") -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        system = f"""Você é um especialista em neurolinguística (PNL), meditação e reprogramação mental.
Usuário: {st.session_state.usuario}.
Maior bloqueio atual: {st.session_state.maior_bloqueio or 'não informado'}.
Objetivo mental: {st.session_state.objetivo_mental or 'não informado'}.
Estado emocional: {st.session_state.estado_emocional}.
{system_extra}
PRINCÍPIOS:
- Baseie-se em PNL, Mindfulness, Terapia Cognitivo-Comportamental e Neurociência
- Tom acolhedor, seguro e transformador — nunca julgue
- Linguagem acessível, sem jargões técnicos desnecessários
- Sempre oriente a buscar ajuda profissional para casos clínicos sérios
- Escreva em português brasileiro natural e humanizado"""
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system},
                {"role": "user",   "content": prompt},
            ],
            model="openai/gpt-oss-120b",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

# --- BARRA DE SALVAR ---
def barra_salvar():
    salvar_perfil_cache(st.session_state.usuario)
    nome_usuario = st.session_state.usuario.lower().replace(' ', '_') or 'minha_sessao'
    total   = len(st.session_state.historico_sessoes)
    salvos  = len(st.session_state.conteudos_salvos)
    medit   = st.session_state.sessoes_meditacao
    diario  = len(st.session_state.diario_entradas)

    col_info, col_btn = st.columns([4, 2])
    with col_info:
        st.markdown(
            f"<div style='background:#F5F3FF;border:1px solid #C4B5FD;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#1A1A2E;line-height:1.6;'>"
            f"💾 <strong>Antes de sair, salve seus dados no computador.</strong><br>"
            f"<span style='color:#888;font-size:0.88em;'>{total} sessões · "
            f"{medit} meditações · {diario} entradas no diário · {salvos} salvos</span>"
            f"</div>",
            unsafe_allow_html=True
        )
    with col_btn:
        st.download_button(
            label="💾 SALVAR MEUS DADOS (.json)",
            data=gerar_json_sessao(),
            file_name=f"mente_poderosa_{nome_usuario}.json",
            mime="application/json",
            use_container_width=True,
            key="mentepod44"
        )
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("""<style>
    .dica-nav{font-size:0.72em;color:#94A3B8;text-align:center;padding:2px 0 6px;}
    .dica-mobile{display:none;}
    .dica-desktop{display:block;}
    @media(max-width:768px){.dica-mobile{display:block;}.dica-desktop{display:none;}}
    </style>
    <div class='dica-nav dica-mobile'>👆 Deslize o dedo para navegar entre as abas</div>
    <div class='dica-nav dica-desktop'>📋 Clique no ícone acima para abrir o menu completo</div>
    """, unsafe_allow_html=True)

# ============================================================
# TELA: LOGIN
# ============================================================
if 'conteudos_salvos' not in st.session_state: st.session_state['conteudos_salvos'] = None
if 'crencas_limitantes' not in st.session_state: st.session_state['crencas_limitantes'] = None
if 'diario_entradas' not in st.session_state: st.session_state['diario_entradas'] = None
if 'estado_emocional' not in st.session_state: st.session_state['estado_emocional'] = None
if 'historico_sessoes' not in st.session_state: st.session_state['historico_sessoes'] = []
if 'maior_bloqueio' not in st.session_state: st.session_state['maior_bloqueio'] = None
if 'objetivo_mental' not in st.session_state: st.session_state['objetivo_mental'] = None
if 'sessoes_meditacao' not in st.session_state: st.session_state['sessoes_meditacao'] = None

if st.session_state.etapa == "Login":
    st.markdown("# 🤖 MENTE PODEROSA")
    st.markdown("<div class=\'card\'><b>🔒 ACESSO RESTRITO A CLIENTES DO QUIZ COM PRÊMIOS</b><br>🔗 <a href='https://quizcompremios.com.br' target='_blank' style='color:#4F46E5;font-weight:700;text-decoration:underline;'>quizcompremios.com.br</a></div>", unsafe_allow_html=True)
    st.info("💻 **Dica:** Pela complexidade dos agentes, no computador a experiência é mais agradável.")
    with st.container():
        nome  = st.text_input("Seu Nome:", key="nome_login")
        chave = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_login")
        arq_j = st.file_uploader("📂 Carregar dados salvos (.json):", type=["json"], key="upload_login")
        dados_login = json.load(arq_j) if arq_j else None
        if st.button("✨ ENTRAR", key="btn_entrar_login"):
            if len(nome.strip()) < 2:
                st.warning("Digite um nome com pelo menos 2 caracteres.")
            elif chave.strip():
                st.session_state.usuario = nome.strip()
                st.session_state.api_key = chave
                if dados_login: carregar_json_sessao(dados_login)
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

elif st.session_state.etapa == "App":



    # TABS — navegação nativa
    (_tab_Home, _tab_Ansiedade, _tab_Autoestima, _tab_Proposito, _tab_Emocoes, _tab_Crencas, _tab_Meditacao, _tab_Diario, _tab_Progresso) = st.tabs(['🏠 Painel', '😰 Ansiedade', '💪 Autoestima', '🌟 Propósito', '❤️ Emoções', '🧠 Crenças', '🧘 Meditação', '📓 Diário', '📈 Progresso'])

    # ── BARRA SALVAR — aparece em todas as abas ──
    with st.expander("💾 Salvar / Carregar meus dados", expanded=False):
        _bsc1, _bsc2 = st.columns(2)
        with _bsc1:
            import json as _jsv
            _dsv = {k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith('_') and k not in ('api_key',)}
            st.download_button("💾 Baixar meus dados (.json)",
                data=_jsv.dumps(_dsv, ensure_ascii=False, indent=2, default=str),
                file_name=f"dados_{st.session_state.get('usuario','user')}.json",
                mime="application/json", key="dl_barra_sv_mentepod")
        with _bsc2:
            _fupsv = st.file_uploader("📂 Carregar dados salvos:", type=["json"], key="ul_barra_sv_mentepod", label_visibility="collapsed")
            if _fupsv:
                try:
                    import json as _jld
                    for _k2,_v2 in _jld.loads(_fupsv.read().decode()).items():
                        if _k2 not in ('api_key','etapa'): st.session_state[_k2] = _v2
                    st.success("✅ Dados restaurados!"); st.rerun()
                except: st.error("Arquivo inválido.")


    with _tab_Home:
        col_u, col_r = st.columns([3, 1])
        with col_u:
            st.title(f"Bem-vindo, {st.session_state.usuario} 🧠✨")
            st.markdown("<span class='badge'>Jornada Mental</span>", unsafe_allow_html=True)
        with col_r:
            if st.button("🚪 Sair", key="mentepod3"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

        # AVISO SE DADOS SUMIRAM
        total_h = len(st.session_state.historico_sessoes)
        if total_h == 0 and st.session_state.sessoes_meditacao == 0:
            st.markdown("""<div style="background:#FEF3C7;border:2px solid #F59E0B;border-radius:12px;
            padding:12px 18px;margin-bottom:4px;color:#000;font-size:0.9em;font-weight:600;">
            ⚠️ Seus dados não estão mais no servidor.
            </div>""", unsafe_allow_html=True)
            arq_home = st.file_uploader("Carregar meus dados salvos (.json):", type=["json"], key="upload_home")
            if arq_home is not None:
                try:
                    dados_home = json.load(arq_home)
                    carregar_json_sessao(dados_home)
                    salvar_perfil_cache(st.session_state.usuario)
                    st.success("✅ Dados recuperados!")
                    st.rerun()
                except Exception:
                    st.error("Arquivo inválido.")

        # PERFIL MENTAL
        st.markdown("#### 🌱 Seu perfil mental")
        col_a, col_b = st.columns(2)
        with col_a:
            st.session_state.maior_bloqueio   = st.text_input(
                "Seu maior bloqueio mental hoje:", value=st.session_state.maior_bloqueio,
                placeholder="ex: ansiedade, baixa autoestima, procrastinação, medo de falhar...", key="mentepod43")
            st.session_state.objetivo_mental  = st.text_input(
                "O que você quer transformar na sua mente:", value=st.session_state.objetivo_mental,
                placeholder="ex: ter mais confiança, parar de me sabotar, dormir melhor...", key="mentepod42")
        with col_b:
            st.session_state.estado_emocional = st.select_slider(
                "Como você está agora:", options=[
                    "Muito mal 😔","Mal 😟","Neutro 😐","Bem 🙂","Muito bem 😁"
                ], value=st.session_state.estado_emocional if st.session_state.estado_emocional in
                ["Muito mal 😔","Mal 😟","Neutro 😐","Bem 🙂","Muito bem 😁"] else "Neutro 😐", key="mentepod41")
            st.session_state.crencas_limitantes = st.text_area(
                "Crenças que te limitam (opcional):", value=st.session_state.crencas_limitantes,
                height=80,
                placeholder="ex: não sou inteligente o suficiente, não mereço ser feliz, sempre falho...", key="mentepod40")


        # MÉTRICAS
        tipos = {}
        for s in st.session_state.historico_sessoes:
            tipos[s['tipo']] = tipos.get(s['tipo'], 0) + 1

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{total_h}</div><div>Sessões realizadas</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.sessoes_meditacao}</div><div>Meditações 🧘</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.diario_entradas)}</div><div>Entradas no diário</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.conteudos_salvos)}</div><div>Conteúdos salvos</div></div>", unsafe_allow_html=True)
        c5.markdown(f"<div class='stat-box'><div class='stat-numero'>{tipos.get('PNL',0)}</div><div>Sessões de PNL</div></div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>💡 <em>'A mente que se abre a uma nova ideia jamais volta ao seu tamanho original.'</em> — Albert Einstein</div>", unsafe_allow_html=True)

        st.markdown("### 🗺️ O que cada aba faz")
        guia = {
            "🧘 Meditação":          "Scripts de meditação guiada personalizados para o seu momento",
            "🗣️ PNL":               "Técnicas de reprogramação: ancoragem, reframing, linha do tempo",
            "💬 Afirmações":         "Afirmações criadas para o SEU problema real — não as genéricas",
            "😴 Sono":               "Protocolo completo para dormir melhor e acordar descansado",
            "😰 Ansiedade":          "Técnicas de respiração, grounding e protocolo de crise",
            "🎯 Visualização":       "Script de visualização criativa do futuro que você quer construir",
            "📖 Diário Mental":      "Prompts de reflexão diária para autoconhecimento profundo",
            "❤️ Salvos":             "Seus conteúdos favoritos e histórico completo",
        }
        for aba, desc in guia.items():
            st.markdown(f"**{aba}** — {desc}")

        if st.session_state.historico_sessoes:
            st.markdown("### 🕐 Últimas Sessões")
            for item in reversed(st.session_state.historico_sessoes[-4:]):
                st.markdown(
                    f"<div class='hist-item'>"
                    f"<span class='badge'>{item['tipo']}</span> "
                    f"<span class='badge-teal'>{item.get('tema', '')[:30]}</span> "
                    f"<small style='color:#888'>{item['data']}</small></div>",
                    unsafe_allow_html=True
                )

        # ========================
        # MEDITAÇÃO GUIADA
        # ========================

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("### 💾 Salvar e Carregar Dados")
        _csl1, _csl2 = st.columns(2)
        with _csl1:
            import json as _json_sv
            _dados_sv = {k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith('_')}
            st.download_button("💾 Salvar dados (.json)",
                data=_json_sv.dumps(_dados_sv, ensure_ascii=False, indent=2, default=str),
                file_name=f"dados_{st.session_state.get('usuario','user')}.json",
                mime="application/json", key="dl_sv_mentepod")
        with _csl2:
            _arq_sv = st.file_uploader("📂 Carregar dados:", type=["json"], key="ul_sv_mentepod")
            if _arq_sv:
                try:
                    import json as _json_ld
                    for _k, _v in _json_ld.loads(_arq_sv.read().decode()).items():
                        st.session_state[_k] = _v
                    st.success("✅ Dados carregados!")
                    st.rerun()
                except: st.error("Arquivo inválido.")

    with _tab_Ansiedade:
        st.header("😰 Gestão de Ansiedade")
        st.markdown("Técnicas de respiração, grounding e protocolos para momentos de crise.")

        st.markdown("""<div style="background:#FFF1F2;border:1px solid #FDA4AF;border-radius:10px;
        padding:10px 14px;margin-bottom:16px;font-size:0.85em;color:#1A1A2E;">
        ⚠️ <strong>Importante:</strong> Este conteúdo é para bem-estar geral. Em casos de ansiedade severa,
        transtorno de pânico ou crises frequentes, procure um psicólogo ou psiquiatra.
        </div>""", unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["🌬️ Técnicas de Respiração","🌍 Grounding e Protocolo de Crise"])

        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                nivel_ans = st.select_slider("Nível de ansiedade agora:", options=[
                    "Leve (1-3)","Moderada (4-6)","Intensa (7-8)","Muito intensa (9-10)"
                ], key="mentepod15_d2")
                tipo_resp = st.selectbox("Técnica de respiração:", [
                    "Respiração 4-7-8 (para dormir e acalmar)","Respiração diafragmática (base)",
                    "Respiração quadrada (box breathing)","Respiração coerente (5-5)",
                    "Respiração alternada (ioga)","Técnica mais indicada para meu caso",
                ], key="mentepod14_d2")
            with col2:
                contexto_ans = st.text_input("Em que situação costuma sentir ansiedade:",
                    placeholder="ex: antes de reuniões, em locais cheios, ao receber críticas...", key="mentepod13_d2")
                duracao_resp = st.selectbox("Tempo disponível:", ["2 minutos","5 minutos","10 minutos","15 minutos"], key="mentepod17_d2")

            if st.button("🌬️ GERAR PROTOCOLO DE RESPIRAÇÃO", key="mentepod18_d2"):
                with st.spinner("Criando seu protocolo de respiração..."):
                    prompt = (
                        f"Crie um protocolo completo de respiração para ansiedade.\n"
                        f"Nível atual: {nivel_ans}. Técnica: {tipo_resp}.\n"
                        f"Contexto de ansiedade: {contexto_ans}. Tempo: {duracao_resp}.\n\n"
                        f"ESTRUTURA:\n\n"
                        f"🌬️ PROTOCOLO DE RESPIRAÇÃO\n"
                        f"Técnica: {tipo_resp} | Para: {nivel_ans}\n\n"
                        f"🧠 COMO ESSA TÉCNICA FUNCIONA NO CÉREBRO:\n"
                        f"[Neurociência simples — como a respiração acalma o sistema nervoso]\n\n"
                        f"📋 PROTOCOLO PASSO A PASSO:\n\n"
                        f"ANTES DE COMEÇAR:\n[Posição, olhos, onde fazer]\n\n"
                        f"A TÉCNICA (com timer):\n"
                        f"[Instruções detalhadas — inspire por X, segure por X, expire por X]\n"
                        f"[Quantas rodadas fazer em {duracao_resp}]\n"
                        f"[O que visualizar ou focar durante]\n\n"
                        f"APÓS A TÉCNICA:\n[O que fazer nos 2 minutos seguintes]\n\n"
                        f"⚡ VERSÃO DE EMERGÊNCIA (30 segundos):\n"
                        f"[Para quando a ansiedade pega de surpresa no contexto '{contexto_ans}']\n\n"
                        f"📅 PRÁTICA PREVENTIVA:\n"
                        f"[Como usar essa técnica antes que a ansiedade apareça]"
                    )
                    res = mente_ia(prompt)
                    if res: st.session_state['res_ansiedade_mentep1'] = str(res)
                    salvar_sessao("Ansiedade", f"Respiração: {tipo_resp[:30]}", res)
                    st.session_state['resp_temp'] = res
                    st.markdown(f"<div class='card-teal'>{res}</div>", unsafe_allow_html=True)

            if st.session_state.get('resp_temp'):
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar protocolo (.txt)", data=st.session_state['resp_temp'],
                        file_name="respiracao_ansiedade.txt", mime="text/plain", use_container_width=True, key="mentepod12_d2")
                with col_sv:
                    if st.button("❤️ Salvar", key="sv_resp", use_container_width=True):
                        st.session_state.conteudos_salvos.append({
                            'tipo': 'Respiração', 'tema': tipo_resp[:40] if 'tipo_resp' in dir() else '',
                            'conteudo': st.session_state['resp_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M'),
                        })
                        st.success("❤️ Salvo!")

        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                tipo_crise = st.selectbox("Tipo de crise mais frequente:", [
                    "Ansiedade generalizada","Ataque de pânico","Overthinking (pensamentos acelerados)",
                    "Crise de choro","Paralisia por medo","Dissociação (se sentir fora do corpo)",
                ], key="mentepod11_d2")
                gatilho    = st.text_input("Principal gatilho:", placeholder="ex: conflito com alguém, notícias ruins, solidão...", key="mentepod19_d2")
            with col2:
                suporte    = st.text_input("O que já ajudou você antes:", placeholder="ex: música, ligar para alguém, caminhar...", key="mentepod20_d2")

            if st.button("🌍 GERAR PROTOCOLO DE CRISE", key="mentepod21_d2"):
                with st.spinner("Criando seu protocolo de emergência..."):
                    prompt = (
                        f"Crie um protocolo de grounding e gestão de crise.\n"
                        f"Tipo de crise: {tipo_crise}. Gatilho: {gatilho}.\n"
                        f"O que já ajudou: {suporte or 'não informado'}.\n\n"
                        f"ESTRUTURA:\n\n"
                        f"🌍 PROTOCOLO DE EMERGÊNCIA — {tipo_crise.upper()}\n\n"
                        f"⚡ TÉCNICA DOS 5-4-3-2-1 (GROUNDING IMEDIATO):\n"
                        f"[Adaptada especificamente para {tipo_crise}]\n"
                        f"5 coisas que você VÊ: [exemplos contextualizados]\n"
                        f"4 coisas que você pode TOCAR: [exemplos]\n"
                        f"3 coisas que você OUVE: [exemplos]\n"
                        f"2 coisas que você CHEIRA: [exemplos]\n"
                        f"1 coisa que você SENTE no paladar: [exemplos]\n\n"
                        f"🚨 PROTOCOLO DOS PRIMEIROS 10 MINUTOS DE CRISE:\n"
                        f"Minuto 1-2: [ação imediata]\n"
                        f"Minuto 3-5: [técnica de respiração específica]\n"
                        f"Minuto 6-10: [grounding e ancoragem]\n\n"
                        f"💬 O QUE DIZER PARA SI MESMO (diálogo interno de crise):\n"
                        f"[Frases específicas para {tipo_crise} — que realmente acalmam]\n\n"
                        f"📲 PLANO DE AÇÃO PÓS-CRISE:\n"
                        f"[O que fazer nas horas seguintes para se recuperar]\n\n"
                        f"🛡️ PREVENÇÃO — IDENTIFICAR O GATILHO '{gatilho}':\n"
                        f"[Como perceber que a crise está chegando antes de começar]\n\n"
                        f"📞 QUANDO BUSCAR AJUDA PROFISSIONAL:\n"
                        f"[Sinais claros de que precisa de apoio especializado]"
                    )
                    res = mente_ia(prompt)
                    if res: st.session_state['res_ansiedade_mentep2'] = str(res)
                    salvar_sessao("Ansiedade", f"Protocolo de crise: {tipo_crise}", res)
                    st.session_state['crise_temp'] = res
                    st.markdown(f"<div class='card-orange'>{res}</div>", unsafe_allow_html=True)

            if st.session_state.get('crise_temp'):
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar protocolo (.txt)", data=st.session_state['crise_temp'],
                        file_name="protocolo_crise.txt", mime="text/plain", use_container_width=True, key="mentepod10_d2")
                with col_sv:
                    if st.button("❤️ Salvar", key="sv_crise", use_container_width=True):
                        st.session_state.conteudos_salvos.append({
                            'tipo': 'Protocolo de Crise', 'tema': tipo_crise if 'tipo_crise' in dir() else '',
                            'conteudo': st.session_state['crise_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M'),
                        })
                        st.success("❤️ Salvo!")

        # ========================
        # VISUALIZAÇÃO CRIATIVA
        # ========================

    with _tab_Autoestima:
        st.header("💪 Autoestima e Autoconfiança")
        st.markdown("*Fortaleça sua autoestima com apoio da IA.*")
        _prompt_autoestima = st.text_area("Descreva sua situação ou dúvida:", height=120, key="mentep_autoestima_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="mentep_autoestima_btn", use_container_width=True):
            if _prompt_autoestima.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_autoestima}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Proposito:
        st.header("🌟 Propósito de Vida")
        st.markdown("*Descubra e alinhe seu propósito de vida.*")
        _prompt_proposito = st.text_area("Descreva sua situação ou dúvida:", height=120, key="mentep_proposito_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="mentep_proposito_btn", use_container_width=True):
            if _prompt_proposito.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_proposito}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Emocoes:
        st.header("❤️ Regulação Emocional")
        st.markdown("*Aprenda a reconhecer e regular suas emoções.*")
        _prompt_emocoes = st.text_area("Descreva sua situação ou dúvida:", height=120, key="mentep_emocoes_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="mentep_emocoes_btn", use_container_width=True):
            if _prompt_emocoes.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_emocoes}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Crencas:
        st.header("🧠 Crenças Limitantes")
        st.markdown("*Identifique e transforme crenças que te travam.*")
        _prompt_crencas = st.text_area("Descreva sua situação ou dúvida:", height=120, key="mentep_crencas_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="mentep_crencas_btn", use_container_width=True):
            if _prompt_crencas.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_crencas}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Meditacao:
        st.header("🧘 Meditação Guiada")
        st.markdown("Scripts de meditação personalizados — para o seu momento e o que você precisa agora.")

        col1, col2 = st.columns(2)
        with col1:
            objetivo_med = st.selectbox("O que você quer trabalhar:", [
                "Ansiedade e tensão","Foco e clareza mental","Autoestima e autoconfiança",
                "Sono e relaxamento profundo","Gratidão e paz interior",
                "Cura emocional","Energia e motivação","Presença e mindfulness",
            ], key="mentepod39")
            tempo_med    = st.selectbox("Tempo disponível:", [
                "5 minutos (meditação rápida)","10 minutos","15 minutos",
                "20 minutos","30 minutos (meditação profunda)",
            ], key="mentepod38")
        with col2:
            estilo_med   = st.selectbox("Estilo de meditação:", [
                "Respiração consciente","Body scan (varredura corporal)",
                "Visualização guiada","Mantra e repetição",
                "Mindfulness (atenção plena)","Meditação transcendental (adaptada)",
            ], key="mentepod37")
            experiencia  = st.radio("Experiência com meditação:", ["Nunca meditei","Já meditei algumas vezes","Medito com frequência"], horizontal=True, key="mentepod4")

        if st.button("🧘 GERAR MEDITAÇÃO GUIADA", key="mentepod5"):
            with st.spinner("Preparando sua meditação personalizada..."):
                prompt = (
                    f"Crie um script completo de meditação guiada.\n"
                    f"Objetivo: {objetivo_med}. Tempo: {tempo_med}.\n"
                    f"Estilo: {estilo_med}. Experiência: {experiencia}.\n"
                    f"Estado emocional atual: {st.session_state.estado_emocional}.\n"
                    f"Maior bloqueio: {st.session_state.maior_bloqueio or 'não informado'}.\n\n"
                    f"FORMATO:\n\n"
                    f"🧘 MEDITAÇÃO: {objetivo_med.upper()}\n"
                    f"Duração: {tempo_med} | Estilo: {estilo_med}\n\n"
                    f"━━━━━━━━━━━━━━━━━━━━━\n"
                    f"PREPARAÇÃO (antes de começar):\n"
                    f"[Como se posicionar, ambiente ideal, o que desligar]\n\n"
                    f"━━━━━━━━━━━━━━━━━━━━━\n"
                    f"INÍCIO — ÂNCORA (2 min):\n"
                    f"[Script palavra por palavra — voz suave, pausas indicadas com '...']]\n"
                    f"[Use '(pausa de X segundos)' para indicar silêncios]\n\n"
                    f"DESENVOLVIMENTO — NÚCLEO ({tempo_med} principal):\n"
                    f"[Script completo da meditação — específico para {objetivo_med}]\n"
                    f"[Inclua respiração, visualizações ou mantras conforme o estilo]\n\n"
                    f"ENCERRAMENTO — RETORNO (2 min):\n"
                    f"[Como sair gentilmente da meditação]\n"
                    f"━━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"💡 DICA PÓS-MEDITAÇÃO:\n"
                    f"[O que fazer nos 5 minutos após a meditação para fixar o estado]\n\n"
                    f"📅 FREQUÊNCIA RECOMENDADA:\n"
                    f"[Quantas vezes por semana e quando é o melhor horário]\n\n"
                    f"🌱 PRÓXIMO PASSO:\n"
                    f"[Como evoluir essa prática ao longo do tempo]"
                )
                res = mente_ia(prompt)
                if res: st.session_state['res_meditacao_mentep3'] = str(res)
                salvar_sessao("Meditação", objetivo_med, res)
                st.session_state.sessoes_meditacao += 1
                st.session_state['med_temp'] = res
                st.markdown(f"<div class='card-dark'>{res}</div>", unsafe_allow_html=True)
                st.success(f"🎉 Meditação {st.session_state.sessoes_meditacao} concluída!")

        if st.session_state.get('med_temp'):
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar meditação (.txt)",
                    data=st.session_state['med_temp'],
                    file_name=f"meditacao_{objetivo_med.replace(' ','_') if 'objetivo_med' in dir() else 'guiada'}.txt",
                    mime="text/plain", use_container_width=True, key="mentepod36")
            with col_sv:
                if st.button("❤️ Salvar meditação", use_container_width=True, key="mentepod6"):
                    st.session_state.conteudos_salvos.append({
                        'tipo': 'Meditação', 'tema': objetivo_med if 'objetivo_med' in dir() else '',
                        'conteudo': st.session_state['med_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("❤️ Salvo!")

        # ========================
        # REPROGRAMAÇÃO COM PNL
        # ========================

    with _tab_Diario:
        st.header("📖 Diário Mental")
        st.markdown("Reflexões guiadas para autoconhecimento profundo — com prompts personalizados pela IA.")

        tab1, tab2 = st.tabs(["✍️ Escrever Hoje","📚 Entradas Anteriores"])

        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                tipo_diario = st.selectbox("Tipo de reflexão de hoje:", [
                    "Reflexão do dia (como foi meu dia)","Gratidão profunda","Autoconhecimento",
                    "Processamento emocional","Planejamento do eu futuro",
                    "Perdão e cura","Crenças e padrões","Livre (IA escolhe pelo meu perfil)",
                ], key="mentepod6_d2")
                estado_hoje = st.select_slider("Como você está agora:", options=[
                    "Muito mal 😔","Mal 😟","Neutro 😐","Bem 🙂","Muito bem 😁"
                ], key="mentepod5_d2")
            with col2:
                evento_hoje = st.text_area("O que aconteceu de significativo hoje:", height=80,
                    placeholder="ex: tive uma briga, recebi uma notícia boa, me senti inseguro em algo...", key="mentepod4_d2")

            if st.button("📖 GERAR PROMPTS DO DIÁRIO", key="mentepod26_d2"):
                with st.spinner("Criando seus prompts personalizados..."):
                    prompt = (
                        f"Crie prompts de diário mental personalizados.\n"
                        f"Tipo: {tipo_diario}. Estado: {estado_hoje}.\n"
                        f"Evento do dia: {evento_hoje or 'não informado'}.\n"
                        f"Maior bloqueio: {st.session_state.maior_bloqueio or 'não informado'}.\n\n"
                        f"ESTRUTURA:\n\n"
                        f"📖 DIÁRIO MENTAL — {tipo_diario.upper()}\n"
                        f"Data: {datetime.now().strftime('%d/%m/%Y')} | Estado: {estado_hoje}\n\n"
                        f"✍️ SEUS PROMPTS DE HOJE (responda com calma, sem julgamento):\n\n"
                        f"[Crie 7-10 prompts profundos e específicos para {tipo_diario}]\n"
                        f"[Cada prompt deve ser uma pergunta aberta que leva à introspecção]\n"
                        f"[Adapte ao estado '{estado_hoje}' e ao evento '{evento_hoje}']\n"
                        f"[Progressão: do mais fácil ao mais profundo]\n\n"
                        f"💡 DICA DE ESCRITA:\n"
                        f"[Como escrever sem censura — técnica do fluxo de consciência]\n\n"
                        f"🌱 INSIGHT PARA FECHAR:\n"
                        f"[Uma reflexão ou perspectiva para encerrar a sessão do diário]\n\n"
                        f"⏰ TEMPO SUGERIDO: [quanto tempo dedicar a esse diário hoje]"
                    )
                    res = mente_ia(prompt)
                    if res: st.session_state['res_diario_mentep4'] = str(res)
                    st.session_state['diario_prompts'] = res
                    st.markdown(f"<div class='card-pink'>{res}</div>", unsafe_allow_html=True)

            if st.session_state.get('diario_prompts'):
                st.markdown("#### ✍️ Escreva aqui sua reflexão:")
                reflexao = st.text_area("Sua reflexão de hoje:", height=200,
                    placeholder="Escreva livremente, sem julgamento. Isso é só seu...", key="mentepod3_d2")

                col_sv, col_dl = st.columns(2)
                with col_sv:
                    if st.button("💾 Salvar entrada no diário", use_container_width=True, key="mentepod27_d2"):
                        if reflexao.strip():
                            st.session_state.diario_entradas.append({
                                'data':     datetime.now().strftime('%d/%m/%Y %H:%M'),
                                'tipo':     tipo_diario if 'tipo_diario' in dir() else '',
                                'estado':   estado_hoje if 'estado_hoje' in dir() else '',
                                'prompts':  st.session_state.get('diario_prompts', ''),
                                'reflexao': reflexao,
                            })
                            salvar_sessao("Diário", tipo_diario if 'tipo_diario' in dir() else 'Reflexão', reflexao[:60])
                            st.success("📖 Entrada salva no seu diário!")
                            st.rerun()
                        else:
                            st.warning("Escreva sua reflexão antes de salvar.")
                with col_dl:
                    if reflexao.strip():
                        entrada_txt = f"DIÁRIO MENTAL — {datetime.now().strftime('%d/%m/%Y')}\n\nPROMPTS:\n{st.session_state.get('diario_prompts','')}\n\nMINHA REFLEXÃO:\n{reflexao}"
                        st.download_button("📋 Baixar entrada (.txt)", data=entrada_txt,
                            file_name=f"diario_{datetime.now().strftime('%d%m%Y')}.txt",
                            mime="text/plain", use_container_width=True, key="mentepod2")

        with tab2:
            if not st.session_state.diario_entradas:
                st.info("Nenhuma entrada no diário ainda. Comece escrevendo sua primeira reflexão!")
            else:
                st.markdown(f"**{len(st.session_state.diario_entradas)} entrada(s) no seu diário**")
                for i, entrada in enumerate(reversed(st.session_state.diario_entradas)):
                    idx_real = len(st.session_state.diario_entradas) - 1 - i
                    with st.expander(f"📖 {entrada['data']} — {entrada['tipo']} — {entrada.get('estado', '')}"):
                        st.markdown("**Prompts:**")
                        st.markdown(f"<div class='card-pink' style='font-size:0.85em;'>{entrada.get('prompts', '')[:500]}...</div>", unsafe_allow_html=True)
                        st.markdown("**Sua reflexão:**")
                        st.markdown(f"<div class='card'>{entrada.get('reflexao', '')}</div>", unsafe_allow_html=True)
                        if st.button("🗑️ Remover", key=f"del_diario_{i}"):
                            st.session_state.diario_entradas.pop(idx_real)
                            st.rerun()

        # ========================
        # SALVOS E PROGRESSO
        # ========================

    with _tab_Progresso:
        pass

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "© 2026 Mente Poderosa — Neurolinguística, Meditação e Reprogramação Mental com IA · Quiz Com Prêmios"
    "</div>", unsafe_allow_html=True
)
