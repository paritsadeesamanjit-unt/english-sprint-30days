import streamlit as st
import streamlit.components.v1 as components
from gtts import gTTS
import io
import json
import os
import base64

# -----------------------------------------------------------------------------
# 1. Page Configuration & Setup
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="English Sprint 30 Days",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

PROGRESS_FILE = "data/user_progress.json"
LESSONS_FILE = "data/lessons.json"

# -----------------------------------------------------------------------------
# 2. Persistence & Progress Tracker
# -----------------------------------------------------------------------------
def load_progress() -> dict:
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"completed_days": [], "scores": {}}
    return {"completed_days": [], "scores": {}}

def save_progress(progress_data: dict):
    os.makedirs("data", exist_ok=True)
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress_data, f, ensure_ascii=False, indent=2)

if "user_data" not in st.session_state:
    st.session_state.user_data = load_progress()

completed_days = set(st.session_state.user_data.get("completed_days", []))

# -----------------------------------------------------------------------------
# 3. Audio Booster Engine (Web Audio API 2.5x GainNode)
# -----------------------------------------------------------------------------
@st.cache_data
def load_curriculum():
    if not os.path.exists(LESSONS_FILE):
        return {}
    with open(LESSONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data(show_spinner=False)
def get_tts_bytes(text: str) -> bytes:
    try:
        tts = gTTS(text=text, lang="en")
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        return buf.getvalue()
    except Exception:
        return b""

def play_audio_button(text: str, key_id: str, label: str = "🔊 ฟังเสียง (ชัด 2.5x)"):
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
            padding: 7px 12px;
            font-size: 12px;
            font-weight: 600;
            border-radius: 6px;
            cursor: pointer;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
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
    components.html(html_code, height=44)

# -----------------------------------------------------------------------------
# 4. AI Feedback Engine (Gemini 3.6 Flash)
# -----------------------------------------------------------------------------
def analyze_with_ai(text_to_check: str, api_key: str) -> str:
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        prompt = f"""
        คุณคือโค้ชสอนภาษาอังกฤษธุรกิจและการสื่อสารในโรงงาน/ออฟฟิศระดับสากล วิเคราะห์ข้อความนี้:
        "{text_to_check}"
        
        ตอบเป็นภาษาไทยแบบกระชับ:
        1. 🎯 **คะแนน (Score 1-10)**: ด้านความถูกต้องและความเป็นธรรมชาติ
        2. ✨ **ประโยคที่ถูกต้องและเป็นมืออาชีพ (Professional Version)**
        3. 🔍 **วิเคราะห์จุดผิด (Grammar & Nuances)**: สรุปเป็นข้อๆ ชัดเจน
        4. 💡 **สำนวน/วลีทางเลือก (Alternatives)**
        """
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )
        return response.text
    except Exception as err:
        return f"⚠️ ไม่สามารถเชื่อมต่อกับ AI ได้: {str(err)}"

# -----------------------------------------------------------------------------
# 5. Sidebar Navigation & Roadmap
# -----------------------------------------------------------------------------
curriculum = load_curriculum()

with st.sidebar:
    st.title("⚡ English Sprint")
    st.caption("หลักสูตรสื่อสารเข้มข้น พูดได้เขียนเป็นใน 30 วัน")
    
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
    check_day = st.checkbox("ทำเครื่องหมายว่าเรียนจบวันนี้แล้ว", value=is_done, key=f"chk_finish_{selected_day}")
    
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
        help="ใช้สำหรับตรวจแก้แกรมม่าในแท็บ AI Coach"
    )

# -----------------------------------------------------------------------------
# 6. Main Learning Dashboard
# -----------------------------------------------------------------------------
day_key = str(selected_day)
lesson = curriculum.get(day_key)

if not lesson:
    st.title(f"Day {selected_day}: กำลังประมวลผลข้อมูล")
    st.info("กรุณาตรวจสอบว่าได้บันทึกไฟล์ `data/lessons.json` เรียบร้อยแล้ว")
else:
    st.title(lesson["title"])
    st.markdown(f"🎯 **เป้าหมายประจำวัน:** {lesson['summary']}")
    st.info(f"💡 **หลักการสำคัญ (Core Framework):** {lesson['rule']}")

    tabs = st.tabs([
        "📖 คำศัพท์ & สำนวนหลัก",
        "🗣️ คลังประโยคฝึกพูด (10 ข้อ)",
        "🎭 บทสนทนาจำลองหน้างาน",
        "✏️ ชุดแบบฝึกหัดเติมคำ",
        "✉️ ตัวช่วยร่างอีเมล",
        "🤖 AI Writing Coach"
    ])

    # ---------------------------------------------------------
    # TAB 1: คำศัพท์และสำนวนหลัก (Vocabulary & Collocations)
    # ---------------------------------------------------------
    with tabs[0]:
        st.subheader("คลังคำศัพท์และ Collocations ประจำวัน")
        st.caption("จำคำศัพท์พร้อมวลีที่มักใช้คู่กันเพื่อนำไปแต่งประโยคได้อย่างเป็นธรรมชาติ")
        
        vocab_list = lesson.get("vocab", [])
        if vocab_list:
            cols = st.columns(2)
            for idx, v in enumerate(vocab_list):
                with cols[idx % 2]:
                    with st.container(border=True):
                        c_w, c_btn = st.columns([3, 2])
                        with c_w:
                            st.markdown(f"#### {v['word']}")
                            st.caption(f"🔊 {v['phonetic']} | *{v['part_of_speech']}*")
                            st.write(f"🇹🇭 **แปล:** {v['meaning']}")
                        with c_btn:
                            play_audio_button(v['word'], f"voc_{selected_day}_{idx}", "🔊 ออกเสียง")
                        
                        st.markdown(f"💬 **ตัวอย่าง:** *\"{v['example']}\"*")
                        st.caption(f"👉 {v['example_th']}")
        else:
            st.write("ไม่มีข้อมูลคำศัพท์สำหรับวันนี้")

    # ---------------------------------------------------------
    # TAB 2: คลังประโยคฝึกพูด (Speaking Patterns Drill)
    # ---------------------------------------------------------
    with tabs[1]:
        st.subheader("คลังประโยคฝึกพูดและออกเสียงจริง (Speaking Patterns)")
        st.caption("ฝึกออกเสียงตามจังหวะและคำแนะนำสัทศาสตร์ (Phonetic Tips) อย่างน้อย 3 ครั้งต่อประโยค")
        
        phrases = lesson.get("phrases", [])
        for idx, item in enumerate(phrases):
            with st.container(border=True):
                col_info, col_audio = st.columns([3, 1])
                with col_info:
                    st.markdown(f"### {idx+1}. {item['en']}")
                    st.write(f"🇹🇭 **คำแปล:** {item['th']}")
                    st.caption(f"💡 **เทคนิคการพูด:** {item['tip']}")
                with col_audio:
                    play_audio_button(item["en"], f"spk_{selected_day}_{idx}", "🔊 กดฟังเสียงชัดเจน")

    # ---------------------------------------------------------
    # TAB 3: บทสนทนาจำลองหน้างาน (Workplace Dialogue Simulation)
    # ---------------------------------------------------------
    with tabs[2]:
        st.subheader("บทสนทนาจำลองสถานการณ์การทำงานจริง (Workplace Dialogue)")
        dialogue = lesson.get("dialogue", [])
        if dialogue:
            for d_idx, turn in enumerate(dialogue):
                with st.container(border=True):
                    col_spk, col_line, col_snd = st.columns([1, 4, 2])
                    with col_spk:
                        st.markdown(f"**👤 {turn['speaker']}**")
                    with col_line:
                        st.markdown(f"**{turn['en']}**")
                        st.caption(f"🇹🇭 {turn['th']}")
                    with col_snd:
                        play_audio_button(turn['en'], f"dlg_{selected_day}_{d_idx}", "🔊 เสียงบทพูด")
        else:
            st.write("ไม่มีบทสนทนาจำลองสำหรับวันนี้")

    # ---------------------------------------------------------
    # TAB 4: ชุดแบบฝึกหัดเติมคำหลายข้อ (Multi-Question Fill-in-the-Blank)
    # ---------------------------------------------------------
    with tabs[3]:
        st.subheader("ชุดแบบฝึกหัดทดสอบความเข้าใจประจำวัน (Daily Quiz Set)")
        st.caption("พิมพ์คำตอบภาษาอังกฤษลงในช่องว่าง แล้วกดตรวจคำตอบทีละข้อ")
        
        exercises = lesson.get("exercises", [])
        if exercises:
            for q_idx, ex in enumerate(exercises):
                with st.container(border=True):
                    st.markdown(f"#### ข้อที่ {q_idx+1}: {ex['thai_prompt']}")
                    st.markdown(f"**ประโยค:** `{ex['prefix']}` &nbsp; [ &nbsp; _____ &nbsp; ] &nbsp; `{ex['suffix']}`")
                    st.caption(f"💡 **คำใบ้:** {ex['hint']}")
                    
                    user_ans = st.text_input(
                        "พิมพ์คำตอบ:", 
                        key=f"ex_input_{selected_day}_{q_idx}", 
                        placeholder="พิมพ์คำตอบภาษาอังกฤษที่นี่..."
                    )
                    
                    if st.button(f"ตรวจคำตอบข้อ {q_idx+1} 🚀", key=f"btn_ex_{selected_day}_{q_idx}"):
                        cleaned = user_ans.strip().lower()
                        acceptable = [a.lower() for a in ex["acceptable_answers"]]
                        
                        if cleaned in acceptable:
                            st.success(f"🎉 **ถูกต้อง!** คำตอบคือ: `{ex['correct_word']}`")
                            st.markdown(f"💬 **ประโยคที่สมบูรณ์:** **{ex['full_sentence']}**")
                            st.info(f"📖 **คำอธิบายไวยากรณ์:** {ex['explanation']}")
                            play_audio_button(ex["full_sentence"], f"ex_snd_ok_{selected_day}_{q_idx}", "🔊 ฟังประโยคที่ถูกต้อง")
                        else:
                            st.error(f"❌ **ยังไม่ถูกต้อง** (เฉลยคือ: `{ex['correct_word']}`)")
                            st.markdown(f"💬 **ประโยคที่ถูกต้อง:** **{ex['full_sentence']}**")
                            st.caption(f"📖 {ex['explanation']}")
                            play_audio_button(ex["full_sentence"], f"ex_snd_err_{selected_day}_{q_idx}", "🔊 ฟังประโยคเฉลย")
        else:
            st.write("ไม่มีแบบฝึกหัดสำหรับวันนี้")

    # ---------------------------------------------------------
    # TAB 5: ตัวช่วยร่างอีเมล (Email & Sentence Builder)
    # ---------------------------------------------------------
    with tabs[4]:
        st.subheader("ประกอบร่างอีเมลและเอกสารสำหรับทำงานจริง")
        email = lesson.get("email_template")
        if email:
            st.markdown(f"📋 **เทมเพลต:** `{email['name']}`")
            with st.form(key=f"form_mail_{selected_day}"):
                f_values = {}
                for field in email["fields"]:
                    f_values[field] = st.text_input(f"ระบุ {field}:")
                built = st.form_submit_button("ประกอบร่างอีเมล (Generate Email) ✨")
                
            if built:
                filled = email["template"].format(**f_values)
                st.markdown("##### ร่างอีเมลที่พร้อมนำไปใช้งาน:")
                st.code(filled, language="text")
                st.download_button(
                    label="📥 ดาวน์โหลดเป็นไฟล์ข้อความ (.txt)",
                    data=filled,
                    file_name=f"email_day_{selected_day}.txt",
                    mime="text/plain"
                )
        else:
            st.write("ไม่มีเทมเพลตสำหรับวันนี้")

    # ---------------------------------------------------------
    # TAB 6: AI Writing Coach
    # ---------------------------------------------------------
    with tabs[5]:
        st.subheader("🤖 ให้ AI ตรวจประโยคและข้อความของคุณ")
        st.caption("พิมพ์ประโยคที่คุณแต่งเองจากเนื้อหาของวันนี้ เพื่อให้ AI ช่วยเกลาคำและวิเคราะห์ระดับภาษา")
        
        draft = st.text_area(
            "ข้อความของคุณ (ภาษาอังกฤษ):",
            placeholder="เช่น: I am working on daily report and I will update inventory tomorrow.",
            height=120
        )
        
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