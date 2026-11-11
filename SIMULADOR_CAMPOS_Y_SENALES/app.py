
import math
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
st.set_page_config(
    page_title="MÓDULO DE NÚMEROS COMPLEJOS Y MAPEO CONFORME",
    page_icon="ℂ",
    layout="wide",
    initial_sidebar_state="collapsed",
)
BASE_DIR = Path(__file__).parent
PLANO_DIR = BASE_DIR / "plano_interactivo"

plano_complejo = components.declare_component(
    "plano_complejo",
    path=str(PLANO_DIR),
)
if "nuevo_real_pendiente" in st.session_state:
    st.session_state["real"] = st.session_state.pop(
        "nuevo_real_pendiente"
    )
if "nuevo_imag_pendiente" in st.session_state:
    st.session_state["imag"] = st.session_state.pop(
        "nuevo_imag_pendiente"
    )
if "real" not in st.session_state:
    st.session_state["real"] = 2.0
if "imag" not in st.session_state:
    st.session_state["imag"] = 1.0
if "last_graph_event" not in st.session_state:
    st.session_state["last_graph_event"] = None
if "alpha_real" not in st.session_state:
    st.session_state["alpha_real"] = 1.0
if "alpha_imag" not in st.session_state:
    st.session_state["alpha_imag"] = 0.0
if "beta_real" not in st.session_state:
    st.session_state["beta_real"] = 0.0
if "beta_imag" not in st.session_state:
    st.session_state["beta_imag"] = 0.0
def fmt(numero, decimales=6):
    """Muestra números con coma decimal y sin ceros innecesarios."""
    numero = float(numero)
    if abs(numero) < 1e-10:
        numero = 0.0
    texto = f"{numero:.{decimales}f}".rstrip("0").rstrip(".")
    if texto in ("", "-0"):
        texto = "0"
    if texto.startswith("."):
        texto = "0" + texto
    elif texto.startswith("-."):
        texto = "-0" + texto[1:]
    return texto.replace(".", ",")
def latex_num(numero, decimales=4):
    """Prepara números para mostrarlos correctamente en LaTeX."""
    return fmt(numero, decimales).replace(",", "{,}")
def complejo_texto(real, imag, simbolo="i"):
    """Convierte dos componentes en una expresión compleja."""
    real = 0.0 if abs(real) < 1e-10 else real
    imag = 0.0 if abs(imag) < 1e-10 else imag
    if imag == 0:
        return fmt(real)
    if real == 0:
        if imag == 1:
            return simbolo
        if imag == -1:
            return f"-{simbolo}"
        return f"{fmt(imag)}{simbolo}"
    signo = "+" if imag > 0 else "-"
    valor_imag = abs(imag)
    parte_imaginaria = (
        simbolo if valor_imag == 1
        else f"{fmt(valor_imag)}{simbolo}"
    )
    return f"{fmt(real)} {signo} {parte_imaginaria}"
def complejo_latex(real, imag):
    """Representación LaTeX de un número complejo."""
    real = 0.0 if abs(real) < 1e-10 else real
    imag = 0.0 if abs(imag) < 1e-10 else imag
    if imag == 0:
        return latex_num(real)
    if real == 0:
        if imag == 1:
            return "i"
        if imag == -1:
            return "-i"
        return rf"{latex_num(imag)}i"
    signo = "+" if imag > 0 else "-"
    valor = abs(imag)
    parte = "i" if valor == 1 else rf"{latex_num(valor)}i"
    return rf"{latex_num(real)} {signo} {parte}"
def tarjeta_resultado(titulo, valor, detalle=None):
    with st.container(border=True):
        st.markdown(
            f'<div class="resultado-titulo notranslate" '
            f'translate="no">{titulo}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="resultado-valor notranslate" '
            f'translate="no">{valor}</div>',
            unsafe_allow_html=True,
        )
        if detalle:
            st.markdown(
                f'<div class="resultado-detalle notranslate" '
                f'translate="no">{detalle}</div>',
                unsafe_allow_html=True,
            )
def encabezado_seccion(icono, titulo, descripcion=None):
    st.markdown(
        f"""
        <div class="section-heading">
            <span class="section-icon">{icono}</span>
            <div>
                <div class="section-title">{titulo}</div>
                {f'<div class="section-description">{descripcion}</div>' if descripcion else ''}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
def tarjeta_formula(titulo, formula, descripcion=None):
    with st.container(border=True):
        st.markdown(
            f'<div class="formula-title">{titulo}</div>',
            unsafe_allow_html=True,
        )
        st.latex(formula)
        if descripcion:
            st.caption(descripcion)
def tarjeta_paso(titulo, formula, explicacion=None):
    with st.container(border=True):
        st.markdown(
            f'<div class="step-title">{titulo}</div>',
            unsafe_allow_html=True,
        )
        st.latex(formula)
        if explicacion:
            st.markdown(
                f'<div class="step-description">{explicacion}</div>',
                unsafe_allow_html=True,
            )
st.markdown(
    r"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
    :root {
        --fondo: #10091d;
        --morado: #a78bfa;
        --morado-claro: #c4b5fd;
        --violeta: #7c3aed;
        --texto: #f4efff;
        --secundario: #b8aaca;
        --borde: rgba(196,181,253,.20);
    }
    html, body, [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(ellipse at 10% 5%, rgba(111,48,180,.19), transparent 38%),
            radial-gradient(ellipse at 90% 25%, rgba(82,42,150,.17), transparent 36%),
            linear-gradient(135deg,#10091d 0%,#160d29 48%,#0d0818 100%) !important;
        color:var(--texto) !important;
        font-family:'Manrope',sans-serif;
    }
    [data-testid="stHeader"],
    [data-testid="stMain"] {
        background:transparent !important;
    }
    [data-testid="stToolbar"] { right:1rem; }
    .block-container {
        max-width:1450px;
        padding-top:1.5rem;
        padding-bottom:3rem;
    }
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {
        color:var(--texto);
    }
    h1,h2,h3,h4,p,label {
        font-family:'Manrope',sans-serif !important;
    }
    /* FONDO MATEMÁTICO */
    .math-world {
        position:fixed;
        inset:0;
        z-index:0;
        overflow:hidden;
        pointer-events:none;
    }
    .math-world::before {
        content:"";
        position:absolute;
        inset:-10%;
        background-image:
            linear-gradient(rgba(190,160,255,.035) 1px,transparent 1px),
            linear-gradient(90deg,rgba(190,160,255,.035) 1px,transparent 1px);
        background-size:58px 58px;
        transform:perspective(700px) rotateX(58deg) scale(1.5);
        transform-origin:center;
        mask-image:linear-gradient(to bottom,transparent,black 25%,black 75%,transparent);
    }
    .math-orb {
        position:absolute;
        border-radius:50%;
        filter:blur(1px);
        opacity:.18;
        background:radial-gradient(circle at 35% 30%,#e9d5ff,#8b5cf6 40%,transparent 72%);
        animation:orbFloat 13s ease-in-out infinite alternate;
    }
    .math-orb.one {
        width:280px;height:280px;left:-90px;top:12%;
    }
    .math-orb.two {
        width:380px;height:380px;right:-150px;top:42%;
        animation-delay:-5s;
    }
    .math-orb.three {
        width:190px;height:190px;left:38%;bottom:-100px;
        animation-delay:-8s;
    }
    @keyframes orbFloat {
        from { transform:translate3d(0,0,0) scale(1); }
        to { transform:translate3d(25px,-30px,0) scale(1.08); }
    }
    .math-symbol {
        position:absolute;
        color:rgba(205,180,255,.19);
        font-family:'DM Mono',monospace;
        font-weight:500;
        user-select:none;
        white-space:nowrap;
        text-shadow:0 0 22px rgba(167,139,250,.25);
        will-change:transform;
        transition:transform .18s ease-out;
    }
    .math-symbol.s1 {left:8%;top:18%;font-size:58px;}
    .math-symbol.s2 {right:12%;top:15%;font-size:48px;}
    .math-symbol.s3 {left:17%;top:62%;font-size:40px;}
    .math-symbol.s4 {right:7%;top:72%;font-size:60px;}
    .math-symbol.s5 {left:48%;top:10%;font-size:35px;}
    .math-symbol.s6 {left:72%;top:45%;font-size:44px;}
    .math-symbol.s7 {left:4%;top:85%;font-size:34px;}
    .math-symbol.s8 {right:32%;bottom:8%;font-size:39px;}
    .math-symbol.s9 {left:35%;top:77%;font-size:30px;}
    .math-symbol.s10 {right:4%;top:38%;font-size:28px;}
    .math-ring {
        position:absolute;
        border:1px solid rgba(180,145,255,.13);
        border-radius:50%;
    }
    .math-ring.r1 {
        width:330px;height:110px;left:4%;top:38%;
        transform:rotate(-25deg);
    }
    .math-ring.r2 {
        width:420px;height:150px;right:4%;top:5%;
        transform:rotate(35deg);
    }
    .math-glow {
        position:fixed;
        width:360px;height:360px;
        left:0;top:0;
        border-radius:50%;
        pointer-events:none;
        background:radial-gradient(circle,rgba(139,92,246,.12),transparent 68%);
        transform:translate3d(-50%,-50%,0);
        z-index:0;
    }
    [data-testid="stAppViewContainer"] > .main,
    [data-testid="stAppViewContainer"] .main .block-container {
        position:relative;
        z-index:1;
    }
    /* ENCABEZADO */
    .hero {
        position:relative;
        overflow:hidden;
        padding:36px 38px;
        margin-bottom:28px;
        border:1px solid rgba(196,181,253,.25);
        border-radius:26px;
        background:
            radial-gradient(circle at 88% 10%,rgba(167,139,250,.28),transparent 30%),
            linear-gradient(125deg,rgba(55,27,91,.94),rgba(24,13,43,.96) 62%,rgba(43,22,72,.92));
        box-shadow:0 18px 60px rgba(0,0,0,.25),inset 0 1px rgba(255,255,255,.07);
    }
    .hero::after {
        content:"ℂ  ∫  ∑  π  ∠";
        position:absolute;
        right:22px;bottom:8px;
        color:rgba(221,204,255,.10);
        font-family:'DM Mono',monospace;
        font-size:clamp(30px,5vw,70px);
        letter-spacing:10px;
        pointer-events:none;
    }
    .hero-kicker {
        color:#c4b5fd;
        font-size:12px;
        letter-spacing:3px;
        font-weight:800;
        margin-bottom:16px;
    }
    .hero-title {
        font-size:clamp(34px,5vw,58px);
        line-height:1.02;
        font-weight:800;
        color:#fff;
        letter-spacing:-2px;
    }
    .hero-title span {
        display:block;
        color:#c4b5fd;
    }
    .hero-description {
        color:#d6c9e8;
        margin-top:18px;
        font-size:15px;
        max-width:650px;
        line-height:1.7;
    }
    /* SECCIONES */
    .section-heading {
        display:flex;
        align-items:center;
        gap:13px;
        margin:30px 0 15px;
    }
    .section-icon {
        display:flex;
        align-items:center;
        justify-content:center;
        width:43px;height:43px;
        border-radius:14px;
        color:#e9ddff;
        font-size:22px;
        background:linear-gradient(135deg,rgba(139,92,246,.35),rgba(91,33,182,.25));
        border:1px solid rgba(196,181,253,.24);
        box-shadow:0 5px 22px rgba(109,40,217,.14);
    }
    .section-title {
        color:#f4efff;
        font-size:21px;
        font-weight:800;
    }
    .section-description {
        color:#aa9aba;
        font-size:12px;
        margin-top:2px;
    }
    /* TARJETAS */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background:linear-gradient(145deg,rgba(40,25,61,.76),rgba(23,14,38,.82)) !important;
        border:1px solid var(--borde) !important;
        border-radius:18px !important;
        box-shadow:0 9px 30px rgba(0,0,0,.12);
    }
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        border-radius:18px !important;
    }
    /* FÓRMULAS */
    .formula-title {
        color:#c4b5fd;
        font-size:13px;
        font-weight:800;
        letter-spacing:.5px;
        margin-bottom:12px;
    }
    [data-testid="stLatex"],
    [data-testid="stLatex"] > div {
        max-width:100%;
    }
    [data-testid="stLatex"] {
        overflow-x:auto;
        overflow-y:hidden;
        padding:4px 0;
    }
    .katex-display {
        overflow-x:auto;
        overflow-y:hidden;
        max-width:100%;
        padding:5px 0;
        color:#f4efff !important;
    }
    .katex {
        color:#f4efff !important;
        font-size:1.12em;
    }
    /* RESULTADOS */
    .resultado-titulo {
        color:#bba8d4;
        font-size:12px;
        font-weight:700;
        text-transform:uppercase;
        letter-spacing:1px;
        margin-bottom:9px;
    }
    .resultado-valor {
        color:#e9ddff;
        font-family:'DM Mono',monospace;
        font-size:clamp(19px,2.3vw,27px);
        font-weight:500;
        overflow-wrap:anywhere;
    }
    .resultado-detalle {
        color:#9585aa;
        font-size:12px;
        margin-top:8px;
    }
    .step-title {
        color:#c4b5fd;
        font-size:14px;
        font-weight:800;
        margin-bottom:9px;
    }
    .step-description {
        color:#b8aaca;
        font-size:12px;
        line-height:1.6;
        margin-top:8px;
    }
    /* ENTRADAS */

    [data-testid="stNumberInput"] label,
    [data-testid="stSelectbox"] label {
        color:#d8c9ed !important;
        font-weight:700 !important;
    }
    [data-testid="stNumberInput"] input,
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background:rgba(19,11,32,.92) !important;
        color:#f4efff !important;
        border-color:rgba(196,181,253,.28) !important;
        border-radius:11px !important;
    }
    [data-testid="stNumberInput"] button {
        color:#d9c8ff !important;
        background:rgba(110,70,170,.25) !important;
        border-color:rgba(196,181,253,.20) !important;
    }
    [data-testid="stCaptionContainer"] {
        color:#a999bd !important;
    }
    /* CUADRO DE INFORMACIÓN DE TRANSFORMACIÓN */
    [data-testid="stAlert"] {
        background:#ffffff !important;
        border:1px solid rgba(196,181,253,.35) !important;
        border-radius:14px !important;
    }
    [data-testid="stAlert"] *,
    [data-testid="stAlert"] p,
    [data-testid="stAlert"] div,
    [data-testid="stAlert"] span {
        color:#4c1d95 !important;
    }
    /* PIE DE PÁGINA */
    .footer {
        text-align:center;
        color:#79698e;
        font-size:11px;
        letter-spacing:1px;
        padding:28px 0 8px;
    }
    /* PANTALLAS PEQUEÑAS */
    @media(max-width:700px) {
        .block-container {
            padding-left:1rem;
            padding-right:1rem;
        }
        .hero {
            padding:25px 21px;
            border-radius:20px;
        }
        .hero-title {letter-spacing:-1px;}
        .hero-description {font-size:13px;}
        .math-symbol {opacity:.55;}
        .math-symbol.s2,
        .math-symbol.s6,
        .math-symbol.s10 {
            display:none;
        }
        .katex {font-size:1em;}
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.html(
    """
    <script>
    (() => {
        if (window.__protectMathInitialized) return;
        window.__protectMathInitialized = true;
        function protectMath() {
            const selectors = [
                '[data-testid="stLatex"]',
                '.katex',
                '.katex-display',
                '.katex-html',
                '.resultado-titulo',
                '.resultado-valor',
                '.resultado-detalle',
                '.formula-title',
                '.step-title'
            ];
            document.querySelectorAll(selectors.join(',')).forEach(element => {
                element.setAttribute("translate", "no");
                element.classList.add("notranslate");
                element.querySelectorAll("*").forEach(child => {
                    child.setAttribute("translate", "no");
                    child.classList.add("notranslate");
                });
            });
        }
        protectMath();
        const observer = new MutationObserver(protectMath);
        observer.observe(document.body, {
            childList:true,
            subtree:true
        });
    })();
    </script>
    """,
    unsafe_allow_javascript=True,
)
st.html(
    """
    <div class="math-world" id="math-world">
        <div class="math-orb one"></div>
        <div class="math-orb two"></div>
        <div class="math-orb three"></div>
        <div class="math-ring r1"></div>
        <div class="math-ring r2"></div>
        <span class="math-symbol s1">∫</span>
        <span class="math-symbol s2">π</span>
        <span class="math-symbol s3">√x</span>
        <span class="math-symbol s4">∞</span>
        <span class="math-symbol s5">ℂ</span>
        <span class="math-symbol s6">θ</span>
        <span class="math-symbol s7">∑</span>
        <span class="math-symbol s8">eⁱθ</span>
        <span class="math-symbol s9">ƒ(z)</span>
        <span class="math-symbol s10">Δ</span>
    </div>
    <div class="math-glow" id="math-glow"></div>
    <script>
    (() => {
        if (window.__mathWorldInitialized) return;
        window.__mathWorldInitialized = true;
        function startMathMotion() {
            const world = document.getElementById("math-world");
            const glow = document.getElementById("math-glow");
            if (!world || !glow) {
                requestAnimationFrame(startMathMotion);
                return;
            }
            const symbols = world.querySelectorAll(".math-symbol");
            let targetX = 0;
            let targetY = 0;
            let currentX = 0;
            let currentY = 0;
            document.addEventListener("pointermove", event => {
                targetX = event.clientX / window.innerWidth - 0.5;
                targetY = event.clientY / window.innerHeight - 0.5;
                glow.style.left = event.clientX + "px";
                glow.style.top = event.clientY + "px";
            }, {passive:true});
            function animate() {
                currentX += (targetX - currentX) * 0.07;
                currentY += (targetY - currentY) * 0.07;
                symbols.forEach((symbol, index) => {
                    const depth = 12 + (index % 5) * 8;
                    symbol.style.transform =
                        `translate3d(${currentX * depth}px, ${currentY * depth}px, 0)`;
                });
                requestAnimationFrame(animate);
            }
            animate();
        }
        startMathMotion();
    })();
    </script>
    """,
    unsafe_allow_javascript=True,
)
st.html(
    """
    <div class="hero">
        <div class="hero-kicker">LABORATORIO INTERACTIVO DE MATEMÁTICAS</div>
        <div class="hero-title">
            MÓDULO DE
            <span>NÚMEROS COMPLEJOS</span>
            Y MAPEO CONFORME
        </div>
        <div class="hero-description">
            Simulador interactivo de números complejos.
            Explora, calcula y visualiza cómo las funciones
            transforman los puntos en el plano complejo.
        </div>
    </div>
    """
)
encabezado_seccion(
    "✦",
    "Construye tu número complejo",
    "Escribe sus componentes o selecciona un punto directamente en el plano.",
)
col_real, col_imag, col_preview = st.columns([1, 1, 1.3])
with col_real:
    real = st.number_input(
        "Parte real (a)",
        key="real",
        step=0.1,
        format="%.10g",
    )
with col_imag:
    imag = st.number_input(
        "Parte imaginaria (b)",
        key="imag",
        step=0.1,
        format="%.10g",
    )
with col_preview:
    with st.container(border=True):
        st.markdown(
            '<div class="resultado-titulo">Número complejo actual</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="resultado-valor notranslate" translate="no">'
            f'z = {complejo_texto(real, imag)}</div>',
            unsafe_allow_html=True,
        )
        st.caption("z = a + bi")
encabezado_seccion(
    "⟳",
    "Transformación",
    "Selecciona una función para observar cómo cambia el número complejo.",
)
col_transformacion, col_ayuda = st.columns([1, 1.5])
with col_transformacion:
    transformacion = st.selectbox(
        "Función compleja",
        ["Ninguna", "z²", "z³", "αz + β"],
        index=0,
    )
with col_ayuda:
    if transformacion == "Ninguna":
        st.info("El plano mostrará el punto original sin aplicar transformaciones.")
    elif transformacion == "z²":
        st.info("Eleva el número complejo al cuadrado.")
    elif transformacion == "z³":
        st.info("Eleva el número complejo al cubo.")
    else:
        st.info("Multiplica z por α y después suma β.")
if transformacion == "αz + β":
    st.markdown("**Define los valores de α y β:**")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        alpha_real = st.number_input(
            "Real de α",
            key="alpha_real",
            step=0.1,
            format="%.10g",
        )
    with c2:
        alpha_imag = st.number_input(
            "Imaginaria de α",
            key="alpha_imag",
            step=0.1,
            format="%.10g",
        )
    with c3:
        beta_real = st.number_input(
            "Real de β",
            key="beta_real",
            step=0.1,
            format="%.10g",
        )
    with c4:
        beta_imag = st.number_input(
            "Imaginaria de β",
            key="beta_imag",
            step=0.1,
            format="%.10g",
        )
else:
    alpha_real = st.session_state.alpha_real
    alpha_imag = st.session_state.alpha_imag
    beta_real = st.session_state.beta_real
    beta_imag = st.session_state.beta_imag
z = complex(real, imag)
alpha = complex(alpha_real, alpha_imag)
beta = complex(beta_real, beta_imag)
if transformacion == "z²":
    w = z ** 2
elif transformacion == "z³":
    w = z ** 3
elif transformacion == "αz + β":
    w = alpha * z + beta
else:
    w = z
w_real = w.real
w_imag = w.imag
encabezado_seccion(
    "⌖",
    "Plano complejo interactivo",
    "Haz clic para seleccionar un punto, arrástralo para moverlo y usa la rueda para acercar o alejar.",
)
evento = plano_complejo(
    x=float(real),
    y=float(imag),
    transformacion=transformacion,
    alpha_real=float(alpha_real),
    alpha_imag=float(alpha_imag),
    beta_real=float(beta_real),
    beta_imag=float(beta_imag),
    height=590,
    key="plano_interactivo",
)
if isinstance(evento, dict):
    nuevo_real = float(evento.get("x", real))
    nuevo_imag = float(evento.get("y", imag))
    event_id = evento.get("event_id")
    if event_id is None:
        event_id = (nuevo_real, nuevo_imag)
    if event_id != st.session_state.last_graph_event:
        st.session_state.last_graph_event = event_id
        st.session_state["nuevo_real_pendiente"] = nuevo_real
        st.session_state["nuevo_imag_pendiente"] = nuevo_imag
        st.rerun()
modulo = abs(z)
angulo_rad = math.atan2(imag, real)
angulo_grados = math.degrees(angulo_rad)
if abs(real) < 1e-10 and abs(imag) < 1e-10:
    angulo_rad_texto = "No definido"
    angulo_grados_texto = "No definido"
else:
    angulo_rad_texto = f"{fmt(angulo_rad)} rad"
    angulo_grados_texto = f"{fmt(angulo_grados)}°"
conjugado = complejo_texto(real, -imag)
st.markdown("---")
encabezado_seccion(
    "∑",
    "Resultados del número complejo",
    "Los resultados se actualizan al escribir o mover el punto.",
)
r1, r2, r3, r4 = st.columns(4)
with r1:
    tarjeta_resultado("Módulo |z|", fmt(modulo), "Distancia al origen")
with r2:
    tarjeta_resultado("Ángulo en radianes", angulo_rad_texto, "Medida angular")
with r3:
    tarjeta_resultado("Ángulo en grados", angulo_grados_texto, "Medida angular")
with r4:
    tarjeta_resultado("Conjugado", conjugado, "Mismo real, imaginario opuesto")
encabezado_seccion(
    "π",
    "Fórmulas fundamentales",
    "Las expresiones se muestran en notación matemática para conservar su presentación en cualquier idioma.",
)
f1, f2 = st.columns(2)
with f1:
    tarjeta_formula(
        "1. Módulo",
        r"|z|=\sqrt{a^2+b^2}",
        "Calcula la distancia entre el origen y el punto.",
    )
with f2:
    tarjeta_formula(
        "2. Ángulo",
        r"\theta=\tan^{-1}\left(\frac{b}{a}\right)",
        "El cálculo interno considera el cuadrante correcto del punto.",
    )
f3, f4 = st.columns(2)
with f3:
    tarjeta_formula(
        "3. Forma polar",
        r"z=r(\cos\theta+i\cdot\sin\theta)",
        "Representa el número usando módulo y ángulo.",
    )
with f4:
    tarjeta_formula(
        "4. Forma exponencial",
        r"z=r\cdot e^{i\theta}",
        "Expresa el número complejo mediante la exponencial.",
    )
f5, f6 = st.columns(2)
with f5:
    tarjeta_formula(
        "5. Identidad de Euler",
        r"e^{i\theta}=\cos\theta+i\cdot\sin\theta",
        "Relaciona la exponencial compleja con seno y coseno.",
    )
with f6:
    tarjeta_formula(
        "6. Número complejo",
        r"z=a+bi",
        "a es la parte real y b es la parte imaginaria.",
    )
encabezado_seccion(
    "◇",
    "Representaciones del número complejo",
    "Observa las formas polar y exponencial con los valores calculados.",
)
if modulo < 1e-10:
    polar_evaluada = r"z=0"
    exponencial_evaluada = r"z=0"
else:
    polar_evaluada = (
        rf"z={latex_num(modulo)}"
        rf"\left(\cos({latex_num(angulo_rad)})"
        rf"+i\cdot\sin({latex_num(angulo_rad)})\right)"
    )
    exponencial_evaluada = (
        rf"z={latex_num(modulo)}"
        rf"\cdot e^{{i({latex_num(angulo_rad)})}}"
    )
p1, p2 = st.columns(2)
with p1:
    tarjeta_formula("Forma polar evaluada", polar_evaluada)
with p2:
    tarjeta_formula("Forma exponencial evaluada", exponencial_evaluada)
encabezado_seccion(
    "⌁",
    "Desarrollo paso a paso",
    "Aquí puedes observar cómo se obtienen los resultados.",
)
st.markdown("#### 1. Cálculo del módulo")
paso_modulo_1 = r"|z|=\sqrt{a^2+b^2}"
paso_modulo_2 = (
    rf"|z|=\sqrt{{({latex_num(real)})^2+({latex_num(imag)})^2}}"
)
paso_modulo_3 = (
    rf"|z|=\sqrt{{{latex_num(real**2)}+{latex_num(imag**2)}}}"
)
paso_modulo_4 = rf"|z|={latex_num(modulo)}"
m1, m2 = st.columns(2)
with m1:
    tarjeta_paso(
        "Paso 1 · Fórmula",
        paso_modulo_1,
        "Partimos de la fórmula del módulo.",
    )
with m2:
    tarjeta_paso(
        "Paso 2 · Sustitución",
        paso_modulo_2,
        "Reemplazamos a y b por los valores del punto.",
    )
m3, m4 = st.columns(2)
with m3:
    tarjeta_paso(
        "Paso 3 · Operaciones",
        paso_modulo_3,
        "Elevamos cada componente al cuadrado.",
    )
with m4:
    tarjeta_paso(
        "Paso 4 · Resultado",
        paso_modulo_4,
        "Calculamos la raíz cuadrada.",
    )
st.markdown("#### 2. Cálculo del ángulo")
if modulo < 1e-10:
    st.info("El ángulo del número complejo cero no está definido.")
else:
    angulo_1 = r"\theta=\tan^{-1}\left(\frac{b}{a}\right)"
    if abs(real) > 1e-10:
        angulo_2 = (
            rf"\theta=\tan^{{-1}}"
            rf"\left(\frac{{{latex_num(imag)}}}{{{latex_num(real)}}}\right)"
        )
        angulo_3 = (
            rf"\theta=\tan^{{-1}}"
            rf"\left({latex_num(imag / real)}\right)"
        )
    else:
        angulo_2 = (
            rf"\theta=\operatorname{{atan2}}"
            rf"({latex_num(imag)},{latex_num(real)})"
        )
        angulo_3 = (
            rf"\theta={latex_num(angulo_rad)}"
            rf"\text{{ rad}}"
        )
    angulo_4 = rf"\theta={latex_num(angulo_grados)}^\circ"
    a1, a2 = st.columns(2)
    with a1:
        tarjeta_paso("Paso 1 · Fórmula", angulo_1)
    with a2:
        tarjeta_paso("Paso 2 · Sustitución", angulo_2)
    a3, a4 = st.columns(2)
    with a3:
        tarjeta_paso("Paso 3 · Cálculo", angulo_3)
    with a4:
        tarjeta_paso("Paso 4 · Conversión a grados", angulo_4)
st.markdown("---")
encabezado_seccion(
    "↗",
    "Procedimiento de la transformación",
    "Desarrollo matemático de la función seleccionada.",
)
if transformacion == "Ninguna":
    tarjeta_paso(
        "Sin transformación",
        rf"f(z)=z={complejo_latex(real, imag)}",
        "El punto transformado coincide con el punto original.",
    )
elif transformacion == "z²":
    tarjeta_paso("Paso 1 · Función", r"f(z)=z^2")
    tarjeta_paso(
        "Paso 2 · Sustituir el número complejo",
        rf"f(z)=({latex_num(real)}+{latex_num(imag)}i)^2",
    )
    tarjeta_paso(
        "Paso 3 · Desarrollar el binomio",
        rf"f(z)=({latex_num(real)}^2-({latex_num(imag)})^2)"
        rf"+2({latex_num(real)})({latex_num(imag)})i",
    )
    tarjeta_paso(
        "Paso 4 · Calcular las componentes",
        rf"f(z)=({latex_num(real**2)}-{latex_num(imag**2)})"
        rf"+({latex_num(2 * real * imag)})i",
    )
    tarjeta_paso(
        "Resultado de la transformación",
        rf"w={complejo_latex(w_real, w_imag)}",
    )
elif transformacion == "z³":
    z2_real = real**2 - imag**2
    z2_imag = 2 * real * imag
    tarjeta_paso("Paso 1 · Función", r"f(z)=z^3")
    tarjeta_paso(
        "Paso 2 · Reescribir la potencia",
        r"z^3=z^2\cdot z",
    )
    tarjeta_paso(
        "Paso 3 · Calcular primero el cuadrado",
        rf"z^2=({latex_num(z2_real)})"
        rf"+({latex_num(z2_imag)})i",
    )
    tarjeta_paso(
        "Paso 4 · Multiplicar por z",
        rf"w=({latex_num(z2_real)}+{latex_num(z2_imag)}i)"
        rf"({latex_num(real)}+{latex_num(imag)}i)",
    )
    tarjeta_paso(
        "Paso 5 · Resultado",
        rf"w={complejo_latex(w_real, w_imag)}",
    )
elif transformacion == "αz + β":
    tarjeta_paso("Paso 1 · Función", r"f(z)=\alpha z+\beta")
    tarjeta_paso(
        "Paso 2 · Valores de entrada",
        rf"\alpha={complejo_latex(alpha_real, alpha_imag)},"
        rf"\quad z={complejo_latex(real, imag)},"
        rf"\quad \beta={complejo_latex(beta_real, beta_imag)}",
    )
    tarjeta_paso(
        "Paso 3 · Multiplicar α por z",
        rf"\alpha z=({latex_num(alpha_real)}"
        rf"+{latex_num(alpha_imag)}i)"
        rf"({latex_num(real)}+{latex_num(imag)}i)",
    )
    tarjeta_paso(
        "Paso 4 · Sumar β",
        rf"w=({complejo_latex((alpha * z).real, (alpha * z).imag)})"
        rf"+({complejo_latex(beta_real, beta_imag)})",
    )
    tarjeta_paso(
        "Resultado de la transformación",
        rf"w={complejo_latex(w_real, w_imag)}",
    )
encabezado_seccion(
    "✧",
    "Comparación de puntos",
    "Compara el número original con el resultado de la transformación.",
)
c1, c2 = st.columns(2)
with c1:
    tarjeta_resultado(
        "Punto original · z",
        complejo_texto(real, imag),
        f"Coordenadas: ({fmt(real)}, {fmt(imag)})",
    )
with c2:
    tarjeta_resultado(
        "Punto transformado · w",
        complejo_texto(w_real, w_imag),
        f"Coordenadas: ({fmt(w_real)}, {fmt(w_imag)})",
    )
st.html(
    """
    <div class="footer">
        LABORATORIO DE MATEMÁTICAS · INGENIERÍA MECATRÓNICA
        <br>
        NÚMEROS COMPLEJOS Y MAPEO CONFORME
    </div>
    """
)