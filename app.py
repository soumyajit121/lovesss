"""
💖 Happy Girlfriend Day — Sneha 💖
A romantic animated single-page experience built with Streamlit.

Run with:  streamlit run app.py
"""

import base64
import os
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="For Sneha 💖", page_icon="💖", layout="wide",
                   initial_sidebar_state="collapsed")

# Hide Streamlit chrome and pin the embedded experience to the REAL browser
# viewport (100vh), not just the component's own box. This is what makes the
# puzzle overlay truly fixed — earlier, the iframe's height only matched its
# content, so scrolling the outer Streamlit page dragged the "fixed" puzzle
# away with it. Forcing the iframe itself to 100vh + giving it its own
# internal scroll means every `position:fixed` element inside now stays
# glued to what the user actually sees, and nothing moves until the puzzle
# is solved.
st.markdown("""
<style>
  #MainMenu, header, footer {visibility: hidden;}
  html, body, .stApp {
      height: 100vh !important; margin:0; padding:0; overflow:hidden !important;
      background:#1a0510;
  }
  .block-container {padding: 0 !important; margin:0 !important; max-width: 100% !important; height:100vh !important;}
  iframe {display:block !important; width:100% !important; height:100vh !important; border:none !important;}
</style>
""", unsafe_allow_html=True)

ASSETS = os.path.dirname(os.path.abspath(__file__))

def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

@st.cache_data(show_spinner=False)
def load_assets():
    photos = []
    for i in range(1, 11):
        p = os.path.join(ASSETS, f"photo{i:02d}.jpg")
        if os.path.exists(p):
            photos.append("data:image/jpeg;base64," + b64(p))
    song_path = os.path.join(ASSETS, "song.mp3")
    full_song_path = os.path.join(ASSETS, "song_full.mp3")
    if os.path.exists(song_path):
        song = "data:audio/mpeg;base64," + b64(song_path)
    elif os.path.exists(full_song_path):
        song = "data:audio/mpeg;base64," + b64(full_song_path)
    else:
        song = ""
    gif_sparkle_path = os.path.join(ASSETS, "bg_sparkle.gif")
    gif_shoot_path = os.path.join(ASSETS, "bg_shoot.gif")
    gif_sparkle = ("data:image/gif;base64," + b64(gif_sparkle_path)) if os.path.exists(gif_sparkle_path) else ""
    gif_shoot = ("data:image/gif;base64," + b64(gif_shoot_path)) if os.path.exists(gif_shoot_path) else ""
    return photos, song, gif_sparkle, gif_shoot

photos, song, gif_sparkle, gif_shoot = load_assets()

captions = [
    "The smile that started it all ✨",
    "My forever golden hour 🌤️",
    "Grace, wrapped in red ❤️",
    "Every birthday wish of mine… is you 🎂",
    "Sweetest thing in the frame (not the cake) 🍰",
    "Elegance has a name — Sneha 🤍",
    "My pink-skies kind of peace 🌸",
    "Crowned with flowers, ruling my heart 👑",
    "Main character energy, always 💫",
    "The night you outshone all the lights 🌙",
]

photo_html = ""
for idx, (src, cap) in enumerate(zip(photos, captions)):
    photo_html += f"""
    <div class="slide {'active' if idx == 0 else ''}" data-idx="{idx}">
        <img src="{src}" alt="Sneha"/>
        <div class="caption">{cap}</div>
    </div>"""

dots_html = "".join(f'<span class="dot {"on" if i==0 else ""}" onclick="goSlide({i})"></span>'
                    for i in range(len(photos)))


html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<link href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Dancing+Script:wght@500;700&family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
<style>
:root {{
  --pink:#ff5d8f; --deep:#1a0510; --rose:#ff8fab; --gold:#ffd166; --violet:#7b2cbf; --maroon:#5c0f2c;
  --ease:cubic-bezier(.19,1,.22,1);
}}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html {{ scroll-behavior:smooth; }}
html,body {{ width:100%; overflow-x:hidden; background:var(--deep);
  font-family:'Poppins',sans-serif; -webkit-overflow-scrolling:touch; }}
body.locked, html.locked {{ overflow:hidden !important; height:100vh !important; }}

/* ============ ANIMATED GRADIENT BACKGROUND ============ */
body::before {{
  content:""; position:fixed; inset:0; z-index:-6;
  background: linear-gradient(-45deg, #1a0510, #3c0d22, #7b1c3f, #c73866, #3c096c, #1a0510);
  background-size: 400% 400%;
  animation: grad 20s ease infinite;
}}
@keyframes grad {{ 0%{{background-position:0% 50%}} 50%{{background-position:100% 50%}} 100%{{background-position:0% 50%}} }}

/* animated colour-theme glow — sweeps warm pink/gold/violet washes across the whole site as you scroll */
#themeGlow {{ position:fixed; inset:-25%; z-index:-5; pointer-events:none; mix-blend-mode:screen;
  opacity:.75; will-change:transform;
  background:
    radial-gradient(circle at 15% 20%, rgba(255,93,143,.55), transparent 38%),
    radial-gradient(circle at 85% 25%, rgba(255,209,102,.4), transparent 36%),
    radial-gradient(circle at 30% 80%, rgba(123,44,191,.5), transparent 40%),
    radial-gradient(circle at 80% 85%, rgba(199,56,102,.5), transparent 40%);
  animation: themeSweep 16s ease-in-out infinite alternate; }}
@keyframes themeSweep {{
  0%   {{ transform:translate(0,0) scale(1) rotate(0deg); filter:hue-rotate(0deg); }}
  50%  {{ transform:translate(2%,-3%) scale(1.12) rotate(6deg); filter:hue-rotate(25deg); }}
  100% {{ transform:translate(-2%,3%) scale(1.05) rotate(-4deg); filter:hue-rotate(-15deg); }}
}}

/* cinematic vignette so the edges feel intimate, not flat */
body::after {{
  content:""; position:fixed; inset:0; z-index:-1; pointer-events:none;
  background: radial-gradient(ellipse at center, transparent 45%, rgba(10,2,8,.6) 100%);
}}

/* ============ PARALLAX STARRY GLOWING SKY (drifts + twinkles + glows) ============ */
#starLayer {{ position:fixed; inset:-10% -10% -10% -10%; z-index:-3; pointer-events:none;
  animation: driftField 70s linear infinite alternate; }}
@keyframes driftField {{ 0%{{transform:translate(0,0)}} 100%{{transform:translate(-3%,2%)}} }}
.star {{ position:absolute; border-radius:50%; background:#fff; animation: twinkle linear infinite; }}
.star.glow {{ box-shadow: 0 0 8px 2px rgba(255,255,255,.95), 0 0 20px 6px rgba(255,143,171,.65); }}
.star.gold {{ background:var(--gold); box-shadow: 0 0 10px 3px rgba(255,209,102,.95), 0 0 24px 7px rgba(255,209,102,.5); }}
@keyframes twinkle {{ 0%,100%{{opacity:.15; transform:scale(.7)}} 50%{{opacity:1; transform:scale(1.3)}} }}
/* soft nebula haze drifting slowly behind the stars for extra depth */
#nebula {{ position:fixed; inset:-20%; z-index:-4; pointer-events:none; opacity:.5; filter:blur(60px);
  background: radial-gradient(circle at 20% 30%, rgba(199,56,102,.35), transparent 40%),
              radial-gradient(circle at 80% 70%, rgba(123,44,191,.3), transparent 45%),
              radial-gradient(circle at 50% 90%, rgba(255,143,171,.25), transparent 40%);
  animation: nebulaDrift 50s ease-in-out infinite alternate; }}
@keyframes nebulaDrift {{ 0%{{transform:translate(0,0) scale(1)}} 100%{{transform:translate(3%,-2%) scale(1.08)}} }}

/* live animated GIF backgrounds — sparkle burst + shooting stars, blended into the sky, drifting on parallax */
.gifLayer {{ position:fixed; inset:-15%; z-index:-4; pointer-events:none;
  background-repeat:repeat; mix-blend-mode:screen; will-change:transform; }}
#gifSparkleLayer {{ opacity:.55; background-size:300px 300px; filter:saturate(1.4) brightness(1.15); }}
#gifShootLayer {{ opacity:.48; background-size:360px 360px; filter:saturate(1.3) brightness(1.1); }}

/* shooting star */
.shoot {{ position:fixed; width:2px; height:2px; background:#fff; border-radius:50%; z-index:-2;
  box-shadow:0 0 6px 2px #fff; animation: shoot 3.4s linear infinite; opacity:0; }}
@keyframes shoot {{
  0%   {{ transform: translate(0,0) rotate(-35deg); opacity:0; }}
  5%   {{ opacity:1; }}
  40%  {{ transform: translate(-60vw, 40vh) rotate(-35deg); opacity:0; }}
  100% {{ opacity:0; }}
}}

/* ============ GLOWING SWEEP — smooth glowing beam continuously running across everything ============ */
#glowSweep {{ position:fixed; inset:0; z-index:-2; pointer-events:none; overflow:hidden; mix-blend-mode:screen; opacity:.5; }}
#glowSweep::before {{
  content:""; position:absolute; top:-60%; left:-70%; width:55%; height:220%;
  background: linear-gradient(100deg, transparent 0%, rgba(255,214,140,.5) 42%, rgba(255,255,255,.85) 50%, rgba(255,143,171,.5) 58%, transparent 100%);
  filter: blur(10px);
  animation: sweepRun 7s linear infinite;
}}
@keyframes sweepRun {{
  0%   {{ transform: translateX(0) rotate(10deg); }}
  100% {{ transform: translateX(260vw) rotate(10deg); }}
}}

/* ============ FLOATING HEARTS ============ */
.fheart {{ position:fixed; bottom:-8vh; z-index:-1; animation: rise linear infinite; opacity:.85;
  filter: drop-shadow(0 0 6px rgba(255,93,143,.8)); }}
@keyframes rise {{
  0%   {{ transform: translateY(0) translateX(0) rotate(0deg) scale(1); opacity:0; }}
  8%   {{ opacity:.9; }}
  100% {{ transform: translateY(-118vh) translateX(var(--sway)) rotate(360deg) scale(1.25); opacity:0; }}
}}

/* ============ FLOATING LOVE WORDS ============ */
.fword {{ position:fixed; z-index:-1; font-family:'Dancing Script',cursive; color:rgba(255,190,215,.5);
  white-space:nowrap; animation: drift linear infinite; }}
@keyframes drift {{
  0%   {{ transform: translateY(105vh); opacity:0; }}
  10%  {{ opacity:.75; }}
  90%  {{ opacity:.5; }}
  100% {{ transform: translateY(-15vh); opacity:0; }}
}}

/* ============ GLITTER SPARKLES ============ */
.sparkle {{ position:fixed; z-index:-1; width:6px; height:6px; pointer-events:none;
  background: radial-gradient(circle, #fff 0%, var(--gold) 45%, transparent 70%);
  animation: spark 2.6s ease-in-out infinite; border-radius:50%; }}
@keyframes spark {{ 0%,100%{{opacity:0; transform:scale(.3) rotate(0)}} 50%{{opacity:1; transform:scale(1.4) rotate(180deg)}} }}

/* ============ CURSOR HEART TRAIL ============ */
.trailHeart {{ position:fixed; z-index:90; pointer-events:none; font-size:14px;
  animation: trailFade 900ms ease-out forwards; }}
@keyframes trailFade {{ 0%{{opacity:.9; transform:scale(1) translateY(0)}} 100%{{opacity:0; transform:scale(.4) translateY(-26px)}} }}

/* ============ PUZZLE OVERLAY — full, locked landing screen ============ */
#puzzleOverlay {{
  position:fixed; inset:0; z-index:200; display:flex; flex-direction:column; align-items:center;
  justify-content:center; gap:18px;
  background: radial-gradient(ellipse at 50% 30%, rgba(199,56,102,.28), transparent 60%),
              linear-gradient(160deg, rgba(10,2,8,.97), rgba(38,6,20,.97));
  backdrop-filter: blur(8px);
  transition: opacity 1.3s ease, visibility 1.3s ease; padding:20px; text-align:center;
}}
#puzzleOverlay.hide {{ opacity:0; visibility:hidden; pointer-events:none; }}
#puzzleOverlay .ring {{ position:absolute; width:min(70vw,520px); height:min(70vw,520px); border-radius:50%;
  border:1px solid rgba(255,143,171,.18); animation: ringSpin 40s linear infinite; }}
#puzzleOverlay .ring.r2 {{ width:min(55vw,400px); height:min(55vw,400px); animation-duration:28s; animation-direction:reverse; }}
@keyframes ringSpin {{ from{{transform:rotate(0)}} to{{transform:rotate(360deg)}} }}
#puzzleOverlay .kicker {{ color:var(--gold); letter-spacing:4px; font-size:clamp(10px,1.8vw,13px); text-transform:uppercase; }}
#puzzleOverlay h1 {{ font-family:'Great Vibes',cursive; color:var(--rose); font-size:clamp(32px,6.4vw,58px);
  text-shadow:0 0 26px rgba(255,93,143,.75); text-align:center; }}
#puzzleOverlay p {{ color:#f2d8e4; font-size:clamp(13px,2.4vw,17px); text-align:center; max-width:520px; font-weight:300; }}
#board {{ display:grid; grid-template-columns:repeat(4, minmax(56px, 92px)); gap:12px; margin-top:6px; position:relative; z-index:2; }}
.card {{ aspect-ratio:1/1; perspective:600px; cursor:pointer; }}
.cardInner {{ width:100%; height:100%; position:relative; transform-style:preserve-3d; transition: transform .5s; }}
.card.flip .cardInner {{ transform: rotateY(180deg); }}
.face {{ position:absolute; inset:0; display:flex; align-items:center; justify-content:center;
  border-radius:14px; backface-visibility:hidden; font-size:clamp(24px,4.4vw,36px); }}
.front {{ background:linear-gradient(135deg,#ff5d8f,#7b1c3f); box-shadow:0 4px 18px rgba(255,93,143,.35); color:#fff; }}
.back  {{ background:#fff4f8; transform:rotateY(180deg); box-shadow:0 4px 18px rgba(0,0,0,.35); }}
.card.matched .back {{ background:#ffe0ec; animation:pulseM .6s ease; }}
@keyframes pulseM {{ 0%{{transform:rotateY(180deg) scale(1)}} 50%{{transform:rotateY(180deg) scale(1.15)}} 100%{{transform:rotateY(180deg) scale(1)}} }}
#moves {{ color:#ffc7da; font-size:13px; letter-spacing:1px; position:relative; z-index:2; }}

/* love blast — bigger, camera-flash celebration */
.blast {{ position:fixed; z-index:120; font-size:26px; pointer-events:none; will-change:transform,opacity;
  animation: blastFly 1.9s var(--ease) forwards; }}
@keyframes blastFly {{
  0%   {{ transform: translate(0,0) scale(.3) rotate(0); opacity:1; }}
  70%  {{ opacity:1; }}
  100% {{ transform: translate(var(--bx), var(--by)) scale(1.7) rotate(var(--br)); opacity:0; }}
}}
#flash {{ position:fixed; inset:0; z-index:119; background:#fff; opacity:0; pointer-events:none; }}
#flash.pop {{ animation: flashPop .5s ease-out; }}
@keyframes flashPop {{ 0%{{opacity:.85}} 100%{{opacity:0}} }}
#blastMsg {{ position:fixed; z-index:121; inset:0; display:flex; align-items:center; justify-content:center;
  font-family:'Great Vibes',cursive; font-size:clamp(40px,9vw,90px); color:#fff; opacity:0; pointer-events:none;
  text-shadow:0 0 30px var(--pink), 0 0 60px var(--pink); transition:opacity .6s; }}
#blastMsg.show {{ opacity:1; animation: zoomIn 1.9s var(--ease); }}
@keyframes zoomIn {{ 0%{{transform:scale(.25)}} 55%{{transform:scale(1.16)}} 100%{{transform:scale(1)}} }}

/* ============ MAIN CONTENT ============ */
#main {{ opacity:0; transition:opacity 1.6s ease .4s; }}
#main.show {{ opacity:1; }}

.hero {{ min-height:96vh; display:flex; flex-direction:column; align-items:center; justify-content:center;
  text-align:center; padding:40px 16px 20px; }}
.hero .pre {{ color:var(--gold); letter-spacing:6px; font-size:clamp(11px,2vw,15px); text-transform:uppercase;
  animation: fadeUp 1.4s ease both .3s; }}
.hero h1 {{ font-family:'Great Vibes',cursive; font-size:clamp(52px,11vw,120px); color:#fff; line-height:1.1;
  text-shadow:0 0 24px rgba(255,93,143,.85), 0 0 70px rgba(255,93,143,.5);
  animation: fadeUp 1.4s ease both .6s, glowPulse 3s ease-in-out infinite 2s; }}
.hero .name {{ font-family:'Great Vibes',cursive; font-size:clamp(64px,13vw,150px); color:var(--rose);
  animation: fadeUp 1.4s ease both .9s, floaty 5s ease-in-out infinite 2.4s; }}
.hero .typing {{ margin-top:18px; color:#ffdce6; font-family:'Playfair Display',serif; font-style:italic;
  font-size:clamp(13px,2.2vw,18px); overflow:hidden; white-space:nowrap; border-right:2px solid #ff6f91;
  width:0; margin-left:auto; margin-right:auto;
  animation: typeIn 3.2s steps(38,end) 1.6s forwards, blinkCaret .7s step-end infinite 1.6s; }}
@keyframes typeIn {{ from{{width:0}} to{{width:35ch}} }}
@keyframes blinkCaret {{ 50%{{border-color:transparent}} }}
.hero .sub {{ margin-top:14px; color:#ffdcE9; font-family:'Dancing Script',cursive; font-size:clamp(18px,3.4vw,28px);
  animation: fadeUp 1.4s ease both 1.2s; }}
.heartbeat {{ font-size:clamp(40px,7vw,64px); margin-top:18px; animation: beat 1.15s ease-in-out infinite; display:inline-block; }}
@keyframes beat {{ 0%,100%{{transform:scale(1)}} 25%{{transform:scale(1.25)}} 40%{{transform:scale(1)}} 60%{{transform:scale(1.2)}} }}
@keyframes fadeUp {{ from{{opacity:0; transform:translateY(34px)}} to{{opacity:1; transform:translateY(0)}} }}

/* generic utility: children of .stagger-group fade/slide in one-by-one when observed */
.stagger-group > * {{ opacity:0; transform:translateY(30px); transition:opacity .9s var(--ease), transform .9s var(--ease); }}
.stagger-group > *.seqIn {{ opacity:1; transform:translateY(0); }}
@keyframes floaty {{ 0%,100%{{transform:translateY(0)}} 50%{{transform:translateY(-12px)}} }}
@keyframes glowPulse {{ 0%,100%{{text-shadow:0 0 24px rgba(255,93,143,.85)}} 50%{{text-shadow:0 0 46px rgba(255,209,102,.95)}} }}
.scrollhint {{ color:#ffb3cd; font-size:13px; margin-top:34px; animation: bounceDn 1.8s infinite; }}
@keyframes bounceDn {{ 0%,100%{{transform:translateY(0)}} 50%{{transform:translateY(10px)}} }}

section {{ padding:70px 18px; max-width:1050px; margin:0 auto; }}
.sectionTitle {{ font-family:'Great Vibes',cursive; text-align:center; color:#fff; font-size:clamp(34px,6.5vw,58px);
  line-height:1.35; margin-bottom:14px; text-shadow:0 0 22px rgba(255,93,143,.8), 0 0 44px rgba(255,209,102,.35);
  animation: titleGlowPulse 4s ease-in-out infinite; }}
@keyframes titleGlowPulse {{
  0%,100% {{ text-shadow:0 0 22px rgba(255,93,143,.8), 0 0 44px rgba(255,209,102,.35); }}
  50%     {{ text-shadow:0 0 32px rgba(255,93,143,1), 0 0 60px rgba(255,209,102,.55); }}
}}
.sectionSub {{ text-align:center; color:#ffc9dc; margin:0 auto 48px; max-width:90%; line-height:1.6;
  font-size:clamp(13px,2.2vw,16px); }}

/* ---- Slideshow ---- */
.slideWrap {{ position:relative; width:min(480px, 92vw); margin:0 auto; aspect-ratio:3/4;
  border-radius:24px; overflow:hidden;
  box-shadow:0 0 0 6px rgba(255,255,255,.08), 0 0 46px rgba(255,93,143,.5), 0 26px 60px rgba(0,0,0,.55); }}
.slide {{ position:absolute; inset:0; opacity:0; transform:scale(1.12) rotate(1.5deg);
  transition: opacity 1.2s ease, transform 1.6s ease; }}
.slide.active {{ opacity:1; transform:scale(1) rotate(0); z-index:2; }}
.slide img {{ width:100%; height:100%; object-fit:cover; animation: kenburns 9s ease-in-out infinite alternate; }}
@keyframes kenburns {{ from{{transform:scale(1)}} to{{transform:scale(1.08)}} }}
.caption {{ position:absolute; bottom:0; left:0; right:0; padding:44px 18px 16px; color:#fff; text-align:center;
  font-family:'Dancing Script',cursive; font-size:clamp(17px,3vw,23px);
  background:linear-gradient(transparent, rgba(20,3,30,.85)); }}
.navBtn {{ position:absolute; top:50%; transform:translateY(-50%); z-index:5; border:none; cursor:pointer;
  background:rgba(255,255,255,.15); color:#fff; width:42px; height:42px; border-radius:50%; font-size:19px;
  backdrop-filter:blur(4px); transition:.25s; }}
.navBtn:hover {{ background:var(--pink); transform:translateY(-50%) scale(1.12); }}
#prevB {{ left:10px; }} #nextB {{ right:10px; }}
.dots {{ display:flex; gap:9px; justify-content:center; margin-top:20px; flex-wrap:wrap; }}
.dot {{ width:10px; height:10px; border-radius:50%; background:rgba(255,255,255,.28); cursor:pointer; transition:.3s; }}
.dot.on {{ background:var(--pink); transform:scale(1.45); box-shadow:0 0 10px var(--pink); }}

/* ---- Reasons / notes cards ---- */
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(250px,1fr)); gap:22px; }}
.note {{ background:rgba(255,255,255,.07); border:1px solid rgba(255,143,171,.35); border-radius:20px;
  padding:26px 22px; backdrop-filter: blur(8px); transition: transform .5s var(--ease), box-shadow .5s var(--ease);
  opacity:0; transform:translateY(46px) scale(.96); box-shadow:0 0 22px rgba(255,93,143,.12); }}
.note.visible {{ animation: cardIn 1.1s var(--ease) forwards; }}
@keyframes cardIn {{ to{{opacity:1; transform:translateY(0) scale(1)}} }}
.note:hover {{ transform:translateY(-8px) scale(1.02); box-shadow:0 14px 40px rgba(255,93,143,.4), 0 0 30px rgba(255,209,102,.2); }}
.note .em {{ font-size:32px; }}
.note h3 {{ color:var(--rose); font-family:'Dancing Script',cursive; font-size:24px; margin:10px 0 8px; }}
.note p {{ color:#f5dbe7; font-size:14.5px; line-height:1.7; font-weight:300; }}

/* ---- Love letter (paragraphs reveal one by one) ---- */
.letter {{ background: linear-gradient(160deg, rgba(255,255,255,.10), rgba(255,255,255,.04));
  border:1px solid rgba(255,209,102,.4); border-radius:26px; padding:clamp(26px,5vw,54px);
  box-shadow: 0 0 60px rgba(123,44,191,.45); position:relative; overflow:hidden; }}
.letter::before {{ content:"❝"; position:absolute; top:-14px; left:16px; font-size:130px; color:rgba(255,143,171,.16); }}
.letter p {{ color:#ffeef5; font-size:clamp(15px,2.4vw,18.5px); line-height:2.05; font-weight:300;
  font-family:'Poppins',sans-serif; margin-bottom:20px;
  opacity:0; transform:translateY(28px); transition:opacity 1s var(--ease), transform 1s var(--ease); }}
.letter p.visible {{ opacity:1; transform:translateY(0); }}
.letter .sig {{ font-family:'Great Vibes',cursive; color:var(--gold); font-size:clamp(26px,4.6vw,38px);
  text-align:right; margin-top:8px; }}

/* ---- Promise ticker ---- */
.tickerWrap {{ overflow:hidden; border-top:1px solid rgba(255,143,171,.3); border-bottom:1px solid rgba(255,143,171,.3);
  padding:16px 0; margin:10px 0 0; }}
.ticker {{ display:inline-block; white-space:nowrap; animation: slideTxt 26s linear infinite;
  font-family:'Dancing Script',cursive; color:#ffd3e2; font-size:clamp(18px,3vw,25px); }}
@keyframes slideTxt {{ from{{transform:translateX(0)}} to{{transform:translateX(-50%)}} }}

/* ---- Footer ---- */
.footer {{ text-align:center; padding:60px 16px 90px; }}
.footer .big {{ font-family:'Great Vibes',cursive; color:#fff; font-size:clamp(34px,7vw,60px);
  text-shadow:0 0 24px rgba(255,93,143,.8); }}
.footer .small {{ color:#ffb9d1; margin-top:14px; font-size:14px; }}

/* ---- Our Story timeline ---- */
.timeline {{ position:relative; max-width:640px; margin:0 auto; padding-left:26px; border-left:2px solid rgba(255,143,171,.35);
  box-shadow: -2px 0 12px rgba(255,143,171,.15); }}
.tl-item {{ position:relative; margin-bottom:34px; text-align:left; }}
.tl-dot {{ position:absolute; left:-33px; top:6px; width:14px; height:14px; border-radius:50%;
  background:radial-gradient(circle, var(--gold), var(--pink)); box-shadow:0 0 12px rgba(255,209,102,.8), 0 0 22px rgba(255,209,102,.4); }}
.tl-card {{ background:rgba(255,255,255,.06); border:1px solid rgba(255,143,171,.28); border-radius:16px; padding:18px 20px;
  box-shadow:0 0 20px rgba(255,93,143,.1); transition:box-shadow .4s var(--ease); }}
.tl-card:hover {{ box-shadow:0 0 28px rgba(255,93,143,.28); }}
.tl-card h3 {{ font-family:'Dancing Script',cursive; color:var(--rose); font-size:22px; margin-bottom:6px; }}
.tl-card p {{ color:#f5dbe7; font-size:14px; line-height:1.7; font-weight:300; }}

/* ---- This or That quiz ---- */
.quizGrid {{ display:flex; flex-direction:column; gap:14px; max-width:520px; margin:0 auto; }}
.quizPair {{ display:flex; align-items:center; justify-content:center; gap:14px; }}
.quizPair span {{ color:#ffb9d1; font-family:'Dancing Script',cursive; font-size:18px; }}
.qOpt {{ flex:1; background:rgba(255,255,255,.07); border:1px solid rgba(255,143,171,.3); color:#ffeef5;
  padding:13px 10px; border-radius:14px; font-size:14px; cursor:pointer; transition:.35s var(--ease);
  box-shadow:0 0 14px rgba(255,93,143,.1); }}
.qOpt:hover {{ transform:translateY(-3px); box-shadow:0 0 20px rgba(255,93,143,.3); }}
.qOpt.picked {{ background:linear-gradient(135deg,var(--pink),var(--violet)); color:#fff; border-color:transparent;
  box-shadow:0 8px 22px rgba(255,93,143,.5), 0 0 30px rgba(255,209,102,.3); transform:scale(1.04); }}
.quizHint {{ text-align:center; color:#ffc9dc; font-size:13px; margin-top:20px; font-style:italic; }}

/* ---- Catch the Hearts game ---- */
#catchGame {{ position:relative; max-width:520px; height:340px; margin:0 auto; border-radius:22px;
  overflow:hidden; background:rgba(255,255,255,.05); border:1px solid rgba(255,143,171,.3);
  box-shadow: inset 0 0 40px rgba(255,93,143,.15), 0 0 30px rgba(255,93,143,.15); }}
#catchGame .fh {{ position:absolute; top:-40px; font-size:26px; cursor:pointer; user-select:none;
  animation: fhFall linear forwards; filter:drop-shadow(0 0 6px rgba(255,93,143,.7)); }}
@keyframes fhFall {{ to {{ transform:translateY(380px); }} }}
#catchHud {{ display:flex; justify-content:space-between; max-width:520px; margin:18px auto 0; padding:0 6px; color:#ffdce6;
  font-family:'Dancing Script',cursive; font-size:19px; }}
#catchStartBtn {{ display:block; margin:18px auto 0; padding:13px 30px; border-radius:50px; border:none;
  background:linear-gradient(135deg,var(--pink),var(--violet)); color:#fff; font-size:15px; cursor:pointer;
  box-shadow:0 8px 22px rgba(255,93,143,.4), 0 0 24px rgba(255,209,102,.25); transition:transform .3s var(--ease), box-shadow .3s var(--ease); }}
#catchStartBtn:hover {{ transform:translateY(-3px) scale(1.05); box-shadow:0 12px 30px rgba(255,93,143,.5), 0 0 34px rgba(255,209,102,.4); }}
#catchResult {{ text-align:center; color:var(--gold); font-family:'Dancing Script',cursive; font-size:22px;
  margin-top:12px; min-height:1.4em; text-shadow:0 0 14px rgba(255,209,102,.6); }}

/* ---- Love Meter game ---- */
#meterWrap {{ max-width:340px; margin:0 auto; text-align:center; }}
#meterOuter {{ width:100%; height:26px; border-radius:20px; background:rgba(255,255,255,.08);
  border:1px solid rgba(255,143,171,.35); overflow:hidden; position:relative; box-shadow:0 0 18px rgba(255,93,143,.15); }}
#meterFill {{ height:100%; width:0%; border-radius:20px;
  background:linear-gradient(90deg,var(--pink),var(--gold)); transition:width .12s linear;
  box-shadow:0 0 14px rgba(255,209,102,.7); }}
#meterPct {{ color:#ffdce6; font-size:14px; margin-top:10px; letter-spacing:1px; }}
#meterBtn {{ display:block; margin:20px auto 0; width:84px; height:84px; border-radius:50%; border:none;
  background:linear-gradient(135deg,var(--pink),var(--violet)); color:#fff; font-size:32px; cursor:pointer;
  box-shadow:0 10px 26px rgba(255,93,143,.5), 0 0 34px rgba(255,209,102,.3); transition:transform .15s var(--ease); user-select:none;
  animation: meterBtnPulse 2.4s ease-in-out infinite; }}
@keyframes meterBtnPulse {{ 0%,100%{{box-shadow:0 10px 26px rgba(255,93,143,.5), 0 0 34px rgba(255,209,102,.3);}} 50%{{box-shadow:0 10px 30px rgba(255,93,143,.7), 0 0 46px rgba(255,209,102,.5);}} }}
#meterBtn:active {{ transform:scale(.9); }}
#meterMsg {{ max-width:420px; margin:18px auto 0; text-align:center; color:#fff; font-family:'Great Vibes',cursive;
  font-size:clamp(22px,4vw,30px); min-height:1.5em; opacity:0; transition:opacity .8s var(--ease);
  text-shadow:0 0 20px rgba(255,93,143,.7); }}
#meterMsg.show {{ opacity:1; }}

/* ---- Finale envelope + surprise ---- */
#envelope {{ width:110px; height:76px; margin:20px auto 10px; position:relative; cursor:pointer; }}
.envBody {{ width:100%; height:100%; background:linear-gradient(160deg,#ffe3ec,#ffc6d9); border-radius:8px;
  display:flex; align-items:center; justify-content:center; font-size:30px; box-shadow:0 10px 30px rgba(255,93,143,.4);
  transition:transform .4s var(--ease), box-shadow .4s var(--ease);
  animation: envGlow 2.6s ease-in-out infinite; }}
@keyframes envGlow {{ 0%,100%{{box-shadow:0 10px 30px rgba(255,93,143,.4);}} 50%{{box-shadow:0 10px 38px rgba(255,93,143,.65), 0 0 30px rgba(255,209,102,.4);}} }}
#envelope:hover .envBody {{ transform:translateY(-6px) scale(1.05); }}
#envelope.opened .envBody {{ animation: envPop .5s var(--ease) forwards; }}
@keyframes envPop {{ 0%{{transform:scale(1)}} 50%{{transform:scale(1.2) rotate(-4deg)}} 100%{{transform:scale(0); opacity:0;}} }}
#finalMsg {{ max-width:480px; margin:0 auto; max-height:0; overflow:hidden; opacity:0;
  transition:max-height 1s var(--ease), opacity .8s var(--ease); }}
#finalMsg.show {{ max-height:520px; opacity:1; margin-top:20px; }}
.finalCard {{ background:linear-gradient(160deg, rgba(255,255,255,.10), rgba(255,255,255,.04));
  border:1px solid rgba(255,209,102,.4); border-radius:22px; padding:32px 26px; box-shadow:0 0 50px rgba(255,93,143,.4), 0 0 80px rgba(123,44,191,.2); }}
.finalHeart {{ font-size:42px; animation: beat 1.15s ease-in-out infinite; }}
.finalCard h3 {{ font-family:'Great Vibes',cursive; color:#fff; font-size:clamp(26px,4.6vw,36px); margin:10px 0 8px;
  text-shadow:0 0 20px rgba(255,93,143,.7); }}
.finalCard p {{ color:#ffeef5; font-size:14.5px; font-weight:300; margin-bottom:20px; }}
.finalBtns {{ display:flex; gap:14px; justify-content:center; flex-wrap:wrap; }}
.yesBtn {{ background:linear-gradient(135deg,var(--pink),var(--violet)); color:#fff; border:none;
  padding:13px 26px; border-radius:50px; font-size:15px; cursor:pointer; box-shadow:0 8px 22px rgba(255,93,143,.4), 0 0 20px rgba(255,209,102,.2);
  transition:transform .3s var(--ease), box-shadow .3s var(--ease); }}
.yesBtn:hover {{ transform:translateY(-3px) scale(1.05); box-shadow:0 12px 30px rgba(255,93,143,.55), 0 0 30px rgba(255,209,102,.4); }}

/* ---- Surprise gift + marry-me reveal ---- */
#giftBox {{ width:120px; height:120px; margin:22px auto 10px; position:relative; cursor:pointer; }}
.giftBody {{ position:absolute; left:0; right:0; bottom:0; top:30px; border-radius:12px;
  background:linear-gradient(160deg,#ff8fab,#c73866); box-shadow:0 10px 30px rgba(255,93,143,.45);
  display:flex; align-items:center; justify-content:center; font-size:40px;
  transition:transform .4s var(--ease), box-shadow .4s var(--ease);
  animation: envGlow 2.6s ease-in-out infinite; }}
.giftLid {{ position:absolute; top:0; left:50%; transform:translateX(-50%); font-size:36px; z-index:2;
  transition: transform .6s var(--ease), opacity .5s var(--ease); }}
#giftBox:hover .giftBody {{ transform:translateY(-6px) scale(1.05); }}
#giftBox.opened .giftBody {{ animation: envPop .5s var(--ease) forwards; }}
#giftBox.opened .giftLid {{ transform:translateX(-50%) translateY(-46px) rotate(-30deg); opacity:0; }}
#marryMsg {{ max-width:480px; margin:0 auto; max-height:0; overflow:hidden; opacity:0;
  transition:max-height 1s var(--ease), opacity .8s var(--ease); }}
#marryMsg.show {{ max-height:560px; opacity:1; margin-top:20px; }}

/* ---- Music button ---- */
#musicBtn {{ position:fixed; bottom:22px; right:22px; z-index:60; width:56px; height:56px; border-radius:50%;
  border:none; cursor:pointer; font-size:23px; color:#fff;
  background:linear-gradient(135deg,var(--pink),var(--violet));
  box-shadow:0 6px 24px rgba(255,93,143,.55); transition:.3s; }}
#musicBtn.playing {{ animation: spinB 4s linear infinite; }}
@keyframes spinB {{ from{{transform:rotate(0)}} to{{transform:rotate(360deg)}} }}
</style>
</head>
<body>

<audio id="song" src="{song}" preload="auto"></audio>
<div id="glowSweep"></div>

<!-- ============ PUZZLE OVERLAY — locked landing screen ============ -->
<div id="puzzleOverlay">
  <div class="ring r1"></div>
  <div class="ring r2"></div>
  <div class="kicker">before anything else opens…</div>
  <h1>A little game before your surprise… 💌</h1>
  <p>Sneha, match all the pairs of love to unlock something made only for you. The page won't move until you do — every match brings you closer to my heart 💘</p>
  <div id="board"></div>
  <div id="moves">Moves: 0</div>
</div>
<div id="flash"></div>
<div id="blastMsg">I Love You, Sneha ❤️</div>

<!-- ============ MAIN PAGE ============ -->
<div id="main">

  <div class="hero">
    <div class="pre" data-speed="0.04">✦ 27 · 07 · 2026 — a day just for you ✦</div>
    <h1 data-speed="0.08">Happy Girlfriend Day in Advance</h1>
    <div class="name" data-speed="0.1">Sneha ❤</div>
    <div class="typing">For Sneha — my favourite person, today and always</div>
    <div class="sub">From the luckiest man alive — yours, always &amp; only, Soumyajit</div>
    <span class="heartbeat">💗</span>
    <div class="scrollhint">scroll down, my love ⌄</div>
  </div>

  <section>
    <div class="sectionTitle" data-speed="-0.04">Every Frame of You 📸</div>
    <div class="sectionSub">Ten pictures. Ten heartbeats. One girl I can't stop looking at.</div>
    <div class="slideWrap" data-speed="0.03">
      {photo_html}
      <button class="navBtn" id="prevB" onclick="stepSlide(-1)">❮</button>
      <button class="navBtn" id="nextB" onclick="stepSlide(1)">❯</button>
    </div>
    <div class="dots">{dots_html}</div>
  </section>

  <section>
    <div class="sectionTitle" data-speed="-0.04">Why I Love You 💝</div>
    <div class="sectionSub">If I listed everything, this page would never end. Here are just a few…</div>
    <div class="grid" data-speed="0.025">
      <div class="note"><div class="em">😊</div><h3>Your Smile</h3>
        <p>That one smile of yours can fix my roughest day in a second. It's my favourite view in the entire world — no sunset even comes close.</p></div>
      <div class="note"><div class="em">👓</div><h3>Those Eyes Behind The Glasses</h3>
        <p>People say eyes speak — yours sing. Every time you look at me, I forget what I was worried about. You see me like nobody else ever has.</p></div>
      <div class="note"><div class="em">🌸</div><h3>Your Grace</h3>
        <p>Saree, kurti, or just a plain white shirt — you carry everything with an elegance that leaves me staring like it's the first time, every time.</p></div>
      <div class="note"><div class="em">💪</div><h3>Your Strength</h3>
        <p>You handle everything life throws with such quiet courage. You inspire me to be better, work harder, and dream bigger — for us.</p></div>
      <div class="note"><div class="em">🎂</div><h3>Your Little Joys</h3>
        <p>The way your face lights up over small things — a tiny cake, a silly joke, a random plan. You turn ordinary days into memories I never want to forget.</p></div>
      <div class="note"><div class="em">🏡</div><h3>You Feel Like Home</h3>
        <p>Wherever you are — that's my favourite place. In a crowd, in silence, on a call at 2 AM… with you, I'm always home.</p></div>
    </div>
  </section>

  <section>
    <div class="sectionTitle" data-speed="-0.04">A Letter For You 💌</div>
    <div class="letter" data-speed="0.02">
      <p>My dearest Sneha,</p>
      <p>Today the world calls it Girlfriend Day — but honestly, every single day has quietly been about you for a long time now. You walked into my life and, without even trying, rearranged everything inside me. My plans, my dreams, my future — somewhere along the way, they all started including you.</p>
      <p>I love how you laugh with your whole heart. I love how you scold me and care for me in the same breath. I love the comfort of talking to you about everything and nothing. With you, I don't have to pretend, perform, or be anyone else — and that freedom is the greatest gift you've ever given me.</p>
      <p>I can't promise a life without problems. But I promise you a hand that will never let go of yours, a heart that will choose you every morning, and a love that will keep growing older — and softer — with us.</p>
      <p>Thank you for being mine. Thank you for choosing me, on my best days and my worst ones. You are, and will always be, my favourite person, my peace, my home, my Sneha.</p>
      <p class="sig">— Forever yours, Soumyajit ❤</p>
    </div>
  </section>

  <section style="padding-top:20px;">
    <div class="tickerWrap">
      <div class="ticker">
        I promise to always hold your hand 🤝 &nbsp;•&nbsp; I promise late-night talks forever 🌙 &nbsp;•&nbsp; I promise to make you laugh every day 😄 &nbsp;•&nbsp; I promise to grow old with you 👵🧓 &nbsp;•&nbsp; I promise you'll never walk alone 💞 &nbsp;•&nbsp;
        I promise to always hold your hand 🤝 &nbsp;•&nbsp; I promise late-night talks forever 🌙 &nbsp;•&nbsp; I promise to make you laugh every day 😄 &nbsp;•&nbsp; I promise to grow old with you 👵🧓 &nbsp;•&nbsp; I promise you'll never walk alone 💞 &nbsp;•&nbsp;
      </div>
    </div>
  </section>

  <section>
    <div class="sectionTitle" data-speed="-0.04">Our Story So Far 🕊️</div>
    <div class="sectionSub">A few chapters I never want to forget.</div>
    <div class="timeline stagger-group" data-speed="0.02">
      <div class="tl-item">
        <div class="tl-dot"></div>
        <div class="tl-card"><h3>The Day We Met</h3>
          <p>Just an ordinary day — until it wasn't. I still remember exactly how it felt.</p></div>
      </div>
      <div class="tl-item">
        <div class="tl-dot"></div>
        <div class="tl-card"><h3>The First "I Miss You"</h3>
          <p>The moment I realised this wasn't just liking someone — it was something a lot bigger.</p></div>
      </div>
      <div class="tl-item">
        <div class="tl-dot"></div>
        <div class="tl-card"><h3>Every Little Adventure Since</h3>
          <p>Every trip, every random plan, every silly fight and softer make-up — all of it, with you.</p></div>
      </div>
      <div class="tl-item">
        <div class="tl-dot"></div>
        <div class="tl-card"><h3>Today</h3>
          <p>Still choosing you. Still grateful. Still a little in disbelief that I get to call you mine.</p></div>
      </div>
    </div>
  </section>

  <section>
    <div class="sectionTitle" data-speed="-0.04">This or That 💫</div>
    <div class="sectionSub">Just for fun — tap your answer.</div>
    <div class="quizGrid" data-speed="0.025">
      <div class="quizPair" data-pair="1"><button class="qOpt">☕ Coffee</button><span>or</span><button class="qOpt">🍵 Tea</button></div>
      <div class="quizPair" data-pair="2"><button class="qOpt">🏖️ Beach</button><span>or</span><button class="qOpt">⛰️ Mountains</button></div>
      <div class="quizPair" data-pair="3"><button class="qOpt">🌅 Morning cuddles</button><span>or</span><button class="qOpt">🌙 Late-night talks</button></div>
      <div class="quizPair" data-pair="4"><button class="qOpt">🎬 Movie night</button><span>or</span><button class="qOpt">🎶 Dance it out</button></div>
      <div class="quizPair" data-pair="5"><button class="qOpt">🍫 Chocolate</button><span>or</span><button class="qOpt">🍰 Cake</button></div>
    </div>
    <div class="quizHint">(Honestly? With you, every answer is the right one.)</div>
  </section>

  <section style="text-align:center;">
    <div class="sectionTitle" data-speed="-0.04">Catch the Hearts 💗</div>
    <div class="sectionSub">15 seconds. Tap every heart you can. No pressure — you already caught mine.</div>
    <div id="catchGame" data-speed="0.02"></div>
    <div id="catchHud"><span id="catchScore">Score: 0</span><span id="catchTime">Time: 15</span></div>
    <button id="catchStartBtn">▶ Start</button>
    <div id="catchResult"></div>
  </section>

  <section style="text-align:center;">
    <div class="sectionTitle" data-speed="-0.04">The Love Meter 💞</div>
    <div class="sectionSub">Press and hold the heart. Watch it fill.</div>
    <div id="meterWrap" data-speed="0.025">
      <div id="meterOuter"><div id="meterFill"></div></div>
      <div id="meterPct">0%</div>
      <button id="meterBtn">💗</button>
    </div>
    <div id="meterMsg"></div>
  </section>

  <section style="text-align:center;">
    <div class="sectionTitle" data-speed="-0.04">One More Thing… 💌</div>
    <div class="sectionSub">I saved the best for last.</div>
    <div id="envelope">
      <div class="envTop"></div>
      <div class="envBody">✉️</div>
    </div>
    <div id="finalMsg">
      <div class="finalCard" data-speed="0.02">
        <div class="finalHeart">💖</div>
        <h3>Will you keep being mine?</h3>
        <p>Not just today — every ordinary day after this one too.</p>
        <div class="finalBtns">
          <button class="yesBtn" id="yesBtn1">Yes 💕</button>
          <button class="yesBtn" id="yesBtn2">Also Yes 💞</button>
        </div>
      </div>
    </div>
  </section>

  <section style="text-align:center;">
    <div class="sectionTitle" data-speed="-0.04">A Surprise Gift 🎁</div>
    <div class="sectionSub">One more thing I've been keeping just for you...</div>
    <div id="giftBox">
      <div class="giftLid">🎀</div>
      <div class="giftBody">🎁</div>
    </div>
    <div id="marryMsg">
      <div class="finalCard" data-speed="0.02">
        <div class="finalHeart">💍</div>
        <h3>Will You Marry Me?</h3>
        <p>Not a question I take lightly — I want every someday with you, starting now.</p>
        <div class="finalBtns">
          <button class="yesBtn" id="marryYes1">Yes, Forever 💍</button>
          <button class="yesBtn" id="marryYes2">A Thousand Times Yes 💕</button>
        </div>
      </div>
    </div>
  </section>

  <div class="footer">
    <div class="big" data-speed="-0.03">Happy Girlfriend Day, Sneha 💖</div>
    <div class="small">Made with all my love, just for you • Soumyajit ∞ Sneha</div>
  </div>
</div>

<button id="musicBtn" title="music">🎵</button>

<script>
/* ================= SCROLL LOCK (puzzle-first, nothing moves before it's solved) ================= */
document.documentElement.classList.add('locked');
document.body.classList.add('locked');
function preventScroll(e){{ e.preventDefault(); }}
document.addEventListener('wheel', preventScroll, {{passive:false}});
document.addEventListener('touchmove', preventScroll, {{passive:false}});
document.addEventListener('keydown', function(e){{
  const keys=['ArrowUp','ArrowDown','PageUp','PageDown','Space','End','Home'];
  if(document.body.classList.contains('locked') && keys.includes(e.code)) e.preventDefault();
}}, {{passive:false}});
function unlockScroll(){{
  document.documentElement.classList.remove('locked');
  document.body.classList.remove('locked');
  document.removeEventListener('wheel', preventScroll, {{passive:false}});
  document.removeEventListener('touchmove', preventScroll, {{passive:false}});
}}

/* ================= BACKGROUND MAGIC ================= */
function rand(a,b){{ return Math.random()*(b-a)+a; }}

const nebula=document.createElement('div'); nebula.id='nebula';
document.body.appendChild(nebula);

const themeGlow=document.createElement('div'); themeGlow.id='themeGlow';
themeGlow.setAttribute('data-speed','-0.03');
document.body.appendChild(themeGlow);

const gifSparkle=document.createElement('div'); gifSparkle.id='gifSparkleLayer'; gifSparkle.className='gifLayer';
gifSparkle.setAttribute('data-speed','-0.06');
if('{gif_sparkle}') gifSparkle.style.backgroundImage=`url('{gif_sparkle}')`;
document.body.appendChild(gifSparkle);

const gifShoot=document.createElement('div'); gifShoot.id='gifShootLayer'; gifShoot.className='gifLayer';
gifShoot.setAttribute('data-speed','0.09');
if('{gif_shoot}') gifShoot.style.backgroundImage=`url('{gif_shoot}')`;
document.body.appendChild(gifShoot);

const starLayer=document.createElement('div'); starLayer.id='starLayer';
document.body.appendChild(starLayer);
for (let i=0;i<160;i++) {{
  const s=document.createElement('div');
  const roll=Math.random();
  s.className='star' + (roll<0.35?' glow':'') + (roll>0.85?' gold':'');
  const sz=rand(1.4,3.8);
  s.style.cssText=`left:${{rand(0,100)}}%; top:${{rand(0,100)}}%; width:${{sz}}px; height:${{sz}}px;
    animation-duration:${{rand(1.6,4.6)}}s; animation-delay:${{rand(0,4)}}s;`;
  starLayer.appendChild(s);
}}
for (let i=0;i<5;i++) {{
  const s=document.createElement('div'); s.className='shoot';
  s.style.cssText=`left:${{rand(55,95)}}vw; top:${{rand(2,30)}}vh; animation-delay:${{rand(0,9)}}s; animation-duration:${{rand(2.6,4)}}s;`;
  document.body.appendChild(s);
}}
const heartChars=['❤️','💖','💕','💗','💘','🌹','💞'];
for (let i=0;i<16;i++) {{
  const h=document.createElement('div'); h.className='fheart';
  h.textContent=heartChars[Math.floor(rand(0,heartChars.length))];
  h.style.cssText=`left:${{rand(0,96)}}vw; font-size:${{rand(15,34)}}px; --sway:${{rand(-14,14)}}vw;
    animation-duration:${{rand(9,20)}}s; animation-delay:${{rand(0,14)}}s;`;
  document.body.appendChild(h);
}}
const words=['I love you','Sneha ❤','Forever & Always','My Everything','Soumyajit ∞ Sneha','You & Me','My Home','My Peace'];
for (let i=0;i<9;i++) {{
  const w=document.createElement('div'); w.className='fword';
  w.textContent=words[i%words.length];
  w.style.cssText=`left:${{rand(2,86)}}vw; font-size:${{rand(15,27)}}px;
    animation-duration:${{rand(14,26)}}s; animation-delay:${{rand(0,16)}}s;`;
  document.body.appendChild(w);
}}
for (let i=0;i<24;i++) {{
  const g=document.createElement('div'); g.className='sparkle';
  g.style.cssText=`left:${{rand(0,100)}}vw; top:${{rand(0,100)}}vh; animation-delay:${{rand(0,2.6)}}s;`;
  document.body.appendChild(g);
}}

/* ================= PARALLAX ON SCROLL (bounded — never drifts elements out of place) ================= */
const allParallaxEls=[...document.querySelectorAll('[data-speed]')];
const parallaxContentEls=allParallaxEls.filter(el=>getComputedStyle(el).position!=='fixed');
const parallaxBgEls=allParallaxEls.filter(el=>getComputedStyle(el).position==='fixed');
let parallaxTicking=false;
function onParallaxScroll(){{
  if(parallaxTicking) return;
  parallaxTicking=true;
  requestAnimationFrame(()=>{{
    const vh=window.innerHeight, y=window.scrollY;
    /* in-flow text/content: offset relative to the element's own position, capped
       so it can never drift into a neighbouring section */
    parallaxContentEls.forEach(el=>{{
      const sp=parseFloat(el.dataset.speed);
      const rect=el.getBoundingClientRect();
      const distFromCentre=(rect.top+rect.height/2)-(vh/2);
      const offset=Math.max(-60,Math.min(60, distFromCentre*sp));
      el.style.transform=`translateY(${{offset}}px)`;
    }});
    /* fixed full-screen background layers: gentle bounded sway instead of
       unbounded linear drift */
    parallaxBgEls.forEach(el=>{{
      const sp=parseFloat(el.dataset.speed);
      const amp=Math.min(240, Math.abs(sp)*2400);
      const offset=Math.sin(y*0.0006)*amp*Math.sign(sp||1);
      el.style.transform=`translateY(${{offset}}px)`;
    }});
    parallaxTicking=false;
  }});
}}
window.addEventListener('scroll', onParallaxScroll, {{passive:true}});

/* ================= CURSOR HEART TRAIL (subtle, throttled) ================= */
let lastTrail=0;
document.addEventListener('mousemove', e=>{{
  const now=Date.now();
  if(now-lastTrail<90) return;
  lastTrail=now;
  const t=document.createElement('div'); t.className='trailHeart';
  t.textContent=heartChars[Math.floor(rand(0,heartChars.length))];
  t.style.left=(e.clientX-6)+'px'; t.style.top=(e.clientY-6)+'px';
  document.body.appendChild(t);
  setTimeout(()=>t.remove(),900);
}});

/* ================= MEMORY PUZZLE ================= */
const emojis=['❤️','💖','💘','🌹'];
let deck=[...emojis,...emojis].sort(()=>Math.random()-0.5);
const board=document.getElementById('board');
let first=null, lock=false, matched=0, moves=0;

deck.forEach(e=>{{
  const c=document.createElement('div'); c.className='card';
  c.innerHTML=`<div class="cardInner"><div class="face front">💌</div><div class="face back">${{e}}</div></div>`;
  c.dataset.v=e;
  c.onclick=()=>flip(c);
  board.appendChild(c);
}});

function flip(c){{
  if(lock||c.classList.contains('flip'))return;
  c.classList.add('flip');
  if(!first){{ first=c; return; }}
  moves++; document.getElementById('moves').textContent='Moves: '+moves;
  if(first.dataset.v===c.dataset.v){{
    first.classList.add('matched'); c.classList.add('matched');
    matched++; first=null;
    miniPop(c);
    if(matched===emojis.length) setTimeout(winSequence,600);
  }} else {{
    lock=true; const f=first;
    setTimeout(()=>{{ f.classList.remove('flip'); c.classList.remove('flip'); lock=false; }},750);
    first=null;
  }}
}}

function miniPop(el){{
  const r=el.getBoundingClientRect();
  for(let i=0;i<6;i++) spawnBlast(r.left+r.width/2, r.top+r.height/2, 90);
}}

function spawnBlast(x,y,dist){{
  const b=document.createElement('div'); b.className='blast';
  b.textContent=heartChars[Math.floor(rand(0,heartChars.length))];
  const ang=rand(0,Math.PI*2), d=rand(dist*0.5,dist*1.6);
  b.style.cssText=`left:${{x}}px; top:${{y}}px; --bx:${{Math.cos(ang)*d}}px; --by:${{Math.sin(ang)*d}}px; --br:${{rand(-260,260)}}deg;`;
  document.body.appendChild(b);
  setTimeout(()=>b.remove(),1700);
}}

const audio=document.getElementById('song');
const musicBtn=document.getElementById('musicBtn');

function winSequence(){{
  /* LOVE BLAST 💥 — camera flash + a much bigger, longer burst */
  const flash=document.getElementById('flash');
  flash.classList.add('pop');

  const cx=innerWidth/2, cy=innerHeight/2;
  let n=0;
  const iv=setInterval(()=>{{
    for(let i=0;i<16;i++) spawnBlast(rand(cx-innerWidth*0.42,cx+innerWidth*0.42), rand(cy-innerHeight*0.38,cy+innerHeight*0.38), 340);
    if(++n>=14) clearInterval(iv);
  }},110);

  const msg=document.getElementById('blastMsg');
  msg.classList.add('show');

  /* play song — always starts at 1:48 (108s) */
  startSongFrom148();

  setTimeout(()=>{{
    msg.classList.remove('show');
    document.getElementById('puzzleOverlay').classList.add('hide');
    document.getElementById('main').classList.add('show');
    unlockScroll();
    onParallaxScroll();
    revealOnScroll();
  }},2700);
}}

musicBtn.onclick=()=>{{
  if(audio.paused){{ audio.play(); musicBtn.classList.add('playing'); musicBtn.textContent='🎵'; }}
  else {{ audio.pause(); musicBtn.classList.remove('playing'); musicBtn.textContent='🔇'; }}
}};

/* ================= SONG START TIME — always begins at 1:48 (108s), loops back to 1:48 ================= */
const SONG_START_SEC = 108;
function startSongFrom148(){{
  const go=()=>{{ try {{ audio.currentTime = SONG_START_SEC; }} catch(e) {{}} audio.play().then(()=>musicBtn.classList.add('playing')).catch(()=>{{}}); }};
  if(audio.readyState >= 1) go();
  else audio.addEventListener('loadedmetadata', go, {{once:true}});
}}
audio.addEventListener('ended', ()=>{{
  audio.currentTime = SONG_START_SEC;
  audio.play().catch(()=>{{}});
}});

/* ================= SLIDESHOW ================= */
const slides=[...document.querySelectorAll('.slide')];
const dots=[...document.querySelectorAll('.dot')];
let cur=0, timer=setInterval(()=>stepSlide(1), 4200);

function show(i){{
  slides[cur].classList.remove('active'); dots[cur].classList.remove('on');
  cur=(i+slides.length)%slides.length;
  slides[cur].classList.add('active'); dots[cur].classList.add('on');
}}
function stepSlide(d){{ show(cur+d); resetT(); }}
function goSlide(i){{ show(i); resetT(); }}
function resetT(){{ clearInterval(timer); timer=setInterval(()=>stepSlide(1),4200); }}

/* ================= SCROLL REVEAL (cards cascade, letter unfolds line by line) ================= */
function revealOnScroll(){{
  const cardObs=new IntersectionObserver(es=>es.forEach(e=>{{
    if(e.isIntersecting){{
      const cards=[...e.target.parentElement.children];
      const idx=cards.indexOf(e.target);
      e.target.style.transitionDelay=(idx*0.12)+'s';
      e.target.classList.add('visible');
      cardObs.unobserve(e.target);
    }}
  }}),{{threshold:.15}});
  document.querySelectorAll('.note').forEach(n=>cardObs.observe(n));

  const letterObs=new IntersectionObserver(es=>es.forEach(e=>{{
    if(e.isIntersecting){{
      const paras=[...e.target.parentElement.querySelectorAll('p')];
      const idx=paras.indexOf(e.target);
      e.target.style.transitionDelay=(idx*0.35)+'s';
      e.target.classList.add('visible');
      letterObs.unobserve(e.target);
    }}
  }}),{{threshold:.3}});
  document.querySelectorAll('.letter p').forEach(p=>letterObs.observe(p));

  const genObs=new IntersectionObserver(es=>es.forEach(e=>{{
    if(e.isIntersecting){{
      const kids=[...e.target.children];
      kids.forEach((k,i)=>{{ k.style.transitionDelay=(i*0.15)+'s'; k.classList.add('seqIn'); }});
      genObs.unobserve(e.target);
    }}
  }}),{{threshold:.2}});
  document.querySelectorAll('.stagger-group').forEach(g=>genObs.observe(g));
}}

/* ================= THIS OR THAT QUIZ ================= */
document.querySelectorAll('.quizPair').forEach(pair=>{{
  const opts=[...pair.querySelectorAll('.qOpt')];
  opts.forEach(btn=>{{
    btn.addEventListener('click',()=>{{
      opts.forEach(o=>o.classList.remove('picked'));
      btn.classList.add('picked');
      const r=btn.getBoundingClientRect();
      for(let i=0;i<5;i++) spawnBlast(r.left+r.width/2, r.top+r.height/2, 70);
    }});
  }});
}});

/* ================= CATCH THE HEARTS GAME ================= */
const catchGame=document.getElementById('catchGame');
const catchStartBtn=document.getElementById('catchStartBtn');
const catchScoreEl=document.getElementById('catchScore');
const catchTimeEl=document.getElementById('catchTime');
const catchResult=document.getElementById('catchResult');
let catchScore=0, catchTimer=null, catchSpawner=null, catchTimeLeft=15, catchRunning=false;

function spawnFallingHeart(){{
  const h=document.createElement('div'); h.className='fh';
  h.textContent=heartChars[Math.floor(rand(0,heartChars.length))];
  const w=catchGame.clientWidth||480;
  h.style.left=rand(10,w-30)+'px';
  const dur=rand(2.6,4.2);
  h.style.animationDuration=dur+'s';
  h.addEventListener('click',()=>{{
    if(!catchRunning) return;
    catchScore++; catchScoreEl.textContent='Score: '+catchScore;
    const r=h.getBoundingClientRect();
    for(let i=0;i<6;i++) spawnBlast(r.left+r.width/2, r.top+r.height/2, 90);
    h.remove();
  }});
  catchGame.appendChild(h);
  setTimeout(()=>{{ if(h.parentNode) h.remove(); }}, dur*1000+50);
}}

function startCatchGame(){{
  if(catchRunning) return;
  catchRunning=true; catchScore=0; catchTimeLeft=15;
  catchScoreEl.textContent='Score: 0';
  catchTimeEl.textContent='Time: 15';
  catchResult.textContent='';
  catchGame.innerHTML='';
  catchStartBtn.textContent='… playing';
  catchSpawner=setInterval(spawnFallingHeart, 420);
  catchTimer=setInterval(()=>{{
    catchTimeLeft--;
    catchTimeEl.textContent='Time: '+catchTimeLeft;
    if(catchTimeLeft<=0) endCatchGame();
  }},1000);
}}
function endCatchGame(){{
  catchRunning=false;
  clearInterval(catchSpawner); clearInterval(catchTimer);
  catchGame.querySelectorAll('.fh').forEach(h=>h.remove());
  catchStartBtn.textContent='▶ Play again';
  let msg='Sweet! 💕';
  if(catchScore>=20) msg="Okay wow — you're unstoppable 😍";
  else if(catchScore>=12) msg='So good at catching hearts (mine included) 💖';
  else if(catchScore>=6) msg='Cute score! Just like you 🥰';
  catchResult.textContent=`${{catchScore}} hearts caught — ${{msg}}`;
}}
catchStartBtn.addEventListener('click', startCatchGame);

/* ================= LOVE METER GAME ================= */
const meterFill=document.getElementById('meterFill');
const meterPct=document.getElementById('meterPct');
const meterBtn=document.getElementById('meterBtn');
const meterMsg=document.getElementById('meterMsg');
let meterVal=0, meterHold=null, meterDone=false;

const meterLines=[
  '25% — you have my attention 👀',
  '50% — okay, this is definitely love 💓',
  '75% — almost there, keep going… 🥺',
  '100% — completely, hopelessly yours 💖'
];

function meterTick(){{
  if(meterDone) return;
  meterVal=Math.min(100, meterVal+2);
  meterFill.style.width=meterVal+'%';
  meterPct.textContent=meterVal+'%';
  if(meterVal===25||meterVal===50||meterVal===75){{
    meterMsg.textContent=meterLines[[25,50,75].indexOf(meterVal)];
    meterMsg.classList.add('show');
  }}
  if(meterVal>=100){{
    meterDone=true;
    meterMsg.textContent=meterLines[3];
    meterMsg.classList.add('show');
    const r=meterBtn.getBoundingClientRect();
    for(let i=0;i<16;i++) spawnBlast(r.left+r.width/2, r.top+r.height/2, 200);
    stopMeterHold();
  }}
}}
function startMeterHold(){{
  if(meterDone) return;
  stopMeterHold();
  meterHold=setInterval(meterTick, 45);
}}
function stopMeterHold(){{ if(meterHold){{ clearInterval(meterHold); meterHold=null; }} }}
meterBtn.addEventListener('mousedown', startMeterHold);
meterBtn.addEventListener('touchstart', e=>{{ e.preventDefault(); startMeterHold(); }}, {{passive:false}});
['mouseup','mouseleave','touchend','touchcancel'].forEach(ev=>meterBtn.addEventListener(ev, stopMeterHold));

/* ================= FINALE ENVELOPE ================= */
const envelope=document.getElementById('envelope');
const finalMsg=document.getElementById('finalMsg');
envelope.addEventListener('click',()=>{{
  if(envelope.classList.contains('opened')) return;
  envelope.classList.add('opened');
  setTimeout(()=>finalMsg.classList.add('show'),350);
  const r=envelope.getBoundingClientRect();
  for(let i=0;i<18;i++) spawnBlast(r.left+r.width/2, r.top+r.height/2, 220);
}});

function bigCelebration(originEl){{
  const flash=document.getElementById('flash');
  flash.classList.remove('pop'); void flash.offsetWidth; flash.classList.add('pop');
  const r=originEl.getBoundingClientRect();
  const cx=r.left+r.width/2, cy=r.top+r.height/2;
  let n=0;
  const iv=setInterval(()=>{{
    for(let i=0;i<14;i++) spawnBlast(rand(cx-innerWidth*0.4,cx+innerWidth*0.4), rand(cy-innerHeight*0.35,cy+innerHeight*0.35), 320);
    if(++n>=10) clearInterval(iv);
  }},110);
}}
document.getElementById('yesBtn1').addEventListener('click', e=>bigCelebration(e.target));
document.getElementById('yesBtn2').addEventListener('click', e=>bigCelebration(e.target));

/* ================= SURPRISE GIFT — WILL YOU MARRY ME ================= */
const giftBox=document.getElementById('giftBox');
const marryMsg=document.getElementById('marryMsg');
giftBox.addEventListener('click', ()=>{{
  if(giftBox.classList.contains('opened')) return;
  giftBox.classList.add('opened');
  setTimeout(()=>marryMsg.classList.add('show'),350);
  const r=giftBox.getBoundingClientRect();
  for(let i=0;i<18;i++) spawnBlast(r.left+r.width/2, r.top+r.height/2, 220);
}});
document.getElementById('marryYes1').addEventListener('click', e=>bigCelebration(e.target));
document.getElementById('marryYes2').addEventListener('click', e=>bigCelebration(e.target));

/* click anywhere → tiny heart */
document.addEventListener('click',e=>{{
  if(document.getElementById('puzzleOverlay').classList.contains('hide'))
    spawnBlast(e.clientX,e.clientY,70);
}});
</script>
</body>
</html>
"""

components.html(html, height=900, scrolling=True)
