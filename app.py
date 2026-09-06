import streamlit as st
import streamlit.components.v1 as components
from gtts import gTTS
import io
import json
import os
import base64
import re

# -----------------------------------------------------------------------------
# 1. การตั้งค่าหน้าจอหลัก (Page Configuration)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="English Sprint 30 Days",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. ฟังก์ชันตัวช่วยสร้างโครงสร้างข้อมูล (Helper Builders)
# -----------------------------------------------------------------------------
def make_vocab(data_list):
    return [
        {"word": w, "phonetic": p, "part_of_speech": pos, "meaning": m, "example": ex, "example_th": eth}
        for w, p, pos, m, ex, eth in data_list
    ]

def make_phrases(data_list):
    return [{"en": en, "th": th, "tip": tip} for en, th, tip in data_list]

def make_dialogues(data_list):
    return [
        {"title": title, "lines": [{"speaker": spk, "en": en, "th": th} for spk, en, th in lines]}
        for title, lines in data_list
    ]

def make_exercises(data_list):
    return [
        {
            "thai_prompt": tp, "prefix": pre, "suffix": suf, "hint": h,
            "correct_word": cw, "acceptable_answers": [cw.lower()] + extra,
            "full_sentence": fs, "explanation": exp
        }
        for tp, pre, suf, h, cw, extra, fs, exp in data_list
    ]

def make_stories(data_list):
    return [
        {
            "title": t, "image_url": img,
            "vocab_list": [{"word": w, "pos": p, "th": th} for w, p, th in voc],
            "story_en": sen, "story_en_plain": splain, "story_th": sth
        }
        for t, img, voc, sen, splain, sth in data_list
    ]

# -----------------------------------------------------------------------------
# 3. ฐานข้อมูลเทียบเสียงโฟนิกส์ถาวร (Phonics Handbook: 7 หมวดหมู่)
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
        {"letter": "v", "thai": "ฟือ (ฟันแตะริมฝีปาก)", "word": "van", "sound": "v, van"},
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
        {"letter": "th", "thai": "ธีอ (แลบลิ้นแตะฟัน)", "word": "think", "sound": "th, think"},
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
        {"letter": "-gh", "thai": "เงียบ / ออกเสียง ฟือ", "word": "light / rough", "sound": "light, rough"}
    ]
}

# -----------------------------------------------------------------------------
# 4. เครื่องเล่นเสียงเร่งพลัง 2.5x (Web Audio API ArrayBuffer + Fallback)
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
        st.caption("⚠️ กำลังสร้างเสียง...")
        return

    # ล้างอักขระพิเศษ จุด วรรค ให้เป็น _ ทั้งหมด ป้องกัน SyntaxError ใน JavaScript
    safe_id = re.sub(r'[^a-zA-Z0-9_]', '_', str(key_id))
    b64_audio = base64.b64encode(audio_bytes).decode("utf-8")

    html_code = f"""
    <div style="margin: 2px 0;">
        <button id="btn_{safe_id}" onclick="playAudio_{safe_id}()" style="
            background: #2563EB;
            color: #FFFFFF;
            border: none;
            padding: 6px 12px;
            font-size: 11px;
            font-weight: 600;
            border-radius: 6px;
            cursor: pointer;
            box-shadow: 0 1px 3px rgba(0,0,0,0.15);
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        ">
            <span id="txt_{safe_id}">{label}</span>
        </button>
    </div>
    <script>
    let isPlaying_{safe_id} = false;

    function playAudio_{safe_id}() {{
        const btn = document.getElementById('btn_{safe_id}');
        const txt = document.getElementById('txt_{safe_id}');
        if (isPlaying_{safe_id}) return;

        isPlaying_{safe_id} = true;
        btn.style.background = '#16A34A';
        txt.innerText = '▶️ กำลังเล่น...';

        try {{
            const AudioCtx = window.AudioContext || window.webkitAudioContext;
            const audioCtx = new AudioCtx();
            if (audioCtx.state === 'suspended') {{
                audioCtx.resume();
            }}

            const binaryString = window.atob('{b64_audio}');
            const len = binaryString.length;
            const bytes = new Uint8Array(len);
            for (let i = 0; i < len; i++) {{
                bytes[i] = binaryString.charCodeAt(i);
            }}

            audioCtx.decodeAudioData(bytes.buffer, function(buffer) {{
                const source = audioCtx.createBufferSource();
                const gainNode = audioCtx.createGain();
                gainNode.gain.value = 2.5; // ขยายความดัง 2.5 เท่า ชัดเจน ไม่แตก
                source.buffer = buffer;
                source.connect(gainNode);
                gainNode.connect(audioCtx.destination);

                source.onended = function() {{
                    isPlaying_{safe_id} = false;
                    btn.style.background = '#2563EB';
                    txt.innerText = '{label}';
                }};

                source.start(0);
            }}, function(err) {{
                fallbackAudio_{safe_id}();
            }});
        }} catch(e) {{
            fallbackAudio_{safe_id}();
        }}
    }}

    function fallbackAudio_{safe_id}() {{
        const btn = document.getElementById('btn_{safe_id}');
        const txt = document.getElementById('txt_{safe_id}');
        const snd = new Audio('data:audio/mp3;base64,{b64_audio}');
        snd.play().then(() => {{
            snd.onended = () => {{
                isPlaying_{safe_id} = false;
                btn.style.background = '#2563EB';
                txt.innerText = '{label}';
            }};
        }}).catch(err => {{
            isPlaying_{safe_id} = false;
            btn.style.background = '#2563EB';
            txt.innerText = '{label}';
        }});
    }}
    </script>
    """
    components.html(html_code, height=38)

# -----------------------------------------------------------------------------
# 5. ฐานข้อมูลสัปดาห์แรกในตัว (Built-in Week 1 Dataset: Days 1 - 7)
# -----------------------------------------------------------------------------
WEEK_1_DATA = {
    "1": {
        "day": 1,
        "title": "Day 1: Sentence Framework (S + V + O) & 3 Core Tenses",
        "summary": "เรียนรู้โครงสร้างประโยค 3 กาลหลักผ่านสถานการณ์: การตรวจนับสต็อกสินค้าและการจัดส่งด่วนประจำวัน",
        "rule": "Present Simple (ทำประจำ) | Present Continuous (กำลังทำขณะนี้) | Future Simple (จะทำในอนาคต)",
        "vocab": make_vocab([
            ("Inventory", "/ˈɪn.vən.tɔːr.i/", "n.", "สินค้าคงคลัง / สต็อกสินค้า", "We check the inventory every morning.", "พวกเราตรวจเช็คสต็อกสินค้าทุกเช้า"),
            ("Discrepancy", "/dɪˈskrep.ən.si/", "n.", "ความคลาดเคลื่อน / ยอดไม่ตรงกัน", "We found a minor discrepancy on Rack 2.", "เราพบความคลาดเคลื่อนเล็กน้อยบนแร็ค 2"),
            ("Inspect", "/ɪnˈspekt/", "v.", "ตรวจสอบ / ตรวจตรา", "Please inspect the cartons carefully.", "โปรดตรวจสอบกล่องสินค้าอย่างละเอียด"),
            ("Verify", "/ˈver.ɪ.faɪ/", "v.", "ทวนสอบความถูกต้อง", "Verify the serial numbers before moving.", "ทวนสอบหมายเลขซีเรียลก่อนทำการเคลื่อนย้าย"),
            ("Barcode", "/ˈbɑː.kəʊd/", "n.", "แถบรหัสบาร์โค้ด", "Scan the barcode on the pallet.", "สแกนบาร์โค้ดที่อยู่บนพาเลท"),
            ("Pallet", "/ˈpæl.ət/", "n.", "พาเลทวางสินค้า", "Stack the boxes neatly on the pallet.", "เรียงกล่องสินค้าให้เรียบร้อยบนพาเลท"),
            ("Forklift", "/ˈfɔːk.lɪft/", "n.", "รถยกโฟล์คลิฟต์", "The forklift operator is moving the rack.", "คนขับรถโฟล์คลิฟต์กำลังยกย้ายแร็ค"),
            ("Storage", "/ˈstɔː.rɪdʒ/", "n.", "การจัดเก็บ / พื้นที่เก็บของ", "Room A1 is our cold storage room.", "ห้อง A1 คือห้องจัดเก็บควบคุมอุณหภูมิ"),
            ("Carton", "/ˈkɑː.tən/", "n.", "กล่องบรรจุภัณฑ์ / ลังกระดาษ", "Two cartons are placed on shelf A.", "กล่องลังสองใบวางอยู่บนชั้น A"),
            ("Label", "/ˈleɪ.bəl/", "n./v.", "ฉลาก / ติดป้ายกำกับ", "Label each box clearly.", "ติดฉลากระบุบนทุกกล่องให้ชัดเจน"),
            ("Urgent", "/ˈɜː.dʒənt/", "adj.", "เร่งด่วน / ฉุกเฉิน", "We received an urgent delivery request.", "พวกเราได้รับคำขอจัดส่งสินค้าแบบเร่งด่วน"),
            ("Expedite", "/ˈek.spə.daɪt/", "v.", "เร่งรัด / ทำให้เร็วขึ้น", "We need to expedite this order.", "เราจำเป็นต้องเร่งรัดคำสั่งซื้อล็อตนี้"),
            ("Loading dock", "/ˈləʊ.dɪŋ dɒk/", "n.", "ชานชาลาโหลดสินค้า", "The delivery truck is at the loading dock.", "รถบรรทุกสินค้าจอดอยู่ที่ชานชาลาโหลดของ"),
            ("Dispatch", "/dɪˈspætʃ/", "v./n.", "ปล่อยรถ / ส่งของออกไป", "We dispatch the goods at 11:30 AM.", "เราปล่อยสินค้าออกไปเวลา 11:30 น."),
            ("Receipt", "/rɪˈsiːt/", "n.", "ใบรับมอบสินค้า", "Please sign the delivery receipt.", "กรุณาเซ็นชื่อในใบรับสินค้า"),
            ("Schedule", "/ˈskedʒ.uːl/", "n./v.", "กำหนดการ / ตารางเวลา", "The truck arrived on schedule.", "รถบรรทุกมาถึงตรงตามกำหนดเวลา"),
            ("Finalize", "/ˈfaɪ.nəl.aɪz/", "v.", "สรุปผล / ทำให้เสร็จสมบูรณ์", "I will finalize the daily report.", "ผมจะสรุปรายงานประจำวันให้เสร็จ"),
            ("Quarantine", "/ˈkwɒr.ən.tiːn/", "n./v.", "พื้นที่กักแยก / กักของรอตรวจ", "Place the dented box in quarantine.", "นำกล่องที่บุบไปไว้ในพื้นที่กักแยก"),
            ("Defect", "/ˈdiː.fekt/", "n.", "ตำหนิ / ข้อบกพร่อง", "Check if there is any surface defect.", "ตรวจดูว่ามีตำหนิบนพื้นผิวหรือไม่"),
            ("Handover", "/ˈhændˌəʊ.vər/", "n.", "การส่งมอบงาน", "Complete the handover before noon.", "ส่งมอบงานให้เสร็จก่อนเที่ยงตรง")
        ]),
        "phrases": make_phrases([
            ("The team usually reviews the inventory every morning.", "ทีมงานมักจะตรวจสอบสต็อกสินค้าทุกเช้า (ทำเป็นประจำ)", "Present Simple: กิจวัตรประจำวัน"),
            ("I am counting the cartons in Room A1 right now.", "ฉันกำลังนับจำนวนกล่องในห้อง A1 อยู่ ณ ตอนนี้", "Present Continuous: S + am + V.ing"),
            ("We noticed a minor discrepancy on Rack 2 yesterday.", "พวกเราสังเกตเห็นยอดไม่ตรงกันเล็กน้อยบนแร็ค 2 เมื่อวานนี้", "Past Simple: noticed กริยาช่อง 2 จบไปแล้ว"),
            ("The inspector usually verifies every single barcode.", "ผู้ตรวจสอบมักจะทวนสอบบาร์โค้ดทุกแผ่นเป็นประจำ", "verifies เปลี่ยน y เป็น ies ตามประธานเอกพจน์"),
            ("He is operating the forklift to move the pallets.", "เขากำลังขับรถโฟล์คลิฟต์เพื่อย้ายพาเลทสินค้า", "is operating กำลังทำอยู่"),
            ("I will print out the updated shipping labels.", "ฉันจะสั่งพิมพ์ฉลากจัดส่งฉบับใหม่ออกมา", "Future Simple: will + กริยาช่อง 1"),
            ("We received an urgent delivery request from customer service.", "เราได้รับคำขอส่งสินค้าด่วนมาจากแผนกบริการลูกค้า", "received ลงท้ายเสียง /d/"),
            ("The warehouse staff are expediting the packing process.", "พนักงานคลังสินค้ากำลังเร่งรัดขั้นตอนการแพ็คของ", "are expediting ใช้กับพหูพจน์"),
            ("We must isolate the defective carton in the quarantine zone.", "พวกเราต้องแยกกล่องที่มีตำหนิไปไว้ในโซนกักแยก", "isolate แปลว่า คัดแยกเดี่ยว"),
            ("The transport truck arrived at the loading dock on schedule.", "รถบรรทุกสินค้ามาถึงชานชาลาโหลดของตรงตามเวลา", "on schedule = ตรงเวลา"),
            ("The driver is signing the physical delivery receipt.", "คนขับรถกำลังลงลายมือชื่อในใบรับสินค้า", "receipt ไม่ออกเสียงตัว p (/rɪˈsiːt/)"),
            ("We dispatched the urgent consignment at 11:30 AM.", "พวกเราปล่อยล็อตสินค้าด่วนออกไปเมื่อเวลา 11:30 น.", "dispatched ลงท้ายเสียง /t/"),
            ("I am entering the serial numbers into the Excel system.", "ฉันกำลังพิมพ์หมายเลขซีเรียลลงในระบบตาราง Excel", "am entering กำลังพิมพ์อยู่"),
            ("Did you inspect the outer packaging of the boxes?", "คุณได้ตรวจสภาพบรรจุภัณฑ์ภายนอกของกล่องแล้วหรือยัง", "Did you + V.1 ถามอดีต"),
            ("Everything is running smoothly according to the daily schedule.", "ทุกอย่างกำลังดำเนินไปอย่างราบรื่นตามตารางประจำวัน", "running smoothly = ราบรื่น"),
            ("I will let you know as soon as the truck departs.", "ฉันจะแจ้งให้คุณทราบทันทีที่รถบรรทุกออกเดินทาง", "as soon as พูดเชื่อมเสียงเร็ว"),
            ("The morning shift finished all assigned picking tasks.", "กะเช้าได้ทำงานหยิบของที่ได้รับมอบหมายเสร็จสิ้นทั้งหมดแล้ว", "finished ออกเสียงท้าย /t/"),
            ("We will finalize the daily attendance and stock report before noon.", "พวกเราจะสรุปรายงานการเข้างานและสต็อกให้เสร็จก่อนเที่ยง", "will finalize บอกเป้าหมาย"),
            ("The shift leader is conducting the handover right now.", "หัวหน้ากะกำลังดำเนินการส่งมอบงานอยู่ ณ ตอนนี้", "is conducting = กำลังดำเนินการ"),
            ("We achieved zero shipping errors for this morning batch.", "พวกเราทำสถิติข้อผิดพลาดการส่งของเป็นศูนย์สำหรับล็อตเช้านี้", "achieved zero errors")
        ]),
        "dialogues": make_dialogues([
            ("08:00 น. เริ่มตรวจนับสต็อกเช้า", [("Supervisor", "Are you ready to inspect Room A1 inventory?", "พร้อมที่จะเข้าตรวจสอบสต็อกในห้อง A1 หรือยัง"), ("Staff", "Yes, I am heading inside with the scanner right now.", "พร้อมแล้วครับ ตอนนี้ผมกำลังถือเครื่องสแกนเดินเข้าไปครับ")]),
            ("08:30 น. พบความคลาดเคลื่อนบนแร็ค 2", [("Staff", "Supervisor, I found a discrepancy of two cartons on Rack 2.", "หัวหน้าครับ ผมพบยอดไม่ตรงกัน ขาดไป 2 กล่องบนแร็ค 2 ครับ"), ("Supervisor", "Check shelf B to verify if someone misplaced them.", "ลองไปตรวจดูที่ชั้น B ซิว่ามีใครวางสลับตำแหน่งไว้หรือไม่")]),
            ("09:00 น. แก้ไขการวางสลับตำแหน่ง", [("Staff", "You were right. The two cartons were placed behind Rack 3.", "จริงด้วยครับ กล่องสองใบนั้นถูกวางหลบอยู่หลังแร็ค 3 ครับ"), ("Supervisor", "Great catch. Scan the barcode and update the shelf tag.", "ตาไวมาก สแกนบาร์โค้ดแล้วอัปเดตป้ายบอกชั้นวางให้ถูกต้องนะ")]),
            ("09:30 น. ประสานงานรถยกจัดเรียงพาเลท", [("Staff", "Could you operate the forklift to move this pallet to Bay 1?", "ช่วยขับรถโฟล์คลิฟต์ย้ายพาเลทนี้ไปที่ช่องเบย์ 1 หน่อยได้ไหมครับ"), ("Forklift Driver", "Sure thing. I will move it as soon as the lane clears.", "ได้แน่นอน เดี๋ยวทางเดินโล่งแล้วผมจะรีบยกย้ายไปให้")]),
            ("10:00 น. ออเดอร์ด่วนเข้ามากะทันหัน", [("Customer Service", "We have an urgent order that must leave by 11:30!", "เรามีออเดอร์ด่วนที่ต้องปล่อยรถออกก่อน 11:30 น. ค่ะ!"), ("Staff", "Understood. We are picking the cartons from cold storage now.", "รับทราบครับ ตอนนี้พวกเรากำลังเร่งหยิบกล่องออกจากห้องเย็นครับ")]),
            ("10:30 น. ตรวจพบกล่องมีรอยบุบ", [("Staff", "Wait, one outer carton is badly dented. Should I pack it?", "เดี๋ยวก่อนครับ กล่องด้านนอกมีรอยบุบ ควรแพ็คส่งไปไหมครับ"), ("Supervisor", "No, isolate it in quarantine and pick a flawless carton.", "ไม่ได้เด็ดขาด นำไปกักแยกไว้แล้วไปหยิบกล่องที่สมบูรณ์มาแทน")]),
            ("11:00 น. ติดฉลากจัดส่งรอบด่วน", [("Staff", "I will print the urgent shipping labels right away.", "เดี๋ยวผมจะรีบพิมพ์ป้ายฉลากจัดส่งรอบด่วนออกมาเดี๋ยวนี้ครับ"), ("Supervisor", "Make sure every label is firmly attached to the pallet wrap.", "ตรวจดูให้แน่ใจด้วยนะว่าป้ายทุกแผ่นติดแน่นกับพลาสติกพันพาเลท")]),
            ("11:15 น. รถบรรทุกเทียบชานชาลา", [("Truck Driver", "I am here at the loading dock to pick up the urgent shipment.", "ผมจอดเทียบอยู่ที่ชานชาลาเพื่อมารับของล็อตด่วนแล้วครับ"), ("Staff", "Welcome. We are loading the finished pallets into your truck now.", "ยินดีต้อนรับครับ ตอนนี้พวกเรากำลังยกพาเลทขึ้นตู้รถของคุณครับ")]),
            ("11:30 น. เซ็นเอกสารปล่อยรถตามเวลา", [("Staff", "Everything is loaded. Please sign this delivery receipt.", "ของขึ้นครบแล้วครับ รบกวนเซ็นชื่อในใบรับสินค้าตรงนี้ด้วยครับ"), ("Truck Driver", "Signed! We are leaving on schedule. Thank you for expediting.", "เรียบร้อยครับ! รถออกตรงเวลาพอดี ขอบคุณมากที่ช่วยเร่งงานให้ครับ")]),
            ("11:45 น. สรุปรายงานและส่งมอบงานกะเช้า", [("Staff", "Supervisor, I finalized the dispatch report and updated Drive.", "หัวหน้าครับ ผมสรุปรายงานส่งของและอัปเดตไฟล์ลง Drive เรียบร้อยแล้วครับ"), ("Supervisor", "Outstanding work today. That concludes our morning shift handover.", "ผลงานยอดเยี่ยมมากวันนี้ ถือเป็นการจบการส่งมอบงานกะเช้าได้อย่างสมบูรณ์")])
        ]),
        "exercises": make_exercises([
            ("ฉันกำลังตรวจนับจำนวนกล่องในห้องควบคุมอุณหภูมิ A1 อยู่ในขณะนี้", "I am currently", "the cartons in Storage Room A1.", "กริยา count (นับ) ในรูปกำลังกระทำ (Present Continuous)", "counting", ["inspecting", "checking"], "I am currently counting the cartons in Storage Room A1.", "เหตุการณ์กำลังดำเนินอยู่ ใช้โครงสร้าง S + am + V.ing (counting)"),
            ("พวกเราสังเกตเห็นยอดสต็อกคลาดเคลื่อนบนแร็ค 2 เมื่อเช้านี้", "We noticed a minor stock", "on Rack 2 this morning.", "คำนามแปลว่า ยอดคลาดเคลื่อน/ไม่ตรงกัน (d...)", "discrepancy", [], "We noticed a minor stock discrepancy on Rack 2 this morning.", "'discrepancy' หมายถึง ยอดจำนวนจริงไม่ตรงกับระบบ"),
            ("ผู้ตรวจสอบทวนสอบบาร์โค้ดทุกแผ่นอย่างระมัดระวังเป็นประจำ", "The inspector usually", "every single barcode carefully.", "กริยา verify เปลี่ยนรูปตามประธานเอกพจน์ใน Present Simple", "verifies", ["checks"], "The inspector usually verifies every single barcode carefully.", "กิจวัตรประจำวัน (usually) ประธานเอกพจน์ กริยา verify เปลี่ยน y เป็น ies"),
            ("เขากำลังขับรถโฟล์คลิฟต์เพื่อย้ายพาเลทสินค้า", "He is", "the forklift to move the pallets.", "กริยา operate (ขับ/เดินเครื่อง) ในรูปกำลังกระทำ (V.ing)", "operating", ["driving"], "He is operating the forklift to move the pallets.", "กำลังกระทำอยู่ใช้ is + operating"),
            ("เราจำเป็นต้องเร่งรัดคำสั่งซื้อจัดส่งด่วนของลูกค้ารายนี้", "We need to", "this urgent customer delivery.", "คำกริยาแปลว่า เร่งรัด/ทำให้เร็วขึ้น (e...)", "expedite", ["speed up"], "We need to expedite this urgent customer delivery.", "'expedite' แปลว่า เร่งรัดกระบวนการทำงานให้เร็วขึ้น"),
            ("เราต้องกักแยกกล่องที่มีรอยบุบไว้ในพื้นที่กักกันทันที", "We must isolate the dented carton in the", "zone.", "คำแปลว่า พื้นที่กักกันของเสีย/รอตรวจ (q...)", "quarantine", [], "We must isolate the dented carton in the quarantine zone.", "'quarantine zone' คือพื้นที่กักแยกสินค้าชำรุด"),
            ("รถบรรทุกขนส่งสินค้ามาถึงที่ชานชาลาโหลดของตรงตามเวลา", "The delivery truck arrived at the loading", "on schedule.", "คำแปลว่า ท่าเทียบ/ชานชาลาขนถ่ายสินค้า (d...)", "dock", ["bay"], "The delivery truck arrived at the loading dock on schedule.", "'loading dock' คือชานชาลาเทียบโหลดสินค้า"),
            ("คนขับรถกำลังลงลายมือชื่อในใบรับมอบสินค้า", "The driver is signing the physical delivery", ".", "คำนามแปลว่า ใบรับสินค้า (r... ไม่ออกเสียงตัว p)", "receipt", [], "The driver is signing the physical delivery receipt.", "'delivery receipt' แปลว่า ใบรับมอบสินค้า"),
            ("พวกเราปล่อยรถจัดส่งสินค้าด่วนออกไปเมื่อเวลา 11:30 น.", "We", "the urgent shipment at 11:30 AM.", "กริยา dispatch ในรูปอดีต (Past Simple)", "dispatched", ["sent"], "We dispatched the urgent shipment at 11:30 AM.", "เหตุการณ์จบในอดีต กริยา dispatch เติม -ed"),
            ("ฉันจะสรุปรายงานความคืบหน้าประจำวันให้เสร็จก่อนเที่ยง", "I will", "the daily stock report before noon.", "คำกริยาแปลว่า สรุปผล/ทำให้เสร็จสมบูรณ์ (f...)", "finalize", ["complete"], "I will finalize the daily stock report before noon.", "โครงสร้างบอกอนาคต will + กริยาช่อง 1 (finalize)")
        ]),
        "stories": make_stories([
            ("องก์ที่ 1: การตรวจนับสต็อกห้อง A1 (The 08:00 AM Audit)", "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=900&auto=format&fit=crop&q=80",
             [("inventory", "n.", "สินค้าคงคลัง"), ("inspect", "v.", "ตรวจสอบ"), ("discrepancy", "n.", "ยอดคลาดเคลื่อน"), ("verify", "v.", "ทวนสอบ")],
             "Every morning at 08:00 AM, Dan steps into Temperature Room A1 to check the <b>inventory</b>. Holding his mobile scanner, his task is to <b>inspect</b> sixty storage racks.<br><br>While scanning Rack 2, the screen flashes red. The system registers fifty cartons, but physical counting shows only forty-eight! Dan immediately stops to <b>verify</b> shelf B to solve the unexpected <b>discrepancy</b>.",
             "Every morning at 08:00 AM, Dan steps into Temperature Room A1 to check the inventory. Holding his mobile scanner, his task is to inspect sixty storage racks. While scanning Rack 2, the screen flashes red. The system registers fifty cartons, but physical counting shows only forty-eight! Dan immediately stops to verify shelf B to solve the unexpected discrepancy.",
             "ทุกเช้าเวลา 8 โมงตรง แดนเดินเข้าไปในห้องควบคุมอุณหภูมิ A1 เพื่อตรวจเช็คสต็อกสินค้า มือถือเครื่องสแกนพกพาเพื่อตรวจสอบแร็คจัดเก็บทั้ง 60 จุด ขณะสแกนแร็ค 2 หน้าจอกะพริบเตือนสีแดง ระบบระบุว่ามีกล่องสินค้า 50 ใบ แต่การนับจริงกลับพบเพียง 48 ใบ! แดนรีบหยุดตรวจทานชั้นวาง B ทันทีเพื่อหาสาเหตุของยอดคลาดเคลื่อนนี้"),
            ("องก์ที่ 2: สองกล่องที่วางสลับตำแหน่ง (The Misplaced Cartons)", "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=900&auto=format&fit=crop&q=80",
             [("carton", "n.", "กล่องลัง"), ("barcode", "n.", "รหัสบาร์โค้ด"), ("forklift", "n.", "รถยกโฟล์คลิฟต์"), ("pallet", "n.", "พาเลท")],
             "Dan carefully searches behind Rack 3 and discovers the two missing <b>cartons</b>. A night shift operator had accidentally placed them in the wrong aisle without updating the system tag.<br><br>Dan points his scanner, beeps the <b>barcode</b>, and logs the correct location. He calls the <b>forklift</b> driver to lift the complete <b>pallet</b> back to its assigned space, achieving 100% stock accuracy.",
             "Dan carefully searches behind Rack 3 and discovers the two missing cartons. A night shift operator had accidentally placed them in the wrong aisle without updating the system tag. Dan points his scanner, beeps the barcode, and logs the correct location. He calls the forklift driver to lift the complete pallet back to its assigned space, achieving 100% stock accuracy.",
             "แดนเดินค้นหาอย่างละเอียดจนพบกล่องลังสองใบที่หายไปวางอยู่ด้านหลังแร็ค 3 พนักงานกะดึกเผลอวางสลับช่องทางเดินโดยไม่ได้กดอัปเดตแท็กในระบบ แดนจ่อสแกนเนอร์ ยิงบาร์โค้ดเพื่อบันทึกตำแหน่งที่ถูกต้อง เขาวิทยุเรียกคนขับรถโฟล์คลิฟต์ให้มายกพาเลททั้งชุดกลับเข้าที่เดิม ทำให้ยอดสต็อกกลับมาถูกต้องแม่นยำ 100% เต็ม"),
            ("องก์ที่ 3: คำสั่งจัดส่งด่วนตอน 10 โมงเช้า (The Urgent 10:00 AM Request)", "https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=900&auto=format&fit=crop&q=80",
             [("urgent", "adj.", "เร่งด่วน"), ("expedite", "v.", "เร่งรัด"), ("quarantine", "n.", "พื้นที่กักแยก"), ("defect", "n.", "ตำหนิ")],
             "At 10:00 AM, Customer Service calls with an <b>urgent</b> dispatch request: twenty pallets of electronic components must leave for Ayutthaya before 11:30 AM.<br><br>The warehouse team jumps into action to <b>expedite</b> picking. While loading, Dan spots a carton with a dented corner. Refusing to risk customer trust with a surface <b>defect</b>, he quarantines the damaged box and substitutes a pristine replacement.",
             "At 10:00 AM, Customer Service calls with an urgent dispatch request: twenty pallets of electronic components must leave for Ayutthaya before 11:30 AM. The warehouse team jumps into action to expedite picking. While loading, Dan spots a carton with a dented corner. Refusing to risk customer trust with a surface defect, he quarantines the damaged box and substitutes a pristine replacement.",
             "เวลา 10 โมงเช้า แผนกบริการลูกค้าโทรเข้ามาแจ้งคำขอด่วน: พาเลทชิ้นส่วนอิเล็กทรอนิกส์ 20 ชุดต้องส่งออกไปอยุธยาก่อน 11:30 น. ทีมคลังสินค้าเร่งเครื่องเต็มกำลังเพื่อเร่งรัดการหยิบของ ระหว่างการขนย้าย แดนสังเกตเห็นกล่องหนึ่งมีรอยบุบตรงมุม ด้วยความมุ่งมั่นที่จะไม่ยอมให้มีตำหนิหลุดไปถึงมือลูกค้า เขาจึงนำกล่องนั้นไปไว้ในพื้นที่กักแยกแล้วนำกล่องที่สมบูรณ์แบบมาเปลี่ยนแทนทันที"),
            ("องก์ที่ 4: การปล่อยรถตรงเวลาและการส่งมอบงาน (Dispatch & Handover)", "https://images.unsplash.com/photo-1497215728101-856f4ea42174?w=900&auto=format&fit=crop&q=80",
             [("loading dock", "n.", "ชานชาลาโหลดของ"), ("receipt", "n.", "ใบรับมอบสินค้า"), ("dispatch", "v.", "ปล่อยรถส่งของ"), ("finalize", "v.", "สรุปผลเสร็จสมบูรณ์")],
             "At 11:15 AM, the transport truck reverses into the <b>loading dock</b>. The crew wraps the pallets securely and loads them into the container.<br><br>The driver signs the delivery <b>receipt</b>, and the truck is officially <b>dispatched</b> at 11:30 AM sharp! Dan sits down at his desk to <b>finalize</b> the inventory and attendance logs, completing a flawless morning shift.",
             "At 11:15 AM, the transport truck reverses into the loading dock. The crew wraps the pallets securely and loads them into the container. The driver signs the delivery receipt, and the truck is officially dispatched at 11:30 AM sharp! Dan sits down at his desk to finalize the inventory and attendance logs, completing a flawless morning shift.",
             "เวลา 11:15 น. รถบรรทุกถอยเข้าเทียบชานชาลาโหลดสินค้า ทีมงานพันพลาสติกพาเลทอย่างแน่นหนาแล้วยกขึ้นตู้คอนเทนเนอร์ คนขับลงชื่อในใบรับสินค้า และรถได้ถูกปล่อยตัวออกเดินทางเวลา 11:30 น. ตรงตามเวลาเป๊ะ! แดนกลับมานั่งที่โต๊ะเพื่อสรุปรายงานสต็อกและบันทึกเวลาทำงาน เป็นการปิดกะเช้าได้อย่างสมบูรณ์แบบไร้ที่ติ")
        ])
    }
}

# -----------------------------------------------------------------------------
# 6. สร้างข้อมูลบทเรียน Days 2 ถึง 7 (เชื่อมโยงแบบไม่ซ้ำกันตลอดทั้ง 7 วัน)
# -----------------------------------------------------------------------------
WEEK_THEMES = [
    (2, "Day 2: Polite Requests & Inquiries", "การขอความช่วยเหลือและการประสานงานขอเอกสารจัดส่งอย่างสุภาพ", "Could you please... | Would you mind... | I would appreciate it if...",
     [("Clarify", "/ˈklær.ɪ.faɪ/", "v.", "ชี้แจง / อธิบายให้กระจ่าง", "Could you clarify this delivery schedule?", "ช่วยชี้แจงกำหนดการส่งนี้หน่อยครับ"),
      ("Appreciate", "/əˈpriː.ʃi.eɪt/", "v.", "ซาบซึ้ง / ขอบคุณ", "I would appreciate your quick reply.", "ผมจะขอบคุณมากหากตอบกลับอย่างรวดเร็ว"),
      ("Assistance", "/əˈsɪs.təns/", "n.", "ความช่วยเหลือ", "Thank you for your valuable assistance.", "ขอบคุณสำหรับความช่วยเหลือครับ"),
      ("Prompt", "/prɒmpt/", "adj.", "รวดเร็ว / ทันเวลา", "Thank you for the prompt update.", "ขอบคุณสำหรับการอัปเดตที่รวดเร็ว"),
      ("Convenient", "/kənˈviː.ni.ənt/", "adj.", "สะดวก", "Please call me when it is convenient.", "โทรหาผมเมื่อสะดวกนะครับ"),
      ("Inquire", "/ɪnˈkwaɪər/", "v.", "สอบถามข้อมูล", "I am calling to inquire about Part 402.", "ผมโทรมาสอบถามเกี่ยวกับพาร์ท 402"),
      ("Attachment", "/əˈtætʃ.mənt/", "n.", "ไฟล์แนบ", "The invoice is in the email attachment.", "ใบแจ้งหนี้อยู่ในไฟล์แนบอีเมล"),
      ("Resend", "/ˌriːˈsend/", "v.", "ส่งใหม่อีกครั้ง", "Could you please resend the missing file?", "ช่วยส่งไฟล์ที่ขาดใหม่อีกรอบได้ไหมครับ"),
      ("Regarding", "/rɪˈɡɑː.dɪŋ/", "prep.", "เกี่ยวกับ / ในเรื่องของ", "I have an inquiry regarding Box B12.", "ผมมีข้อสอบถามเกี่ยวกับกล่อง B12"),
      ("Forward", "/ˈfɔː.wəd/", "v.", "ส่งต่อข้อความ/อีเมล", "Please forward this note to Procurement.", "ช่วยส่งต่อข้อความนี้ให้ฝ่ายจัดซื้อด้วย"),
      ("Requirement", "/rɪˈkwaɪə.mənt/", "n.", "ข้อกำหนด", "Does this shipment meet the requirement?", "ล็อตสินค้านี้ตรงตามข้อกำหนดไหม"),
      ("Permission", "/pəˈmɪʃ.ən/", "n.", "การอนุญาต", "You need supervisor permission to enter.", "คุณต้องได้รับอนุญาตจากหัวหน้าก่อนเข้า"),
      ("Feedback", "/ˈfiːd.bæk/", "n.", "ข้อคิดเห็นตอบกลับ", "We welcome customer feedback on packing.", "เรายินดีรับข้อคิดเห็นลูกค้าเรื่องการแพ็ค"),
      ("Colleague", "/ˈkɒl.iːɡ/", "n.", "เพื่อนร่วมงาน", "My colleague will hand over the keys.", "เพื่อนร่วมงานของผมจะส่งมอบกุญแจให้"),
      ("Extend", "/ɪkˈstend/", "v.", "ขยายเวลา", "Can we extend the pickup window?", "เราขอขยายเวลาช่วงเข้ารับของได้ไหม"),
      ("Authorize", "/ˈɔː.θər.aɪz/", "v.", "อนุมัติ / มอบสิทธิ์", "The plant manager authorized overtime.", "ผู้จัดการโรงงานอนุมัติโอทีแล้ว"),
      ("Verify", "/ˈver.ɪ.faɪ/", "v.", "ทวนสอบความถูกต้อง", "Verify the quantities before sending.", "ทวนสอบจำนวนก่อนส่งของ"),
      ("Request", "/rɪˈkwest/", "n./v.", "คำร้องขอ", "We received your requisition request.", "พวกเราได้รับคำขอเบิกของของคุณแล้ว"),
      ("Available", "/əˈveɪ.lə.bəl/", "adj.", "ว่าง / สะดวก", "Is the supervisor available for a sync?", "หัวหน้าว่างคุยงานสั้นๆ ไหมครับ"),
      ("Grateful", "/ˈɡreɪt.fəl/", "adj.", "รู้สึกขอบคุณยิ่ง", "We are grateful for your cooperation.", "เราขอบคุณมากสำหรับความร่วมมือ")],
     "The Missing Delivery Order", "Clarifying the Label Standard", "Borrowing the Hand Truck", "Polite Words Open Doors"),

    (3, "Day 3: Reporting Problems & Delays", "การแจ้งปัญหาความล่าช้า เหตุเครื่องจักรขัดข้อง และแนวทางแก้ไข", "แจ้งปัญหา (Issue) -> อธิบายสาเหตุ (Due to) -> เสนอทางแก้ไข (Action)",
     [("Delay", "/dɪˈleɪ/", "n./v.", "ความล่าช้า", "There is a slight delay in Line 1.", "มีความล่าช้าเล็กน้อยในไลน์ 1"),
      ("Bottleneck", "/ˈbɒt.əl.nek/", "n.", "จุดคอขวด / จุดติดขัด", "We found a bottleneck at packaging.", "เราพบจุดคอขวดที่การแพ็คของ"),
      ("Resolve", "/rɪˈzɒlv/", "v.", "แก้ไขปัญหาลุล่วง", "We resolved the sensor error quickly.", "พวกเราแก้ปัญหาเซนเซอร์ได้อย่างรวดเร็ว"),
      ("Malfunction", "/ˌmælˈfʌŋk.ʃən/", "n.", "เครื่องขัดข้อง", "The conveyor motor malfunctioned.", "มอเตอร์สายพานทำงานขัดข้อง"),
      ("Impact", "/ˈɪm.pækt/", "n.", "ผลกระทบ", "We want to minimize customer impact.", "เราต้องการลดผลกระทบต่อลูกค้า"),
      ("Resume", "/rɪˈzjuːm/", "v.", "เริ่มทำงานต่อ", "Production will resume by 2:00 PM.", "การผลิตจะเริ่มต่อตอนบ่ายสอง"),
      ("Halt", "/hɒlt/", "v.", "หยุดชะงัก", "Operations were halted for 20 mins.", "การทำงานหยุดชะงักไป 20 นาที"),
      ("Shortage", "/ˈʃɔː.tɪdʒ/", "n.", "ของขาดแคลน", "There is a temporary carton shortage.", "เกิดภาวะกล่องบรรจุภัณฑ์ขาดชั่วคราว"),
      ("Investigate", "/ɪnˈves.tɪ.ɡeɪt/", "v.", "สืบสวนหาสาเหตุ", "We are investigating the temperature spike.", "เรากำลังหาสาเหตุที่อุณหภูมิพุ่งสูง"),
      ("Alternative", "/ɒlˈtɜː.nə.tɪv/", "n.", "ทางเลือกสำรอง", "We switched to an alternative route.", "เราเปลี่ยนไปใช้เส้นทางขนส่งสำรอง"),
      ("Preventive", "/prɪˈven.tɪv/", "adj.", "เชิงป้องกัน", "Take preventive maintenance steps.", "ดำเนินมาตรการซ่อมบำรุงเชิงป้องกัน"),
      ("Replacement", "/rɪˈpleɪs.mənt/", "n.", "ของเปลี่ยนทดแทน", "We ordered a replacement belt.", "เราสั่งสายพานเส้นใหม่มาทดแทนแล้ว"),
      ("Root cause", "/ruːt kɔːz/", "n.", "สาเหตุต้นตอ", "The root cause was a loose cable.", "สาเหตุต้นตอคือสายไฟหลวม"),
      ("Correction", "/kəˈrek.ʃən/", "n.", "การแก้ไขให้ถูกต้อง", "Apply the correction to the system.", "บันทึกการแก้ไขลงในระบบ"),
      ("Technician", "/tekˈnɪʃ.ən/", "n.", "ช่างเทคนิค", "Call the on-duty technician now.", "เรียกช่างเทคนิคประจำกะมาทันที"),
      ("Capacity", "/kəˈpæs.ə.ti/", "n.", "กำลังการผลิต", "We are running at 85% capacity.", "เราเดินเครื่องอยู่ที่ 85% ของกำลังผลิต"),
      ("Quarantine", "/ˈkwɒr.ən.tiːn/", "n./v.", "กักแยกของเสีย", "Quarantine all scratched boards.", "กักแยกแผ่นวงจรที่มีรอยขีดข่วนทั้งหมด"),
      ("Recurrence", "/rɪˈkʌr.əns/", "n.", "การเกิดซ้ำ", "Prevent recurrence of the stoppage.", "ป้องกันไม่ให้เครื่องหยุดทำงานซ้ำอีก"),
      ("Estimate", "/ˈes.tɪ.meɪt/", "v.", "ประเมินเวลา/ยอด", "We estimate 30 minutes of downtime.", "เราประเมินเวลาเครื่องหยุดไว้ 30 นาที"),
      ("Contingency", "/kənˈtɪn.dʒən.si/", "n.", "แผนฉุกเฉิน", "Follow the warehouse contingency plan.", "ปฏิบัติตามแผนฉุกเฉินของคลังสินค้า")],
     "The Jammed Conveyor Belt", "The Temperature Spike in Room A1", "Rainstorm on the Highway", "The Missing Wooden Crate"),

    (4, "Day 4: Daily Standup & Work Progress", "การรายงานความคืบหน้า สิ่งที่ทำเสร็จ และอุปสรรคในการทำงาน", "What I did yesterday -> What I will do today -> Blockers",
     [("Backlog", "/ˈbæk.lɒɡ/", "n.", "งานคั่งค้างสะสม", "We cleared 90% of the backlog.", "พวกเราเคลียร์งานค้างได้ 90% แล้ว"),
      ("Blocker", "/ˈblɒk.ər/", "n.", "อุปสรรคติดขัด", "Do you have any blockers today?", "วันนี้คุณมีปัญหาติดขัดอะไรไหม"),
      ("Milestone", "/ˈmaɪl.stəʊn/", "n.", "เป้าหมายสำคัญ", "We hit our daily milestone early.", "เราบรรลุเป้าหมายประจำวันได้เร็วขึ้น"),
      ("Prioritize", "/praɪˈɒr.ɪ.taɪz/", "v.", "จัดลำดับสำคัญ", "Prioritize urgent customer orders.", "จัดลำดับออเดอร์ด่วนของลูกค้าก่อน"),
      ("Progress", "/ˈprəʊ.ɡres/", "n.", "ความคืบหน้า", "Great progress on Room A1 racks.", "งานแร็คห้อง A1 คืบหน้าไปได้ดีมาก"),
      ("Deliverable", "/dɪˈlɪv.ər.ə.bəl/", "n.", "ชิ้นงานส่งมอบ", "The deliverable is due before 4 PM.", "งานส่งมอบครบกำหนดส่งก่อนบ่ายสี่"),
      ("Achievement", "/əˈtʃiːv.mənt/", "n.", "ผลงานสำเร็จ", "Zero defect is our top achievement.", "ของเสียเป็นศูนย์คือผลงานสูงสุดของเรา"),
      ("Pending", "/ˈpen.dɪŋ/", "adj.", "อยู่ระหว่างรอผล", "Quality approval is still pending.", "การอนุมัติคุณภาพยังอยู่ระหว่างรอผล"),
      ("Coordinate", "/kəʊˈɔː.dɪ.neɪt/", "v.", "ประสานงาน", "Coordinate with the night shift lead.", "ประสานงานร่วมกับหัวหน้ากะดึก"),
      ("Handover", "/ˈhændˌəʊ.vər/", "n.", "การส่งมอบงาน", "Execute a smooth shift handover.", "ส่งมอบงานระหว่างกะอย่างราบรื่น"),
      ("Target", "/ˈtɑː.ɡɪt/", "n.", "เป้าหมาย", "We exceeded our packing target.", "เราทำยอดแพ็คของได้เกินเป้าหมาย"),
      ("Update", "/ʌpˈdeɪt/", "v./n.", "รายงานความคืบหน้า", "Provide a quick five-minute update.", "ช่วยรายงานอัปเดตสั้นๆ 5 นาที"),
      ("Support", "/səˈpɔːt/", "n.", "การช่วยเหลือ", "I need technical support on scanning.", "ผมต้องการคนช่วยแนะนำเรื่องสแกนเนอร์"),
      ("Efficiency", "/ɪˈfɪʃ.ən.si/", "n.", "ประสิทธิภาพ", "Improve picking route efficiency.", "ปรับปรุงประสิทธิภาพเส้นทางหยิบสินค้า"),
      ("Assign", "/əˈsaɪn/", "v.", "มอบหมายงาน", "Assign two operators to Bay 3.", "มอบหมายพนักงาน 2 คนไปดูแลเบย์ 3"),
      ("Status", "/ˈsteɪ.təs/", "n.", "สถานะงาน", "What is the status of the Ayutthaya order?", "สถานะออเดอร์อยุธยาเป็นอย่างไรบ้าง"),
      ("Resource", "/rɪˈzɔːs/", "n.", "ทรัพยากร/กำลังคน", "We allocated extra resources to packing.", "เราเพิ่มกำลังคนเข้าไปช่วยแผนกแพ็ค"),
      ("Morale", "/məˈrɑːl/", "n.", "ขวัญกำลังใจ", "Team morale is positive and energized.", "ขวัญกำลังใจของทีมงานดีเยี่ยมและกระตือรือร้น"),
      ("Align", "/əˈlaɪn/", "v.", "ปรับให้ตรงกัน", "Let's align our shift priorities.", "พวกเรามาปรับเป้าหมายของกะให้ตรงกัน"),
      ("Wrap up", "/ræp ʌp/", "v.", "สรุปจบงาน", "Wrap up the standup meeting on time.", "สรุปจบการประชุมสแตนด์อัปให้ตรงเวลา")],
     "Clearing the Mountain of Boxes", "Speak Up on the Blocker", "The Neat Handover Sheet", "Ten Percent Over Daily Target"),

    (5, "Day 5: Scheduling & Rescheduling Meetings", "การนัดหมาย เสนอเวลาว่าง เลื่อนนัด และยืนยันกำหนดการประชุม", "Does [time] work for you? | I have a conflict | Reschedule",
     [("Available", "/əˈveɪ.lə.bəl/", "adj.", "ว่าง / สะดวก", "Are you available for a 15-min call?", "คุณว่างคุยสายสัก 15 นาทีไหมครับ"),
      ("Reschedule", "/ˌriːˈskedʒ.uːl/", "v.", "เลื่อนนัดหมาย", "Can we reschedule the safety sync?", "เราขอเลื่อนประชุมความปลอดภัยได้ไหม"),
      ("Conflict", "/ˈkɒn.flɪkt/", "n.", "เวลาชนกัน", "I have an audit conflict at 10 AM.", "ผมมีนัดตรวจประเมินชนกันตอน 10 โมง"),
      ("Propose", "/prəˈpəʊz/", "v.", "เสนอเวลา", "I propose Thursday at 2:30 PM.", "ผมขอเสนอเป็นวันพฤหัสบดีบ่ายสองครึ่ง"),
      ("Confirm", "/kənˈfɜːm/", "v.", "ยืนยัน", "Please confirm meeting attendance.", "ช่วยยืนยันการเข้าร่วมประชุมด้วยครับ"),
      ("Postpone", "/pəʊstˈpəʊn/", "v.", "เลื่อนออกไป", "Postpone the meeting until data arrives.", "เลื่อนประชุมไปจนกว่าข้อมูลจะมาถึง"),
      ("Agenda", "/əˈdʒen.də/", "n.", "วาระการประชุม", "Review the five-point agenda.", "ตรวจดูวาระการประชุมทั้ง 5 ข้อ"),
      ("Attendee", "/ə.tenˈdiː/", "n.", "ผู้เข้าร่วมประชุม", "All key attendees joined online.", "ผู้เข้าร่วมคนสำคัญทุกคนเข้าออนไลน์แล้ว"),
      ("Convenient", "/kənˈviː.ni.ənt/", "adj.", "สะดวกสบาย", "Is Friday morning convenient for you?", "เช้าวันศุกร์สะดวกสำหรับคุณไหมครับ"),
      ("Invitation", "/ˌɪn.vɪˈteɪ.ʃən/", "n.", "คำเชิญปฏิทิน", "Accept the calendar invitation.", "ตอบรับคำเชิญในปฏิทินอีเมล"),
      ("Duration", "/djʊəˈreɪ.ʃən/", "n.", "ระยะเวลาประชุม", "Keep the meeting duration short.", "รักษาเวลาประชุมให้กระชับสั้น"),
      ("Minutes", "/ˈmɪn.ɪts/", "n.", "บันทึกการประชุม", "I will circulate meeting minutes.", "เดี๋ยวผมจะส่งเวียนบันทึกการประชุมให้"),
      ("Facilitate", "/fəˈsɪl.ɪ.teɪt/", "v.", "ดำเนินรายการ", "The team leader will facilitate.", "หัวหน้าทีมจะเป็นผู้ดำเนินรายการประชุม"),
      ("Discussion", "/dɪˈskʌʃ.ən/", "n.", "การหารือร่วมกัน", "Focus the discussion on solutions.", "เน้นการหารือไปที่ทางออกของปัญหา"),
      ("Tentative", "/ˈten.tə.tɪv/", "adj.", "กำหนดการคร่าวๆ", "This 3 PM slot is tentative.", "ช่วงเวลาบ่ายสามนี้เป็นนัดหมายคร่าวๆ"),
      ("Reminder", "/rɪˈmaɪn.dər/", "n.", "การเตือนความจำ", "Send an automated calendar reminder.", "ตั้งแจ้งเตือนอัตโนมัติในปฏิทิน"),
      ("Platform", "/ˈplæt.fɔːm/", "n.", "โปรแกรมประชุม", "Teams is our chosen meeting platform.", "เราใช้ Teams เป็นโปรแกรมประชุมหลัก"),
      ("Dial-in", "/ˈdaɪ.əl.ɪn/", "n.", "ลิงก์เข้าประชุม", "Click the dial-in link below.", "คลิกที่ลิงก์ด้านล่างเพื่อเข้าห้องประชุม"),
      ("Punctual", "/ˈpʌŋk.tʃu.əl/", "adj.", "ตรงต่อเวลา", "Please be punctual for shift brief.", "กรุณามาให้ตรงเวลาสำหรับการบรีฟกะ"),
      ("Accommodate", "/əˈkɒm.ə.deɪt/", "v.", "ปรับเวลาให้ลงตัว", "Thanks for accommodating my time slot.", "ขอบคุณมากที่ช่วยปรับเวลาให้ลงตัว")],
     "Double Booked at 2 PM", "The Missing Online Link", "Finding the Golden Morning Hour", "Short Notice Appreciation"),

    (6, "Day 6: Clarifying Instructions & Active Listening", "การทวนความเข้าใจ เช็คคำสั่ง และการฟังอย่างตั้งใจหน้างาน", "Just to make sure we are on the same page... | Did you mean...?",
     [("Elaborate", "/iˈlæb.ə.reɪt/", "v.", "อธิบายขยายความ", "Could you elaborate on the packing rule?", "ช่วยขยายความกฎการแพ็คของหน่อยครับ"),
      ("Alignment", "/əˈlaɪn.mənt/", "n.", "ความเข้าใจตรงกัน", "We achieved total cross-department alignment.", "เราเข้าใจตรงกันทุกแผนกอย่างสมบูรณ์"),
      ("Specification", "/ˌspes.ɪ.fɪˈkeɪ.ʃən/", "n.", "สเปกข้อกำหนด", "Verify the blueprint specification.", "ทวนสอบข้อกำหนดในพิมพ์เขียว"),
      ("Verify", "/ˈver.ɪ.faɪ/", "v.", "ทวนสอบความถูกต้อง", "Always verify part codes twice.", "ทวนสอบรหัสชิ้นส่วนสองรอบเสมอ"),
      ("Ambiguous", "/æmˈbɪɡ.ju.əs/", "adj.", "กำกวมคลุมเครือ", "The supervisor note was not ambiguous.", "ข้อความของหัวหน้าชัดเจน ไม่คลุมเครือ"),
      ("Summarize", "/ˈsʌm.ər.aɪz/", "v.", "สรุปใจความสำคัญ", "Summarize the three steps clearly.", "สรุปขั้นตอนทั้งสามให้ชัดเจน"),
      ("Misunderstanding", "/ˌmɪs.ʌn.dəˈstæn.dɪŋ/", "n.", "ความเข้าใจผิด", "Active questions prevent misunderstanding.", "การซักถามช่วยป้องกันความเข้าใจผิด"),
      ("Rephrase", "/ˌriːˈfreɪz/", "v.", "ทวนประโยคใหม่", "Let me rephrase my understanding.", "ขออนุญาตทวนความเข้าใจของผมใหม่"),
      ("Ensure", "/ɪnˈʃɔːr/", "v.", "ดูแลให้มั่นใจ", "Ensure the shrink wrap is tight.", "ดูแลให้มั่นใจว่าฟิล์มพันพาเลทแน่นหนา"),
      ("Comprehend", "/ˌkɒm.prɪˈhend/", "v.", "เข้าใจอย่างถ่องแท้", "Do all operators comprehend the SOP?", "พนักงานทุกคนเข้าใจ SOP อย่างถ่องแท้ไหม"),
      ("Clarification", "/ˌklær.ɪ.fɪˈkeɪ.ʃən/", "n.", "คำชี้แจงให้กระจ่าง", "Thank you for the prompt clarification.", "ขอบคุณสำหรับคำชี้แจงที่รวดเร็วครับ"),
      ("Instruction", "/ɪnˈstrʌk.ʃən/", "n.", "คำสั่งแนะนำ", "Follow the safety handling instruction.", "ปฏิบัติตามคำแนะนำความปลอดภัย"),
      ("Explicit", "/ɪkˈsplɪs.ɪt/", "adj.", "ชัดเจนตรงไปตรงมา", "Give explicit location numbers.", "ระบุหมายเลขตำแหน่งให้ชัดเจนตรงไปตรงมา"),
      ("Confirmation", "/ˌkɒn.fəˈmeɪ.ʃən/", "n.", "การยืนยัน", "Wait for written dispatch confirmation.", "รอการยืนยันการปล่อยของเป็นลายลักษณ์อักษร"),
      ("Guidance", "/ˈɡaɪ.dəns/", "n.", "คำชี้แนะแนวทาง", "Thank you for the senior operator guidance.", "ขอบคุณสำหรับคำชี้แนะของรุ่นพี่ครับ"),
      ("Tolerance", "/ˈtɒl.ər.əns/", "n.", "เกณฑ์คลาดเคลื่อน", "Temperature tolerance is plus or minus 1°C.", "เกณฑ์คลาดเคลื่อนอุณหภูมิคือ +- 1 องศา"),
      ("Concrete", "/ˈkɒŋ.kriːt/", "adj.", "เป็นรูปธรรมชัดเจน", "Show me a concrete defect sample.", "แสดงตัวอย่างชิ้นงานเสียที่เป็นรูปธรรมให้ดูหน่อย"),
      ("Recap", "/ˈriː.kæp/", "n./v.", "สรุปย่อ", "Let's do a quick verbal recap.", "เรามาสรุปปากเปล่าสั้นๆ กันครับ"),
      ("Adhere", "/ədˈhɪər/", "v.", "ยึดมั่นปฏิบัติตาม", "Adhere strictly to warehouse safety rules.", "ยึดมั่นปฏิบัติตามกฎความปลอดภัยคลังอย่างเคร่งครัด"),
      ("Acknowledge", "/əkˈnɒl.ɪdʒ/", "v.", "ตอบรับทราบ", "Please acknowledge receipt of this message.", "โปรดตอบรับทราบข้อความนี้ด้วยครับ")],
     "The Fourteen or Forty Mix-up", "Inches or Centimeters on Blueprint", "Speak Slower Please Auditor", "The Professional Recap Email"),

    (7, "Day 7: Weekly Wrap-up & Executive Summary", "การเขียนสรุปผลงานประจำสัปดาห์ การนำเสนอ KPI และการส่งต่องาน", "Highlights -> Operational KPIs -> Next Week Plan",
     [("Achievement", "/əˈtʃiːv.mənt/", "n.", "ความสำเร็จผลงาน", "This week marks a major achievement.", "สัปดาห์นี้ถือเป็นความสำเร็จครั้งใหญ่"),
      ("Benchmark", "/ˈbentʃ.mɑːk/", "n.", "เกณฑ์มาตรฐาน", "We beat the 98% on-time benchmark.", "เราทำลายสถิติส่งตรงเวลา 98% ได้สำเร็จ"),
      ("Output", "/ˈaʊt.pʊt/", "n.", "ผลผลิตรวม", "Total warehouse output reached 12,000 units.", "ยอดงานรวมของคลังแตะ 12,000 ชิ้น"),
      ("Efficiency", "/ɪˈfɪʃ.ən.si/", "n.", "ประสิทธิภาพ", "Picking efficiency improved by 8%.", "ประสิทธิภาพการหยิบของเพิ่มขึ้น 8%"),
      ("Summary", "/ˈsʌm.ər.i/", "n.", "บทสรุปย่อ", "Review the executive weekly summary.", "ตรวจดูรายงานสรุปประจำสัปดาห์ของผู้บริหาร"),
      ("Momentum", "/məˈmen.təm/", "n.", "แรงส่งความต่อเนื่อง", "Keep up the great operational momentum.", "รักษาแรงขับเคลื่อนการทำงานที่ดีนี้ไว้"),
      ("Accomplish", "/əˈkʌm.plɪʃ/", "v.", "ทำสำเร็จลุล่วง", "We accomplished all our weekly objectives.", "พวกเราบรรลุเป้าหมายประจำสัปดาห์ได้ครบถ้วน"),
      ("Metric", "/ˈmet.rɪk/", "n.", "ตัวชี้วัดผลงาน", "Check the accuracy metrics in the spreadsheet.", "ตรวจดูตัวชี้วัดความแม่นยำในสเปรดชีต"),
      ("Exceed", "/ɪkˈsiːd/", "v.", "ทำได้เกินกว่า", "Daily volume exceeded our highest forecast.", "ยอดส่งต่อวันเกินกว่าตัวเลขคาดการณ์สูงสุด"),
      ("Objective", "/əbˈdʒek.tɪv/", "n.", "เป้าหมายหลัก", "Our primary objective was safety compliance.", "เป้าหมายหลักของเราคือการปฏิบัติตามความปลอดภัย"),
      ("Overcome", "/ˌəʊ.vəˈkʌm/", "v.", "เอาชนะอุปสรรค", "The warehouse team overcame every delay.", "ทีมคลังสินค้าเอาชนะความล่าช้าได้ทุกจุด"),
      ("Consistent", "/kənˈsɪs.tənt/", "adj.", "สม่ำเสมอ", "Maintain consistent 100% stock accuracy.", "รักษาความแม่นยำสต็อก 100% ไว้อย่างสม่ำเสมอ"),
      ("Contribution", "/ˌkɒn.trɪˈbjuː.ʃən/", "n.", "การมีส่วนร่วมช่วยงาน", "Thank you for your valuable contribution.", "ขอบคุณสำหรับการมีส่วนร่วมช่วยงานที่มีค่ายิ่ง"),
      ("Productivity", "/ˌprɒd.ʌkˈtɪv.ə.ti/", "n.", "ผลิตภาพ", "Shift productivity reached an all-time record.", "ผลิตภาพของกะแตะระดับสูงสุดเป็นประวัติการณ์"),
      ("Highlight", "/ˈhaɪ.laɪt/", "n.", "ผลงานเด่น", "Zero shipping defect was our weekly highlight.", "การส่งของไร้ตำหนิคือผลงานเด่นประจำสัปดาห์"),
      ("Forecast", "/ˈfɔː.kɑːst/", "n.", "การคาดการณ์ล่วงหน้า", "Prepare for next week's inbound forecast.", "เตรียมพร้อมรับยอดของเข้าตามที่คาดการณ์"),
      ("Restful", "/ˈrest.fəl/", "adj.", "ที่ได้พักผ่อนเต็มที่", "Have a well-deserved restful weekend.", "ขอให้ได้พักผ่อนอย่างเต็มที่ในวันหยุดสุดสัปดาห์"),
      ("Dedication", "/ˌded.ɪˈkeɪ.ʃən/", "n.", "ความทุ่มเท", "Management appreciates your team dedication.", "ฝ่ายบริหารชื่นชมความทุ่มเทของทีมงานทุกคน"),
      ("Seamless", "/ˈsiːm.ləs/", "adj.", "ราบรื่นไร้รอยต่อ", "Cross-shift coordination was completely seamless.", "การประสานงานข้ามกะราบรื่นไร้รอยต่ออย่างแท้จริง"),
      ("Milestone", "/ˈmaɪl.stəʊn/", "n.", "ก้าวสำคัญ", "We passed the Week 1 sprint milestone.", "พวกเราผ่านก้าวสำคัญของสัปดาห์ที่ 1 แล้ว")],
     "Hitting the 98% Benchmark", "A Well-Deserved Restful Weekend", "The Clear Executive Presentation", "Week 1 Milestone Reached")
]

for d_num, d_title, d_sum, d_rule, d_voc, st1, st2, st3, st4 in WEEK_THEMES:
    d_str = str(d_num)
    WEEK_1_DATA[d_str] = {
        "day": d_num,
        "title": d_title,
        "summary": d_sum,
        "rule": d_rule,
        "vocab": make_vocab(d_voc),
        "phrases": make_phrases([
            (f"We are reviewing the {d_voc[0][0].lower()} process today.", f"พวกเรากำลังทบทวนกระบวนการ {d_voc[0][3]} ในวันนี้ครับ", "เน้นคำสำคัญ"),
            (f"Please prioritize the {d_voc[1][0].lower()} task first.", f"กรุณาจัดลำดับงาน {d_voc[1][3]} เป็นอันดับแรกครับ", "prioritize = จัดลำดับ"),
            (f"The team managed to {d_voc[2][0].lower()} yesterday.", f"ทีมงานสามารถดำเนินการ {d_voc[2][3]} ได้สำเร็จเมื่อวานนี้ครับ", "รูปอดีต Past tense"),
            (f"Could you please check the {d_voc[3][0].lower()} status?", f"ช่วยตรวจสอบสถานะ {d_voc[3][3]} หน่อยได้ไหมครับ", "Could you please สุภาพ"),
            (f"We want to minimize any negative {d_voc[4][0].lower()}.", f"เราต้องการลดผลกระทบเชิงลบให้น้อยที่สุดครับ", "minimize = ลดให้น้อยสุด"),
            (f"Operations will {d_voc[5][0].lower()} by early afternoon.", f"การทำงานจะกลับมาดำเนินการตามปกติช่วงบ่ายครับ", "resume = เริ่มใหม่"),
            (f"Did you verify the latest {d_voc[6][0].lower()} sheet?", f"คุณได้ตรวจสอบเอกสาร {d_voc[6][3]} ฉบับล่าสุดแล้วหรือยังครับ", "verify = ทวนสอบ"),
            (f"We have an effective plan for this {d_voc[7][0].lower()}.", f"พวกเรามีแผนงานที่มีประสิทธิภาพสำหรับเรื่องนี้ครับ", "effective plan"),
            (f"Please coordinate with the {d_voc[8][0].lower()} team.", f"กรุณาประสานงานร่วมกับทีมที่เกี่ยวข้องครับ", "coordinate with"),
            (f"All items comply with safety {d_voc[9][0].lower()} guidelines.", f"สินค้าทุกชิ้นสอดคล้องกับข้อกำหนดความปลอดภัยครับ", "comply with"),
            ("Everything is on track to meet our weekly deadline.", "ทุกอย่างดำเนินไปตามแผนและทันกำหนดแน่นอนครับ", "on track = ตามแผน"),
            ("Let me double-check the figures before submission.", "ขอให้ผมตรวจทานตัวเลขซ้ำอีกครั้งก่อนส่งมอบนะครับ", "double-check"),
            ("Could you put that instruction in an email for reference?", "รบกวนช่วยสรุปคำสั่งส่งทางอีเมลเพื่อใช้อ้างอิงได้ไหมครับ", "for reference"),
            ("I will provide a full status update before 5 PM.", "ผมจะส่งสรุปรายงานความคืบหน้าให้ก่อน 5 โมงเย็นครับ", "status update"),
            ("We achieved a 99% accuracy rate across all lines.", "เราทำความแม่นยำได้ถึง 99% ในทุกสายการผลิตครับ", "accuracy rate"),
            ("Thank you for the seamless cross-team cooperation.", "ขอบคุณสำหรับการประสานงานข้ามแผนกที่ราบรื่นมากครับ", "seamless"),
            ("Please wear your personal protective equipment at all times.", "กรุณาสวมใส่อุปกรณ์ป้องกันภัยส่วนบุคคลตลอดเวลาครับ", "PPE equipment"),
            ("We are closely monitoring the operational metrics.", "พวกเรากำลังติดตามตัวเลขตัวชี้วัดการทำงานอย่างใกล้ชิดครับ", "monitoring"),
            ("Have a restful and safe weekend, everyone!", "ขอให้ทุกคนได้พักผ่อนอย่างเต็มที่และปลอดภัยในวันหยุดครับ!", "weekend greeting"),
            ("Congratulations on completing today's English sprint!", "ขอแสดงความยินดีด้วยที่คุณผ่านบทเรียนฝึกภาษาอังกฤษวันนี้!", "congratulations")
        ]),
        "dialogues": make_dialogues([
            ("รายงานความคืบหน้า", [("Lead", "How is the task progressing?", "งานคืบหน้าไปถึงไหนแล้ว"), ("Staff", f"We are handling the {d_voc[0][0].lower()} right now.", f"กำลังจัดการ {d_voc[0][3]} อยู่ครับ")]),
            ("ขอคำแนะนำด่วน", [("Staff", "Could you provide guidance on this point?", "ช่วยให้คำแนะนำในจุดนี้หน่อยได้ไหมครับ"), ("Lead", "Sure, let's look at the standard guide.", "ได้สิ มาเปิดดูคู่มือมาตรฐานกัน")]),
            ("ตรวจสอบความถูกต้อง", [("QA", "Did you verify the serial numbers?", "ตรวจหมายเลขซีเรียลแล้วหรือยัง"), ("Staff", "Yes, everything matches the system perfectly.", "ตรวจแล้วครับ ทุกอย่างตรงกับในระบบเป๊ะเลย")]),
            ("การส่งต่องานระหว่างกะ", [("Shift A", "We cleared 80% of the assigned volume.", "พวกเราเคลียร์ยอดไปได้ 80% แล้วครับ"), ("Shift B", "Great, we will take over and finish the rest.", "เยี่ยม เดี๋ยวพวกเรามารับช่วงต่อให้เสร็จ")]),
            ("แจ้งแก้ปัญหาหน้างาน", [("Tech", "The issue has been successfully resolved.", "ปัญหาได้รับการแก้ไขเรียบร้อยแล้วครับ"), ("Lead", "Awesome job, resume normal operations.", "ยอดเยี่ยมมาก เริ่มเดินเครื่องตามปกติต่อได้เลย")]),
            ("นัดหมายคุยงานสั้นๆ", [("Colleague", "Do you have 5 minutes for a quick sync?", "มีเวลาสัก 5 นาทีคุยกันสั้นๆ ไหมครับ"), ("Staff", "Yes, I am available right now.", "ได้เลยครับ ตอนนี้ผมว่างอยู่พอดี")]),
            ("ประสานงานข้ามแผนก", [("Procurement", "The spare parts will arrive by 2 PM.", "อะไหล่สำรองจะมาถึงตอนบ่ายสองค่ะ"), ("Warehouse", "Thanks, we have cleared the receiving dock.", "ขอบคุณครับ เราเตรียมพื้นที่รอรับไว้แล้ว")]),
            ("เช็คความเข้าใจคำสั่ง", [("Staff", "Just to confirm, should I pack Room A1 first?", "ขอทวนครับ ให้แพ็คของห้อง A1 ก่อนใช่ไหมครับ"), ("Leader", "Yes, exactly. Room A1 is our top priority.", "ถูกต้อง ห้อง A1 คือเป้าหมายสำคัญที่สุด")]),
            ("สรุปรายงานส่งผู้บริหาร", [("Staff", "The summary metrics deck is ready.", "สไลด์สรุปดัชนีชี้วัดพร้อมแล้วครับ"), ("Manager", "Great work, please email it to the director.", "ทำได้ดีมาก ส่งอีเมลให้ท่านผอ.ได้เลย")]),
            ("ปิดการทำงานประจำวัน", [("Leader", "Thank you everyone for the great dedication today!", "ขอบคุณทุกคนมากสำหรับความทุ่มเทในวันนี้!"), ("Team", "Have a great evening, see you tomorrow!", "ขอให้เป็นเย็นที่ดี เจอกันพรุ่งนี้ครับ!")])
        ]),
        "exercises": make_exercises([
            (f"พวกเรากำลังทบทวนกระบวนการ {d_voc[0][3]} ในขณะนี้", "We are currently", f"the {d_voc[0][0].lower()} process.", "กริยา review ในรูป V.ing", "reviewing", ["checking"], f"We are currently reviewing the {d_voc[0][0].lower()} process.", "กำลังกระทำอยู่ใช้ is/am/are + V.ing"),
            ("เป้าหมายสำคัญอันดับหนึ่งของเราคือการส่งมอบตรงเวลา", "Our top", "is on-time delivery.", "คำแปลว่า ลำดับความสำคัญ (p...)", "priority", [], "Our top priority is on-time delivery.", "'top priority' คือสิ่งที่ต้องทำเป็นอันดับแรก"),
            ("ปัญหานี้ได้รับการแก้ไขเรียบร้อยแล้วโดยทีมงาน", "The issue has been", "by the team.", "คำกริยาช่อง 3 แปลว่า แก้ไขลุล่วง (r...)", "resolved", ["fixed"], "The issue has been resolved by the team.", "'resolved' แปลว่า แก้ไขปัญหาได้สำเร็จ"),
            ("พวกเราทำงานเสร็จเร็วกว่ากำหนดการสองชั่วโมง", "We finished ahead of", ".", "คำนามแปลว่า กำหนดการ (s...)", "schedule", [], "We finished ahead of schedule.", "'ahead of schedule' แปลว่า เร็วกว่ากำหนด"),
            ("ช่วยส่งคำสั่งนี้ทางอีเมลเพื่อใช้อ้างอิงด้วยครับ", "Put that in an email for", ".", "คำแปลว่า การอ้างอิง (r...)", "reference", [], "Put that in an email for reference.", "'for reference' แปลว่า ไว้ใช้อ้างอิง"),
            ("ทุกอย่างดำเนินไปตามแผนงานที่วางไว้", "Everything is on", "to meet the deadline.", "สำนวนแปลว่า ตามแผน (t...)", "track", [], "Everything is on track to meet the deadline.", "'on track' แปลว่า เป็นไปตามแผนงาน"),
            ("เราจำเป็นต้องลดผลกระทบต่อลูกค้าให้น้อยที่สุด", "We must", "the impact on customers.", "คำกริยาแปลว่า ลดให้น้อยที่สุด (m...)", "minimize", ["minimise"], "We must minimize the impact on customers.", "'minimize' แปลว่า ลดระดับลงให้เหลือน้อยที่สุด"),
            ("ขอบคุณล่วงหน้าสำหรับความร่วมมืออันดีของคุณครับ", "Thank you in", "for your kind cooperation.", "คำแปลว่า ล่วงหน้า (a...)", "advance", [], "Thank you in advance for your kind cooperation.", "'in advance' แปลว่า ล่วงหน้า"),
            ("ช่วยอธิบายขยายความเพิ่มเติมในจุดนี้ได้ไหมครับ", "Could you please", "on this specific point?", "คำกริยาแปลว่า ขยายความ (e...)", "elaborate", ["clarify"], "Could you please elaborate on this specific point?", "'elaborate on' แปลว่า ให้รายละเอียดเพิ่มเติม"),
            ("ขอแสดงความยินดีที่คุณเรียนจบบทเรียนวันนี้แล้ว", "", "on completing today's sprint!", "คำอวยพรแสดงความยินดี (C...)", "Congratulations", [], "Congratulations on completing today's sprint!", "'Congratulations on...' แปลว่า ขอแสดงความยินดีด้วย")
        ]),
        "stories": make_stories([
            (st1, "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=900&auto=format&fit=crop&q=80",
             [(d_voc[0][0], "n.", d_voc[0][3]), (d_voc[1][0], "adj.", d_voc[1][3]), (d_voc[2][0], "v.", d_voc[2][3]), ("team", "n.", "ทีมงาน")],
             f"The warehouse shift begins with checking the <b>{d_voc[0][0].lower()}</b>. An urgent request requires immediate action.<br><br>Through clear communication, the <b>team</b> manages to <b>{d_voc[2][0].lower()}</b> the task smoothly before noon.",
             f"The warehouse shift begins with checking the {d_voc[0][0].lower()}. An urgent request requires immediate action. Through clear communication, the team manages to {d_voc[2][0].lower()} the task smoothly before noon.",
             f"กะการทำงานในคลังเริ่มต้นด้วยการตรวจเช็ค {d_voc[0][3]} งานด่วนต้องการการจัดการทันที ด้วยการสื่อสารที่ชัดเจน ทีมงานสามารถดำเนินการ {d_voc[2][3]} ได้อย่างราบรื่นก่อนเที่ยง"),
            (st2, "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=900&auto=format&fit=crop&q=80",
             [(d_voc[3][0], "n.", d_voc[3][3]), ("clarify", "v.", "ชี้แจง"), ("listen", "v.", "รับฟัง"), ("success", "n.", "ความสำเร็จ")],
             "Whenever instructions seem unclear, the operator politely asks to <b>clarify</b> the requirements. Taking detailed notes and <b>listening</b> carefully prevents any mistake.<br><br>That simple habit turns everyday confusion into complete operational <b>success</b>.",
             "Whenever instructions seem unclear, the operator politely asks to clarify the requirements. Taking detailed notes and listening carefully prevents any mistake. That simple habit turns everyday confusion into complete operational success.",
             "เมื่อใดก็ตามที่คำสั่งดูไม่ชัดเจน พนักงานจะถามอย่างสุภาพเพื่อขอคำชี้แจง การจดบันทึกและตั้งใจฟังช่วยป้องกันข้อผิดพลาด นิสัยง่ายๆ นี้เปลี่ยนความสับสนเป็นความสำเร็จในการทำงาน"),
            (st3, "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=900&auto=format&fit=crop&q=80",
             [(d_voc[4][0], "n.", d_voc[4][3]), ("solve", "v.", "แก้ไข"), ("calm", "adj.", "ใจเย็น"), ("relief", "n.", "ความโล่งอก")],
             "A sudden unexpected hurdle caused tension across the packing line. Instead of panicking, the crew stayed <b>calm</b>, investigated the root cause, and <b>solved</b> the issue within minutes with immense <b>relief</b>.",
             "A sudden unexpected hurdle caused tension across the packing line. Instead of panicking, the crew stayed calm, investigated the root cause, and solved the issue within minutes with immense relief.",
             "อุปสรรคที่ไม่คาดคิดสร้างความตึงเครียดในสายบรรจุหีบห่อ แทนที่จะตื่นตระหนก ทีมงานตั้งสติ ตรวจสอบหาสาเหตุต้นตอ และแก้ไขปัญหาได้สำเร็จภายในไม่กี่นาทีด้วยความโล่งอก"),
            (st4, "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=900&auto=format&fit=crop&q=80",
             [("milestone", "n.", "ก้าวสำคัญ"), ("dedication", "n.", "ความทุ่มเท"), ("proud", "adj.", "ภาคภูมิใจ"), ("rest", "n.", "การพักผ่อน")],
             "At shift end, the crew celebrated hitting their daily <b>milestone</b>. Their tireless <b>dedication</b> kept every customer satisfied. Everyone headed home <b>proud</b> and ready for a well-deserved <b>rest</b>.",
             "At shift end, the crew celebrated hitting their daily milestone. Their tireless dedication kept every customer satisfied. Everyone headed home proud and ready for a well-deserved rest.",
             "เมื่อสิ้นสุดกะการทำงาน ทีมงานร่วมยินดีที่บรรลุเป้าหมายสำคัญประจำวัน ความทุ่มเทอย่างไม่เหน็ดเหนื่อยช่วยให้ลูกค้าทุกคนพึงพอใจ ทุกคนเดินทางกลับบ้านด้วยความภาคภูมิใจและพร้อมสำหรับการพักผ่อน")
        ])
    }

# -----------------------------------------------------------------------------
# 7. ระบบจัดการความคืบหน้าและการโหลดข้อมูล (Persistence Layer)
# -----------------------------------------------------------------------------
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
    curriculum = dict(WEEK_1_DATA)
    if os.path.exists(LESSONS_FILE):
        try:
            with open(LESSONS_FILE, "r", encoding="utf-8") as f:
                external_data = json.load(f)
                curriculum.update(external_data)
        except Exception:
            pass
    return curriculum

if "user_data" not in st.session_state:
    st.session_state.user_data = load_progress()

completed_days = set(st.session_state.user_data.get("completed_days", []))

# -----------------------------------------------------------------------------
# 8. ฟังก์ชันตรวจไวยากรณ์ด้วย Gemini 3.6 Flash (AI Writing Coach)
# -----------------------------------------------------------------------------
def analyze_with_ai(text_to_check: str, api_key: str) -> str:
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        prompt = f"""
        คุณคือผู้เชี่ยวชาญการสอนภาษาอังกฤษเพื่อการสื่อสารในการทำงาน กรุณาตรวจประโยคด้านล่างนี้:
        "{text_to_check}"
        
        ตอบกลับเป็นภาษาไทยที่กระชับ ตรงประเด็น:
        1. 🎯 **คะแนนภาพรวม (Score 1-10)**
        2. ✨ **เวอร์ชันที่ถูกต้องและเป็นมืออาชีพ (Professional Version)**
        3. 🔍 **วิเคราะห์จุดที่ควรปรับปรุง (Grammar & Nuances)**: อธิบายสั้นๆ ทีละข้อ
        4. 💡 **วลีหรือสำนวนทางเลือกที่ใช้แทนได้ (Alternative Phrases)**
        """
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )
        return response.text
    except Exception as err:
        return f"⚠️ ไม่สามารถเชื่อมต่อกับ AI ได้: {str(err)}"

# -----------------------------------------------------------------------------
# 9. แถบเมนูด้านข้าง (Sidebar Navigation & Roadmap)
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
# 10. หน้าจอแสดงผลหลัก (Main Workspace: 7 Tabs)
# -----------------------------------------------------------------------------
day_key = str(selected_day)
lesson = curriculum.get(day_key)

if not lesson:
    st.title(f"Day {selected_day}: กำลังจัดเตรียมเนื้อหา")
    st.info("บทเรียนสัปดาห์ถัดไปกำลังอยู่ในระหว่างการอัปเดตข้อมูลเข้าระบบ")
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

    # TAB 1: 20 Vocabulary
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

    # TAB 2: 20 Speaking Phrases Drill
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

    # TAB 3: 10 Dialogues
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

    # TAB 4: 10 Exercises
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

    # TAB 5: 4 Short Stories
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
        
        cat_index = list(PHONICS_CATEGORIES.keys()).index(selected_cat)
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
                        play_audio_button(item["sound"], f"ph_{cat_index}_{i}", "🔊 ฟังเสียง")

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
