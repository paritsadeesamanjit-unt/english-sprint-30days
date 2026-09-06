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
# 2. Helper Data Builder for Week 1 (Day 1 - Day 7)
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
# 3. Complete Week 1 Curriculum Dataset
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
             [("available", "adj.", "ว่าง"), ("clarify", "pos", "ชี้แจง"), ("project", "n.", "โครงการ"), ("solution", "n.", "ทางออก")],
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
    }
}

# -----------------------------------------------------------------------------
# 4. Generate Days 3 to 7 Programmatically (Fully Rich Dataset)
# -----------------------------------------------------------------------------
DAY_CONFIGS = [
    (3, "Day 3: Reporting Problems & Delays", "การแจ้งปัญหา ความล่าช้า และเสนอทางออก", "แจ้งปัญหา (Issue) -> อธิบายสาเหตุ (Due to) -> เสนอทางแก้ไข (Action)",
     [("Delay", "/dɪˈleɪ/", "n./v.", "ความล่าช้า", "There is a slight delay.", "มีความล่าช้าเล็กน้อย"),
      ("Bottleneck", "/ˈbɒt.əl.nek/", "n.", "จุดคอขวด", "We found a bottleneck at packing.", "พบจุดคอขวดที่การแพ็ค"),
      ("Resolve", "/rɪˈzɒlv/", "v.", "แก้ไขลุล่วง", "We resolved the issue.", "พวกเราแก้ปัญหาแล้ว"),
      ("Malfunction", "/ˌmælˈfʌŋk.ʃən/", "n.", "เครื่องขัดข้อง", "The motor malfunctioned.", "มอเตอร์ขัดข้อง"),
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
      ("Contingency", "/kənˈtɪn.dʒən.si/", "n.", "แผนฉุกเฉิน", "Follow the contingency plan.", "ทำตามแผนฉุกเฉิน")]),
    (4, "Day 4: Daily Standup & Work Progress", "การรายงานสิ่งที่ทำเสร็จ สิ่งที่กำลังทำ และอุปสรรค", "What I did yesterday -> What I will do today -> Blockers",
     [("Backlog", "/ˈbæk.lɒɡ/", "n.", "งานคั่งค้าง", "We cleared the backlog.", "พวกเราเคลียร์งานค้างเสร็จแล้ว"),
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
      ("Wrap up", "/ræp ʌp/", "v.", "สรุปจบงาน", "Wrap up the standup meeting.", "สรุปจบการประชุมสแตนด์อัป")]),
    (5, "Day 5: Scheduling & Rescheduling Meetings", "การนัดหมาย เสนอเวลาว่าง เลื่อนนัด และยืนยันกำหนดการ", "ระบุเวลาชัดเจน + เสนอทางเลือก (Does [time] work for you?)",
     [("Available", "/əˈveɪ.lə.bəl/", "adj.", "ว่าง / สะดวก", "Are you available tomorrow?", "พรุ่งนี้คุณว่างไหมครับ"),
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
      ("Accommodate", "/əˈkɒm.ə.deɪt/", "v.", "ปรับเวลาให้ลงตัว", "Thanks for accommodating me.", "ขอบคุณที่ปรับเวลาให้")]),
    (6, "Day 6: Clarifying Instructions & Active Listening", "การทวนความเข้าใจ เช็คคำสั่ง เพื่อป้องกันความผิดพลาด", "Let me confirm... | Just to clarify... | Did you mean...?",
     [("Elaborate", "/iˈlæb.ə.reɪt/", "v.", "อธิบายขยายความ", "Could you elaborate further?", "ช่วยอธิบายเพิ่มเติมได้ไหม"),
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
      ("Acknowledge", "/əkˈnɒl.ɪdʒ/", "v.", "ตอบรับทราบ", "Please acknowledge this mail.", "โปรดตอบรับทราบอีเมลนี้")]),
    (7, "Day 7: Weekly Wrap-up & Executive Summary", "การเขียนสรุปผลงานประจำสัปดาห์ (Highlights, KPIs, Plans)", "เน้นสรุปแบบ Bullet points กระชับ พร้อมตัวเลขชี้วัดผลงาน",
     [("Achievement", "/əˈtʃiːv.mənt/", "n.", "ความสำเร็จผลงาน", "This is a great achievement.", "นี่คือความสำเร็จที่ยอดเยี่ยม"),
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
      ("Milestone", "/ˈmaɪl.stəʊn/", "n.", "ก้าวสำคัญ", "We hit the week 1 milestone.", "เราผ่านก้าวสัปดาห์ที่ 1 แล้ว")])
]

# ประมวลผลสร้าง Day 3 ถึง Day 7 ลงใน WEEK_1_DATA
for d_num, d_title, d_sum, d_rule, d_voc in DAY_CONFIGS:
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
            (f"Efficiency at Work (Day {d_num})", "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=900&auto=format&fit=crop&q=80",
             [(d_voc[0][0], "n.", d_voc[0][3]), (d_voc[1][0], "adj.", d_voc[1][3]), (d_voc[2][0], "v.", d_voc[2][3]), ("team", "n.", "ทีมงาน")],
             f"The warehouse shift begins with checking the <b>{d_voc[0][0].lower()}</b>. An urgent request requires immediate action.<br><br>Through clear communication, the <b>team</b> manages to <b>{d_voc[2][0].lower()}</b> the task smoothly before noon.",
             f"The warehouse shift begins with checking the {d_voc[0][0].lower()}. An urgent request requires immediate action. Through clear communication, the team manages to {d_voc[2][0].lower()} the task smoothly before noon.",
             f"กะการทำงานในคลังเริ่มต้นด้วยการตรวจเช็ค {d_voc[0][3]} งานด่วนต้องการการจัดการทันที ด้วยการสื่อสารที่ชัดเจน ทีมงานสามารถดำเนินการ {d_voc[2][3]} ได้อย่างราบรื่นก่อนเที่ยง"),
            (f"Active Communication (Day {d_num})", "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=900&auto=format&fit=crop&q=80",
             [(d_voc[3][0], "n.", d_voc[3][3]), ("clarify", "v.", "ชี้แจง"), ("listen", "v.", "รับฟัง"), ("success", "n.", "ความสำเร็จ")],
             "Whenever instructions seem unclear, Tan politely asks to <b>clarify</b> the requirements. He takes detailed notes and <b>listens</b> carefully.<br><br>That simple habit turns confusion into complete operational <b>success</b>.",
             "Whenever instructions seem unclear, Tan politely asks to clarify the requirements. He takes detailed notes and listens carefully. That simple habit turns confusion into complete operational success.",
             "เมื่อใดก็ตามที่คำสั่งดูไม่ชัดเจน ธันจะถามอย่างสุภาพเพื่อขอคำชี้แจง เขาจดบันทึกและตั้งใจฟัง นิสัยง่ายๆ นี้เปลี่ยนความสับสนเป็นความสำเร็จในการทำงานอย่างสมบูรณ์"),
            (f"Solving the Puzzle (Day {d_num})", "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=900&auto=format&fit=crop&q=80",
             [(d_voc[4][0], "n.", d_voc[4][3]), ("solve", "v.", "แก้ไข"), ("calm", "adj.", "ใจเย็น"), ("relief", "n.", "ความโล่งอก")],
             "A sudden error code caused tension on the packing line. Instead of panicking, the crew stayed <b>calm</b>, inspected the sensors, and <b>solved</b> the issue within minutes with immense <b>relief</b>.",
             "A sudden error code caused tension on the packing line. Instead of panicking, the crew stayed calm, inspected the sensors, and solved the issue within minutes with immense relief.",
             "รหัสข้อผิดพลาดกะทันหันสร้างความตึงเครียดในสายบรรจุหีบห่อ แทนที่จะตื่นตระหนก ทีมงานตั้งสติ ตรวจสอบเซนเซอร์ และแก้ไขปัญหาได้สำเร็จภายในไม่กี่นาทีด้วยความโล่งอก"),
            (f"Friday Milestone (Day {d_num})", "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=900&auto=format&fit=crop&q=80",
             [("milestone", "n.", "ก้าวสำคัญ"), ("dedication", "n.", "ความทุ่มเท"), ("proud", "adj.", "ภาคภูมิใจ"), ("rest", "n.", "การพักผ่อน")],
             "At the end of the shift, the team celebrated hitting their weekly <b>milestone</b>. Their tireless <b>dedication</b> kept every customer satisfied. Everyone headed home <b>proud</b> and ready for a well-deserved <b>rest</b>.",
             "At the end of the shift, the team celebrated hitting their weekly milestone. Their tireless dedication kept every customer satisfied. Everyone headed home proud and ready for a well-deserved rest.",
             "เมื่อสิ้นสุดกะการทำงาน ทีมงานร่วมยินดีที่บรรลุเป้าหมายสำคัญประจำสัปดาห์ ความทุ่มเทอย่างไม่เหน็ดเหนื่อยช่วยให้ลูกค้าทุกคนพึงพอใจ ทุกคนเดินทางกลับบ้านด้วยความภาคภูมิใจและพร้อมสำหรับการพักผ่อนอย่างเต็มที่")
        ])
    }

# -----------------------------------------------------------------------------
# 5. Persistence Layer
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
# 6. Audio Booster Engine (Web Audio API 2.5x)
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
# 7. AI Writing Coach (Gemini 3.6 Flash)
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
# 8. Sidebar Navigation
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
# 9. Main Learning Dashboard
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
