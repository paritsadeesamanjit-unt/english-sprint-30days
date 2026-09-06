import streamlit as st
import streamlit.components.v1 as components
from gtts import gTTS
import io
import json
import os
import base64

# -----------------------------------------------------------------------------
# 1. Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="English Sprint 30 Days",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. Permanent Phonics Handbook Data (เทียบเสียงกลุ่มพยัญชนะ อังกฤษ-ไทย)
# -----------------------------------------------------------------------------
PHONICS_CATEGORIES = {
    "1. พยัญชนะต้น 1 ตัว": [
        {"letter": "b", "thai": "บี", "word": "bat", "sound": "b, bat"},
        {"letter": "c", "thai": "คี / ซี", "word": "cat / city", "sound": "c, cat, city"},
        {"letter": "d", "thai": "ดี", "word": "dog", "sound": "d, dog"},
        {"letter": "f", "thai": "ฟือ", "word": "fish", "sound": "f, fish"},
        {"letter": "g", "thai": "กี / จี", "word": "gun / gem", "sound": "g, gun, gem"},
        {"letter": "h", "thai": "ฮา", "word": "hat", "sound": "h, hat"},
        {"letter": "j", "thai": "จี", "word": "jam", "sound": "j, jam"},
        {"letter": "k", "thai": "คี", "word": "king", "sound": "k, king"},
        {"letter": "l", "thai": "ลือ", "word": "lion", "sound": "l, lion"},
        {"letter": "m", "thai": "อึม", "word": "man", "sound": "m, man"},
        {"letter": "n", "thai": "อึน", "word": "net", "sound": "n, net"},
        {"letter": "p", "thai": "พี", "word": "pen", "sound": "p, pen"},
        {"letter": "q", "thai": "คยู", "word": "queen", "sound": "q, queen"},
        {"letter": "r", "thai": "รู", "word": "red", "sound": "r, red"},
        {"letter": "s", "thai": "ซี", "word": "sun", "sound": "s, sun"},
        {"letter": "t", "thai": "ที", "word": "top", "sound": "t, top"},
        {"letter": "v", "thai": "ฟือ (กัดริมฝีปาก)", "word": "van", "sound": "v, van"},
        {"letter": "w", "thai": "วู", "word": "wet", "sound": "w, wet"},
        {"letter": "x", "thai": "อี (เอ็กซ์)", "word": "x-ray", "sound": "x, x-ray"},
        {"letter": "y", "thai": "ยี", "word": "yes", "sound": "y, yes"},
        {"letter": "z", "thai": "ซีอ (สั่นในลำคอ)", "word": "zoo", "sound": "z, zoo"}
    ],
    "2. พยัญชนะควบต้น 2 ตัว (l / r)": [
        {"letter": "bl", "thai": "บลือ", "word": "black", "sound": "bl, black"},
        {"letter": "cl", "thai": "คลือ", "word": "clap", "sound": "cl, clap"},
        {"letter": "fl", "thai": "ฟลือ", "word": "flag", "sound": "fl, flag"},
        {"letter": "gl", "thai": "กลือ", "word": "glass", "sound": "gl, glass"},
        {"letter": "pl", "thai": "พลือ", "word": "play", "sound": "pl, play"},
        {"letter": "sl", "thai": "สลือ", "word": "sleep", "sound": "sl, sleep"},
        {"letter": "br", "thai": "บรู", "word": "brown", "sound": "br, brown"},
        {"letter": "cr", "thai": "ครู", "word": "crab", "sound": "cr, crab"},
        {"letter": "dr", "thai": "ดรู", "word": "drum", "sound": "dr, drum"},
        {"letter": "fr", "thai": "ฟรู", "word": "frog", "sound": "fr, frog"},
        {"letter": "gr", "thai": "กรู", "word": "green", "sound": "gr, green"},
        {"letter": "pr", "thai": "พรู", "word": "press", "sound": "pr, press"},
        {"letter": "tr", "thai": "ทรู", "word": "truck", "sound": "tr, truck"}
    ],
    "3. พยัญชนะควบต้น (s & 3 ตัว)": [
        {"letter": "sc", "thai": "สกี", "word": "scan", "sound": "sc, scan"},
        {"letter": "sk", "thai": "สกี", "word": "sky", "sound": "sk, sky"},
        {"letter": "sm", "thai": "สเมือ", "word": "small", "sound": "sm, small"},
        {"letter": "sn", "thai": "สเนือ", "word": "snake", "sound": "sn, snake"},
        {"letter": "sp", "thai": "สปี", "word": "speak", "sound": "sp, speak"},
        {"letter": "st", "thai": "สตี", "word": "stop", "sound": "st, stop"},
        {"letter": "sw", "thai": "สวู", "word": "swim", "sound": "sw, swim"},
        {"letter": "tw", "thai": "ทวู", "word": "twin", "sound": "tw, twin"},
        {"letter": "scr", "thai": "สครู", "word": "screen", "sound": "scr, screen"},
        {"letter": "spl", "thai": "สปลือ", "word": "splash", "sound": "spl, splash"},
        {"letter": "spr", "thai": "สปรู", "word": "spring", "sound": "spr, spring"},
        {"letter": "str", "thai": "สตรู", "word": "street", "sound": "str, street"},
        {"letter": "shr", "thai": "ชรู", "word": "shrimp", "sound": "shr, shrimp"},
        {"letter": "squ", "thai": "สควู", "word": "square", "sound": "squ, square"}
    ],
    "4. สองตัวหนึ่งเสียง (Digraphs)": [
        {"letter": "ch", "thai": "ชุ", "word": "check", "sound": "ch, check"},
        {"letter": "sh", "thai": "ชุ", "word": "ship", "sound": "sh, ship"},
        {"letter": "th", "thai": "ธีอ (แลบลิ้น)", "word": "think", "sound": "th, think"},
        {"letter": "wh", "thai": "ว", "word": "when", "sound": "wh, when"},
        {"letter": "ph", "thai": "ฟือ", "word": "phone", "sound": "ph, phone"},
        {"letter": "qu", "thai": "ควู", "word": "quick", "sound": "qu, quick"},
        {"letter": "ck", "thai": "คี", "word": "dock", "sound": "ck, dock"},
        {"letter": "ng", "thai": "อึง", "word": "ring", "sound": "ng, ring"},
        {"letter": "tch", "thai": "ชุ", "word": "catch", "sound": "tch, catch"},
        {"letter": "dge", "thai": "จี", "word": "bridge", "sound": "dge, bridge"},
        {"letter": "ff", "thai": "ฟือ", "word": "staff", "sound": "ff, staff"},
        {"letter": "ll", "thai": "อึล", "word": "bell", "sound": "ll, bell"},
        {"letter": "ss", "thai": "ซี", "word": "pass", "sound": "ss, pass"},
        {"letter": "zz", "thai": "ซีอ", "word": "buzz", "sound": "zz, buzz"}
    ],
    "5. พยัญชนะท้าย 1 ตัว": [
        {"letter": "-b", "thai": "บึ", "word": "cab", "sound": "b, cab"},
        {"letter": "-d", "thai": "ดึ", "word": "red", "sound": "d, red"},
        {"letter": "-f", "thai": "ฟึอ", "word": "brief", "sound": "f, brief"},
        {"letter": "-g", "thai": "กึ", "word": "bag", "sound": "g, bag"},
        {"letter": "-k", "thai": "กึ", "word": "pack", "sound": "k, pack"},
        {"letter": "-l", "thai": "อึล", "word": "ball", "sound": "l, ball"},
        {"letter": "-m", "thai": "อึม", "word": "team", "sound": "m, team"},
        {"letter": "-n", "thai": "อึน", "word": "scan", "sound": "n, scan"},
        {"letter": "-p", "thai": "ปึ", "word": "stop", "sound": "p, stop"},
        {"letter": "-s", "thai": "ซี", "word": "bus", "sound": "s, bus"},
        {"letter": "-t", "thai": "ตี", "word": "part", "sound": "t, part"},
        {"letter": "-v", "thai": "ฝึอ", "word": "move", "sound": "v, move"},
        {"letter": "-x", "thai": "กึซี", "word": "box", "sound": "x, box"},
        {"letter": "-z", "thai": "ซีอ", "word": "quiz", "sound": "z, quiz"}
    ],
    "6. พยัญชนะท้าย 2-3 ตัว": [
        {"letter": "-nd", "thai": "นดึ", "word": "send", "sound": "nd, send"},
        {"letter": "-nt", "thai": "นตี", "word": "print", "sound": "nt, print"},
        {"letter": "-mp", "thai": "มปึ", "word": "ramp", "sound": "mp, ramp"},
        {"letter": "-st", "thai": "สตี", "word": "fast", "sound": "st, fast"},
        {"letter": "-sk", "thai": "สกี", "word": "desk", "sound": "sk, desk"},
        {"letter": "-ft", "thai": "ฟตี", "word": "shift", "sound": "ft, shift"},
        {"letter": "-ld", "thai": "ลดึ", "word": "hold", "sound": "ld, hold"},
        {"letter": "-lk", "thai": "ลกึ", "word": "bulk", "sound": "lk, bulk"},
        {"letter": "-lp", "thai": "ลปึ", "word": "help", "sound": "lp, help"},
        {"letter": "-pt", "thai": "ปตี", "word": "kept", "sound": "pt, kept"},
        {"letter": "-ct", "thai": "คตี", "word": "inspect", "sound": "ct, inspect"},
        {"letter": "-nk", "thai": "งกึ", "word": "tank", "sound": "nk, tank"},
        {"letter": "-nch", "thai": "นชุ", "word": "branch", "sound": "nch, branch"},
        {"letter": "-rst", "thai": "รสตี", "word": "first", "sound": "rst, first"}
    ],
    "7. ตัวอักษรไม่ออกเสียง (Silent Letters)": [
        {"letter": "kn-", "thai": "นือ (ไม่ออกเสียง k)", "word": "know", "sound": "silent k, know"},
        {"letter": "wr-", "thai": "รู (ไม่ออกเสียง w)", "word": "write", "sound": "silent w, write"},
        {"letter": "gn-", "thai": "นือ (ไม่ออกเสียง g)", "word": "sign", "sound": "silent g, sign"},
        {"letter": "-mb", "thai": "อึม (ไม่ออกเสียง b)", "word": "climb", "sound": "silent b, climb"},
        {"letter": "-bt", "thai": "ตี (ไม่ออกเสียง b)", "word": "doubt", "sound": "silent b, doubt"},
        {"letter": "-lk", "thai": "กี (ไม่ออกเสียง l)", "word": "walk", "sound": "silent l, walk"},
        {"letter": "ps-", "thai": "ซี (ไม่ออกเสียง p)", "word": "psychology", "sound": "silent p, psychology"},
        {"letter": "pn-", "thai": "อึน (ไม่ออกเสียง p)", "word": "pneumatic", "sound": "silent p, pneumatic"},
        {"letter": "-gh", "thai": "เงียบ / เสียง ฟือ", "word": "light / rough", "sound": "light, rough"}
    ]
}

# -----------------------------------------------------------------------------
# 3. Audio Booster Engine (Web Audio API 2.5x)
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def get_tts_bytes(text: str) -> bytes:
    try:
        tts = gTTS(text=text, lang="en")
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        return buf.getvalue()
    except Exception:
        return b""

def play_audio_button(text: str, key_id: str, label: str = "🔊 ฟังเสียง (ขยาย 2.5x)"):
    audio_bytes = get_tts_bytes(text)
    if not audio_bytes:
        st.caption("⚠️ ไม่สามารถสร้างเสียงได้")
        return
    
    b64_audio = base64.b64encode(audio_bytes).decode("utf-8")
    html_code = f"""
    <div style="margin: 3px 0;">
        <button id="btn_{key_id}" onclick="playAudio_{key_id}()" style="
            background: #2563EB;
            color: #FFFFFF;
            border: none;
            padding: 6px 10px;
            font-size: 11px;
            font-weight: 600;
            border-radius: 6px;
            cursor: pointer;
            box-shadow: 0 1px 3px rgba(0,0,0,0.15);
            transition: all 0.2s ease;
        ">
            <span id="txt_{key_id}">{label}</span>
        </button>
        <audio id="aud_{key_id}" src="data:audio/mp3;base64,{b64_audio}"></audio>
    </div>
    <script>
    let ctx_{key_id} = null;
    let src_{key_id} = null;
    let gain_{key_id} = null;

    function playAudio_{key_id}() {{
        const audio = document.getElementById('aud_{key_id}');
        const btn = document.getElementById('btn_{key_id}');
        const txt = document.getElementById('txt_{key_id}');
        
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!ctx_{key_id}) {{
            ctx_{key_id} = new AudioCtx();
            src_{key_id} = ctx_{key_id}.createMediaElementSource(audio);
            gain_{key_id} = ctx_{key_id}.createGain();
            gain_{key_id}.gain.value = 2.5;
            src_{key_id}.connect(gain_{key_id});
            gain_{key_id}.connect(ctx_{key_id}.destination);
        }}

        if (ctx_{key_id}.state === 'suspended') ctx_{key_id}.resume();

        if (audio.paused) {{
            audio.currentTime = 0;
            audio.play();
            btn.style.background = '#16A34A';
            txt.innerText = '▶️ กำลังเล่น...';
        }} else {{
            audio.pause();
            audio.currentTime = 0;
            btn.style.background = '#2563EB';
            txt.innerText = '{label}';
        }}

        audio.onended = function() {{
            btn.style.background = '#2563EB';
            txt.innerText = '{label}';
        }};
    }}
    </script>
    """
    components.html(html_code, height=40)

# -----------------------------------------------------------------------------
# 4. Helper Builders & Hybrid Data Loader
# -----------------------------------------------------------------------------
def make_vocab(data_list):
    return [{"word": w, "phonetic": p, "part_of_speech": pos, "meaning": m, "example": ex, "example_th": eth} for w, p, pos, m, ex, eth in data_list]

def make_phrases(data_list):
    return [{"en": en, "th": th, "tip": tip} for en, th, tip in data_list]

def make_dialogues(data_list):
    return [{"title": title, "lines": [{"speaker": spk, "en": en, "th": th} for spk, en, th in lines]} for title, lines in data_list]

def make_exercises(data_list):
    return [{"thai_prompt": tp, "prefix": pre, "suffix": suf, "hint": h, "correct_word": cw, "acceptable_answers": [cw.lower()] + extra, "full_sentence": fs, "explanation": exp} for tp, pre, suf, h, cw, extra, fs, exp in data_list]

def make_stories(data_list):
    return [{"title": t, "image_url": img, "vocab_list": [{"word": w, "pos": p, "th": th} for w, p, th in voc], "story_en": sen, "story_en_plain": splain, "story_th": sth} for t, img, voc, sen, splain, sth in data_list]

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
PROGRESS_FILE = os.path.join(DATA_DIR, "user_progress.json")
LESSONS_FILE = os.path.join(DATA_DIR, "lessons.json")

def load_progress() -> dict:
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"completed_days": []}
    return {"completed_days": []}

def save_progress(data: dict):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_curriculum():
    curriculum = {}
    if os.path.exists(LESSONS_FILE):
        try:
            with open(LESSONS_FILE, "r", encoding="utf-8") as f:
                curriculum = json.load(f)
        except Exception:
            pass
    return curriculum

if "user_data" not in st.session_state:
    st.session_state.user_data = load_progress()

completed_days = set(st.session_state.user_data.get("completed_days", []))

# -----------------------------------------------------------------------------
# 5. AI Writing Coach (Gemini 3.6 Flash)
# -----------------------------------------------------------------------------
def analyze_with_ai(text_to_check: str, api_key: str) -> str:
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        prompt = f"""
        คุณคือผู้เชี่ยวชาญการสอนภาษาอังกฤษเพื่อการสื่อสารในการทำงาน กรุณาตรวจประโยคด้านล่างนี้:
        "{text_to_check}"
        
        ตอบกลับเป็นภาษาไทยที่กระชับ:
        1. 🎯 คะแนน (Score 1-10)
        2. ✨ เวอร์ชันที่ถูกต้องและเป็นมืออาชีพ (Professional Version)
        3. 🔍 วิเคราะห์จุดที่ควรปรับปรุง (Grammar & Nuances)
        4. 💡 วลีหรือสำนวนทางเลือก (Alternative Phrases)
        """
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )
        return response.text
    except Exception as err:
        return f"⚠️ ไม่สามารถเชื่อมต่อกับ AI ได้: {str(err)}"

# -----------------------------------------------------------------------------
# 6. Sidebar Navigation
# -----------------------------------------------------------------------------
curriculum = load_curriculum()

with st.sidebar:
    st.title("⚡ English Sprint")
    st.caption("หลักสูตรเข้มข้น พูดได้เขียนเป็นใน 30 วัน")
    
    total_days = 30
    done_count = len(completed_days)
    percent = done_count / total_days
    
    st.subheader("📊 ความคืบหน้าภาพรวม")
    st.progress(percent)
    st.write(f"**สำเร็จแล้ว {done_count} จาก {total_days} วัน** ({int(percent * 100)}%)")
    
    st.divider()
    
    selected_day = st.selectbox(
        "เลือกบทเรียนประจำวัน:",
        list(range(1, 31)),
        format_func=lambda d: f"Day {d} {'✅' if d in completed_days else '⏳'}"
    )
    
    is_done = selected_day in completed_days
    check_day = st.checkbox("ทำเครื่องหมายว่าเรียนจบวันนี้แล้ว", value=is_done, key=f"chk_{selected_day}")
    
    if check_day != is_done:
        if check_day:
            completed_days.add(selected_day)
        else:
            completed_days.discard(selected_day)
        st.session_state.user_data["completed_days"] = sorted(list(completed_days))
        save_progress(st.session_state.user_data)
        st.rerun()
        
    st.divider()
    st.subheader("🔑 ตั้งค่า Gemini AI")
    env_api_key = st.secrets.get("GEMINI_API_KEY", "") if "GEMINI_API_KEY" in st.secrets else ""
    user_api_key = st.text_input(
        "Gemini API Key:",
        value=env_api_key,
        type="password",
        placeholder="AIzaSy...",
        help="ใช้สำหรับตรวจไวยากรณ์ในแท็บ AI Coach"
    )

# -----------------------------------------------------------------------------
# 7. Main Learning Dashboard & Phonics Tab
# -----------------------------------------------------------------------------
day_key = str(selected_day)
lesson = curriculum.get(day_key)

if not lesson:
    st.title(f"Day {selected_day}: กำลังจัดเตรียมเนื้อหา")
    st.info("กำลังอัปเดตข้อมูลบทเรียนของวันนี้เข้าระบบ")
else:
    st.title(lesson["title"])
    st.markdown(f"🎯 **เป้าหมายประจำวัน:** {lesson['summary']}")
    st.info(f"💡 **หลักการสำคัญ (Core Framework):** {lesson['rule']}")

    tabs = st.tabs([
        "📖 คำศัพท์ & สำนวน (20 คำ)",
        "🗣️ คลังประโยคฝึกพูด (20 ข้อ)",
        "🎭 บทสนทนาจำลอง (10 ฉาก)",
        "✏️ แบบฝึกหัดเติมคำ (10 ข้อ)",
        "📚 ฝึกอ่านเรื่องสั้นภาพประกอบ (4 เรื่อง)",
        "🔤 เทียบเสียงโฟนิกส์ & พยัญชนะ",
        "🤖 AI Writing Coach"
    ])

    # TAB 1: Vocabulary
    with tabs[0]:
        st.subheader("คลังคำศัพท์และสำนวนสำคัญประจำวัน (20 รายการ)")
        vocab_list = lesson.get("vocab", [])
        if vocab_list:
            cols = st.columns(2)
            for idx, v in enumerate(vocab_list):
                with cols[idx % 2]:
                    with st.container(border=True):
                        c_text, c_audio = st.columns([3, 2])
                        with c_text:
                            st.markdown(f"#### {idx+1}. {v['word']}")
                            st.caption(f"🔊 {v.get('phonetic', '')} | *{v.get('part_of_speech', '')}*")
                            st.write(f"🇹🇭 **แปล:** {v['meaning']}")
                        with c_audio:
                            play_audio_button(v['word'], f"voc_{selected_day}_{idx}", "🔊 เสียงคำศัพท์")
                        st.markdown(f"💬 **ตัวอย่าง:** *\"{v['example']}\"*")
                        st.caption(f"👉 {v['example_th']}")
        else:
            st.write("ไม่มีข้อมูลคำศัพท์")

    # TAB 2: Speaking Phrases
    with tabs[1]:
        st.subheader("คลังประโยคฝึกพูดสื่อสารจริง (20 ประโยค)")
        phrases = lesson.get("phrases", [])
        for idx, item in enumerate(phrases):
            with st.container(border=True):
                col_txt, col_snd = st.columns([3, 1])
                with col_txt:
                    st.markdown(f"### {idx+1}. {item['en']}")
                    st.write(f"🇹🇭 **คำแปล:** {item['th']}")
                    st.caption(f"💡 **เทคนิคการพูด:** {item['tip']}")
                with col_snd:
                    play_audio_button(item["en"], f"spk_{selected_day}_{idx}", "🔊 กดฟังเสียงชัดเจน")

    # TAB 3: Dialogues
    with tabs[2]:
        st.subheader("บทสนทนาจำลองสถานการณ์การทำงานจริง (10 ฉากสนทนา)")
        dialogues = lesson.get("dialogues", [])
        if dialogues:
            for s_idx, scene in enumerate(dialogues):
                with st.expander(f"📍 ฉากที่ {s_idx+1}: {scene['title']}", expanded=(s_idx == 0)):
                    for line_idx, line in enumerate(scene["lines"]):
                        c_avatar, c_content, c_voice = st.columns([1, 4, 2])
                        with c_avatar:
                            st.markdown(f"**👤 {line['speaker']}**")
                        with c_content:
                            st.markdown(f"**{line['en']}**")
                            st.caption(f"🇹🇭 {line['th']}")
                        with c_voice:
                            play_audio_button(line['en'], f"dlg_{selected_day}_{s_idx}_{line_idx}", "🔊 เสียงบทพูด")
        else:
            st.write("ไม่มีบทสนทนาสำหรับวันนี้")

    # TAB 4: Exercises
    with tabs[3]:
        st.subheader("ชุดแบบฝึกหัดเติมคำในประโยค (10 ข้อ)")
        exercises = lesson.get("exercises", [])
        if exercises:
            for q_idx, ex in enumerate(exercises):
                with st.container(border=True):
                    st.markdown(f"#### ข้อที่ {q_idx+1}: {ex['thai_prompt']}")
                    st.markdown(f"**ประโยค:** `{ex['prefix']}` &nbsp; [ &nbsp; _____ &nbsp; ] &nbsp; `{ex['suffix']}`")
                    st.caption(f"💡 **คำใบ้:** {ex['hint']}")
                    user_ans = st.text_input("พิมพ์คำตอบ:", key=f"ex_input_{selected_day}_{q_idx}", placeholder="พิมพ์คำตอบภาษาอังกฤษที่นี่...")
                    
                    if st.button(f"ตรวจคำตอบข้อ {q_idx+1} 🚀", key=f"btn_ex_{selected_day}_{q_idx}"):
                        cleaned = user_ans.strip().lower()
                        acceptable = [a.lower() for a in ex["acceptable_answers"]]
                        if cleaned in acceptable:
                            st.success(f"🎉 **ถูกต้อง!** คำตอบคือ: `{ex['correct_word']}`")
                            st.markdown(f"💬 **ประโยคที่สมบูรณ์:** **{ex['full_sentence']}**")
                            st.info(f"📖 **คำอธิบายไวยากรณ์:** {ex['explanation']}")
                            play_audio_button(ex["full_sentence"], f"snd_ex_ok_{selected_day}_{q_idx}", "🔊 ฟังประโยคที่ถูกต้อง")
                        else:
                            st.error(f"❌ **ยังไม่ถูกต้อง** (เฉลยคือ: `{ex['correct_word']}`)")
                            st.markdown(f"💬 **ประโยคที่ถูกต้อง:** **{ex['full_sentence']}**")
                            st.caption(f"📖 {ex['explanation']}")
                            play_audio_button(ex["full_sentence"], f"snd_ex_err_{selected_day}_{q_idx}", "🔊 ฟังประโยคเฉลย")
        else:
            st.write("ไม่มีแบบฝึกหัดสำหรับวันนี้")

    # TAB 5: Short Stories
    with tabs[4]:
        st.subheader("📚 ฝึกอ่านเรื่องสั้น ไม่เก่งก็อ่านได้ (วันละ 4 เรื่อง)")
        st.caption("อ่านเรื่องสั้นเพลินๆ พร้อมภาพประกอบ กล่องคำศัพท์ และคำแปลไทย")
        stories = lesson.get("stories", [])
        if stories:
            for st_idx, item in enumerate(stories):
                with st.container(border=True):
                    st.markdown(f"## เรื่องที่ {st_idx+1}: {item['title']}")
                    if item.get("image_url"):
                        st.image(item["image_url"], use_container_width=True, caption=f"ภาพประกอบ: {item['title']}")
                    st.divider()
                    col_vocab, col_story = st.columns([1, 2])
                    with col_vocab:
                        st.markdown("### 📌 คำศัพท์น่ารู้")
                        for w in item.get("vocab_list", []):
                            st.markdown(f"• **{w['word']}** *({w['pos']})*\n  = {w['th']}")
                    with col_story:
                        st.markdown(f"### 📖 {item['title']}")
                        st.markdown(f"<div style='font-size: 16px; line-height: 1.7;'>{item['story_en']}</div>", unsafe_allow_html=True)
                        play_audio_button(item['story_en_plain'], f"story_audio_{selected_day}_{st_idx}", "🔊 กดฟังเสียงเรื่องสั้นทั้งเรื่อง")
                        st.markdown("<hr style='border: 1px dashed #CBD5E1;'>", unsafe_allow_html=True)
                        st.markdown("#### 🇹🇭 คำแปลภาษาไทย:")
                        st.write(item["story_th"])
        else:
            st.write("ไม่มีเรื่องสั้นสำหรับวันนี้")

    # TAB 6: Phonics & Pronunciation Handbook (ถอดแบบจากรูปภาพ 100%)
    with tabs[5]:
        st.subheader("🔤 เทียบเสียงกลุ่มเสียงพยัญชนะภาษาอังกฤษ-ไทย (Phonics Guide)")
        st.caption("คู่มือฝึกออกเสียงโฟนิกส์: เสียงต้น เสียงควบ เสียงท้าย และตัวอักษรไม่ออกเสียง พร้อมตัวอย่างและปุ่มกดฟังสำเนียงเจ้าของภาษา")
        
        selected_cat = st.radio(
            "เลือกกลุ่มเสียงที่ต้องการฝึกออกเสียง:",
            list(PHONICS_CATEGORIES.keys()),
            horizontal=True
        )
        
        items = PHONICS_CATEGORIES[selected_cat]
        cols = st.columns(3)
        for i, item in enumerate(items):
            with cols[i % 3]:
                with st.container(border=True):
                    c_letter, c_btn = st.columns([2, 2])
                    with c_letter:
                        st.markdown(f"### `{item['letter']}`")
                        st.markdown(f"🇹🇭 **อ่านว่า:** `{item['thai']}`")
                        st.caption(f"ตัวอย่างคำ: **{item['word']}**")
                    with c_btn:
                        play_audio_button(item["sound"], f"ph_{selected_cat[:2]}_{i}", "🔊 ฟังเสียง")

    # TAB 7: AI Writing Coach
    with tabs[6]:
        st.subheader("🤖 ให้ AI ตรวจประโยคและข้อความของคุณ")
        draft = st.text_area("ข้อความของคุณ (ภาษาอังกฤษ):", placeholder="เช่น: I am working on daily report and I will update inventory tomorrow.", height=120)
        
        if st.button("ส่งตรวจกับ AI (Analyze) 🔍", type="primary"):
            key_to_use = user_api_key.strip()
            if not key_to_use:
                st.warning("⚠️ กรุณากรอก Gemini API Key ที่แถบด้านซ้ายก่อนใช้งาน")
            elif not draft.strip():
                st.warning("กรุณาพิมพ์ข้อความภาษาอังกฤษก่อนส่งตรวจ")
            else:
                with st.spinner("AI กำลังวิเคราะห์ไวยากรณ์และความเป็นมืออาชีพ..."):
                    res = analyze_with_ai(draft, key_to_use)
                    st.markdown(res)
