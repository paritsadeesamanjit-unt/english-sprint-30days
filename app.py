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

# กำหนดเส้นทางไฟล์แบบ Absolute Path ป้องกันปัญหา Streamlit Cloud หาโฟลเดอร์ไม่เจอ
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
LESSONS_FILE = os.path.join(DATA_DIR, "lessons.json")
PROGRESS_FILE = os.path.join(DATA_DIR, "user_progress.json")

# -----------------------------------------------------------------------------
# 2. Built-in Fail-Safe Curriculum (สัปดาห์ที่ 1: Day 1 - Day 7 จัดเต็ม)
# -----------------------------------------------------------------------------
BUILTIN_WEEK_1 = {
  "1": {
    "day": 1,
    "title": "Day 1: Sentence Framework (S + V + O) & 3 Core Tenses",
    "summary": "ปูพื้นฐานการสร้างประโยค 3 กาลหลักที่ครอบคลุมการพูดในชีวิตประจำวันและหน้างาน 80%",
    "rule": "Present Simple (ทำประจำ) | Present Continuous (กำลังทำขณะนี้) | Future Simple (จะทำในอนาคต)",
    "vocab": [
      {"word": "Inventory", "phonetic": "/ˈɪn.vən.tɔːr.i/", "part_of_speech": "n.", "meaning": "สินค้าคงคลัง / สต็อกสินค้า", "example": "We check the inventory every morning.", "example_th": "พวกเราตรวจเช็คสต็อกสินค้าทุกเช้า"},
      {"word": "Urgent", "phonetic": "/ˈɜː.dʒənt/", "part_of_speech": "adj.", "meaning": "เร่งด่วน / ฉุกเฉิน", "example": "This is an urgent delivery.", "example_th": "นี่คือการส่งสินค้าแบบเร่งด่วน"},
      {"word": "Discrepancy", "phonetic": "/dɪˈskrep.ən.si/", "part_of_speech": "n.", "meaning": "ความคลาดเคลื่อน / ยอดไม่ตรงกัน", "example": "We found a minor discrepancy.", "example_th": "เราพบความคลาดเคลื่อนเล็กน้อย"},
      {"word": "Finalize", "phonetic": "/ˈfaɪ.nəl.aɪz/", "part_of_speech": "v.", "meaning": "สรุปผล / ทำให้เสร็จสมบูรณ์", "example": "I will finalize the report today.", "example_th": "ฉันจะสรุปรายงานให้เสร็จวันนี้"},
      {"word": "Inspect", "phonetic": "/ɪnˈspekt/", "part_of_speech": "v.", "meaning": "ตรวจสอบ / ตรวจตรา", "example": "Please inspect the goods carefully.", "example_th": "โปรดตรวจสอบสินค้าอย่างระมัดระวัง"},
      {"word": "Schedule", "phonetic": "/ˈskedʒ.uːl/", "part_of_speech": "n./v.", "meaning": "กำหนดการ / จัดตาราง", "example": "Everything is on schedule.", "example_th": "ทุกอย่างเป็นไปตามกำหนดการ"},
      {"word": "Operate", "phonetic": "/ˈɒp.ər.eɪt/", "part_of_speech": "v.", "meaning": "เดินเครื่อง / ปฏิบัติการ", "example": "He knows how to operate this machine.", "example_th": "เขารู้วิธีเดินเครื่องจักรเครื่องนี้"},
      {"word": "Maintenance", "phonetic": "/ˈmeɪn.tən.əns/", "part_of_speech": "n.", "meaning": "การบำรุงรักษา", "example": "Regular maintenance prevents breakdowns.", "example_th": "การบำรุงรักษาตามรอบช่วยป้องกันเครื่องเสีย"},
      {"word": "Shipment", "phonetic": "/ˈʃɪp.mənt/", "part_of_speech": "n.", "meaning": "การจัดส่งสินค้า / สินค้าล็อตส่ง", "example": "The shipment arrived on time.", "example_th": "สินค้าล็อตจัดส่งมาถึงตรงเวลา"},
      {"word": "Warehouse", "phonetic": "/ˈweə.haʊs/", "part_of_speech": "n.", "meaning": "คลังสินค้า / โกดัง", "example": "The warehouse is well organized.", "example_th": "คลังสินค้าได้รับการจัดระเบียบอย่างดี"},
      {"word": "Defect", "phonetic": "/ˈdiː.fekt/", "part_of_speech": "n.", "meaning": "ตำหนิ / ข้อบกพร่อง", "example": "Zero defect is our ultimate goal.", "example_th": "ของเสียเป็นศูนย์คือเป้าหมายสูงสุดของเรา"},
      {"word": "Quantity", "phonetic": "/ˈkwɒn.tə.ti/", "part_of_speech": "n.", "meaning": "ปริมาณ / จำนวน", "example": "Please double-check the order quantity.", "example_th": "ช่วยตรวจทานจำนวนสั่งซื้ออีกครั้ง"},
      {"word": "Approve", "phonetic": "/əˈpruːv/", "part_of_speech": "v.", "meaning": "อนุมัติ / เห็นชอบ", "example": "The manager approved the request.", "example_th": "ผู้จัดการอนุมัติคำขอเรียบร้อยแล้ว"},
      {"word": "Deliver", "phonetic": "/dɪˈlɪv.ər/", "part_of_speech": "v.", "meaning": "ส่งมอบ / นำส่ง", "example": "We deliver goods within 24 hours.", "example_th": "เราส่งมอบสินค้าภายใน 24 ชั่วโมง"},
      {"word": "Supplier", "phonetic": "/səˈplaɪ.ər/", "part_of_speech": "n.", "meaning": "ผู้จัดหาวัตถุดิบ / ซัพพลายเออร์", "example": "Our supplier sent high-quality parts.", "example_th": "ซัพพลายเออร์ส่งชิ้นส่วนคุณภาพสูงมาให้"},
      {"word": "Pallet", "phonetic": "/ˈpæl.ət/", "part_of_speech": "n.", "meaning": "พาเลทวางสินค้า", "example": "Stack the boxes onto the pallet.", "example_th": "เรียงกล่องสินค้าลงบนพาเลท"},
      {"word": "Confirm", "phonetic": "/kənˈfɜːm/", "part_of_speech": "v.", "meaning": "ยืนยัน", "example": "Please confirm the delivery time.", "example_th": "โปรดยืนยันเวลาส่งมอบ"},
      {"word": "Label", "phonetic": "/ˈleɪ.bəl/", "part_of_speech": "n./v.", "meaning": "ฉลาก / ติดป้ายระบุ", "example": "Label each box with a barcode.", "example_th": "ติดฉลากบาร์โค้ดลงบนทุกกล่อง"},
      {"word": "Storage", "phonetic": "/ˈstɔː.rɪdʒ/", "part_of_speech": "n.", "meaning": "การจัดเก็บ / พื้นที่เก็บของ", "example": "Room A1 is our cold storage room.", "example_th": "ห้อง A1 คือห้องจัดเก็บควบคุมอุณหภูมิ"},
      {"word": "Dispatch", "phonetic": "/dɪˈspætʃ/", "part_of_speech": "v./n.", "meaning": "ส่งของออกไป / การส่งพัสดุ", "example": "We dispatch five trucks daily.", "example_th": "เราปล่อยรถขนส่งสินค้าออกไปวันละ 5 คัน"}
    ],
    "phrases": [
      {"en": "I am working on the daily report right now.", "th": "ฉันกำลังทำรายงานประจำวันอยู่ตอนนี้", "tip": "เน้นเสียงที่ working และ report"},
      {"en": "I will send you the updated file this afternoon.", "th": "ฉันจะส่งไฟล์ที่อัปเดตให้คุณบ่ายวันนี้", "tip": "ย่อ I will เป็น I'll /aɪl/"},
      {"en": "The team usually reviews the inventory every morning.", "th": "ทีมมักจะตรวจสอบสต็อกสินค้าทุกๆ เช้า", "tip": "usually ออกเสียงเน้นพยางค์แรก /ˈjuː.ʒu.ə.li/"},
      {"en": "We completed the urgent shipment yesterday.", "th": "พวกเราจัดการการจัดส่งด่วนเสร็จเรียบร้อยเมื่อวานนี้", "tip": "completed ออกเสียงลงท้ายด้วย /t/"},
      {"en": "Could you please confirm receipt of the goods?", "th": "ช่วยยืนยันการรับสินค้าให้หน่อยได้ไหมครับ", "tip": "receipt ไม่ออกเสียงตัว p (/rɪˈsiːt/)"},
      {"en": "The production line is running smoothly today.", "th": "สายการผลิตวันนี้กำลังดำเนินไปอย่างราบรื่นครับ", "tip": "smoothly ออกเสียง th แบบแลบลิ้นสั้นๆ"},
      {"en": "We noticed a minor issue during the morning shift.", "th": "เราสังเกตเห็นปัญหาเล็กน้อยในระหว่างกะเช้าครับ", "tip": "noticed ออกเสียงท้าย /t/"},
      {"en": "I will let you know as soon as the batch is ready.", "th": "ฉันจะแจ้งให้คุณทราบทันทีที่ล็อตสินค้าพร้อมครับ", "tip": "เชื่อมเสียง as soon as /əz-suːn-əz/"},
      {"en": "Please stack the pallets against the wall.", "th": "ช่วยวางซ้อนพาเลทชิดผนังด้วยครับ", "tip": "stack the pallets เชื่อมเสียง k กับ th"},
      {"en": "Did you verify the serial numbers on the boxes?", "th": "คุณได้ตรวจสอบหมายเลขซีเรียลบนกล่องแล้วหรือยังครับ", "tip": "verify ออกเสียง /ˈver.ɪ.faɪ/"},
      {"en": "We are currently organizing Temperature Room A1.", "th": "ตอนนี้พวกเรากำลังจัดระเบียบห้องควบคุมอุณหภูมิ A1 ครับ", "tip": "currently ออกเสียง 3 พยางค์ชัดเจน"},
      {"en": "The courier is waiting at the loading dock.", "th": "คนขับรถขนส่งกำลังรออยู่ที่จุดเทียบรับสินค้าครับ", "tip": "loading dock = ท่าขนถ่ายสินค้า"},
      {"en": "I need to print out the barcode labels immediately.", "th": "ผมจำเป็นต้องพิมพ์ป้ายบาร์โค้ดออกมาทันทีครับ", "tip": "print out เชื่อมเสียงเป็น /prɪn-taʊt/"},
      {"en": "How many boxes are left on this rack?", "th": "มีกล่องเหลืออยู่บนแร็คนี้อีกกี่กล่องครับ", "tip": "are left on เชื่อมเสียง t กับ on"},
      {"en": "All raw materials have arrived in good condition.", "th": "วัตถุดิบทั้งหมดมาถึงในสภาพสมบูรณ์เรียบร้อยครับ", "tip": "in good condition = สภาพดีเยี่ยม"},
      {"en": "We must follow the safety guidelines strictly.", "th": "พวกเราต้องปฏิบัติตามกฎความปลอดภัยอย่างเคร่งครัด", "tip": "strictly ลงท้ายด้วย /li/"},
      {"en": "I checked the physical count against the Excel sheet.", "th": "ผมตรวจสอบยอดนับจริงเทียบกับตาราง Excel แล้วครับ", "tip": "against the sheet = เทียบกับตาราง"},
      {"en": "The forklift is undergoing regular maintenance.", "th": "รถโฟล์คลิฟต์กำลังอยู่ระหว่างการบำรุงรักษาตามรอบครับ", "tip": "forklift ออกเสียง /ˈfɔːk.lɪft/"},
      {"en": "Please wear your safety helmet before entering.", "th": "กรุณาสวมหมวกนิรภัยก่อนเข้าไปด้านในครับ", "tip": "safety helmet = หมวกนิรภัย"},
      {"en": "Let me double-check the packing list once more.", "th": "ขอให้ผมตรวจทานใบรายการบรรจุภัณฑ์อีกสักครั้งนะครับ", "tip": "double-check = ตรวจทานซ้ำ"}
    ],
    "dialogues": [
      {"title": "ตรวจนับสต็อกเช้า", "lines": [{"speaker": "Leader", "en": "How is the inventory check going?", "th": "การตรวจนับสต็อกเป็นอย่างไรบ้าง"}, {"speaker": "Staff", "en": "We are counting Rack 1 to 3 right now.", "th": "กำลังนับแร็ค 1 ถึง 3 อยู่ครับ"}]},
      {"title": "แจ้งยอดคลาดเคลื่อน", "lines": [{"speaker": "Staff", "en": "There is a discrepancy of 10 boxes.", "th": "พบยอดคลาดเคลื่อน 10 กล่องครับ"}, {"speaker": "Leader", "en": "Check the dispatch log immediately.", "th": "ไปตรวจสมุดส่งของทันทีเลย"}]},
      {"title": "สินค้าด่วนลูกค้า", "lines": [{"speaker": "CS", "en": "This urgent order must leave by noon.", "th": "ออเดอร์ด่วนนี้ต้องส่งออกก่อนเที่ยงค่ะ"}, {"speaker": "Staff", "en": "Understood. We will pick it first.", "th": "รับทราบครับ เดี๋ยวหยิบให้ก่อนเลย"}]},
      {"title": "รถรับสินค้ามาถึง", "lines": [{"speaker": "Driver", "en": "I am here for the shipment.", "th": "ผมมารับสินค้าล็อตนี้ครับ"}, {"speaker": "Staff", "en": "Please park at Dock 4.", "th": "รบกวนถอยเข้าช่องจอด 4 เลยครับ"}]},
      {"title": "บาร์โค้ดชำรุด", "lines": [{"speaker": "Worker", "en": "The barcode label is torn.", "th": "ฉลากบาร์โค้ดฉีกขาดครับ"}, {"speaker": "Leader", "en": "Print a replacement label now.", "th": "สั่งพิมพ์ฉลากใหม่ออกมาติดเลย"}]},
      {"title": "ตรวจอุณหภูมิห้อง A1", "lines": [{"speaker": "QA", "en": "What is the temperature in Room A1?", "th": "อุณหภูมิในห้อง A1 เท่าไหร่ครับ"}, {"speaker": "Staff", "en": "It is steady at 22 degrees.", "th": "คงที่อยู่ที่ 22 องศาครับ"}]},
      {"title": "กล่องมีรอยบุบ", "lines": [{"speaker": "Staff", "en": "Two cartons arrived dented.", "th": "มีกล่องบุบมา 2 กล่องครับ"}, {"speaker": "Leader", "en": "Quarantine them and take photos.", "th": "กักแยกไว้แล้วถ่ายรูปเก็บไว้เลย"}]},
      {"title": "ยืมอุปกรณ์ลากพาเลท", "lines": [{"speaker": "Staff A", "en": "Are you using the pallet jack?", "th": "คุณใช้แฮนด์ลิฟต์อยู่ไหมครับ"}, {"speaker": "Staff B", "en": "No, you can take it now.", "th": "ไม่แล้วครับ เอาไปได้เลย"}]},
      {"title": "ส่งต่องานระหว่างกะ", "lines": [{"speaker": "Morning", "en": "We completed 500 units today.", "th": "กะเช้าเราทำเสร็จ 500 ชิ้นแล้ว"}, {"speaker": "Night", "en": "Got it. We will clear the rest.", "th": "รับทราบครับ เดี๋ยวเคลียร์ที่เหลือให้"}]},
      {"title": "สรุปรายงานรายวัน", "lines": [{"speaker": "Staff", "en": "The attendance summary is ready.", "th": "รายงานการเข้างานพร้อมแล้วครับ"}, {"speaker": "Leader", "en": "Upload it to Google Drive.", "th": "อัปโหลดเข้า Google Drive ได้เลย"}]}
    ],
    "exercises": [
      {"thai_prompt": "ฉันส่งเอกสารให้ลูกค้าเรียบร้อยแล้วเมื่อวานนี้", "prefix": "I", "suffix": "the document to the client yesterday.", "hint": "send เปลี่ยนเป็นอดีต (Past Simple)", "acceptable_answers": ["sent"], "correct_word": "sent", "full_sentence": "I sent the document to the client yesterday.", "explanation": "เหตุการณ์ในอดีต (yesterday) ใช้กริยาช่อง 2 คือ sent"},
      {"thai_prompt": "พวกเรากำลังตรวจสอบสต็อกสินค้าอยู่ในขณะนี้", "prefix": "We are currently", "suffix": "the inventory in the warehouse.", "hint": "check ในรูปกำลังกระทำ (V.ing)", "acceptable_answers": ["checking"], "correct_word": "checking", "full_sentence": "We are currently checking the inventory in the warehouse.", "explanation": "กำลังกระทำอยู่ใช้ is/am/are + V.ing"},
      {"thai_prompt": "ฉันจะแจ้งให้คุณทราบทันทีที่มีข้อมูลอัปเดต", "prefix": "I will", "suffix": "you know as soon as there is an update.", "hint": "คำกริยาแปลว่า ปล่อย/ให้ (l...)", "acceptable_answers": ["let"], "correct_word": "let", "full_sentence": "I will let you know as soon as there is an update.", "explanation": "'let you know' แปลว่า แจ้งให้คุณทราบ"},
      {"thai_prompt": "เครื่องจักรหยุดทำงานเนื่องจากเหตุขัดข้องทางเทคนิค", "prefix": "The machine stopped running", "suffix": "to technical issues.", "hint": "คำเชื่อมแปลว่า เนื่องจาก (d...)", "acceptable_answers": ["due"], "correct_word": "due", "full_sentence": "The machine stopped running due to technical issues.", "explanation": "'due to' แปลว่า เนื่องจาก ตามด้วยคำนาม"},
      {"thai_prompt": "ช่วยยืนยันการรับสินค้าล็อตนี้ให้ด้วยครับ", "prefix": "Could you please", "suffix": "receipt of this shipment?", "hint": "คำกริยาแปลว่า ยืนยัน (c...)", "acceptable_answers": ["confirm"], "correct_word": "confirm", "full_sentence": "Could you please confirm receipt of this shipment?", "explanation": "'confirm receipt' แปลว่า ยืนยันการรับของ"},
      {"thai_prompt": "ทุกอย่างดำเนินไปตามกำหนดการที่วางไว้", "prefix": "Everything is running according to", "suffix": ".", "hint": "คำนามแปลว่า กำหนดการ (s...)", "acceptable_answers": ["schedule"], "correct_word": "schedule", "full_sentence": "Everything is running according to schedule.", "explanation": "'according to schedule' แปลว่า ตามกำหนดการ"},
      {"thai_prompt": "รถขนส่งสินค้ามาถึงที่ท่าเทียบรับสินค้าเรียบร้อยแล้ว", "prefix": "The truck has arrived at the loading", "suffix": ".", "hint": "คำแปลว่า ท่าเทียบโหลดของ (d...)", "acceptable_answers": ["dock"], "correct_word": "dock", "full_sentence": "The truck has arrived at the loading dock.", "explanation": "'loading dock' แปลว่า ท่าขนถ่ายสินค้า"},
      {"thai_prompt": "กรุณาติดฉลากบาร์โค้ดลงบนทุกกล่องอย่างระมัดระวัง", "prefix": "Please", "suffix": "a barcode on every carton carefully.", "hint": "คำกริยาแปลว่า ติดฉลาก (l...)", "acceptable_answers": ["label"], "correct_word": "label", "full_sentence": "Please label a barcode on every carton carefully.", "explanation": "'label' ใช้เป็นกริยาแปลว่า ติดฉลาก"},
      {"thai_prompt": "เราจำเป็นต้องเก็บชิ้นส่วนที่มีตำหนิไว้ในพื้นที่กักแยก", "prefix": "We must put defective parts in the", "suffix": "area.", "hint": "พื้นที่กักกัน/แยกของ (q...)", "acceptable_answers": ["quarantine"], "correct_word": "quarantine", "full_sentence": "We must put defective parts in the quarantine area.", "explanation": "'quarantine area' คือพื้นที่กักแยกสินค้า"},
      {"thai_prompt": "พวกเราทำงานล่าช้ากว่ากำหนดการเดิมเล็กน้อยในวันนี้", "prefix": "We are running slightly", "suffix": "schedule today.", "hint": "คำบุพบทแปลว่า ช้ากว่า/อยู่หลัง (b...)", "acceptable_answers": ["behind"], "correct_word": "behind", "full_sentence": "We are running slightly behind schedule today.", "explanation": "'behind schedule' แปลว่า ช้ากว่ากำหนดการ"}
    ],
    "stories": [
      {
        "title": "Too Much Foam",
        "image_url": "https://images.unsplash.com/photo-1545173168-9f1947eebb7f?w=900&auto=format&fit=crop&q=80",
        "vocab_list": [{"word": "washing machine", "pos": "n.", "th": "เครื่องซักผ้า"}, {"word": "break", "pos": "v.", "th": "เสีย/พัง"}, {"word": "laundromat", "pos": "n.", "th": "ร้านซักผ้าหยอดเหรียญ"}, {"word": "foam", "pos": "n.", "th": "ฟองสบู่"}],
        "story_en": "Eric’s <b>washing machine breaks</b>, so he visits a <b>laundromat</b>. He puts clothes into a machine, adds soap, and presses Start. Minutes later, <b>foam</b> pours onto the floor.<br><br>The staff turns it off and points to his bottle: “That is dish soap, not laundry detergent!”",
        "story_en_plain": "Eric’s washing machine breaks, so he visits a laundromat. He puts clothes into a machine, adds soap, and presses Start. Minutes later, foam pours onto the floor. The staff turns it off and points to his bottle: That is dish soap, not laundry detergent!",
        "story_th": "เครื่องซักผ้าของอีริกพัง เขาจึงไปร้านซักผ้าหยอดเหรียญ เขาใส่ผ้า เติมน้ำยา แล้วกดเริ่ม ไม่กี่นาทีต่อมาฟองไหลทะลักเต็มพื้น พนักงานรีบมาปิดแล้วชี้ขวดในมือเขา: นั่นมันน้ำยาล้างจาน ไม่ใช่น้ำยาซักผ้า!"
      },
      {
        "title": "The Power Cut",
        "image_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=900&auto=format&fit=crop&q=80",
        "vocab_list": [{"word": "apartment", "pos": "n.", "th": "อพาร์ตเมนต์"}, {"word": "suddenly", "pos": "adv.", "th": "กะทันหัน"}, {"word": "flashlight", "pos": "n.", "th": "ไฟฉาย"}, {"word": "neighbor", "pos": "n.", "th": "เพื่อนบ้าน"}],
        "story_en": "At eight o'clock, the lights in Maya's <b>apartment</b> <b>suddenly</b> go out. She grabs a <b>flashlight</b> and walks out to meet her <b>neighbors</b>.<br><br>Without internet, they share snacks and tell stories under candlelight, enjoying the cozy evening together.",
        "story_en_plain": "At eight o'clock, the lights in Maya's apartment suddenly go out. She grabs a flashlight and walks out to meet her neighbors. Without internet, they share snacks and tell stories under candlelight, enjoying the cozy evening together.",
        "story_th": "ตอนสองทุ่ม ไฟในอพาร์ตเมนต์ของมายาดับลงกะทันหัน เธอคว้าไฟฉายเดินออกไปเจอเพื่อนบ้าน เมื่อไม่มีเน็ต ทุกคนจึงแบ่งขนมและเล่าเรื่องสนุกสนานใต้แสงเทียนอย่างมีความสุข"
      },
      {
        "title": "The Missing Barcode",
        "image_url": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=900&auto=format&fit=crop&q=80",
        "vocab_list": [{"word": "scanner", "pos": "n.", "th": "เครื่องสแกน"}, {"word": "carton", "pos": "n.", "th": "กล่องลัง"}, {"word": "smudge", "pos": "v.", "th": "เปื้อนเลอะ"}, {"word": "serial number", "pos": "n.", "th": "หมายเลขลำดับ"}],
        "story_en": "Sam's <b>scanner</b> fails because the <b>carton</b> barcode is wet and <b>smudged</b>. The truck departs soon.<br><br>He calmly reads the tiny <b>serial number</b>, keys it into the system manually, prints a new label, and loads the box safely.",
        "story_en_plain": "Sam's scanner fails because the carton barcode is wet and smudged. The truck departs soon. He calmly reads the tiny serial number, keys it into the system manually, prints a new label, and loads the box safely.",
        "story_th": "เครื่องสแกนของแซมอ่านไม่ได้เพราะบาร์โค้ดบนกล่องเปียกและเปื้อนหมึก ขณะที่รถบรรทุกใกล้จะออก เขาตั้งสติอ่านเลขซีเรียลตัวจิ๋ว พิมพ์เข้าระบบ สั่งพิมพ์ฉลากใหม่ แล้วยกของขึ้นรถได้ทันเวลา"
      },
      {
        "title": "A Warm Cup of Coffee",
        "image_url": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=900&auto=format&fit=crop&q=80",
        "vocab_list": [{"word": "exhausted", "pos": "adj.", "th": "เหนื่อยล้ามาก"}, {"word": "shift", "pos": "n.", "th": "กะการทำงาน"}, {"word": "colleague", "pos": "n.", "th": "เพื่อนร่วมงาน"}, {"word": "recharge", "pos": "v.", "th": "เติมพลัง"}],
        "story_en": "After an eight-hour <b>shift</b> counting boxes in Room A1, Tom is <b>exhausted</b>.<br><br>His <b>colleague</b> Sarah hands him a warm cup of coffee with a smile: “Great work today!” That simple kindness <b>recharges</b> his spirit instantly.",
        "story_en_plain": "After an eight-hour shift counting boxes in Room A1, Tom is exhausted. His colleague Sarah hands him a warm cup of coffee with a smile: Great work today! That simple kindness recharges his spirit instantly.",
        "story_th": "หลังจบกะ 8 ชั่วโมงตรวจนับกล่องในห้อง A1 ทอมเหนื่อยล้ามาก ซาร่าเพื่อนร่วมงานยื่นกาแฟอุ่นๆ พร้อมรอยยิ้ม: วันนี้ทำได้ยอดเยี่ยมมาก! น้ำใจเล็กๆ ช่วยเติมพลังให้เขาทันที"
      }
    ]
  }
}

# -----------------------------------------------------------------------------
# 3. Robust Hybrid Loader (ตรวจหาไฟล์ ถ้าไม่พบสลับใช้ Built-in Data ทันที)
# -----------------------------------------------------------------------------
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
    """โหลดจาก data/lessons.json ถ้าหาไม่เจอหรืออ่านไม่ได้ จะสลับใช้ BUILTIN_WEEK_1 ทันที"""
    curriculum_data = {}
    
    # พยายามโหลดจากไฟล์จริงบนดิสก์
    if os.path.exists(LESSONS_FILE):
        try:
            with open(LESSONS_FILE, "r", encoding="utf-8") as f:
                curriculum_data = json.load(f)
        except Exception:
            pass

    # ผสานข้อมูล Built-in เพื่อให้แน่ใจว่าสัปดาห์แรกมีข้อมูลครบแน่นอนเสมอ
    for day_k, day_v in BUILTIN_WEEK_1.items():
        if day_k not in curriculum_data:
            curriculum_data[day_k] = day_v
            
    return curriculum_data

if "user_data" not in st.session_state:
    st.session_state.user_data = load_progress()

completed_days = set(st.session_state.user_data.get("completed_days", []))

# -----------------------------------------------------------------------------
# 4. Enhanced Audio Booster Engine (Web Audio API 2.5x)
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
        st.caption("⚠️ ไม่สามารถประมวลผลเสียงได้")
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
    components.html(html_code, height=44)

# -----------------------------------------------------------------------------
# 5. AI Writing & Grammar Coach (Gemini 3.6 Flash)
# -----------------------------------------------------------------------------
def analyze_with_ai(text_to_check: str, api_key: str) -> str:
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        prompt = f"""
        คุณคือผู้เชี่ยวชาญการสอนภาษาอังกฤษเพื่อการสื่อสารในโรงงานและออฟฟิศระดับสากล กรุณาตรวจประโยคภาษาอังกฤษด้านล่างนี้:
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
# 7. Main Learning Dashboard
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
        "🤖 AI Writing Coach"
    ])

    # ---------------------------------------------------------
    # TAB 1: 20 Vocabulary & Idioms
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # TAB 2: 20 Speaking Phrases Drill
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # TAB 3: 10 Workplace Dialogue Scenarios
    # ---------------------------------------------------------
    with tabs[2]:
        st.subheader("บทสนทนาจำลองสถานการณ์การทำงานจริง (10 ฉากสนทนา)")
        dialogues = lesson.get("dialogues", [])
        if dialogues:
            for s_idx, scene in enumerate(dialogues):
                with st.expander(f"📍 ฉากที่ {s_idx+1}: {scene['title']}", expanded=(s_idx==0)):
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

    # ---------------------------------------------------------
    # TAB 4: 10 Fill-in-the-Blank Exercises
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # TAB 5: 4 Short Stories with Illustrations
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # TAB 6: AI Writing Coach
    # ---------------------------------------------------------
    with tabs[5]:
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
