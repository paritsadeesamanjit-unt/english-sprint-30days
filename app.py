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
# 2. Helper Data Builders
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
# 3. Complete Week 1 Dataset (Days 1 - 7: 100% Unique Content)
# -----------------------------------------------------------------------------
WEEK_1_DATA = {
    "1": {
        "day": 1,
        "title": "Day 1: Sentence Framework (S + V + O) & 3 Core Tenses",
        "summary": "ปูพื้นฐานประโยค 3 กาลหลักที่ใช้บ่อยที่สุดในการทำงาน (Present Simple, Continuous, Future)",
        "rule": "Present Simple (ทำประจำ) | Present Continuous (กำลังทำขณะนี้) | Future Simple (จะทำในอนาคต)",
        "vocab": make_vocab([
            ("Inventory", "/ˈɪn.vən.tɔːr.i/", "n.", "สินค้าคงคลัง / สต็อก", "We check inventory every morning.", "เราตรวจเช็คสต็อกทุกเช้า"),
            ("Urgent", "/ˈɜː.dʒənt/", "adj.", "เร่งด่วน / ฉุกเฉิน", "This is an urgent delivery.", "นี่คือการส่งสินค้าแบบเร่งด่วน"),
            ("Discrepancy", "/dɪˈskrep.ən.si/", "n.", "ยอดคลาดเคลื่อน / ไม่ตรงกัน", "We found a minor discrepancy.", "เราพบความคลาดเคลื่อนเล็กน้อย"),
            ("Finalize", "/ˈfaɪ.nəl.aɪz/", "v.", "สรุปผล / ทำเสร็จสมบูรณ์", "I will finalize the report today.", "ฉันจะสรุปรายงานให้เสร็จวันนี้"),
            ("Inspect", "/ɪnˈspekt/", "v.", "ตรวจสอบ / ตรวจตรา", "Please inspect the goods carefully.", "โปรดตรวจสอบสินค้าอย่างระมัดระวัง"),
            ("Schedule", "/ˈskedʒ.uːl/", "n./v.", "กำหนดการ / ตารางเวลา", "Everything is on schedule.", "ทุกอย่างเป็นไปตามกำหนดการ"),
            ("Operate", "/ˈɒp.ər.eɪt/", "v.", "เดินเครื่อง / ปฏิบัติการ", "He operates this machine daily.", "เขาเดินเครื่องจักรนี้ทุกวัน"),
            ("Maintenance", "/ˈmeɪn.tən.əns/", "n.", "การบำรุงรักษา", "Regular maintenance prevents stops.", "การบำรุงรักษาช่วยป้องกันเครื่องหยุด"),
            ("Shipment", "/ˈʃɪp.mənt/", "n.", "การจัดส่ง / ล็อตส่งสินค้า", "The shipment arrived on time.", "สินค้าล็อตส่งมาถึงตรงเวลา"),
            ("Warehouse", "/ˈweə.haʊs/", "n.", "คลังสินค้า / โกดัง", "The warehouse is well organized.", "คลังสินค้าจัดระเบียบอย่างดี"),
            ("Defect", "/ˈdiː.fekt/", "n.", "ตำหนิ / ของเสีย", "Zero defect is our ultimate goal.", "ของเสียเป็นศูนย์คือเป้าหมายหลัก"),
            ("Quantity", "/ˈkwɒn.tə.ti/", "n.", "จำนวน / ปริมาณ", "Check the order quantity again.", "ตรวจทานจำนวนสั่งซื้ออีกครั้ง"),
            ("Approve", "/əˈpruːv/", "v.", "อนุมัติ / เห็นชอบ", "The manager approved the request.", "ผู้จัดการอนุมัติคำขอแล้ว"),
            ("Deliver", "/dɪˈlɪv.ər/", "v.", "ส่งมอบ / นำส่ง", "We deliver goods within 24 hours.", "เราส่งมอบสินค้าภายใน 24 ชม."),
            ("Supplier", "/səˈplaɪ.ər/", "n.", "ผู้จัดส่งวัตถุดิบ", "Our supplier sent quality parts.", "ซัพพลายเออร์ส่งชิ้นส่วนคุณภาพดี"),
            ("Pallet", "/ˈpæl.ət/", "n.", "พาเลทวางสินค้า", "Stack the boxes onto the pallet.", "วางกล่องซ้อนลงบนพาเลท"),
            ("Confirm", "/kənˈfɜːm/", "v.", "ยืนยัน", "Please confirm the delivery time.", "โปรดยืนยันเวลาส่งมอบ"),
            ("Label", "/ˈleɪ.bəl/", "n./v.", "ฉลาก / ติดป้ายระบุ", "Label each carton with a barcode.", "ติดฉลากบาร์โค้ดลงบนทุกกล่อง"),
            ("Storage", "/ˈstɔː.rɪdʒ/", "n.", "การจัดเก็บ / พื้นที่เก็บ", "Room A1 is our cold storage room.", "ห้อง A1 คือห้องจัดเก็บควบคุมอุณหภูมิ"),
            ("Dispatch", "/dɪˈspætʃ/", "v./n.", "ส่งของออกไป / การปล่อยรถ", "We dispatch five trucks daily.", "เราปล่อยรถขนส่งสินค้าวันละ 5 คัน")
        ]),
        "phrases": make_phrases([
            ("I am working on the daily report right now.", "ฉันกำลังทำรายงานประจำวันอยู่ตอนนี้", "เน้นเสียงที่ working และ report"),
            ("I will send you the updated file this afternoon.", "ฉันจะส่งไฟล์ที่อัปเดตให้คุณบ่ายวันนี้", "ย่อ I will เป็น I'll /aɪl/"),
            ("The team usually reviews the inventory every morning.", "ทีมมักจะตรวจสอบสต็อกสินค้าทุกๆ เช้า", "usually ลงเสียงหนักพยางค์แรก"),
            ("We completed the urgent shipment yesterday.", "พวกเราจัดการการจัดส่งด่วนเสร็จเรียบร้อยเมื่อวานนี้", "completed ลงท้ายเสียง /t/"),
            ("Could you please confirm receipt of the goods?", "ช่วยยืนยันการรับสินค้าให้หน่อยได้ไหมครับ", "receipt ไม่ออกเสียงตัว p (/rɪˈsiːt/)"),
            ("The production line is running smoothly today.", "สายการผลิตวันนี้กำลังดำเนินไปอย่างราบรื่นครับ", "smoothly ออกเสียง th แบบแลบลิ้น"),
            ("We noticed a minor issue during the morning shift.", "เราสังเกตเห็นปัญหาเล็กน้อยในระหว่างกะเช้าครับ", "noticed ลงท้ายเสียง /t/"),
            ("I will let you know as soon as the batch is ready.", "ฉันจะแจ้งให้คุณทราบทันทีที่ล็อตสินค้าพร้อมครับ", "เชื่อมเสียง as soon as /əz-suːn-əz/"),
            ("Please stack the pallets against the wall.", "ช่วยวางซ้อนพาเลทชิดผนังด้วยครับ", "stack the pallets เชื่อมเสียง k กับ th"),
            ("Did you verify the serial numbers on the boxes?", "คุณได้ตรวจสอบหมายเลขซีเรียลบนกล่องแล้วหรือยังครับ", "verify ออกเสียง /ˈver.ɪ.faɪ/"),
            ("We are currently organizing Temperature Room A1.", "ตอนนี้พวกเรากำลังจัดระเบียบห้องควบคุมอุณหภูมิ A1 ครับ", "currently ออกเสียง 3 พยางค์"),
            ("The courier is waiting at the loading dock.", "คนขับรถขนส่งกำลังรออยู่ที่จุดเทียบรับสินค้าครับ", "loading dock = ท่าขนถ่ายสินค้า"),
            ("I need to print out the barcode labels immediately.", "ผมจำเป็นต้องพิมพ์ป้ายบาร์โค้ดออกมาทันทีครับ", "print out เชื่อมเสียงเป็น /prɪn-taʊt/"),
            ("How many boxes are left on this rack?", "มีกล่องเหลืออยู่บนแร็คนี้อีกกี่กล่องครับ", "left on เชื่อมเสียง t กับ on"),
            ("All raw materials have arrived in good condition.", "วัตถุดิบทั้งหมดมาถึงในสภาพสมบูรณ์เรียบร้อยครับ", "in good condition = สภาพดีเยี่ยม"),
            ("We must follow the safety guidelines strictly.", "พวกเราต้องปฏิบัติตามกฎความปลอดภัยอย่างเคร่งครัด", "strictly ลงท้ายด้วย /li/"),
            ("I checked the physical count against the Excel sheet.", "ผมตรวจสอบยอดนับจริงเทียบกับตาราง Excel แล้วครับ", "against the sheet = เทียบกับตาราง"),
            ("The forklift is undergoing regular maintenance.", "รถโฟล์คลิฟต์กำลังอยู่ระหว่างการบำรุงรักษาตามรอบครับ", "forklift ออกเสียง /ˈfɔːk.lɪft/"),
            ("Please wear your safety helmet before entering.", "กรุณาสวมหมวกนิรภัยก่อนเข้าไปด้านในครับ", "safety helmet = หมวกนิรภัย"),
            ("Let me double-check the packing list once more.", "ขอให้ผมตรวจทานใบรายการบรรจุภัณฑ์อีกสักครั้งนะครับ", "double-check = ตรวจทานซ้ำ")
        ]),
        "dialogues": make_dialogues([
            ("ตรวจนับสต็อกเช้า", [("Leader", "How is the inventory check going?", "การตรวจนับสต็อกเป็นอย่างไรบ้าง"), ("Staff", "We are counting Rack 1 to 3 right now.", "กำลังนับแร็ค 1 ถึง 3 อยู่ครับ")]),
            ("แจ้งยอดคลาดเคลื่อน", [("Staff", "There is a discrepancy of 10 boxes.", "พบยอดคลาดเคลื่อน 10 กล่องครับ"), ("Leader", "Check the dispatch log immediately.", "ไปตรวจสมุดส่งของทันทีเลย")]),
            ("สินค้าด่วนลูกค้า", [("CS", "This urgent order must leave by noon.", "ออเดอร์ด่วนนี้ต้องส่งออกก่อนเที่ยงค่ะ"), ("Staff", "Understood. We will pick it first.", "รับทราบครับ เดี๋ยวหยิบให้ก่อนเลย")]),
            ("รถรับสินค้ามาถึง", [("Driver", "I am here for the shipment.", "ผมมารับสินค้าล็อตนี้ครับ"), ("Staff", "Please park at Dock 4.", "รบกวนถอยเข้าช่องจอด 4 เลยครับ")]),
            ("บาร์โค้ดชำรุด", [("Worker", "The barcode label is torn.", "ฉลากบาร์โค้ดฉีกขาดครับ"), ("Leader", "Print a replacement label now.", "สั่งพิมพ์ฉลากใหม่ออกมาติดเลย")]),
            ("ตรวจอุณหภูมิห้อง A1", [("QA", "What is the temperature in Room A1?", "อุณหภูมิในห้อง A1 เท่าไหร่ครับ"), ("Staff", "It is steady at 22 degrees.", "คงที่อยู่ที่ 22 องศาครับ")]),
            ("กล่องมีรอยบุบ", [("Staff", "Two cartons arrived dented.", "มีกล่องบุบมา 2 กล่องครับ"), ("Leader", "Quarantine them and take photos.", "กักแยกไว้แล้วถ่ายรูปเก็บไว้เลย")]),
            ("ยืมอุปกรณ์ลากพาเลท", [("Staff A", "Are you using the pallet jack?", "คุณใช้แฮนด์ลิฟต์อยู่ไหมครับ"), ("Staff B", "No, you can take it now.", "ไม่แล้วครับ เอาไปได้เลย")]),
            ("ส่งต่องานระหว่างกะ", [("Morning", "We completed 500 units today.", "กะเช้าเราทำเสร็จ 500 ชิ้นแล้ว"), ("Night", "Got it. We will clear the rest.", "รับทราบครับ เดี๋ยวเคลียร์ที่เหลือให้")]),
            ("สรุปรายงานรายวัน", [("Staff", "The attendance summary is ready.", "รายงานการเข้างานพร้อมแล้วครับ"), ("Leader", "Upload it to Google Drive.", "อัปโหลดเข้า Google Drive ได้เลย")])
        ]),
        "exercises": make_exercises([
            ("ฉันส่งเอกสารให้ลูกค้าเรียบร้อยแล้วเมื่อวานนี้", "I", "the document to the client yesterday.", "send เปลี่ยนเป็นอดีต (Past Simple)", "sent", ["already sent"], "I sent the document to the client yesterday.", "เหตุการณ์ในอดีต (yesterday) ใช้กริยาช่อง 2 คือ sent"),
            ("พวกเรากำลังตรวจสอบสต็อกสินค้าอยู่ในขณะนี้", "We are currently", "the inventory in the warehouse.", "check ในรูปกำลังกระทำ (V.ing)", "checking", ["reviewing"], "We are currently checking the inventory in the warehouse.", "กำลังกระทำอยู่ใช้ is/am/are + V.ing"),
            ("ฉันจะแจ้งให้คุณทราบทันทีที่มีข้อมูลอัปเดต", "I will", "you know as soon as there is an update.", "คำกริยาแปลว่า ปล่อย/ให้ (l...)", "let", [], "I will let you know as soon as there is an update.", "'let you know' แปลว่า แจ้งให้คุณทราบ"),
            ("เครื่องจักรหยุดทำงานเนื่องจากเหตุขัดข้องทางเทคนิค", "The machine stopped running", "to technical issues.", "คำเชื่อมแปลว่า เนื่องจาก (d...)", "due", [], "The machine stopped running due to technical issues.", "'due to' แปลว่า เนื่องจาก ตามด้วยคำนาม"),
            ("ช่วยยืนยันการรับสินค้าล็อตนี้ให้ด้วยครับ", "Could you please", "receipt of this shipment?", "คำกริยาแปลว่า ยืนยัน (c...)", "confirm", ["verify"], "Could you please confirm receipt of this shipment?", "'confirm receipt' แปลว่า ยืนยันการรับของ"),
            ("ทุกอย่างดำเนินไปตามกำหนดการที่วางไว้", "Everything is running according to", ".", "คำนามแปลว่า กำหนดการ (s...)", "schedule", ["plan"], "Everything is running according to schedule.", "'according to schedule' แปลว่า ตามกำหนดการ"),
            ("รถขนส่งสินค้ามาถึงที่ท่าเทียบรับสินค้าเรียบร้อยแล้ว", "The truck has arrived at the loading", ".", "คำแปลว่า ท่าเทียบโหลดของ (d...)", "dock", ["bay"], "The truck has arrived at the loading dock.", "'loading dock' แปลว่า ท่าขนถ่ายสินค้า"),
            ("กรุณาติดฉลากบาร์โค้ดลงบนทุกกล่องอย่างระมัดระวัง", "Please", "a barcode on every carton carefully.", "คำกริยาแปลว่า ติดฉลาก (l...)", "label", ["attach"], "Please label a barcode on every carton carefully.", "'label' ใช้เป็นกริยาแปลว่า ติดฉลาก"),
            ("เราจำเป็นต้องเก็บชิ้นส่วนที่มีตำหนิไว้ในพื้นที่กักแยก", "We must put defective parts in the", "area.", "พื้นที่กักกัน/แยกของ (q...)", "quarantine", ["isolated"], "We must put defective parts in the quarantine area.", "'quarantine area' คือพื้นที่กักแยกสินค้า"),
            ("พวกเราทำงานล่าช้ากว่ากำหนดการเดิมเล็กน้อยในวันนี้", "We are running slightly", "schedule today.", "คำบุพบทแปลว่า ช้ากว่า/อยู่หลัง (b...)", "behind", [], "We are running slightly behind schedule today.", "'behind schedule' แปลว่า ช้ากว่ากำหนดการ")
        ]),
        "stories": make_stories([
            ("Too Much Foam", "https://images.unsplash.com/photo-1545173168-9f1947eebb7f?w=900&auto=format&fit=crop&q=80",
             [("washing machine", "n.", "เครื่องซักผ้า"), ("break", "v.", "เสีย/พัง"), ("laundromat", "n.", "ร้านซักผ้าหยอดเหรียญ"), ("foam", "n.", "ฟองสบู่")],
             "Eric’s <b>washing machine breaks</b>, so he visits a <b>laundromat</b>. He puts clothes into a machine, adds soap, and presses Start. Minutes later, <b>foam</b> pours onto the floor.<br><br>The staff turns it off and points to his bottle: “That is dish soap, not laundry detergent!”",
             "Eric’s washing machine breaks, so he visits a laundromat. He puts clothes into a machine, adds soap, and presses Start. Minutes later, foam pours onto the floor. The staff turns it off and points to his bottle: That is dish soap, not laundry detergent!",
             "เครื่องซักผ้าของอีริกพัง เขาจึงไปร้านซักผ้าหยอดเหรียญ เขาใส่ผ้า เติมน้ำยา แล้วกดเริ่ม ไม่กี่นาทีต่อมาฟองไหลทะลักเต็มพื้น พนักงานรีบมาปิดแล้วชี้ขวดในมือเขา: นั่นมันน้ำยาล้างจาน ไม่ใช่น้ำยาซักผ้า!"),
            ("The Power Cut", "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=900&auto=format&fit=crop&q=80",
             [("apartment", "n.", "อพาร์ตเมนต์"), ("suddenly", "adv.", "กะทันหัน"), ("flashlight", "n.", "ไฟฉาย"), ("neighbor", "n.", "เพื่อนบ้าน")],
             "At eight o'clock, the lights in Maya's <b>apartment</b> <b>suddenly</b> go out. She grabs a <b>flashlight</b> and walks out to meet her <b>neighbors</b>.<br><br>Without internet, they share snacks and tell stories under candlelight, enjoying the cozy evening together.",
             "At eight o'clock, the lights in Maya's apartment suddenly go out. She grabs a flashlight and walks out to meet her neighbors. Without internet, they share snacks and tell stories under candlelight, enjoying the cozy evening together.",
             "ตอนสองทุ่ม ไฟในอพาร์ตเมนต์ของมายาดับลงกะทันหัน เธอคว้าไฟฉายเดินออกไปเจอเพื่อนบ้าน เมื่อไม่มีเน็ต ทุกคนจึงแบ่งขนมและเล่าเรื่องสนุกสนานใต้แสงเทียนอย่างมีความสุข"),
            ("The Missing Barcode", "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=900&auto=format&fit=crop&q=80",
             [("scanner", "n.", "เครื่องสแกน"), ("carton", "n.", "กล่องลัง"), ("smudge", "v.", "เปื้อนเลอะ"), ("serial number", "n.", "หมายเลขลำดับ")],
             "Sam's <b>scanner</b> fails because the <b>carton</b> barcode is wet and <b>smudged</b>. The truck departs soon.<br><br>He calmly reads the tiny <b>serial number</b>, keys it into the system manually, prints a new label, and loads the box safely.",
             "Sam's scanner fails because the carton barcode is wet and smudged. The truck departs soon. He calmly reads the tiny serial number, keys it into the system manually, prints a new label, and loads the box safely.",
             "เครื่องสแกนของแซมอ่านไม่ได้เพราะบาร์โค้ดบนกล่องเปียกและเปื้อนหมึก ขณะที่รถบรรทุกใกล้จะออก เขาตั้งสติอ่านเลขซีเรียลตัวจิ๋ว พิมพ์เข้าระบบ สั่งพิมพ์ฉลากใหม่ แล้วยกของขึ้นรถได้ทันเวลา"),
            ("A Warm Cup of Coffee", "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=900&auto=format&fit=crop&q=80",
             [("exhausted", "adj.", "เหนื่อยล้ามาก"), ("shift", "n.", "กะการทำงาน"), ("colleague", "n.", "เพื่อนร่วมงาน"), ("recharge", "v.", "เติมพลัง")],
             "After an eight-hour <b>shift</b> counting boxes in Room A1, Tom is <b>exhausted</b>.<br><br>His <b>colleague</b> Sarah hands him a warm cup of coffee with a smile: “Great work today!” That simple kindness <b>recharges</b> his spirit instantly.",
             "After an eight-hour shift counting boxes in Room A1, Tom is exhausted. His colleague Sarah hands him a warm cup of coffee with a smile: Great work today! That simple kindness recharges his spirit instantly.",
             "หลังจบกะ 8 ชั่วโมงตรวจนับกล่องในห้อง A1 ทอมเหนื่อยล้ามาก ซาร่าเพื่อนร่วมงานยื่นกาแฟอุ่นๆ พร้อมรอยยิ้ม: วันนี้ทำได้ยอดเยี่ยมมาก! น้ำใจเล็กๆ ช่วยเติมพลังให้เขาทันที")
        ])
    },
    "2": {
        "day": 2,
        "title": "Day 2: Polite Requests & Inquiries",
        "summary": "เทคนิคการขอความช่วยเหลือ การสอบถาม และประสานงานอย่างมืออาชีพ",
        "rule": "ใช้ Could you please... หรือ Would you mind... แทนการออกคำสั่งตรงๆ",
        "vocab": make_vocab([
            ("Clarify", "/ˈklær.ɪ.faɪ/", "v.", "ชี้แจง / อธิบายให้กระจ่าง", "Could you clarify this point?", "ช่วยชี้แจงประเด็นนี้หน่อยได้ไหมครับ"),
            ("Appreciate", "/əˈpriː.ʃi.eɪt/", "v.", "ซาบซึ้ง / ขอบคุณ", "I appreciate your quick help.", "ผมขอบคุณสำหรับความช่วยเหลืออันรวดเร็ว"),
            ("Assistance", "/əˈsɪs.təns/", "n.", "ความช่วยเหลือ", "Thank you for your assistance.", "ขอบคุณสำหรับความช่วยเหลือครับ"),
            ("Prompt", "/prɒmpt/", "adj.", "รวดเร็ว / ทันเวลา", "Thank you for the prompt reply.", "ขอบคุณสำหรับการตอบกลับอย่างรวดเร็ว"),
            ("Convenient", "/kənˈviː.ni.ənt/", "adj.", "สะดวก", "Call me when it is convenient.", "โทรหาผมเมื่อสะดวกนะครับ"),
            ("Inquire", "/ɪnˈkwaɪər/", "v.", "สอบถาม / ขอข้อมูล", "I am calling to inquire about pricing.", "ผมโทรมาเพื่อสอบถามเรื่องราคา"),
            ("Attachment", "/əˈtætʃ.mənt/", "n.", "ไฟล์แนบ", "Please see the attachment.", "โปรดดูรายละเอียดในไฟล์แนบครับ"),
            ("Resend", "/ˌriːˈsend/", "v.", "ส่งใหม่อีกครั้ง", "Could you please resend the file?", "ช่วยส่งไฟล์ใหม่อีกรอบได้ไหมครับ"),
            ("Regarding", "/rɪˈɡɑː.dɪŋ/", "prep.", "เกี่ยวกับ / ในเรื่องของ", "I have a question regarding safety.", "ผมมีคำถามเกี่ยวกับความปลอดภัย"),
            ("Forward", "/ˈfɔː.wəd/", "v.", "ส่งต่อ (อีเมล/ข้อความ)", "Please forward this email to Jane.", "ช่วยส่งต่ออีเมลนี้ให้เจนด้วยครับ"),
            ("Requirement", "/rɪˈkwaɪə.mənt/", "n.", "ข้อกำหนด / ความต้องการ", "Does it meet customer requirements?", "มันตรงตามข้อกำหนดลูกค้าไหม"),
            ("Permission", "/pəˈmɪʃ.ən/", "n.", "การอนุญาต", "You need permission to enter.", "คุณต้องได้รับอนุญาตก่อนเข้าพื้นที่"),
            ("Feedback", "/ˈfiːd.bæk/", "n.", "ข้อเสนอแนะ / คำติชม", "We welcome your honest feedback.", "เรายินดีรับฟังข้อเสนอแนะที่จริงใจ"),
            ("Colleague", "/ˈkɒl.iːɡ/", "n.", "เพื่อนร่วมงาน", "My colleague will assist you.", "เพื่อนร่วมงานของผมจะช่วยดูแลคุณครับ"),
            ("Extend", "/ɪkˈstend/", "v.", "ขยายเวลา / ยืดออกไป", "Can we extend the deadline?", "เราขอขยายเวลาส่งงานได้ไหมครับ"),
            ("Authorize", "/ˈɔː.θər.aɪz/", "v.", "มอบอำนาจ / อนุมัติ", "He is authorized to sign.", "เขาได้รับมอบอำนาจให้เซ็นเอกสาร"),
            ("Verify", "/ˈver.ɪ.faɪ/", "v.", "ตรวจสอบยืนยัน", "Verify the numbers carefully.", "ตรวจสอบตัวเลขอย่างละเอียด"),
            ("Request", "/rɪˈkwest/", "n./v.", "คำขอ / ร้องขอ", "We received your request.", "พวกเราได้รับคำขอของคุณแล้ว"),
            ("Available", "/əˈveɪ.lə.bəl/", "adj.", "ว่าง / พร้อมใช้", "Is the supervisor available?", "หัวหน้างานว่างอยู่ไหมครับ"),
            ("Grateful", "/ˈɡreɪt.fəl/", "adj.", "รู้สึกขอบคุณยิ่ง", "I would be grateful for your advice.", "ผมจะขอบคุณมากสำหรับคำแนะนำ")
        ]),
        "phrases": make_phrases([
            ("Could you please clarify the delivery schedule?", "ช่วยชี้แจงกำหนดการจัดส่งสินค้าให้ชัดเจนได้ไหมครับ", "Could you please สุภาพกว่า Can you"),
            ("Would you mind checking this detail for me?", "รบกวนช่วยตรวจสอบรายละเอียดตรงนี้ให้หน่อยได้ไหมครับ", "หลัง Would you mind ตามด้วย V.ing เสมอ"),
            ("I would appreciate it if you could reply by today.", "จะขอบคุณมากหากคุณสามารถตอบกลับได้ภายในวันนี้", "ใช้เร่งงานอย่างสุภาพ"),
            ("May I ask for an update regarding the shipment?", "ขออนุญาตสอบถามความคืบหน้าเกี่ยวกับการจัดส่งได้ไหมครับ", "May I ask for สุภาพและเป็นทางการมาก"),
            ("Do you have five minutes for a quick sync?", "คุณสะดวกคุยสายสั้นๆ สัก 5 นาทีไหมครับ", "quick sync = ประชุมอัปเดตงานสั้นๆ"),
            ("Please let me know if you need any further information.", "แจ้งได้เลยนะครับหากต้องการข้อมูลเพิ่มเติม", "ประโยคปิดท้ายอีเมลยอดนิยม"),
            ("Could you resend the attachment? I did not receive it.", "ช่วยส่งไฟล์แนบมาใหม่อีกครั้งได้ไหมครับ พอดีผมยังไม่ได้รับ", "resend เน้นเสียง /riːˈsend/"),
            ("Would it be possible to arrange a meeting tomorrow?", "พอจะเป็นไปได้ไหมที่จะขอนัดประชุมวันพรุ่งนี้ครับ", "Would it be possible to... นุ่มนวลมาก"),
            ("Could you give me a hand with these heavy boxes?", "ช่วยผมยกกล่องหนักพวกนี้หน่อยได้ไหมครับ", "give me a hand = ช่วยเหลือ"),
            ("I was wondering if you could check this document.", "ผมอยากทราบว่าคุณพอจะช่วยดูเอกสารนี้ได้ไหมครับ", "I was wondering if... เป็นรูปขอร้องขั้นสูง"),
            ("May I borrow your scanner for just a few minutes?", "ขออนุญาตยืมเครื่องสแกนสักสองสามนาทีได้ไหมครับ", "borrow = ขอยืม"),
            ("Could you please forward the invoice to Accounting?", "ช่วยส่งต่อใบแจ้งหนี้ให้ฝ่ายบัญชีด้วยได้ไหมครับ", "forward to = ส่งต่อให้"),
            ("Would you mind speaking a little louder, please?", "รบกวนช่วยพูดดังขึ้นอีกนิดหนึ่งได้ไหมครับ", "speaking เติม -ing หลัง mind"),
            ("Could you kindly remind the team about the deadline?", "ช่วยกรุณาเตือนทีมงานเรื่องกำหนดส่งงานด้วยได้ไหมครับ", "Could you kindly... สุภาพและเป็นกันเอง"),
            ("May I have your approval on this overtime request?", "ขออนุมัติจากคุณสำหรับคำขอทำโอทีนี้ได้ไหมครับ", "approval = การอนุมัติ"),
            ("Could you show me how to use this software?", "ช่วยสอนวิธีใช้งานโปรแกรมนี้ให้ผมหน่อยได้ไหมครับ", "show me how to = สอนวิธีทำ"),
            ("I would be grateful if you could confirm by noon.", "จะยินดีเป็นอย่างยิ่งหากคุณยืนยันกลับมาภายในเที่ยงนี้", "grateful = รู้สึกขอบคุณ"),
            ("Could you please make sure the door is locked?", "ช่วยดูแลให้มั่นใจว่าประตูล็อคเรียบร้อยแล้วได้ไหมครับ", "make sure = ทำให้แน่ใจ"),
            ("Can you double-check the part number for me?", "ช่วยตรวจทานหมายเลขชิ้นส่วนซ้ำให้ผมหน่อยได้ไหมครับ", "double-check = ตรวจทานซ้ำ"),
            ("Thank you in advance for your kind cooperation.", "ขอบคุณล่วงหน้าสำหรับความร่วมมืออันดีของคุณครับ", "in advance = ล่วงหน้า")
        ]),
        "dialogues": make_dialogues([
            ("ขอให้ช่วยตรวจไฟล์", [("A", "Could you please check this Excel file for me?", "ช่วยดูไฟล์ Excel นี้ให้หน่อยได้ไหมครับ"), ("B", "Sure, send it over and I will look at it.", "ได้สิ ส่งมาเลยเดี๋ยวผมดูให้ครับ")]),
            ("ขอให้ส่งไฟล์แนบใหม่", [("Staff", "The attachment was missing in your email.", "ในอีเมลของคุณไม่มีไฟล์แนบมาด้วยครับ"), ("Vendor", "Sorry about that! I will resend it right now.", "ขอโทษด้วยครับ! เดี๋ยวผมรีบส่งใหม่ทันที")]),
            ("ขอนัดประชุม 5 นาที", [("Leader", "Do you have 5 minutes for a quick sync?", "คุณมีเวลาสัก 5 นาทีคุยกันสั้นๆ ไหม"), ("Staff", "Yes, I am available right now.", "ว่างครับ คุยตอนนี้ได้เลยครับ")]),
            ("ขอเข้าพบผู้จัดการ", [("Staff", "May I talk to the manager for a moment?", "ขออนุญาตคุยกับผู้จัดการสักครู่ได้ไหมครับ"), ("Admin", "He is in a meeting. Please wait until 2 PM.", "ท่านติดประชุมอยู่ค่ะ รบกวนรอถึงบ่ายสองนะคะ")]),
            ("ขอยืมเครื่องสแกน", [("Tom", "May I borrow your scanner for ten minutes?", "ขอยืมเครื่องสแกนของคุณสัก 10 นาทีได้ไหม"), ("Jack", "Go ahead, I am not using it right now.", "เอาไปได้เลย ตอนนี้ฉันไม่ได้ใช้อยู่พอดี")]),
            ("ขอให้ชี้แจงสเปก", [("Engineer", "Could you clarify the thickness tolerance?", "ช่วยชี้แจงเกณฑ์ความหนาที่ยอมรับได้หน่อยครับ"), ("QA", "It must be between 1.5 and 1.8 millimeters.", "ต้องอยู่ระหว่าง 1.5 ถึง 1.8 มิลลิเมตรครับ")]),
            ("ขอให้ช่วยยกของ", [("Worker A", "Could you give me a hand with this rack?", "ช่วยผมยกแร็คตัวนี้หน่อยได้ไหมครับ"), ("Worker B", "Hold on, let me put on my gloves first.", "รอแป๊บนะ ขอฉันใส่ถุงมือก่อน")]),
            ("ขอขยายเวลาส่งงาน", [("Leader", "Would it be possible to extend the deadline?", "พอจะเป็นไปได้ไหมที่จะขอขยายเวลาส่งมอบ"), ("Client", "We can grant you one extra day until Friday.", "เราขยายเวลาให้ได้อีก 1 วันจนถึงวันศุกร์ครับ")]),
            ("ขอให้เซ็นอนุมัติ", [("Staff", "Could you please sign off on this requisition?", "ช่วยลงนามอนุมัติใบเบิกของนี้ให้หน่อยครับ"), ("Supervisor", "Let me review the quantities first.", "ขอผมดูจำนวนรายการก่อนนะ")]),
            ("ขอความเห็นหลังพรีเซนต์", [("Presenter", "I would appreciate your feedback on my slides.", "ผมจะขอบคุณมากหากคุณให้ความเห็นเรื่องสไลด์"), ("Colleague", "They were clear and very easy to follow.", "สไลด์ชัดเจนและเข้าใจง่ายมากเลยครับ")])
        ]),
        "exercises": make_exercises([
            ("รบกวนช่วยตรวจสอบรายละเอียดตรงนี้ให้หน่อยได้ไหมครับ", "Would you mind", "this detail for me?", "check หลัง Would you mind ต้องเป็นรูป Gerund", "checking", [], "Would you mind checking this detail for me?", "โครงสร้าง Would you mind + V.ing เสมอ"),
            ("ช่วยชี้แจงกำหนดการส่งสินค้าให้ชัดเจนได้ไหมครับ", "Could you please", "the delivery schedule?", "คำกริยาแปลว่า ทำให้ชัดเจน/ชี้แจง (c...)", "clarify", ["explain"], "Could you please clarify the delivery schedule?", "Could you please + กริยาช่อง 1 ใช้ขอร้องอย่างสุภาพ"),
            ("ผมจะขอบคุณเป็นอย่างยิ่งหากคุณสามารถตอบกลับได้ภายในวันนี้", "I would", "it if you could reply by today.", "คำกริยาแปลว่า ซาบซึ้ง/ขอบคุณ (a...)", "appreciate", [], "I would appreciate it if you could reply by today.", "'I would appreciate it if...' เป็นสำนวนขอความร่วมมือชั้นสูง"),
            ("ขออนุญาตสอบถามความคืบหน้าเกี่ยวกับพัสดุนี้ได้ไหมครับ", "May I ask for an update", "the shipment?", "คำบุพบทแปลว่า เกี่ยวกับ (ขึ้นต้นด้วย r)", "regarding", ["about"], "May I ask for an update regarding the shipment?", "'regarding' แปลว่า เกี่ยวกับ ใช้ในบริบททางการ"),
            ("คุณพอจะมีเวลาสัก 5 นาทีคุยงานสั้นๆ ไหมครับ", "Do you have five minutes for a", "sync?", "คำแปลว่า รวดเร็ว/ว่องไว (q...)", "quick", ["short"], "Do you have five minutes for a quick sync?", "'quick sync' แปลว่า ประชุมอัปเดตสั้นๆ"),
            ("ช่วยส่งต่ออีเมลฉบับนี้ไปยังฝ่ายจัดซื้อให้หน่อยได้ไหมครับ", "Could you please", "this email to Procurement?", "คำกริยาแปลว่า ส่งต่อ (f...)", "forward", ["send"], "Could you please forward this email to Procurement?", "'forward' แปลว่า ส่งต่ออีเมล"),
            ("พอจะเป็นไปได้ไหมที่จะเลื่อนเวลาประชุมออกไป", "Would it be", "to postpone the meeting?", "คำแปลว่า เป็นไปได้ (p...)", "possible", [], "Would it be possible to postpone the meeting?", "'Would it be possible to...' แปลว่า พอจะเป็นไปได้ไหม"),
            ("ช่วยส่งไฟล์แนบมาใหม่อีกครั้งได้ไหมครับ", "Could you please", "the attachment?", "คำกริยาแปลว่า ส่งซ้ำอีกรอบ (r...)", "resend", [], "Could you please resend the attachment?", "'resend' แปลว่า ส่งใหม่อีกครั้ง"),
            ("ช่วยมาช่วยผมยกของตรงนี้หน่อยได้ไหมครับ", "Could you give me a", "with this task?", "สำนวนแปลว่า ยื่นมือช่วยเหลือ (h...)", "hand", [], "Could you give me a hand with this task?", "'give me a hand' แปลว่า ช่วยเหลือ"),
            ("ขอบคุณล่วงหน้าสำหรับความช่วยเหลืออันดีของคุณครับ", "Thank you in", "for your kind assistance.", "คำแปลว่า ล่วงหน้า (a...)", "advance", [], "Thank you in advance for your kind assistance.", "'in advance' แปลว่า ล่วงหน้า")
        ]),
        "stories": make_stories([
            ("The Forgotten Attachment", "https://images.unsplash.com/photo-1497215728101-856f4ea42174?w=900&auto=format&fit=crop&q=80",
             [("attachment", "n.", "ไฟล์แนบ"), ("forget", "v.", "ลืม"), ("client", "n.", "ลูกค้า"), ("resend", "v.", "ส่งใหม่")],
             "David clicks Send on an important email to his <b>client</b>. A minute later, he realizes he <b>forgot</b> to attach the invoice.<br><br>He politely replies: “Please find the <b>attachment</b> included in this message, with my apologies.” The client replies with a smile emoji.",
             "David clicks Send on an important email to his client. A minute later, he realizes he forgot to attach the invoice. He politely replies: Please find the attachment included in this message, with my apologies. The client replies with a smile emoji.",
             "เดวิดกดส่งอีเมลสำคัญหาลูกค้า หนึ่งนาทีต่อมาเขานึกขึ้นได้ว่าลืมแนบใบแจ้งหนี้ เขาจึงรีบส่งตามไปอย่างสุภาพ: ขออภัยด้วยครับ โปรดดูไฟล์แนบในอีเมลฉบับนี้ ลูกค้าตอบกลับมาพร้อมอีโมจิยิ้ม"),
            ("A Quick Five Minutes", "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=900&auto=format&fit=crop&q=80",
             [("available", "adj.", "ว่าง"), ("clarify", "v.", "ชี้แจง"), ("project", "n.", "โครงการ"), ("solution", "n.", "ทางออก")],
             "Lisa sees her supervisor walking past. “Do you have five minutes to <b>clarify</b> the label format?” she asks.<br><br>Her boss stops, looks at the sample, and points out the correct barcode standard. That five-minute chat saves the team three hours of rework.",
             "Lisa sees her supervisor walking past. Do you have five minutes to clarify the label format? she asks. Her boss stops, looks at the sample, and points out the correct barcode standard. That five-minute chat saves the team three hours of rework.",
             "ลิซ่าเห็นหัวหน้าเดินผ่านมา จึงถามว่า: พอมีเวลา 5 นาทีช่วยดูรูปแบบฉลากหน่อยได้ไหมคะ หัวหน้าหยุดดูตัวอย่างแล้วชี้จุดมาตรฐานบาร์โค้ดที่ถูกต้อง การคุยแค่ 5 นาทีช่วยประหยัดเวลาแก้งานได้ถึง 3 ชั่วโมง"),
            ("Borrowing the Hand Truck", "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=900&auto=format&fit=crop&q=80",
             [("borrow", "v.", "ขอยืม"), ("heavy", "adj.", "หนัก"), ("cooperation", "n.", "ความร่วมมือ"), ("return", "v.", "นำมาคืน")],
             "Ken needs to move twenty <b>heavy</b> boxes across Room A1. He walks over to Line 3: “May I <b>borrow</b> your hand truck for fifteen minutes?”<br><br>The operator agrees cheerfully. Ken finishes early and <b>returns</b> the cart with a cold can of green tea as thanks.",
             "Ken needs to move twenty heavy boxes across Room A1. He walks over to Line 3: May I borrow your hand truck for fifteen minutes? The operator agrees cheerfully. Ken finishes early and returns the cart with a cold can of green tea as thanks.",
             "เคนต้องย้ายกล่องหนัก 20 กล่องในห้อง A1 เขาเดินไปที่สายการผลิตที่ 3: ขอยืมรถเข็นสัก 15 นาทีได้ไหมครับ เพื่อนร่วมงานยินดีให้ยืม เคนทำงานเสร็จเร็วและนำรถเข็นมาคืนพร้อมชาเขียวเย็นเป็นการขอบคุณ"),
            ("Polite Words Open Doors", "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=900&auto=format&fit=crop&q=80",
             [("polite", "adj.", "สุภาพ"), ("urgent", "adj.", "เร่งด่วน"), ("customs", "n.", "ศุลกากร"), ("clearance", "n.", "การผ่านพิธีการ")],
             "An international shipment was stuck at <b>customs</b>. Instead of demanding immediate release, Nancy wrote a very <b>polite</b> email explaining the medical urgency.<br><br>Touched by her respectful tone, the customs officer expedited the <b>clearance</b> within the hour.",
             "An international shipment was stuck at customs. Instead of demanding immediate release, Nancy wrote a very polite email explaining the medical urgency. Touched by her respectful tone, the customs officer expedited the clearance within the hour.",
             "สินค้าด่วนระหว่างประเทศติดอยู่ที่ด่านศุลกากร แทนที่จะส่งอีเมลสั่งการ แนนซี่เขียนอธิบายความจำเป็นอย่างสุภาพ เจ้าหน้าที่ประทับใจในความนุ่มนวล จึงเร่งดำเนินเรื่องให้เสร็จสิ้นภายในหนึ่งชั่วโมง")
        ])
    },
    "3": {
        "day": 3,
        "title": "Day 3: Reporting Problems & Delays",
        "summary": "การแจ้งปัญหา ความล่าช้า และการเสนอทางออกอย่างเป็นมืออาชีพ",
        "rule": "แจ้งปัญหา (Issue) -> อธิบายสาเหตุ (Due to) -> เสนอทางแก้ไข (Action)",
        "vocab": make_vocab([
            ("Delay", "/dɪˈleɪ/", "n./v.", "ความล่าช้า / ทำให้ช้า", "There is a slight delay.", "มีความล่าช้าเกิดขึ้นเล็กน้อย"),
            ("Bottleneck", "/ˈbɒt.əl.nek/", "n.", "จุดคอขวด / จุดติดขัด", "We found a bottleneck at packing.", "พบจุดคอขวดที่การแพ็ค"),
            ("Resolve", "/rɪˈzɒlv/", "v.", "แก้ไขปัญหาลุล่วง", "We resolved the issue.", "พวกเราแก้ปัญหาแล้ว"),
            ("Malfunction", "/ˌmælˈfʌŋk.ʃən/", "n.", "เครื่องขัดข้อง / ผิดปกติ", "The motor malfunctioned.", "มอเตอร์ขัดข้อง"),
            ("Impact", "/ˈɪm.pækt/", "n.", "ผลกระทบ", "We want to minimize the impact.", "เราต้องการลดผลกระทบ"),
            ("Resume", "/rɪˈzjuːm/", "v.", "เริ่มทำงานต่อ", "Production will resume soon.", "การผลิตจะเริ่มต่อเร็วๆ นี้"),
            ("Halt", "/hɒlt/", "v.", "หยุดชะงัก", "Operations were halted.", "การทำงานหยุดชะงัก"),
            ("Shortage", "/ˈʃɔː.tɪdʒ/", "n.", "ของขาดแคลน", "There is a material shortage.", "เกิดภาวะวัตถุดิบขาด"),
            ("Investigate", "/ɪnˈves.tɪ.ɡeɪt/", "v.", "สืบสวนหาสาเหตุ", "We are investigating the cause.", "เรากำลังหาสาเหตุ"),
            ("Alternative", "/ɒlˈtɜː.nə.tɪv/", "n.", "ทางเลือกสำรอง", "We have an alternative plan.", "เรามีแผนสำรอง"),
            ("Preventive", "/prɪˈven.tɪv/", "adj.", "เชิงป้องกัน", "Take preventive action.", "ดำเนินมาตรการป้องกัน"),
            ("Replacement", "/rɪˈpleɪs.mənt/", "n.", "ของเปลี่ยนทดแทน", "We ordered a replacement.", "เราสั่งของทดแทนแล้ว"),
            ("Root cause", "/ruːt kɔːz/", "n.", "สาเหตุต้นตอ", "Identify the root cause.", "ระบุสาเหตุต้นตอ"),
            ("Correction", "/kəˈrek.ʃən/", "n.", "การแก้ไข", "Make the correction now.", "ทำการแก้ไขทันที"),
            ("Technician", "/tekˈnɪʃ.ən/", "n.", "ช่างเทคนิค", "Call the on-duty technician.", "เรียกช่างประจำกะมา"),
            ("Capacity", "/kəˈpæs.ə.ti/", "n.", "กำลังการผลิต", "We run at 80% capacity.", "เราเดินเครื่องที่ 80%"),
            ("Quarantine", "/ˈkwɒr.ən.tiːn/", "n./v.", "กักแยกของเสีย", "Quarantine the damaged goods.", "กักแยกสินค้าที่เสียหาย"),
            ("Recurrence", "/rɪˈkʌr.əns/", "n.", "การเกิดซ้ำ", "Prevent recurrence of error.", "ป้องกันการเกิดข้อผิดพลาดซ้ำ"),
            ("Estimate", "/ˈes.tɪ.meɪt/", "v.", "ประเมินเวลา/ยอด", "Estimate two hours of delay.", "ประเมินว่าช้าไป 2 ชม."),
            ("Contingency", "/kənˈtɪn.dʒən.si/", "n.", "แผนฉุกเฉิน", "Follow the contingency plan.", "ทำตามแผนฉุกเฉิน")
        ]),
        "phrases": make_phrases([
            ("We are experiencing a slight delay due to technical issues.", "เรากำลังประสบปัญหาล่าช้าเล็กน้อยเนื่องจากปัญหาทางเทคนิค", "due to ตามด้วยคำนามเสมอ"),
            ("We have already taken corrective actions to resolve this.", "เราได้ดำเนินมาตรการแก้ไขเพื่อจัดการปัญหานี้เรียบร้อยแล้ว", "corrective actions = มาตรการแก้ไข"),
            ("There is a minor discrepancy in the count.", "พบความคลาดเคลื่อนเล็กน้อยในจำนวนนับ", "discrepancy = ยอดไม่ตรงกัน"),
            ("We are doing our best to minimize the impact on production.", "พวกเรากำลังทำเต็มที่เพื่อลดผลกระทบต่อสายการผลิตให้น้อยที่สุด", "minimize the impact เป็นสำนวนมืออาชีพ"),
            ("The machine is temporarily out of service for maintenance.", "เครื่องจักรหยุดทำงานชั่วคราวเพื่อรับการซ่อมบำรุงครับ", "out of service = ปิดซ่อม/งดบริการ"),
            ("We expect operations to resume by 3:00 PM.", "เราคาดว่าจะกลับมาเดินเครื่องได้อีกครั้งตอนบ่าย 3 โมง", "resume = เริ่มต่อ"),
            ("The root cause was identified as a sensor failure.", "สาเหตุที่แท้จริงตรวจพบว่าเกิดจากเซนเซอร์ขัดข้อง", "root cause = สาเหตุต้นตอ"),
            ("We apologize for the inconvenience and will keep you updated.", "ขออภัยในความไม่สะดวกและจะคอยรายงานความคืบหน้าครับ", "ประโยคจบการแจ้งปัญหามาตรฐาน"),
            ("Production was halted for thirty minutes due to power loss.", "สายการผลิตหยุดชะงักไป 30 นาทีเนื่องจากไฟดับ", "halted = หยุดชะงัก"),
            ("Our technician is currently troubleshooting the error code.", "ช่างเทคนิคกำลังตรวจสอบแก้รหัสข้อผิดพลาดอยู่ครับ", "troubleshooting = วิเคราะห์แก้ปัญหา"),
            ("We switched to our backup supplier to avoid a material shortage.", "เราเปลี่ยนไปใช้ซัพพลายเออร์สำรองเพื่อเลี่ยงของขาด", "backup supplier = ผู้จัดหาสำรอง"),
            ("Please isolate the damaged goods immediately.", "กรุณาแยกสินค้าที่ชำรุดออกไปโดยทันทีครับ", "isolate = แยกเดี่ยว"),
            ("This error occurred during the system calibration.", "ข้อผิดพลาดนี้เกิดขึ้นระหว่างการปรับเทียบค่าระบบ", "occurred = เกิดขึ้น"),
            ("We are currently running at 70% capacity.", "ปัจจุบันเราเดินเครื่องอยู่ที่ 70% ของกำลังการผลิตครับ", "capacity = กำลังการผลิต"),
            ("The estimated delay is approximately two hours.", "ความล่าช้าโดยประมาณอยู่ที่ราวๆ สองชั่วโมงครับ", "approximately = โดยประมาณ"),
            ("All operators have been briefed on the contingency plan.", "พนักงานทุกคนได้รับฟังการชี้แจงแผนสำรองแล้วครับ", "contingency plan = แผนฉุกเฉิน"),
            ("No customer orders will be affected by this incident.", "จะไม่มีออเดอร์ของลูกค้าได้รับผลกระทบจากเหตุการณ์นี้ครับ", "will be affected = ได้รับผลกระทบ"),
            ("We have implemented preventive measures to avoid recurrence.", "เราได้ใช้มาตรการป้องกันเพื่อไม่ให้เกิดซ้ำแล้วครับ", "recurrence = การเกิดซ้ำ"),
            ("Please escalate this issue to the engineering manager.", "รบกวนส่งต่อเรื่องนี้ให้ผู้จัดการฝ่ายวิศวกรรมด้วยครับ", "escalate = ส่งต่อเรื่องด่วน"),
            ("Everything is back under control now.", "ตอนนี้ทุกอย่างกลับมาอยู่ภายใต้การควบคุมเรียบร้อยแล้วครับ", "under control = ควบคุมได้")
        ]),
        "dialogues": make_dialogues([
            ("เครื่องจักรสายพานหยุดกะทันหัน", [("Lead", "Why did Line 2 stop?", "ทำไมสายการผลิตที่ 2 ถึงหยุด"), ("Tech", "The conveyor belt jammed. Fixing it now.", "สายพานติดขัดครับ กำลังแก้ไขอยู่")]),
            ("แจ้งลูกค้าเรื่องสินค้าดีเลย์", [("Staff", "Your delivery will be delayed by one hour.", "สินค้าของคุณจะล่าช้าไป 1 ชั่วโมงครับ"), ("Client", "Thank you for informing us in advance.", "ขอบคุณที่แจ้งให้เราทราบล่วงหน้าครับ")]),
            ("วัตถุดิบขาดสต็อก", [("Purchasing", "The raw material shipment is stuck at port.", "วัตถุดิบติดอยู่ที่ท่าเรือครับ"), ("Manager", "Use our safety stock for today's run.", "นำสต็อกสำรองออกมาใช้ก่อนสำหรับวันนี้")]),
            ("ตรวจพบรอยขีดข่วนบนชิ้นงาน", [("Inspector", "I spotted surface scratches on this batch.", "ผมพบรอยขีดข่วนบนผิวชิ้นงานล็อตนี้ครับ"), ("Lead", "Quarantine them and notify QA right away.", "กักแยกไว้แล้วรีบแจ้ง QA ทันที")]),
            ("ไฟฟ้าดับในโกดัง", [("Staff", "The power is out in Warehouse B.", "ไฟดับในโกดัง B ครับ"), ("Lead", "The generator will kick in in 30 seconds.", "เครื่องปั่นไฟสำรองจะทำงานใน 30 วินาที")]),
            ("รถโฟล์คลิฟต์แบตหมด", [("Driver", "Forklift number 3 has a dead battery.", "รถโฟล์คลิฟต์เบอร์ 3 แบตหมดครับ"), ("Lead", "Plug it in and switch to Forklift 5.", "เสียบชาร์จไว้แล้วไปใช้เบอร์ 5 แทน")]),
            ("อุณหภูมิห้องเย็นเกินเกณฑ์", [("QA", "Room A1 rose to 26 degrees Celsius.", "ห้อง A1 อุณหภูมิพุ่งไป 26 องศาแล้ว"), ("Tech", "I will reset the compressor unit now.", "เดี๋ยวผมรีเซ็ตคอมเพรสเซอร์เดี๋ยวนี้ครับ")]),
            ("กล่องสินค้าตกหล่น", [("Operator", "One box fell from the top shelf.", "มีกล่องหนึ่งตกลงมาจากชั้นบนสุดครับ"), ("Lead", "Check if the inner products are intact.", "ตรวจดูว่าสินค้าข้างในยังสมบูรณ์ดีไหม")]),
            ("ระบบสแกนออนไลน์ล่ม", [("Staff", "The Wi-Fi dropped; scanners cannot sync.", "เน็ตหลุดครับ สแกนเนอร์ส่งข้อมูลไม่ได้"), ("IT", "We are restarting the access point.", "พวกเรากำลังรีสตาร์ตตัวกระจายสัญญาณครับ")]),
            ("รายงานผู้จัดการเมื่อแก้เสร็จ", [("Staff", "Line 2 is fully operational again.", "สายการผลิตที่ 2 กลับมาเดินเครื่องปกติแล้วครับ"), ("Manager", "Great recovery. Document the root cause.", "กู้สถานการณ์ได้ดีมาก จดบันทึกสาเหตุไว้ด้วยนะ")])
        ]),
        "exercises": make_exercises([
            ("เรากำลังประสบปัญหาล่าช้าเล็กน้อยเนื่องจากปัญหาทางเทคนิค", "We are experiencing a slight delay", "technical issues.", "คำบุพบทแปลว่า เนื่องจาก (d...)", "due to", [], "We are experiencing a slight delay due to technical issues.", "ใช้วลี due to ตามด้วยคำนามเพื่ออธิบายสาเหตุ"),
            ("พวกเรากำลังทำทุกอย่างเพื่อลดผลกระทบต่อลูกค้าให้น้อยที่สุด", "We are doing our best to", "the impact on customers.", "คำกริยาแปลว่า ลดให้น้อยที่สุด (m...)", "minimize", ["minimise"], "We are doing our best to minimize the impact on customers.", "'minimize' แปลว่า ลดระดับลงให้เหลือน้อยที่สุด"),
            ("ปัญหานี้ได้รับการแก้ไขเรียบร้อยแล้วโดยทีมวิศวกร", "This problem has been", "by the engineering team.", "คำกริยาช่อง 3 แปลว่า แก้ไขลุล่วง (r...)", "resolved", ["fixed"], "This problem has been resolved by the engineering team.", "'resolved' นิยมใช้ในความหมายว่า แก้ไขปัญหาสำเร็จ"),
            ("เครื่องจักรหยุดทำงานลงอย่างกะทันหัน", "The machinery was", "unexpectedly.", "คำกริยาช่อง 3 แปลว่า ถูกสั่งหยุด/ชะงัก (h...)", "halted", ["stopped"], "The machinery was halted unexpectedly.", "'halted' หมายถึง การหยุดชะงักลง"),
            ("เราจำเป็นต้องแยกสินค้าที่มีตำหนิออกทันที", "We must", "the defective items immediately.", "คำกริยาแปลว่า แยกเดี่ยว/กักแยก (i...)", "isolate", ["quarantine"], "We must isolate the defective items immediately.", "'isolate' แปลว่า แยกชิ้นส่วนที่มีปัญหาออก"),
            ("การผลิตจะกลับมาเริ่มต้นใหม่อีกครั้งเวลาบ่ายสองโมง", "Production will", "at 2:00 PM.", "คำกริยาแปลว่า กลับมาเริ่มต่อ (r...)", "resume", [], "Production will resume at 2:00 PM.", "'resume' แปลว่า เริ่มทำงานใหม่อีกครั้งหลังจากหยุดไป"),
            ("สาเหตุที่แท้จริงเกิดจากเซนเซอร์ตรวจจับเสีย", "The", "cause was a broken sensor.", "คำแปลว่า รากเหง้า/ต้นตอ (r...)", "root", [], "The root cause was a broken sensor.", "'root cause' คือสาเหตุที่แท้จริงของปัญหา"),
            ("เรามีแผนสำรองเพื่อป้องกันสินค้าขาดแคลน", "We have a", "plan in place.", "คำแปลว่า ทางเลือกสำรอง (c... หรือ a...)", "contingency", ["backup", "alternative"], "We have a contingency plan in place.", "'contingency plan' แปลว่า แผนฉุกเฉินสำรอง"),
            ("เรากำลังเผชิญกับภาวะขาดแคลนวัตถุดิบ", "We are facing a material", ".", "คำนามแปลว่า การขาดแคลน (s...)", "shortage", [], "We are facing a material shortage.", "'shortage' แปลว่า ภาวะของขาดแคลน"),
            ("ตอนนี้สถานการณ์ทั้งหมดกลับมาอยู่ภายใต้การควบคุมแล้ว", "The situation is back", "control now.", "คำบุพบทแปลว่า ใต้ (u...)", "under", [], "The situation is back under control now.", "'under control' แปลว่า อยู่ในการควบคุม")
        ]),
        "stories": make_stories([
            ("The Jammed Conveyor", "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=900&auto=format&fit=crop&q=80",
             [("conveyor", "n.", "สายพานลำเลียง"), ("jam", "v.", "ติดขัด"), ("technician", "n.", "ช่างเทคนิค"), ("resume", "v.", "เริ่มทำงานต่อ")],
             "A loud screech echoes across the packing area. A plastic box <b>jammed</b> inside the <b>conveyor</b> belt, halting all movement.<br><br>The on-duty <b>technician</b> clears the blockage and inspects the motor. Within twenty minutes, the line <b>resumes</b> safely without damaging a single product.",
             "A loud screech echoes across the packing area. A plastic box jammed inside the conveyor belt, halting all movement. The on-duty technician clears the blockage and inspects the motor. Within twenty minutes, the line resumes safely without damaging a single product.",
             "เสียงดังเอี๊ยดก้องไปทั่วแผนกบรรจุหีบห่อ กล่องพลาสติกติดขัดในสายพานลำเลียงทำให้ทุกอย่างหยุดชะงัก ช่างเทคนิคประจำกะรีบเคลียร์จุดติดขัดและตรวจเช็คมอเตอร์ ภายใน 20 นาทีสายการผลิตก็กลับมาเดินเครื่องได้ตามปกติโดยไม่มีสินค้าเสียหาย"),
            ("The Temperature Warning", "https://images.unsplash.com/photo-1584467735815-f778f274e296?w=900&auto=format&fit=crop&q=80",
             [("temperature", "n.", "อุณหภูมิ"), ("warning", "n.", "การเตือนภัย"), ("sensor", "n.", "เซนเซอร์"), ("relief", "n.", "ความโล่งอก")],
             "A red flashing light warns that Room A1's <b>temperature</b> reached 25°C. Sensitive electronics components must stay below 22°C.<br><br>The team quickly investigates and discovers a faulty door seal, not a broken cooler. They shut the inner door tightly, cooling the room back to safety with a collective sigh of <b>relief</b>.",
             "A red flashing light warns that Room A1's temperature reached 25°C. Sensitive electronics components must stay below 22°C. The team quickly investigates and discovers a faulty door seal, not a broken cooler. They shut the inner door tightly, cooling the room back to safety with a collective sigh of relief.",
             "ไฟแดงกะพริบเตือนว่าอุณหภูมิในห้อง A1 แตะ 25 องศา ซึ่งชิ้นส่วนอิเล็กทรอนิกส์ต้องเก็บต่ำกว่า 22 องศา ทีมงานรีบตรวจพบว่าขอบยางประตูไม่สนิท ไม่ใช่แอร์เสีย พวกเขาปิดประตูด้านในให้แน่นจนอุณหภูมิลดลงสู่ระดับปลอดภัยด้วยความโล่งอก"),
            ("Rainstorm on the Highway", "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?w=900&auto=format&fit=crop&q=80",
             [("rainstorm", "n.", "พายุฝน"), ("highway", "n.", "ทางหลวง"), ("safety", "n.", "ความปลอดภัย"), ("intact", "adj.", "สมบูรณ์ดี")],
             "Truck Driver Somchai was heading from Ayutthaya to Pathum Thani when a fierce <b>rainstorm</b> struck the <b>highway</b>. Visibility dropped to near zero.<br><br>Prioritizing <b>safety</b>, Somchai safely parked at a rest area and notified the warehouse. He arrived forty minutes late, but every single pallet was completely dry and <b>intact</b>.",
             "Truck Driver Somchai was heading from Ayutthaya to Pathum Thani when a fierce rainstorm struck the highway. Visibility dropped to near zero. Prioritizing safety, Somchai safely parked at a rest area and notified the warehouse. He arrived forty minutes late, but every single pallet was completely dry and intact.",
             "คนขับรถสมชายกำลังวิ่งจากอยุธยาไปปทุมธานี แต่พายุฝนกระหน่ำบนทางหลวงจนมองแทบไม่เห็นทาง เขาเลือกความปลอดภัยโดยจอดพักที่จุดพักรถและโทรแจ้งคลังสินค้า เขาส่งของช้าไป 40 นาที แต่สินค้าทุกพาเลทแห้งสนิทและสมบูรณ์ 100%"),
            ("The Missing Crate", "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=900&auto=format&fit=crop&q=80",
             [("crate", "n.", "ลังไม้ / ตะกร้า"), ("discrepancy", "n.", "ยอดคลาดเคลื่อน"), ("location", "n.", "ตำแหน่ง"), ("correct", "v.", "แก้ไข")],
             "During the cycle count, one wooden <b>crate</b> of connectors was missing from Rack A1112. The audit showed an alarming <b>discrepancy</b>.<br><br>Instead of panicking, the team checked the adjacent shelf and found it mislabeled under A1113. They quickly <b>corrected</b> the system tag with zero loss.",
             "During the cycle count, one wooden crate of connectors was missing from Rack A1112. The audit showed an alarming discrepancy. Instead of panicking, the team checked the adjacent shelf and found it mislabeled under A1113. They quickly corrected the system tag with zero loss.",
             "ระหว่างการนับสต็อก ลังคอนเนกเตอร์หายไปหนึ่งลังจากแร็ค A1112 ซึ่งทำให้ยอดไม่ตรงอย่างน่าตกใจ ทีมงานตั้งสติแล้วเดินตรวจแร็คข้างๆ จนพบว่าถูกวางสลับไว้ที่ A1113 พวกเขาจึงรีบแก้ไขแท็กในระบบให้ถูกต้องโดยไม่มีของสูญหาย")
        ])
    },
    "4": {
        "day": 4,
        "title": "Day 4: Daily Standup & Work Progress",
        "summary": "การรายงานสิ่งที่ทำเสร็จ สิ่งที่กำลังทำ และอุปสรรคในการทำงานประจำวัน",
        "rule": "รูปแบบ 3 ขั้น: What I did yesterday -> What I will do today -> Blockers",
        "vocab": make_vocab([
            ("Backlog", "/ˈbæk.lɒɡ/", "n.", "งานคั่งค้าง", "We cleared the backlog.", "พวกเราเคลียร์งานค้างเสร็จแล้ว"),
            ("Blocker", "/ˈblɒk.ər/", "n.", "อุปสรรคติดขัด", "Do you have any blockers?", "คุณมีอะไรติดขัดไหม"),
            ("Milestone", "/ˈmaɪl.stəʊn/", "n.", "เป้าหมายสำคัญ", "We reached a new milestone.", "เราบรรลุเป้าหมายสำคัญ"),
            ("Prioritize", "/praɪˈɒr.ɪ.taɪz/", "v.", "จัดลำดับสำคัญ", "Prioritize safety first.", "จัดลำดับความปลอดภัยไว้ก่อน"),
            ("Progress", "/ˈprəʊ.ɡres/", "n.", "ความคืบหน้า", "Good progress was made.", "มีความคืบหน้าที่ดีมาก"),
            ("Deliverable", "/dɪˈlɪv.ər.ə.bəl/", "n.", "ชิ้นงานส่งมอบ", "The deliverable is due today.", "งานส่งมอบครบกำหนดวันนี้"),
            ("Achievement", "/əˈtʃiːv.mənt/", "n.", "ผลงานสำเร็จ", "Great team achievement.", "ผลงานยอดเยี่ยมของทีม"),
            ("Pending", "/ˈpen.dɪŋ/", "adj.", "อยู่ระหว่างรอผล", "Approval is pending.", "กำลังรออนุมัติอยู่"),
            ("Coordinate", "/kəʊˈɔː.dɪ.neɪt/", "v.", "ประสานงาน", "I will coordinate with QA.", "ผมจะประสานงานกับ QA"),
            ("Handover", "/ˈhændˌəʊ.vər/", "n.", "การส่งมอบงาน", "Do a smooth shift handover.", "ส่งมอบงานระหว่างกะอย่างราบรื่น"),
            ("Target", "/ˈtɑː.ɡɪt/", "n.", "เป้าหมาย", "We hit our daily target.", "เราทำยอดได้ตามเป้า"),
            ("Update", "/ʌpˈdeɪt/", "v./n.", "รายงานความคืบหน้า", "Give me a quick update.", "ช่วยอัปเดตสั้นๆ ให้ฟังหน่อย"),
            ("Support", "/səˈpɔːt/", "n.", "การช่วยเหลือ", "I need technical support.", "ผมต้องการความช่วยเหลือทางเทคนิค"),
            ("Efficiency", "/ɪˈfɪʃ.ən.si/", "n.", "ประสิทธิภาพ", "Boost warehouse efficiency.", "เพิ่มประสิทธิภาพคลัง"),
            ("Assign", "/əˈsaɪn/", "v.", "มอบหมายงาน", "Assign tasks to the crew.", "มอบหมายงานให้ทีม"),
            ("Status", "/ˈsteɪ.təs/", "n.", "สถานะงาน", "What is the status now?", "สถานะงานตอนนี้เป็นอย่างไร"),
            ("Resource", "/rɪˈzɔːs/", "n.", "ทรัพยากร/กำลังคน", "We need more resources.", "เราต้องการกำลังคนเพิ่ม"),
            ("Morale", "/məˈrɑːl/", "n.", "ขวัญกำลังใจ", "Team morale is high.", "ขวัญกำลังใจทีมงานดีมาก"),
            ("Align", "/əˈlaɪn/", "v.", "ปรับให้ตรงกัน", "Let's align our tasks.", "มาปรับงานให้ตรงกัน"),
            ("Wrap up", "/ræp ʌp/", "v.", "สรุปจบงาน", "Wrap up the standup meeting.", "สรุปจบการประชุมสแตนด์อัป")
        ]),
        "phrases": make_phrases([
            ("Yesterday, I finalized the inspection report.", "เมื่อวานนี้ผมสรุปรายงานการตรวจสอบเสร็จเรียบร้อยแล้วครับ", "finalize = สรุปเสร็จสมบูรณ์"),
            ("Today, I am focusing on clearing the backlog.", "วันนี้ผมจะโฟกัสที่การเคลียร์งานที่คั่งค้างอยู่ครับ", "focusing on = ทุ่มความสนใจ"),
            ("I am currently blocked by pending approval from QA.", "ตอนนี้ผมติดปัญหาเรื่องรอการอนุมัติจากแผนก QA ครับ", "blocked by = ติดขัดเรื่อง"),
            ("Everything is on track to meet the deadline.", "ทุกอย่างดำเนินไปตามแผนและทันกำหนดแน่นอนครับ", "on track = เป็นไปตามแผน"),
            ("We completed five cycles ahead of schedule.", "พวกเรานับสต็อกเสร็จก่อนเวลา 5 รอบครับ", "ahead of schedule = เร็วกว่ากำหนด"),
            ("My top priority today is checking Rack 4.", "เป้าหมายหลักของผมวันนี้คือการตรวจแร็ค 4 ครับ", "top priority = เรื่องสำคัญอันดับแรก"),
            ("I will collaborate with the night shift leader.", "ผมจะประสานงานกับหัวหน้ากะดึกครับ", "collaborate = ร่วมมือกัน"),
            ("No major blockers were reported this morning.", "ไม่มีรายงานปัญหาติดขัดรุนแรงเช้านี้ครับ", "no major blockers"),
            ("We hit our target of packing 800 units.", "เราทำยอดแพ็คของได้ตามเป้า 800 ชิ้นครับ", "hit our target = บรรลุเป้าหมาย"),
            ("I need fifteen minutes of technical support.", "ผมต้องการความช่วยเหลือทางเทคนิคสัก 15 นาทีครับ", "technical support = ความช่วยเหลือด้านเทคนิค"),
            ("The attendance sheet has been updated.", "ตารางการเข้างานได้รับการอัปเดตแล้วครับ", "attendance sheet = ใบลงเวลา"),
            ("We are currently running at full efficiency.", "ตอนนี้เราเดินงานเต็มประสิทธิภาพครับ", "full efficiency = เต็มประสิทธิภาพ"),
            ("I will deliver the finalized document by 4 PM.", "ผมจะส่งเอกสารฉบับสมบูรณ์ให้ก่อน 4 โมงเย็นครับ", "deliver = นำส่ง"),
            ("Let's align our tasks before starting the shift.", "พวกเรามาปรับเป้าหมายงานให้ตรงกันก่อนเริ่มกะกันครับ", "align tasks = ปรับงานให้ตรงกัน"),
            ("Who is assigned to inspect the incoming shipment?", "ใครได้รับมอบหมายให้ตรวจสินค้าที่รับเข้ามาครับ", "assigned to = มอบหมายให้"),
            ("We managed to reduce processing time by 10%.", "เราลดระยะเวลาการทำงานลงได้ถึง 10% ครับ", "processing time = ระยะเวลาทำงาน"),
            ("I will follow up on the missing quotation today.", "วันนี้ผมจะติดตามเรื่องใบเสนอราคาที่ยังขาดอยู่ครับ", "follow up on = ติดตามเรื่อง"),
            ("The team morale is high and productive.", "กำลังใจของทีมงานดีมากและทำงานได้ผลงานสูงครับ", "morale = ขวัญกำลังใจ"),
            ("Please log your completed items in the system.", "ช่วยบันทึกรายการที่ทำเสร็จลงในระบบด้วยครับ", "log in the system = บันทึกเข้าระบบ"),
            ("That wraps up my morning standup report.", "นั่นคือสรุปรายงานการประชุมสแตนด์อัปเช้านี้ของผมครับ", "wraps up = ปิดท้ายสรุป")
        ]),
        "dialogues": make_dialogues([
            ("รายงานกะสแตนด์อัป", [("Leader", "What is your main task today, Sam?", "วันนี้งานหลักของคุณคืออะไร แซม"), ("Sam", "I am clearing the Room A1 backlog.", "ผมจะเคลียร์งานคั่งค้างในห้อง A1 ครับ")]),
            ("แจ้งติดขัดรอเอกสาร", [("Staff", "I am blocked by the missing invoice.", "ผมติดปัญหาเรื่องยังไม่ได้ใบแจ้งหนี้ครับ"), ("Leader", "I will call the accounting team now.", "เดี๋ยวผมโทรตามบัญชีให้เดี๋ยวนี้")]),
            ("แจ้งทำยอดทะลุเป้า", [("Lead", "Did we reach our target yesterday?", "เมื่อวานเราทำยอดถึงเป้าไหม"), ("Staff", "Yes, we packed 1,200 units, 10% over target.", "ถึงครับ แพ็คได้ 1,200 ชิ้น เกินเป้า 10% ครับ")]),
            ("ขอความช่วยเหลือจากเพื่อนร่วมงาน", [("Operator", "I need support with heavy lifting today.", "วันนี้ผมอยากได้คนช่วยยกของหนักครับ"), ("Colleague", "I will join you after my coffee break.", "เดี๋ยวฉันไปช่วยหลังจากพักดื่มกาแฟนะ")]),
            ("ส่งมอบงานก่อนเลิกกะ", [("A", "All pallets on Rack 5 are verified.", "พาเลททั้งหมดบนแร็ค 5 ตรวจสอบแล้ว"), ("B", "Thanks, I will take over Rack 6 now.", "ขอบคุณ เดี๋ยวผมรับช่วงต่อแร็ค 6 เอง")]),
            ("รายงานระบบคอมพิวเตอร์พร้อมใช้", [("IT", "The warehouse scanner system is fully updated.", "ระบบสแกนเนอร์ของคลังอัปเดตเรียบร้อยแล้ว"), ("Staff", "Great, the sync is much faster now.", "ยอดเยี่ยม ส่งข้อมูลไวขึ้นเยอะเลยครับ")]),
            ("แบ่งหน้าที่ในกะเช้า", [("Leader", "Ken, handle inbound. Lisa, handle packing.", "เคนดูของเข้า ลิซ่าดูแลการแพ็คของนะ"), ("Both", "Understood, we are on it.", "รับทราบครับ/ค่ะ พวกเราลุยเลย")]),
            ("ติดตามเรื่องความปลอดภัย", [("Safety Officer", "Remember to wear high-visibility vests.", "อย่าลืมสวมเสื้อกั๊กสะท้อนแสงกันทุกคนนะ"), ("Team", "Yes, safety first every single day.", "รับทราบครับ ปลอดภัยไว้ก่อนทุกๆ วัน")]),
            ("รายงานการซ่อมบำรุงรถโฟล์คลิฟต์", [("Mechanic", "Forklift maintenance is complete.", "การบำรุงรักษารถโฟล์คลิฟต์เสร็จแล้วครับ"), ("Driver", "Awesome, I will do a quick brake test.", "เยี่ยมเลย เดี๋ยวผมขอทดสอบเบรกแป๊บหนึ่ง")]),
            ("ปิดการประชุมยามเช้า", [("Manager", "Let's have a safe and productive day!", "ขอให้เป็นวันที่ปลอดภัยและมีผลงานยอดเยี่ยมนะ!"), ("Team", "Let's do this!", "ลุยกันเลยครับ!")])
        ]),
        "exercises": make_exercises([
            ("ทุกอย่างดำเนินไปตามแผนเพื่อส่งงานให้ทันกำหนด", "Everything is on", "to meet the deadline.", "สำนวนแปลว่า ตามแผน (t...)", "track", [], "Everything is on track to meet the deadline.", "'on track' แปลว่า เป็นไปตามแผนงาน"),
            ("วันนี้ผมมุ่งเน้นไปที่การเคลียร์งานที่ค้างอยู่", "Today, I am", "on clearing the backlog.", "คำกริยาเติม -ing แปลว่า จดจ่อ/มุ่งเน้น (f...)", "focusing", [], "Today, I am focusing on clearing the backlog.", "'focusing on' แปลว่า ให้ความสำคัญ/จดจ่อ"),
            ("ผมติดปัญหาเรื่องยังรอการอนุมัติอยู่ครับ", "I am", "by pending approval.", "คำกริยาช่อง 3 แปลว่า ติดขัด (b...)", "blocked", [], "I am blocked by pending approval.", "'blocked by' แปลว่า ติดปัญหาหรือติดขัดจาก..."),
            ("งานส่งมอบชิ้นสุดท้ายมีกำหนดส่งวันนี้", "The final", "is due today.", "คำนามแปลว่า ชิ้นงานส่งมอบ (d...)", "deliverable", [], "The final deliverable is due today.", "'deliverable' คือผลงานที่ต้องส่งมอบ"),
            ("เมื่อวานนี้ผมสรุปรายงานการตรวจเสร็จเรียบร้อยแล้ว", "Yesterday, I", "the inspection report.", "คำกริยาอดีตแปลว่า ทำให้เสร็จสิ้น (f...)", "finalized", [], "Yesterday, I finalized the inspection report.", "'finalized' แปลว่า ทำเสร็จสมบูรณ์ในอดีต"),
            ("พวกเราทำงานเสร็จเร็วกว่ากำหนดการสองชั่วโมง", "We finished two hours ahead of", ".", "คำนามแปลว่า กำหนดการ (s...)", "schedule", [], "We finished two hours ahead of schedule.", "'ahead of schedule' แปลว่า เร็วกว่ากำหนด"),
            ("ใครได้รับมอบหมายให้ดูแลงานชิ้นนี้ครับ", "Who is", "to this task?", "คำกริยาช่อง 3 แปลว่า มอบหมาย (a...)", "assigned", [], "Who is assigned to this task?", "'assigned to' แปลว่า ได้รับมอบหมายให้ทำ"),
            ("เป้าหมายสำคัญอันดับหนึ่งของฉันคือการจัดระเบียบแร็ค", "My top", "is organizing the racks.", "คำแปลว่า ลำดับความสำคัญ (p...)", "priority", [], "My top priority is organizing the racks.", "'top priority' คือสิ่งที่ต้องทำเป็นอันดับแรก"),
            ("เราจำเป็นต้องประสานงานกับทีมงานกะดึก", "We must", "with the night shift team.", "คำกริยาแปลว่า ประสานงาน (c...)", "coordinate", ["collaborate"], "We must coordinate with the night shift team.", "'coordinate with' แปลว่า ประสานงานร่วมกับ"),
            ("นั่นคือสรุปรายงานการประชุมประจำเช้าของผมครับ", "That", "up my morning report.", "คำกริยาเติม s แปลว่า ห่อ/สรุปปิดท้าย (w...)", "wraps", [], "That wraps up my morning report.", "'wraps up' แปลว่า จบหรือสรุปรายงาน")
        ]),
        "stories": make_stories([
            ("Clearing the Mountain", "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=900&auto=format&fit=crop&q=80",
             [("backlog", "n.", "งานคั่งค้าง"), ("standup", "n.", "การประชุมสั้น"), ("target", "n.", "เป้าหมาย"), ("celebrate", "v.", "ฉลอง")],
             "At the morning <b>standup</b>, the team faced a daunting <b>backlog</b> of five hundred unverified parcels.<br><br>The leader broke the quota into small hourly targets. By 4 PM, they met the <b>target</b> and shared a box of warm donuts to <b>celebrate</b>.",
             "At the morning standup, the team faced a daunting backlog of five hundred unverified parcels. The leader broke the quota into small hourly targets. By 4 PM, they met the target and shared a box of warm donuts to celebrate.",
             "ในการประชุมสแตนด์อัปยามเช้า ทีมงานต้องเผชิญกับพัสดุคั่งค้างที่ยังไม่ตรวจนับถึง 500 กล่อง หัวหน้าทีมจึงแบ่งเป้าหมายออกเป็นชั่วโมงๆ เมื่อถึงบ่ายสี่โมง พวกเขาก็ทำสำเร็จตามเป้าและแบ่งโดนัทฉลองร่วมกัน"),
            ("Speak Up on the Blocker", "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=900&auto=format&fit=crop&q=80",
             [("blocker", "n.", "อุปสรรค"), ("honest", "adj.", "ซื่อสัตย์/ตรงไปตรงมา"), ("guide", "v.", "แนะนำ"), ("solve", "v.", "แก้ไข")],
             "During the sync, junior operator Leo raised his hand: “I have a <b>blocker</b>. I don’t fully understand the new wiring diagram.”<br><br>Senior engineer Paul appreciated his <b>honest</b> update, spent ten minutes to <b>guide</b> him, and <b>solved</b> the issue on the spot.",
             "During the sync, junior operator Leo raised his hand: I have a blocker. I don’t fully understand the new wiring diagram. Senior engineer Paul appreciated his honest update, spent ten minutes to guide him, and solved the issue on the spot.",
             "ระหว่างประชุม ลีโอช่างเทคนิครุ่นใหม่ยกมือขึ้นอย่างตรงไปตรงมา: ผมติดปัญหาตรงที่ไม่ค่อยเข้าใจแบบวงจรไฟฟ้าอันใหม่ครับ พอลวิศวกรอาวุโสชื่นชมความซื่อสัตย์ ใช้เวลา 10 นาทีช่วยสอนจนแก้ปัญหาได้ทันที"),
            ("The Shift Handover Log", "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=900&auto=format&fit=crop&q=80",
             [("handover", "n.", "การส่งต่องาน"), ("accurate", "adj.", "แม่นยำ"), ("shift", "n.", "กะทำงาน"), ("smooth", "adj.", "ราบรื่น")],
             "Before clocking out, Niran completed a neat <b>handover</b> sheet specifying which racks were counted and which boxes remained.<br><br>The night <b>shift</b> supervisor was thrilled by the clear notes, allowing a perfectly <b>smooth</b> and error-free operation until dawn.",
             "Before clocking out, Niran completed a neat handover sheet specifying which racks were counted and which boxes remained. The night shift supervisor was thrilled by the clear notes, allowing a perfectly smooth and error-free operation until dawn.",
             "ก่อนสแกนนิ้วกลับบ้าน นิรันดร์เขียนบันทึกส่งมอบงานอย่างเป็นระเบียบว่าแร็คไหนนับแล้วและกล่องไหนที่ยังค้างอยู่ หัวหน้ากะดึกประทับใจในความชัดเจน ทำให้การทำงานกะกลางคืนราบรื่นไร้ข้อผิดพลาดจนถึงเช้า"),
            ("Ten Percent Over Target", "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=900&auto=format&fit=crop&q=80",
             [("target", "n.", "เป้าหมาย"), ("efficient", "adj.", "มีประสิทธิภาพ"), ("cheer", "v.", "ส่งเสียงยินดี"), ("teamwork", "n.", "การทำงานเป็นทีม")],
             "Line 3 was challenged to pack 1,000 units. By reorganizing their workbench, their workflow became remarkably <b>efficient</b>.<br><br>At shift end, they counted 1,100 finished boxes! The room erupted into <b>cheers</b>, celebrating the power of great <b>teamwork</b>.",
             "Line 3 was challenged to pack 1,000 units. By reorganizing their workbench, their workflow became remarkably efficient. At shift end, they counted 1,100 finished boxes! The room erupted into cheers, celebrating the power of great teamwork.",
             "สายการผลิตที่ 3 ได้รับโจทย์ให้แพ็คของ 1,000 ชิ้น ด้วยการจัดระเบียบโต๊ะทำงานใหม่ กระบวนการจึงมีประสิทธิภาพขึ้นอย่างเห็นได้ชัด เมื่อจบกะ พวกเขานับได้ถึง 1,100 กล่อง ทั้งห้องส่งเสียงเฮฉลองพลังแห่งการทำงานเป็นทีม")
        ])
    },
    "5": {
        "day": 5,
        "title": "Day 5: Scheduling & Rescheduling Meetings",
        "summary": "การนัดหมาย เสนอเวลาว่าง เลื่อนนัด และยืนยันกำหนดการอย่างมืออาชีพ",
        "rule": "ระบุเวลาชัดเจน + เสนอทางเลือก (Does [time] work for you?)",
        "vocab": make_vocab([
            ("Available", "/əˈveɪ.lə.bəl/", "adj.", "ว่าง / สะดวก", "Are you available tomorrow?", "พรุ่งนี้คุณว่างไหมครับ"),
            ("Reschedule", "/ˌriːˈskedʒ.uːl/", "v.", "เลื่อนนัดหมาย", "Can we reschedule our call?", "ขอเลื่อนนัดคุยสายได้ไหม"),
            ("Conflict", "/ˈkɒn.flɪkt/", "n.", "เวลาชนกัน", "I have a scheduling conflict.", "ผมมีตารางเวลาชนกัน"),
            ("Propose", "/prəˈpəʊz/", "v.", "เสนอเวลา", "I propose Friday at 2 PM.", "ผมขอเสนอวันศุกร์บ่ายสอง"),
            ("Confirm", "/kənˈfɜːm/", "v.", "ยืนยัน", "Confirm the meeting room.", "ช่วยยืนยันห้องประชุมด้วย"),
            ("Postpone", "/pəʊstˈpəʊn/", "v.", "เลื่อนออกไป", "The sync was postponed.", "การประชุมถูกเลื่อนออกไป"),
            ("Agenda", "/əˈdʒen.də/", "n.", "วาระการประชุม", "Check the meeting agenda.", "ตรวจดูวาระการประชุม"),
            ("Attendee", "/ə.tenˈdiː/", "n.", "ผู้เข้าร่วม", "All attendees arrived.", "ผู้เข้าร่วมทุกคนมาถึงแล้ว"),
            ("Convenient", "/kənˈviː.ni.ənt/", "adj.", "สะดวกสบาย", "Is Thursday convenient?", "วันพฤหัสบดีสะดวกไหม"),
            ("Invitation", "/ˌɪn.vɪˈteɪ.ʃən/", "n.", "คำเชิญปฏิทิน", "Send a calendar invitation.", "ส่งคำเชิญปฏิทินมาด้วย"),
            ("Duration", "/djʊəˈreɪ.ʃən/", "n.", "ระยะเวลาประชุม", "The duration is 30 mins.", "ระยะเวลาคือ 30 นาที"),
            ("Minutes", "/ˈmɪn.ɪts/", "n.", "บันทึกการประชุม", "Send the meeting minutes.", "ส่งบันทึกการประชุม"),
            ("Facilitate", "/fəˈsɪl.ɪ.teɪt/", "v.", "ดำเนินรายการ", "Who will facilitate the call?", "ใครจะดำเนินรายการประชุม"),
            ("Discussion", "/dɪˈskʌʃ.ən/", "n.", "การหารือ", "We had a great discussion.", "เรามีการหารือที่ดีมาก"),
            ("Tentative", "/ˈten.tə.tɪv/", "adj.", "กำหนดการคร่าวๆ", "This is a tentative date.", "นี่คือวันนัดคร่าวๆ"),
            ("Reminder", "/rɪˈmaɪn.dər/", "n.", "การเตือนความจำ", "Send a quick reminder.", "ส่งการเตือนความจำสั้นๆ"),
            ("Platform", "/ˈplæt.fɔːm/", "n.", "โปรแกรมประชุม", "Teams is our platform.", "เราใช้ Teams ประชุม"),
            ("Dial-in", "/ˈdaɪ.əl.ɪn/", "n.", "ลิงก์เข้าประชุม", "Here is the dial-in link.", "นี่คือลิงก์เข้าประชุม"),
            ("Punctual", "/ˈpʌŋk.tʃu.əl/", "adj.", "ตรงต่อเวลา", "Please be punctual.", "กรุณาตรงต่อเวลา"),
            ("Accommodate", "/əˈkɒm.ə.deɪt/", "v.", "ปรับเวลาให้ลงตัว", "Thanks for accommodating me.", "ขอบคุณที่ปรับเวลาให้")
        ]),
        "phrases": make_phrases([
            ("Are you available for a quick meeting tomorrow at 2 PM?", "คุณสะดวกประชุมสั้นๆ พรุ่งนี้ตอนบ่าย 2 โมงไหมครับ", "available ออกเสียงว่า /əˈveɪ.lə.bəl/"),
            ("Does Thursday morning work for you?", "เช้าวันพฤหัสบดีสะดวกสำหรับคุณไหมครับ", "Does ... work for you? เป็นคำถามสุภาพมาก"),
            ("I am afraid I have a scheduling conflict at that time.", "ผมเกรงว่าผมจะมีนัดชนกันในช่วงเวลาดังกล่าวครับ", "scheduling conflict = นัดซ้อนชนกัน"),
            ("Could we reschedule our sync to Friday instead?", "พวกเราขอเลื่อนการประชุมสั้นๆ ไปเป็นวันศุกร์แทนได้ไหมครับ", "reschedule = เลื่อนนัด"),
            ("Please send over a calendar invite once confirmed.", "เมื่อยืนยันแล้ว รบกวนส่งคำเชิญปฏิทินมาให้ด้วยนะครับ", "calendar invite = คำเชิญปฏิทิน"),
            ("Any time after 3:00 PM works perfectly for me.", "เวลาไหนก็ได้หลังบ่าย 3 โมง สะดวกสำหรับผมทั้งหมดเลยครับ", "works perfectly for me"),
            ("I would like to confirm our appointment for Monday.", "ผมขออนุญาตยืนยันการนัดหมายของเราในวันจันทร์นี้นะครับ", "confirm our appointment"),
            ("Sorry for the short notice regarding this meeting change.", "ขออภัยด้วยครับที่แจ้งเปลี่ยนแปลงกำหนดประชุมกระชั้นชิด", "short notice = แจ้งกะทันหัน"),
            ("Would next Tuesday be more convenient for the team?", "วันอังคารหน้าจะสะดวกกับทีมมากกว่าไหมครับ", "more convenient = สะดวกกว่า"),
            ("I will send the meeting link fifteen minutes prior.", "ผมจะส่งลิงก์ห้องประชุมให้ล่วงหน้า 15 นาทีครับ", "prior = ก่อนล่วงหน้า"),
            ("Let's postpone the review until the data is verified.", "เราเลื่อนการทบทวนไปจนกว่าข้อมูลจะตรวจเสร็จดีกว่าครับ", "postpone = เลื่อนออกไป"),
            ("The meeting is scheduled to last approximately thirty minutes.", "การประชุมถูกกำหนดไว้ที่ประมาณ 30 นาทีครับ", "last approximately = กินเวลาราวๆ"),
            ("Could you please add John to the meeting invite?", "ช่วยเพิ่มจอห์นเข้าไปในรายชื่อผู้เข้าร่วมประชุมด้วยได้ไหมครับ", "add to the invite"),
            ("I have an urgent production issue and cannot join today.", "ผมติดปัญหาด่วนในสายการผลิต คงเข้าร่วมวันนี้ไม่ได้ครับ", "cannot join = เข้าร่วมไม่ได้"),
            ("Please find the proposed agenda attached for your review.", "โปรดดูวาระการประชุมที่เสนอในเอกสารแนบครับ", "proposed agenda = วาระที่เสนอ"),
            ("Can we move our call thirty minutes earlier?", "เราเลื่อนเวลาคุยให้เร็วขึ้น 30 นาทีได้ไหมครับ", "earlier = เร็วขึ้น"),
            ("I will be five minutes late due to traffic.", "ผมจะเข้าประชุมสาย 5 นาทีเนื่องจากรถติดครับ", "late due to"),
            ("Let's lock in the time for Thursday at 10 AM.", "เราขอล็อกเวลานัดเป็นวันพฤหัสบดี 10 โมงเช้าเลยนะครับ", "lock in = ล็อกเวลายืนยัน"),
            ("Thank you for accommodating my busy schedule.", "ขอบคุณมากที่ช่วยปรับเวลาตามตารางงานที่ยุ่งของผมครับ", "accommodating = ปรับตัวยืดหยุ่นให้"),
            ("Looking forward to our discussion tomorrow.", "รอคอยที่จะได้พูดคุยหารือกันในวันพรุ่งนี้นะครับ", "looking forward to = ตั้งตารอ")
        ]),
        "dialogues": make_dialogues([
            ("นัดเวลาคุยสเปกงาน", [("A", "Does tomorrow morning work for you?", "เช้าพรุ่งนี้สะดวกสำหรับคุณไหมครับ"), ("B", "Yes, 9:30 AM works perfectly.", "ได้เลยครับ เก้าโมงครึ่งสะดวกมาก")]),
            ("ขอเลื่อนนัดเพราะติดงานด่วน", [("Staff", "I have a conflict at 2 PM. Can we move it?", "ผมมีนัดชนตอนบ่ายสอง ขอเลื่อนได้ไหมครับ"), ("Client", "No problem, how about Friday at 10 AM?", "ไม่มีปัญหา วันศุกร์สิบโมงเช้าเป็นอย่างไร")]),
            ("ขอล็อกห้องประชุมใหญ่", [("Admin", "The main conference room is reserved for you.", "ห้องประชุมใหญ่จองไว้ให้คุณแล้วค่ะ"), ("Lead", "Thank you, please send the key card.", "ขอบคุณครับ รบกวนส่งคีย์การ์ดมาด้วยนะครับ")]),
            ("ประชุมผ่านโปรแกรม Teams", [("Host", "Can everyone see my shared screen?", "ทุกคนมองเห็นหน้าจอที่ผมแชร์ไหมครับ"), ("User", "Yes, loud and clear.", "เห็นชัดเจนและได้ยินเสียงชัดมากครับ")]),
            ("แจ้งขอเข้าประชุมสาย", [("Tech", "I will join 10 minutes late due to Line 1.", "ผมจะเข้าสาย 10 นาทีเพราะติดดูไลน์ 1 ครับ"), ("Host", "Understood, we will cover your part later.", "รับทราบ เดี๋ยวเราค่อยคุยส่วนของคุณทีหลัง")]),
            ("ยืนยันเวลากับซัพพลายเออร์", [("Buyer", "Confirming our supplier review for Thursday.", "ขอยืนยันนัดประเมินซัพพลายเออร์วันพฤหัสบดีนะ"), ("Vendor", "Confirmed. We have our slides ready.", "ยืนยันครับ พวกเราเตรียมสไลด์พร้อมแล้ว")]),
            ("ขอส่งคนอื่นเข้าประชุมแทน", [("Manager", "I cannot make it, but Dan will represent me.", "ผมไปไม่ได้ แต่แดนจะเป็นตัวแทนผมเข้าประชุม"), ("Leader", "Perfect, Dan knows the project well.", "ยอดเยี่ยมครับ แดนเข้าใจงานนี้เป็นอย่างดี")]),
            ("ขยายเวลาประชุมต่อ", [("Speaker", "We have 5 minutes left, but need more time.", "เหลือเวลา 5 นาทีแต่เราต้องการคุยต่ออีกหน่อย"), ("All", "We can stay another 15 minutes.", "พวกเราอยู่ต่อได้อีก 15 นาทีครับ")]),
            ("เตือนความจำก่อนเริ่มประชุม", [("Secretary", "Quick reminder: project sync starts in 10 mins.", "เตือนความจำ: ประชุมโปรเจกต์เริ่มในอีก 10 นาทีค่ะ"), ("Team", "Thanks, heading to the meeting room now.", "ขอบคุณครับ กำลังเดินไปห้องประชุมเดี๋ยวนี้")]),
            ("ส่งสรุปบันทึกการประชุม", [("Staff", "I just emailed the meeting minutes to all.", "ผมเพิ่งส่งบันทึกการประชุมทางอีเมลให้ทุกคนแล้วครับ"), ("Manager", "Great summary, thanks for the prompt action.", "สรุปได้ดีมาก ขอบคุณสำหรับการทำงานที่รวดเร็ว")])
        ]),
        "exercises": make_exercises([
            ("บ่ายวันพรุ่งนี้สะดวกสำหรับคุณไหมครับ", "Does tomorrow afternoon", "for you?", "คำกริยาแปลว่า ใช้การได้/สะดวก (w...)", "work", [], "Does tomorrow afternoon work for you?", "สำนวน 'Does [time] work for you?' แปลว่า วัน/เวลานั้นสะดวกไหม"),
            ("ผมเกรงว่าผมจะมีนัดหมายซ้อนกันในช่วงเวลานั้นครับ", "I am afraid I have a scheduling", "at that time.", "คำนามแปลว่า ขัดแย้ง/ชนกัน (c...)", "conflict", [], "I am afraid I have a scheduling conflict at that time.", "'scheduling conflict' แปลว่า ตารางเวลาชนกัน"),
            ("พวกเราสามารถเลื่อนการประชุมไปสัปดาห์หน้าได้ไหมครับ", "Could we", "the meeting to next week?", "คำกริยาแปลว่า กำหนดวันเวลาใหม่ (r...)", "reschedule", [], "Could we reschedule the meeting to next week?", "'reschedule' แปลว่า เลื่อนกำหนดการนัด"),
            ("คุณว่างสำหรับการคุยงานสั้นๆ ไหมครับ", "Are you", "for a short call?", "คำแปลว่า ว่าง/สะดวก (a...)", "available", [], "Are you available for a short call?", "'available' แปลว่า ว่างหรือสะดวก"),
            ("โปรดส่งคำเชิญปฏิทินมาให้ผมด้วยครับ", "Please send over a calendar", ".", "คำแปลว่า คำเชิญ (i...)", "invite", ["invitation"], "Please send over a calendar invite.", "'calendar invite' แปลว่า บัตรเชิญปฏิทินนัดหมาย"),
            ("เวลาไหนก็ได้หลังบ่ายสองโมงสะดวกสำหรับฉันมาก", "Any time after 2 PM works", "for me.", "คำกริยาวิเศษณ์แปลว่า อย่างสมบูรณ์แบบ (p...)", "perfectly", [], "Any time after 2 PM works perfectly for me.", "'works perfectly' แปลว่า สะดวกอย่างยิ่ง"),
            ("ขออภัยที่แจ้งเปลี่ยนแปลงเวลากะทันหันครับ", "Sorry for the short", "regarding the change.", "คำแปลว่า การบอกล่วงหน้าสั้นๆ (n...)", "notice", [], "Sorry for the short notice regarding the change.", "'short notice' แปลว่า แจ้งในเวลากระชั้นชิด"),
            ("เรามาเลื่อนการประชุมไปจนกว่าข้อมูลจะพร้อมดีกว่า", "Let's", "the meeting until data is ready.", "คำกริยาแปลว่า เลื่อนออกไป (p...)", "postpone", [], "Let's postpone the meeting until data is ready.", "'postpone' แปลว่า เลื่อนออกไป"),
            ("โปรดดูวาระการประชุมที่แนบมานี้", "Please check the attached meeting", ".", "คำนามแปลว่า วาระการประชุม (a...)", "agenda", [], "Please check the attached meeting agenda.", "'meeting agenda' แปลว่า วาระการประชุม"),
            ("ขอยืนยันนัดหมายของเราในวันพฤหัสบดีครับ", "Confirming our", "for Thursday.", "คำนามแปลว่า การนัดหมาย (a...)", "appointment", [], "Confirming our appointment for Thursday.", "'appointment' แปลว่า การนัดหมาย")
        ]),
        "stories": make_stories([
            ("Double Booked at 2 PM", "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=900&auto=format&fit=crop&q=80",
             [("conflict", "n.", "เวลาชนกัน"), ("reschedule", "v.", "เลื่อนนัด"), ("polite", "adj.", "สุภาพ"), ("smooth", "adj.", "ราบรื่น")],
             "Mark noticed two calendar meetings booked at 2 PM: one with QA and one with a supplier.<br><br>He sent a <b>polite</b> email explaining the <b>conflict</b> and <b>rescheduled</b> the vendor call to 3:30 PM. Both meetings proceeded in a completely <b>smooth</b> manner.",
             "Mark noticed two calendar meetings booked at 2 PM: one with QA and one with a supplier. He sent a polite email explaining the conflict and rescheduled the vendor call to 3:30 PM. Both meetings proceeded in a completely smooth manner.",
             "มาร์คพบว่าปฏิทินของเขามีนัดซ้อนกันสองนัดตอนบ่ายสอง: นัดหนึ่งกับ QA อีกนัดกับซัพพลายเออร์ เขาจึงส่งข้อความอย่างสุภาพเพื่อขอเลื่อนเวลากับซัพพลายเออร์ไปเป็นบ่ายสามโมงครึ่ง ทั้งสองการประชุมจึงดำเนินไปได้อย่างราบรื่น"),
            ("The Missing Meeting Link", "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=900&auto=format&fit=crop&q=80",
             [("invite", "n.", "คำเชิญ"), ("dial-in", "n.", "ลิงก์เข้าประชุม"), ("punctual", "adj.", "ตรงเวลา"), ("productive", "adj.", "ได้ผลงานดี")],
             "Ten minutes before the cross-plant sync, engineers noticed the <b>dial-in</b> link was missing from the calendar <b>invite</b>.<br><br>Anna immediately re-sent the update with the link. All participants joined <b>punctual</b> and prepared, making the sync remarkably <b>productive</b>.",
             "Ten minutes before the cross-plant sync, engineers noticed the dial-in link was missing from the calendar invite. Anna immediately re-sent the update with the link. All participants joined punctual and prepared, making the sync remarkably productive.",
             "สิบนาทีก่อนเริ่มประชุมข้ามโรงงาน วิศวกรสังเกตเห็นว่าไม่มีลิงก์เข้าประชุมในคำเชิญปฏิทิน แอนนารีบส่งอัปเดตพร้อมลิงก์ใหม่ทันที ทุกคนจึงเข้าประชุมได้อย่างตรงเวลาและได้ข้อสรุปการทำงานที่ยอดเยี่ยม"),
            ("Finding the Golden Hour", "https://images.unsplash.com/photo-1497215728101-856f4ea42174?w=900&auto=format&fit=crop&q=80",
             [("convenient", "adj.", "สะดวก"), ("poll", "v.", "สำรวจความเห็น"), ("unanimous", "adj.", "เป็นเอกฉันท์"), ("cooperation", "n.", "ความร่วมมือ")],
             "Scheduling four busy shift managers seemed impossible until Ploy sent a quick survey: “Does 8:30 AM before shift start work for you?”<br><br>The vote was <b>unanimous</b>. Early morning proved the most <b>convenient</b> hour, leading to great cross-shift <b>cooperation</b>.",
             "Scheduling four busy shift managers seemed impossible until Ploy sent a quick survey: Does 8:30 AM before shift start work for you? The vote was unanimous. Early morning proved the most convenient hour, leading to great cross-shift cooperation.",
             "การจัดเวลาให้หัวหน้ากะ 4 คนที่งานยุ่งดูเป็นเรื่องยาก จนกระทั่งพลอยส่งแบบสำรวจสั้นๆ: เช้า 8:30 น. ก่อนเริ่มกะสะดวกไหมคะ ทุกคนตอบเห็นชอบเป็นเอกฉันท์ ช่วงเช้าตรู่กลายเป็นเวลาที่สะดวกที่สุดและนำมาซึ่งความร่วมมืออันดี"),
            ("Short Notice Gratitude", "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=900&auto=format&fit=crop&q=80",
             [("notice", "n.", "การแจ้งล่วงหน้า"), ("apologize", "v.", "ขอโทษ"), ("understanding", "adj.", "ที่เข้าใจผู้อื่น"), ("respect", "n.", "ความเคารพ")],
             "A pipe burst in the warehouse forced Karan to cancel a job interview on just twenty minutes' <b>notice</b>.<br><br>Instead of an automated message, he phoned the candidate to <b>apologize</b> personally. The candidate was deeply <b>understanding</b>, creating mutual <b>respect</b> from day one.",
             "A pipe burst in the warehouse forced Karan to cancel a job interview on just twenty minutes' notice. Instead of an automated message, he phoned the candidate to apologize personally. The candidate was deeply understanding, creating mutual respect from day one.",
             "ท่อน้ำแตกในคลังสินค้าบีบให้การันต้องยกเลิกนัดสัมภาษณ์ล่วงหน้าเพียง 20 นาที แทนที่จะส่งอีเมลอัตโนมัติ เขาเลือกโทรไปขอโทษผู้สมัครด้วยตนเอง ผู้สมัครเข้าใจสถานการณ์อย่างมาก และสร้างความประทับใจและความเคารพซึ่งกันและกันตั้งแต่วันแรก")
        ])
    },
    "6": {
        "day": 6,
        "title": "Day 6: Clarifying Instructions & Active Listening",
        "summary": "การทวนความเข้าใจ เช็คคำสั่ง เพื่อป้องกันความผิดพลาดในการทำงาน",
        "rule": "Let me confirm... | Just to clarify... | Did you mean...?",
        "vocab": make_vocab([
            ("Elaborate", "/iˈlæb.ə.reɪt/", "v.", "อธิบายขยายความ", "Could you elaborate further?", "ช่วยอธิบายเพิ่มเติมได้ไหม"),
            ("Alignment", "/əˈlaɪn.mənt/", "n.", "ความเข้าใจตรงกัน", "We need team alignment.", "เราต้องเข้าใจตรงกัน"),
            ("Specification", "/ˌspes.ɪ.fɪˈkeɪ.ʃən/", "n.", "สเปกข้อกำหนด", "Read the specifications.", "อ่านข้อกำหนดสเปก"),
            ("Verify", "/ˈver.ɪ.faɪ/", "v.", "ทวนสอบความถูกต้อง", "Verify the serial numbers.", "ทวนสอบหมายเลขซีเรียล"),
            ("Ambiguous", "/æmˈbɪɡ.ju.əs/", "adj.", "กำกวมคลุมเครือ", "The instruction was ambiguous.", "คำสั่งมีความคลุมเครือ"),
            ("Summarize", "/ˈsʌm.ər.aɪz/", "v.", "สรุปใจความ", "Summarize the main points.", "สรุปประเด็นสำคัญ"),
            ("Misunderstanding", "/ˌmɪs.ʌn.dəˈstæn.dɪŋ/", "n.", "ความเข้าใจผิด", "Avoid misunderstanding.", "หลีกเลี่ยงความเข้าใจผิด"),
            ("Rephrase", "/ˌriːˈfreɪz/", "v.", "ทวนประโยคใหม่", "Let me rephrase my point.", "ขอผมพูดใหม่ให้เข้าใจง่าย"),
            ("Ensure", "/ɪnˈʃɔːr/", "v.", "ดูแลให้มั่นใจ", "Ensure the box is sealed.", "ดูแลให้มั่นใจว่ากล่องปิดสนิท"),
            ("Comprehend", "/ˌkɒm.prɪˈhend/", "v.", "เข้าใจลึกซึ้ง", "Do you comprehend the SOP?", "คุณเข้าใจ SOP ครบถ้วนไหม"),
            ("Clarification", "/ˌklær.ɪ.fɪˈkeɪ.ʃən/", "n.", "คำชี้แจง", "Thanks for the clarification.", "ขอบคุณสำหรับคำชี้แจง"),
            ("Instruction", "/ɪnˈstrʌk.ʃən/", "n.", "คำสั่งแนะนำ", "Follow safety instructions.", "ทำตามคำแนะนำความปลอดภัย"),
            ("Explicit", "/ɪkˈsplɪs.ɪt/", "adj.", "ชัดเจนตรงไปตรงมา", "Give explicit instructions.", "ให้คำสั่งที่ชัดเจนตรงไปตรงมา"),
            ("Confirmation", "/ˌkɒn.fəˈmeɪ.ʃən/", "n.", "การยืนยัน", "Wait for confirmation.", "รอการยืนยัน"),
            ("Guidance", "/ˈɡaɪ.dəns/", "n.", "คำชี้แนะ", "Thank you for your guidance.", "ขอบคุณสำหรับคำชี้แนะ"),
            ("Tolerance", "/ˈtɒl.ər.əns/", "n.", "เกณฑ์คลาดเคลื่อน", "Check the tolerance limit.", "ตรวจเกณฑ์ความคลาดเคลื่อน"),
            ("Concrete", "/ˈkɒŋ.kriːt/", "adj.", "เป็นรูปธรรมชัดเจน", "Give a concrete example.", "ยกตัวอย่างที่เป็นรูปธรรม"),
            ("Recap", "/ˈriː.kæp/", "n./v.", "สรุปย่อ", "Send a meeting recap.", "ส่งอีเมลสรุปย่อ"),
            ("Adhere", "/ədˈhɪər/", "v.", "ยึดมั่นปฏิบัติตาม", "Adhere to the standard.", "ปฏิบัติตามมาตรฐาน"),
            ("Acknowledge", "/əkˈnɒl.ɪdʒ/", "v.", "ตอบรับทราบ", "Please acknowledge this mail.", "โปรดตอบรับทราบอีเมลนี้")
        ]),
        "phrases": make_phrases([
            ("Just to make sure we are on the same page, should I prepare the report first?", "เพื่อความเข้าใจที่ตรงกัน ผมควรเตรียมรายงานก่อนใช่ไหมครับ", "on the same page = เข้าใจตรงกัน"),
            ("Could you please elaborate on what you mean by that?", "ช่วยขยายความสิ่งที่คุณหมายถึงเพิ่มเติมอีกนิดได้ไหมครับ", "elaborate = อธิบายเพิ่ม"),
            ("If I understand correctly, the deadline is moved to next Monday.", "ถ้าผมเข้าใจถูกต้อง กำหนดส่งเลื่อนไปเป็นวันจันทร์หน้าใช่ไหมครับ", "If I understand correctly"),
            ("Could you please speak a bit slower? I want to catch every detail.", "ช่วยพูดช้าลงอีกนิดนึงได้ไหมครับ พอดีผมอยากจดรายละเอียดให้ครบถ้วน", "speak a bit slower"),
            ("Let me rephrase that to make sure I got your point.", "ขออนุญาตทวนประโยคอีกครั้งเพื่อให้แน่ใจว่าผมเข้าใจประเด็นของคุณครับ", "rephrase = เปลี่ยนคำทบทวน"),
            ("Did you mean the raw material batch or the finished goods?", "คุณหมายถึงล็อตวัตถุดิบหรือสินค้าสำเร็จรูปครับ", "Did you mean...?"),
            ("Could you please put that instruction in an email for reference?", "รบกวนช่วยสรุปคำสั่งส่งมาทางอีเมลเพื่อใช้อ้างอิงได้ไหมครับ", "for reference = ใช้อ้างอิง"),
            ("I understand your point clearly now. Thank you for the clarification.", "ตอนนี้ผมเข้าใจประเด็นของคุณอย่างชัดเจนแล้วครับ ขอบคุณสำหรับคำชี้แจง", "clarification = คำชี้แจง"),
            ("So, to confirm: Step 1 is scanning, and Step 2 is labeling, correct?", "สรุปคือ ขั้นตอนที่ 1 สแกน และขั้นตอนที่ 2 ติดฉลาก ถูกต้องไหมครับ", "to confirm = เพื่อยืนยัน"),
            ("Are there any specific tolerances we need to adhere to?", "มีค่าความคลาดเคลื่อนเฉพาะที่พวกเราต้องปฏิบัติตามไหมครับ", "adhere to = ยึดถือตาม"),
            ("What is the expected outcome of this process change?", "ผลลัพธ์ที่คาดหวังจากการเปลี่ยนกระบวนการนี้คืออะไรครับ", "expected outcome = ผลที่คาดหวัง"),
            ("I want to double-check before I take action.", "ผมอยากตรวจสอบความถูกต้องอีกครั้งก่อนที่จะลงมือทำครับ", "double-check"),
            ("Please correct me if I am wrong.", "ท้วงติงได้เลยนะครับหากผมเข้าใจอะไรผิดไป", "correct me if I am wrong"),
            ("Does everyone understand the new SOP requirements?", "ทุกคนเข้าใจข้อกำหนดของ SOP ตัวใหม่ครบถ้วนแล้วใช่ไหมครับ", "new SOP requirements"),
            ("Could you provide a concrete example of this defect?", "ช่วยยกตัวอย่างของเสียแบบชัดเจนเป็นรูปธรรมให้ดูหน่อยได้ไหมครับ", "concrete example = ตัวอย่างชัดเจน"),
            ("I hear what you are saying, but let's check the manual.", "ผมเข้าใจสิ่งที่คุณพูดครับ แต่เรามาเปิดคู่มือเช็คกันอีกทีดีกว่า", "I hear what you are saying"),
            ("Let's summarize the key action points before we leave.", "เรามาสรุปการบ้านสิ่งที่ต้องทำก่อนแยกย้ายกันครับ", "key action points"),
            ("I will send a recap email by the end of the day.", "ผมจะส่งอีเมลสรุปประเด็นให้ภายในสิ้นวันนี้นะครับ", "recap email = อีเมลสรุป"),
            ("Can you hear me clearly on the call?", "ได้ยินเสียงผมชัดเจนในสายไหมครับ", "hear me clearly"),
            ("Thank you for clearing up that confusion.", "ขอบคุณมากครับที่ช่วยเคลียร์ความสับสนตรงนั้นให้กระจ่าง", "clearing up = เคลียร์ให้ชัด")
        ]),
        "dialogues": make_dialogues([
            ("ทวนความเข้าใจคำสั่งหัวหน้า", [("Leader", "Pack all green boxes first.", "แพ็คกล่องสีเขียวทั้งหมดก่อนนะ"), ("Staff", "To confirm, only green boxes for now?", "ขอทวนครับ ตอนนี้ทำเฉพาะกล่องเขียวใช่ไหมครับ")]),
            ("ขอให้พูดช้าลงหน่อย", [("Foreigner", "We need to dispatch the cargo ASAP via airfreight.", "เราต้องส่งคาร์โก้ด่วนที่สุดทางเครื่องบิน"), ("Staff", "Could you please speak a bit slower?", "ช่วยพูดช้าลงอีกนิดหนึ่งได้ไหมครับ")]),
            ("ถามแยกแยะระหว่างสองล็อต", [("QA", "Inspect batch forty-five.", "ตรวจแบทช์ 45 ด้วยนะ"), ("Staff", "Did you mean 45A or 45B?", "หมายถึง 45A หรือ 45B ครับ")]),
            ("ขอให้อธิบายขยายความ", [("Staff", "Could you elaborate on the test criteria?", "ช่วยขยายความเกณฑ์การทดสอบหน่อยครับ"), ("Engineer", "It must withstand 50 Newtons of force.", "มันต้องทนแรงกดได้ 50 นิวตันครับ")]),
            ("ขอให้พิมพ์คำสั่งส่งมาทางอีเมล", [("Staff", "Could you put that in an email for reference?", "ช่วยสรุปทางอีเมลไว้ใช้อ้างอิงหน่อยได้ไหมครับ"), ("Manager", "Sure, I will send it in 5 minutes.", "ได้เลย เดี๋ยวผมส่งให้ใน 5 นาที")]),
            ("เช็คความเข้าใจเรื่องเดดไลน์", [("Staff", "If I understand correctly, delivery is on Friday?", "ถ้าเข้าใจถูกคือส่งมอบวันศุกร์ใช่ไหมครับ"), ("Client", "Yes, exactly on Friday morning.", "ใช่ครับ วันศุกร์เช้าแน่นอน")]),
            ("ถามหาสาเหตุที่แท้จริง", [("Auditor", "What caused the label misprint?", "อะไรทำให้พิมพ์ฉลากผิดครับ"), ("Operator", "The thermal ribbon was loosely installed.", "ริบบอนความร้อนใส่ไว้หลวมครับ")]),
            ("ขอตัวอย่างข้อบกพร่องจริง", [("New Hire", "Could you show me a sample defect?", "ช่วยเปิดตัวอย่างของเสียให้ดูหน่อยได้ไหมครับ"), ("Trainer", "Look at this crack along the edge.", "ดูรอยร้าวตามขอบตรงนี้เป็นตัวอย่างนะ")]),
            ("ทวนตัวเลขยอดนับสินค้า", [("Staff", "Did you say 14 or 40 boxes?", "เมื่อกี้คุณพูดว่า 14 หรือ 40 กล่องนะครับ"), ("Counter", "Fourteen. One-four.", "สิบสี่ครับ หนึ่งกับสี่")]),
            ("สรุปหลังคุยงานจบ", [("Staff", "I will send a recap email right away.", "เดี๋ยวผมรีบส่งอีเมลสรุปให้ทันทีครับ"), ("Leader", "Thanks, that ensures we are aligned.", "ขอบคุณ ช่วยให้เราเข้าใจตรงกันดีมาก")])
        ]),
        "exercises": make_exercises([
            ("เพื่อให้แน่ใจว่าเราเข้าใจตรงกัน", "Just to make sure we are on the", "page.", "คำแปลว่า หน้าเดียวกัน (s...)", "same", [], "Just to make sure we are on the same page.", "'on the same page' หมายถึง มีความเข้าใจตรงกัน"),
            ("ช่วยอธิบายขยายความเพิ่มเติมในจุดนี้ได้ไหมครับ", "Could you please", "on this specific point?", "คำกริยาแปลว่า ขยายความ (e...)", "elaborate", [], "Could you please elaborate on this specific point?", "'elaborate on' แปลว่า ให้รายละเอียดเพิ่มเติม"),
            ("ถ้าผมเข้าใจถูกต้อง งานนี้ต้องส่งมอบภายในวันพรุ่งนี้", "If I understand", ", this must be sent tomorrow.", "คำกริยาวิเศษณ์แปลว่า อย่างถูกต้อง (c...)", "correctly", [], "If I understand correctly, this must be sent tomorrow.", "'If I understand correctly' เป็นสำนวนเช็คความเข้าใจ"),
            ("ช่วยพูดช้าลงอีกนิดหนึ่งได้ไหมครับ", "Could you please speak a bit", "?", "คำแปลว่า ช้าลง (s...)", "slower", [], "Could you please speak a bit slower?", "'speak a bit slower' แปลว่า พูดช้าลงอีกนิด"),
            ("คุณหมายถึงชิ้นส่วนตัวเก่าหรือตัวใหม่ครับ", "Did you", "the old part or the new one?", "คำกริยาแปลว่า หมายถึง (m...)", "mean", [], "Did you mean the old part or the new one?", "'Did you mean...?' แปลว่า คุณหมายถึง...ใช่ไหม"),
            ("ขอให้ผมทวนประโยคเพื่อความเข้าใจที่ถูกต้อง", "Let me", "that to be clear.", "คำกริยาแปลว่า พูดใหม่ด้วยคำอื่น (r...)", "rephrase", [], "Let me rephrase that to be clear.", "'rephrase' แปลว่า ทวนด้วยคำพูดใหม่"),
            ("ช่วยส่งคำสั่งนี้ทางอีเมลเพื่อใช้อ้างอิงด้วยครับ", "Put that in an email for", ".", "คำแปลว่า การอ้างอิง (r...)", "reference", [], "Put that in an email for reference.", "'for reference' แปลว่า ไว้ใช้อ้างอิง"),
            ("ขอบคุณมากสำหรับคำชี้แจงที่ชัดเจนครับ", "Thank you for the", ".", "คำนามแปลว่า คำชี้แจง (c...)", "clarification", [], "Thank you for the clarification.", "'clarification' แปลว่า คำชี้แจงให้กระจ่าง"),
            ("เราต้องทำให้มั่นใจว่ากระบวนการปลอดภัย", "We must", "that the process is safe.", "คำกริยาแปลว่า ทำให้มั่นใจ (e...)", "ensure", [], "We must ensure that the process is safe.", "'ensure' แปลว่า ทำให้แน่ใจ"),
            ("ท้วงติงผมได้เลยหากผมเข้าใจผิดไป", "Please", "me if I am wrong.", "คำกริยาแปลว่า แก้ไขให้ถูกต้อง (c...)", "correct", [], "Please correct me if I am wrong.", "'correct me if I am wrong' แปลว่า ท้วงได้ถ้าผมผิด")
        ]),
        "stories": make_stories([
            ("The Fourteen or Forty Mix-up", "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=900&auto=format&fit=crop&q=80",
             [("clarify", "v.", "ชี้แจง"), ("shout", "v.", "ตะโกน"), ("pallet", "n.", "พาเลท"), ("prevent", "v.", "ป้องกัน")],
             "Over noisy machine hums, Ben heard his supervisor <b>shout</b>: “Load forty pallets!” But the small truck could only hold fourteen.<br><br>Ben stepped closer to <b>clarify</b>: “Did you say 14 or 40?” The boss laughed: “Fourteen! Good catch.” Active listening <b>prevented</b> a major shipping blunder.",
             "Over noisy machine hums, Ben heard his supervisor shout: Load forty pallets! But the small truck could only hold fourteen. Ben stepped closer to clarify: Did you say 14 or 40? The boss laughed: Fourteen! Good catch. Active listening prevented a major shipping blunder.",
             "ท่ามกลางเสียงเครื่องจักรดัง เบนได้ยินหัวหน้าตะโกนว่า: โหลด 40 พาเลท! แต่รถบรรทุกคันเล็กบรรทุกได้เพียง 14 พาเลท เบนเดินเข้าไปถามซ้ำ: 14 หรือ 40 นะครับ หัวหน้าหัวเราะ: สิบสี่จ้า ขอบใจที่ทวน การตั้งใจฟังช่วยป้องกันความผิดพลาดใหญ่ได้ทันเวลา"),
            ("Inches or Centimeters?", "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=900&auto=format&fit=crop&q=80",
             [("alignment", "n.", "ความตรงกัน"), ("blueprint", "n.", "พิมพ์เขียว"), ("dimension", "n.", "ขนาดสัดส่วน"), ("flawless", "adj.", "ไร้ที่ติ")],
             "Before cutting metal racks for Room A1, Team Leader Sam held a short briefing: “Let’s double-check all <b>dimensions</b> on the <b>blueprint</b>.”<br><br>They caught an error where height was marked in inches instead of centimeters! Fixing it ensured the assembly was completely <b>flawless</b>.",
             "Before cutting metal racks for Room A1, Team Leader Sam held a short briefing: Let’s double-check all dimensions on the blueprint. They caught an error where height was marked in inches instead of centimeters! Fixing it ensured the assembly was completely flawless.",
             "ก่อนตัดแร็คเหล็กสำหรับห้อง A1 หัวหน้าแซมเรียกคุยสั้นๆ: มาทวนขนาดสัดส่วนในพิมพ์เขียวกันอีกรอบนะ พวกเขาตรวจพบว่าความสูงถูกเขียนเป็นหน่วยนิ้วแทนที่จะเป็นเซนติเมตร! การตรวจทวนช่วยให้การประกอบเสร็จสมบูรณ์แบบไร้ที่ติ"),
            ("Speak Slower, Please", "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=900&auto=format&fit=crop&q=80",
             [("auditor", "n.", "ผู้ตรวจประเมิน"), ("rapidly", "adv.", "อย่างรวดเร็ว"), ("polite", "adj.", "สุภาพ"), ("praise", "v.", "ชมเชย")],
             "An American customer auditor spoke <b>rapidly</b> while inspecting the warehouse. Operator Joy <b>politely</b> raised her hand: “Could you please speak a bit slower so I capture every note?”<br><br>The auditor smiled, slowed his pace, and later <b>praised</b> Joy for her clear and confident communication.",
             "An American customer auditor spoke rapidly while inspecting the warehouse. Operator Joy politely raised her hand: Could you please speak a bit slower so I capture every note? The auditor smiled, slowed his pace, and later praised Joy for her clear and confident communication.",
             "ผู้ตรวจประเมินชาวอเมริกันพูดเร็วมากขณะตรวจคลังสินค้า จอยพนักงานสาวกล้ายกมือถามอย่างสุภาพ: ช่วยพูดช้าลงอีกนิดได้ไหมคะเพื่อหนูจะได้จดครบทุกข้อ ผู้ตรวจยิ้ม พูดช้าลง และยังเอ่ยปากชมเชยความมั่นใจในการสื่อสารของเธอ"),
            ("The Bulleted Recap Email", "https://images.unsplash.com/photo-1497215728101-856f4ea42174?w=900&auto=format&fit=crop&q=80",
             [("recap", "n.", "สรุปย่อ"), ("habit", "n.", "นิสัย"), ("agreement", "n.", "ข้อตกลง"), ("clarity", "n.", "ความชัดเจน")],
             "After an intense phone discussion about revised delivery dates, Dan always writes a quick <b>recap</b> email with bulleted points.<br><br>This simple professional <b>habit</b> created unquestionable <b>clarity</b> and mutual <b>agreement</b>, completely eliminating misunderstandings between departments.",
             "After an intense phone discussion about revised delivery dates, Dan always writes a quick recap email with bulleted points. This simple professional habit created unquestionable clarity and mutual agreement, completely eliminating misunderstandings between departments.",
             "หลังจากคุยสายเรื่องการเปลี่ยนรอบส่งของ แดนจะส่งอีเมลสรุปประเด็นเป็นข้อๆ สั้นๆ เสมอ นิสัยการทำงานอย่างมืออาชีพนี้สร้างความชัดเจนและข้อตกลงที่ตรงกัน ช่วยขจัดความเข้าใจผิดระหว่างแผนกได้อย่างสิ้นเชิง")
        ])
    },
    "7": {
        "day": 7,
        "title": "Day 7: Weekly Wrap-up & Executive Summary",
        "summary": "การเขียนสรุปผลงานประจำสัปดาห์ (Highlights, Metrics, Next Week Plan)",
        "rule": "เน้นสรุปแบบ Bullet points กระชับ ชัดเจน พร้อมระบุตัวเลขชี้วัดผลงาน",
        "vocab": make_vocab([
            ("Achievement", "/əˈtʃiːv.mənt/", "n.", "ความสำเร็จผลงาน", "This is a great achievement.", "นี่คือความสำเร็จที่ยอดเยี่ยม"),
            ("Benchmark", "/ˈbentʃ.mɑːk/", "n.", "เกณฑ์มาตรฐาน", "We beat the benchmark.", "เราทำได้ดีกว่าเกณฑ์มาตรฐาน"),
            ("Output", "/ˈaʊt.pʊt/", "n.", "ผลผลิตรวม", "Total output hit 10,000 units.", "ยอดผลผลิตแตะหมื่นชิ้น"),
            ("Efficiency", "/ɪˈfɪʃ.ən.si/", "n.", "ประสิทธิภาพ", "Picking efficiency rose by 8%.", "ประสิทธิภาพการหยิบของเพิ่ม 8%"),
            ("Summary", "/ˈsʌm.ər.i/", "n.", "บทสรุปย่อ", "Here is the weekly summary.", "นี่คือสรุปประจำสัปดาห์"),
            ("Momentum", "/məˈmen.təm/", "n.", "แรงส่งความต่อเนื่อง", "Keep up the great momentum.", "รักษาแรงขับเคลื่อนที่ดีไว้"),
            ("Accomplish", "/əˈkʌm.plɪʃ/", "v.", "ทำสำเร็จลุล่วง", "We accomplished all goals.", "พวกเราทำเป้าหมายสำเร็จครบ"),
            ("Metric", "/ˈmet.rɪk/", "n.", "ตัวชี้วัดผลงาน", "Review operational metrics.", "ตรวจดูตัวชี้วัดผลการทำงาน"),
            ("Exceed", "/ɪkˈsiːd/", "v.", "ทำได้เกินกว่า", "Output exceeded forecast.", "ยอดผลิตเกินกว่าคาดการณ์"),
            ("Objective", "/əbˈdʒek.tɪv/", "n.", "เป้าหมายหลัก", "Our objective was achieved.", "เป้าหมายของเราบรรลุผล"),
            ("Overcome", "/ˌəʊ.vəˈkʌm/", "v.", "เอาชนะอุปสรรค", "We overcame the delays.", "พวกเราเอาชนะความล่าช้าได้"),
            ("Consistent", "/kənˈsɪs.tənt/", "adj.", "สม่ำเสมอ", "Show consistent quality.", "แสดงคุณภาพที่สม่ำเสมอ"),
            ("Contribution", "/ˌkɒn.trɪˈbjuː.ʃən/", "n.", "การมีส่วนร่วมช่วย", "Thanks for your contribution.", "ขอบคุณสำหรับการช่วยงาน"),
            ("Productivity", "/ˌprɒd.ʌkˈtɪv.ə.ti/", "n.", "ผลิตภาพ", "Productivity reached record high.", "ผลิตภาพแตะระดับสูงสุด"),
            ("Highlight", "/ˈhaɪ.laɪt/", "n.", "ผลงานเด่น", "Here are weekly highlights.", "นี่คือผลงานเด่นประจำสัปดาห์"),
            ("Forecast", "/ˈfɔː.kɑːst/", "n.", "การคาดการณ์", "Review next week's forecast.", "ดูยอดคาดการณ์สัปดาห์หน้า"),
            ("Restful", "/ˈrest.fəl/", "adj.", "ที่ได้พักผ่อนเต็มที่", "Have a restful weekend.", "ขอให้ได้พักผ่อนอย่างเต็มที่"),
            ("Dedication", "/ˌded.ɪˈkeɪ.ʃən/", "n.", "ความทุ่มเท", "Your dedication is recognized.", "ความทุ่มเทของคุณได้รับการยอมรับ"),
            ("Seamless", "/ˈsiːm.ləs/", "adj.", "ราบรื่นไร้รอยต่อ", "Seamless teamwork this week.", "การทำงานร่วมกันราบรื่นมาก"),
            ("Milestone", "/ˈmaɪl.stəʊn/", "n.", "ก้าวสำคัญ", "We hit the week 1 milestone.", "เราผ่านก้าวสัปดาห์ที่ 1 แล้ว")
        ]),
        "phrases": make_phrases([
            ("Here is the summary of our weekly achievements.", "นี่คือสรุปผลการดำเนินงานที่สำเร็จในสัปดาห์นี้ครับ", "achievement = ความสำเร็จ"),
            ("We achieved a 98% on-time delivery rate this week.", "สัปดาห์นี้เราทำอัตราการส่งมอบตรงเวลาได้ถึง 98% ครับ", "ระบุตัวเลขสร้างความน่าเชื่อถือ"),
            ("Our top priority for next week is system optimization.", "เป้าหมายสำคัญอันดับแรกสำหรับสัปดาห์หน้าคือการปรับปรุงระบบครับ", "top priority = สำคัญที่สุด"),
            ("Thank you all for your hard work throughout the week.", "ขอบคุณทุกคนสำหรับการทำงานอย่างหนักตลอดทั้งสัปดาห์ครับ", "คำขอบคุณทีมงานวันศุกร์"),
            ("We managed to overcome all unexpected delays.", "พวกเราสามารถเอาชนะและจัดการความล่าช้าที่ไม่คาดคิดได้ทั้งหมดครับ", "overcome = เอาชนะอุปสรรค"),
            ("Total scrap was reduced by 4.5% compared to last week.", "ยอดของเสียรวมลดลงไป 4.5% เมื่อเทียบกับสัปดาห์ที่แล้วครับ", "compared to = เมื่อเทียบกับ"),
            ("Please review the attached spreadsheet for full metrics.", "โปรดดูไฟล์สเปรดชีตที่แนบมาสำหรับตัวเลขดัชนีชี้วัดฉบับเต็มครับ", "metrics = ตัวชี้วัด"),
            ("Have a restful weekend, everyone!", "ขอให้ทุกคนได้พักผ่อนอย่างเต็มที่ในวันหยุดสุดสัปดาห์นะครับ!", "restful weekend = วันหยุดที่ได้พักผ่อน"),
            ("We successfully hit all our weekly KPIs.", "พวกเราทำผลงานบรรลุตัวชี้วัด KPI ประจำสัปดาห์ได้ทั้งหมดครับ", "hit KPIs = บรรลุตัวชี้วัด"),
            ("The warehouse reorganization project is 50% complete.", "โปรเจกต์จัดระเบียบคลังสินค้าสำเร็จไปแล้ว 50% ครับ", "percent complete"),
            ("No safety incidents occurred during the entire week.", "ไม่มีอุบัติเหตุด้านความปลอดภัยเกิดขึ้นเลยตลอดทั้งสัปดาห์ครับ", "no safety incidents"),
            ("Production output exceeded the original forecast.", "ยอดการผลิตทำได้เกินกว่าตัวเลขที่คาดการณ์ไว้แต่แรกครับ", "exceeded the forecast"),
            ("Let's maintain this positive momentum into Monday.", "มารักษาแรงผลักดันเชิงบวกนี้ต่อเนื่องไปถึงวันจันทร์กันครับ", "maintain momentum"),
            ("I appreciate each person's dedication to quality.", "ผมขอชื่นชมความทุ่มเทในเรื่องคุณภาพของทุกคนครับ", "dedication to quality"),
            ("Next week's shipment schedule will be heavy on Tuesday.", "ตารางส่งของสัปดาห์หน้าจะหนาแน่นมากในวันอังคารครับ", "heavy on Tuesday"),
            ("The inventory variance was under 0.1%, our best record.", "ยอดนับสต็อกคลาดเคลื่อนต่ำกว่า 0.1% ซึ่งเป็นสถิติดีที่สุดของเรา", "best record"),
            ("Thank you for the seamless cross-department collaboration.", "ขอบคุณสำหรับการประสานงานข้ามแผนกที่ราบรื่นมากครับ", "seamless collaboration"),
            ("Please submit your overtime logs before leaving today.", "กรุณาส่งใบบันทึกโอทีก่อนกลับบ้านในวันนี้ด้วยครับ", "overtime logs"),
            ("We are ready to tackle the new challenges next week.", "พวกเราพร้อมที่จะรับมือกับความท้าทายใหม่ในสัปดาห์หน้าแล้วครับ", "tackle challenges"),
            ("Congratulations on completing Week 1 of English Sprint!", "ขอแสดงความยินดีด้วยที่คุณเรียนจบสัปดาห์ที่ 1 ของ English Sprint!", "congratulations on")
        ]),
        "dialogues": make_dialogues([
            ("รายงานสรุปวันศุกร์กับผู้จัดการ", [("Manager", "How did we wrap up the week, Sam?", "สัปดาห์นี้ปิดยอดผลงานเป็นอย่างไรบ้าง แซม"), ("Sam", "We achieved 99% accuracy on inventory counts.", "เราทำความแม่นยำสต็อกได้ถึง 99% ครับ")]),
            ("ฉลองยอดของเสียลดลง", [("QA", "Scrap rate dropped by 4.5% this week!", "อัตราของเสียลดลงไป 4.5% ในสัปดาห์นี้!"), ("Lead", "Outstanding work by all shift operators.", "ผลงานยอดเยี่ยมของพนักงานทุกคนทุกกะเลย")]),
            ("ทบทวนเรื่องความปลอดภัยรอบสัปดาห์", [("Officer", "Zero accidents recorded for five straight days.", "ไม่มีอุบัติเหตุเลยตลอด 5 วันติดต่อกัน"), ("Team", "Safety is our number one culture.", "ความปลอดภัยคือวัฒนธรรมอันดับหนึ่งของเรา")]),
            ("เป้าหมายสำหรับสัปดาห์หน้า", [("Leader", "What is our focus for Monday morning?", "วันจันทร์เช้าเราจะเน้นเรื่องอะไรกัน"), ("Staff", "We will start reorganizing Room A2 racks.", "เราจะเริ่มจัดระเบียบแร็คในห้อง A2 ครับ")]),
            ("ขอบคุณทีมงานก่อนแยกย้าย", [("Supervisor", "Thank you everyone for the great dedication.", "ขอบคุณทุกคนมากสำหรับความทุ่มเทอันยอดเยี่ยม"), ("Staff", "Have a wonderful weekend, boss!", "ขอให้มีวันหยุดสุดสัปดาห์ที่ดีครับหัวหน้า!")]),
            ("ส่งไฟล์สรุปดัชนีชี้วัด", [("Staff", "The weekly KPI deck is emailed to executives.", "ส่งสไลด์ KPI รายสัปดาห์ให้ผู้บริหารทางอีเมลแล้วครับ"), ("Director", "I received it. The numbers look impressive.", "ได้รับแล้ว ตัวเลขดูน่าประทับใจมาก")]),
            ("นัดหมายเช้าวันจันทร์", [("Lead", "Standup meeting is at 8:00 AM sharp on Monday.", "การประชุมสแตนด์อัปวันจันทร์เวลาแปดโมงเช้าตรงนะ"), ("Team", "We will be there on time.", "พวกเราจะไปตรงเวลาแน่นอนครับ")]),
            ("ตรวจเช็คเครื่องจักรก่อนหยุดเสาร์อาทิตย์", [("Tech", "All machines are shut down and safely locked.", "เครื่องจักรทุกตัวปิดสวิตช์และล็อกเรียบร้อยครับ"), ("Lead", "Perfect. Turn off the main warehouse lights.", "ยอดเยี่ยม ปิดไฟหลักในโกดังได้เลย")]),
            ("ชื่นชมการแก้ปัญหาเฉพาะหน้า", [("Customer", "Thank you for handling our urgent order yesterday.", "ขอบคุณที่ช่วยจัดการออเดอร์ด่วนให้เราเมื่อวานนะ"), ("Staff", "Our pleasure. We are always ready to support.", "ด้วยความยินดีครับ เราพร้อมช่วยเหลือเสมอ")]),
            ("จบสัปดาห์แรกของหลักสูตร", [("Learner", "I learned so many useful workplace phrases this week!", "สัปดาห์นี้ผมได้เรียนวลีที่ใช้ทำงานจริงเยอะมากเลย!"), ("Coach", "Keep practicing daily. Week 2 will be even better!", "ฝึกฝนทุกวันอย่างต่อเนื่องนะ สัปดาห์ที่สองจะยิ่งเข้มข้นขึ้น!")])
        ]),
        "exercises": make_exercises([
            ("เป้าหมายสำคัญอันดับหนึ่งของเราในสัปดาห์หน้าคือการปรับปรุงระบบ", "Our top", "for next week is system optimization.", "คำแปลว่า ลำดับความสำคัญ (p...)", "priority", [], "Our top priority is system optimization.", "'top priority' คือสิ่งที่ต้องทำเป็นอันดับแรก"),
            ("พวกเราทำอัตราการส่งมอบสินค้าตรงเวลาได้ถึง 98% ในสัปดาห์นี้", "We", "a 98% on-time delivery rate this week.", "คำกริยาอดีตแปลว่า ทำสำเร็จ (a...)", "achieved", [], "We achieved a 98% on-time delivery rate this week.", "'achieved' แปลว่า ทำสำเร็จหรือบรรลุเป้าหมาย"),
            ("ยอดของเสียรวมลดลงเมื่อเปรียบเทียบกับสัปดาห์ที่แล้ว", "Total scrap was reduced", "to last week.", "คำแปลว่า เปรียบเทียบ (c... ตามด้วย to)", "compared", [], "Total scrap was reduced compared to last week.", "'compared to' แปลว่า เมื่อเปรียบเทียบกับ"),
            ("นี่คือสรุปผลการดำเนินงานประจำสัปดาห์ของเราครับ", "Here is the", "of our weekly achievements.", "คำนามแปลว่า บทสรุป (s...)", "summary", [], "Here is the summary of our weekly achievements.", "'summary' แปลว่า บทสรุปย่อ"),
            ("พวกเราสามารถเอาชนะอุปสรรคที่ไม่คาดคิดได้ทั้งหมด", "We managed to", "all unexpected delays.", "คำกริยาแปลว่า เอาชนะ (o...)", "overcome", [], "We managed to overcome all unexpected delays.", "'overcome' แปลว่า เอาชนะอุปสรรค"),
            ("ยอดการผลิตทำได้สูงกว่าเป้าหมายที่คาดการณ์ไว้", "Output", "the original forecast.", "คำกริยาอดีตแปลว่า เกินกว่า (e...)", "exceeded", [], "Output exceeded the original forecast.", "'exceeded' แปลว่า ทำได้เกินกว่าเป้าหมาย"),
            ("มารักษาแรงผลักดันเชิงบวกนี้ต่อไปจนถึงวันจันทร์กันครับ", "Let's maintain this", "into Monday.", "คำนามแปลว่า แรงขับเคลื่อนต่อเนื่อง (m...)", "momentum", [], "Let's maintain this momentum into Monday.", "'momentum' แปลว่า แรงส่งหรือความต่อเนื่อง"),
            ("ขอให้ทุกคนได้พักผ่อนอย่างเต็มที่ในวันหยุดสุดสัปดาห์ครับ", "Have a", "weekend, everyone!", "คำคุณศัพท์แปลว่า ที่ได้พักผ่อนเต็มที่ (r...)", "restful", [], "Have a restful weekend, everyone!", "'restful weekend' แปลว่า วันหยุดที่ได้พักผ่อนอย่างสบายใจ"),
            ("ไม่มีอุบัติเหตุด้านความปลอดภัยเกิดขึ้นเลยในสัปดาห์นี้", "No safety", "occurred this week.", "คำนามพหูพจน์แปลว่า อุบัติเหตุ/เหตุการณ์ (i...)", "incidents", [], "No safety incidents occurred this week.", "'safety incidents' แปลว่า เหตุการณ์ด้านความปลอดภัย"),
            ("ขอแสดงความยินดีที่คุณเรียนจบสัปดาห์ที่ 1 แล้ว", "", "on completing Week 1!", "คำอวยพรแสดงความยินดี (C...)", "Congratulations", [], "Congratulations on completing Week 1!", "'Congratulations on...' แปลว่า ขอแสดงความยินดีด้วยกับ...")
        ]),
        "stories": make_stories([
            ("Hitting the 98% Benchmark", "https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=900&auto=format&fit=crop&q=80",
             [("benchmark", "n.", "เกณฑ์มาตรฐาน"), ("on-time", "adj.", "ตรงเวลา"), ("achieve", "v.", "ทำสำเร็จ"), ("cheer", "v.", "ไชโยดีใจ")],
             "Friday afternoon was tense in the dispatch office. The team needed one final delivery confirmation to hit their 98% <b>on-time</b> <b>benchmark</b>.<br><br>At 4:45 PM, the radio crackled: “Truck 12 delivered safely to Pathum Thani!” The entire office <b>cheered</b> in triumphant celebration.",
             "Friday afternoon was tense in the dispatch office. The team needed one final delivery confirmation to hit their 98% on-time benchmark. At 4:45 PM, the radio crackled: Truck 12 delivered safely to Pathum Thani! The entire office cheered in triumphant celebration.",
             "บ่ายวันศุกร์ในออฟฟิศปล่อยรถเต็มไปด้วยความลุ้นระทึก ทีมงานต้องการการยืนยันส่งของอีกคันเดียวเพื่อพิชิตเกณฑ์ส่งตรงเวลา 98% ตอน 16.45 น. วิทยุแจ้งเข้ามา: รถคันที่ 12 ส่งของถึงปทุมธานีเรียบร้อย! ทั้งห้องส่งเสียงเฮฉลองความสำเร็จร่วมกันอย่างกึกก้อง"),
            ("A Well-Deserved Rest", "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=900&auto=format&fit=crop&q=80",
             [("exhausted", "adj.", "เหนื่อยล้า"), ("dedication", "n.", "ความทุ่มเท"), ("pride", "n.", "ความภาคภูมิใจ"), ("restful", "adj.", "ได้พักผ่อน")],
             "Krit clocked out on Friday evening feeling pleasantly tired yet beaming with <b>pride</b>. His team had reorganized sixty locations in Room A1 with zero errors.<br><br>He looked back at the spotless warehouse aisles, smiled, and headed home ready for a truly <b>restful</b> weekend.",
             "Krit clocked out on Friday evening feeling pleasantly tired yet beaming with pride. His team had reorganized sixty locations in Room A1 with zero errors. He looked back at the spotless warehouse aisles, smiled, and headed home ready for a truly restful weekend.",
             "กฤชสแกนนิ้วเลิกงานเย็นวันศุกร์ด้วยความเหนื่อยล้าแต่เปี่ยมด้วยความภาคภูมิใจ ทีมของเขาจัดระเบียบ 60 ช่องเก็บของในห้อง A1 ได้สำเร็จแบบไร้ข้อผิดพลาด เขามองกลับไปที่ช่องทางเดินคลังสินค้าที่สะอาดตา ยิ้มกว้าง และเดินทางกลับบ้านเพื่อพักผ่อนอย่างเต็มที่"),
            ("The Executive Presentation", "https://images.unsplash.com/photo-1497215728101-856f4ea42174?w=900&auto=format&fit=crop&q=80",
             [("executive", "n.", "ผู้บริหาร"), ("summary", "n.", "บทสรุป"), ("metrics", "n.", "ตัวชี้วัด"), ("praise", "v.", "ชื่นชม")],
             "Presenting to the Managing Director can be nerve-racking, but Natt summarized the warehouse operations into three crystal-clear <b>metrics</b>.<br><br>The director nodded approvingly and warmly <b>praised</b> the team for their data transparency and operational clarity.",
             "Presenting to the Managing Director can be nerve-racking, but Natt summarized the warehouse operations into three crystal-clear metrics. The director nodded approvingly and warmly praised the team for their data transparency and operational clarity.",
             "การรายงานต่อหน้ากรรมการผู้จัดการอาจทำให้ตื่นเต้น แต่นัทสรุปผลงานคลังสินค้าเป็น 3 ตัวชี้วัดที่ชัดเจนกระจ่างแจ้ง กรรมการผู้จัดการพยักหน้าเห็นชอบและเอ่ยปากชมเชยความโปร่งใสในข้อมูลและความชัดเจนในการทำงานของทีม"),
            ("Week 1 Milestone Reached", "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=900&auto=format&fit=crop&q=80",
             [("milestone", "n.", "ก้าวสำคัญ"), ("consistency", "n.", "ความสม่ำเสมอ"), ("confidence", "n.", "ความมั่นใจ"), ("fluent", "adj.", "คล่องแคล่ว")],
             "Looking back on his study notes on Sunday, Dan realized he had practiced over one hundred new English sentences in just seven days.<br><br>He no longer felt shy to speak during factory walkthroughs. Daily <b>consistency</b> had turned into genuine speaking <b>confidence</b>.",
             "Looking back on his study notes on Sunday, Dan realized he had practiced over one hundred new English sentences in just seven days. He no longer felt shy to speak during factory walkthroughs. Daily consistency had turned into genuine speaking confidence.",
             "เมื่อเปิดดูสมุดโน้ตในวันอาทิตย์ แดนพบว่าตัวเองได้ฝึกประโยคภาษาอังกฤษใหม่ๆ ไปมากกว่า 100 ประโยคในเวลาเพียง 7 วัน เขาไม่รู้สึกเคอะเขินอีกต่อไปเวลาต้องพูดภาษาอังกฤษในโรงงาน ความสม่ำเสมอในทุกๆ วันได้เปลี่ยนเป็นความมั่นใจในการพูดอย่างแท้จริง")
        ])
    }
}

# -----------------------------------------------------------------------------
# 4. Persistence Layer
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
# 5. Audio Booster Engine (Web Audio API 2.5x)
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
# 6. AI Writing Coach (Gemini 3.6 Flash)
# -----------------------------------------------------------------------------
def analyze_with_ai(text_to_check: str, api_key: str) -> str:
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        prompt = f"""
        คุณคือผู้เชี่ยวชาญการสอนภาษาอังกฤษเพื่อการสื่อสารในโรงงานและออฟฟิศระดับสากล กรุณาตรวจประโยคด้านล่างนี้:
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
# 7. Sidebar Navigation
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
# 8. Main Learning Dashboard
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

    # TAB 5: Short Stories (4 Unique Stories per Day with Realistic Imagery)
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

    # TAB 6: AI Coach
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
