from flask import Flask, request, render_template_string
import os, random, string, requests, uuid
from datetime import datetime, timedelta
import calendar

app = Flask(__name__)

ZENOPAY_API_KEY = os.getenv("ZENOPAY_API_KEY")
ZENOPAY_ACCOUNT_ID = os.getenv("ZENOPAY_ACCOUNT_ID", "zp31356735")

# ===== VOCHA ZA KALENDA TU - HAKUNA MASAA =====
def tarehe_mwisho(kifurushi):
    leo = datetime.now()
    if kifurushi == "LEO":
        return leo.replace(hour=23, minute=59, second=59)
    if kifurushi == "SIKU 1":
        kesho = leo + timedelta(days=1)
        return kesho.replace(hour=23, minute=59, second=59)
    if kifurushi == "WIKI HII":
        siku_zilizobaki = 6 - leo.weekday() # Jumapili=6
        jumapili = leo + timedelta(days=siku_zilizobaki)
        return jumapili.replace(hour=23, minute=59, second=59)
    if kifurushi == "MWEZI HUU":
        siku_za_mwezi = calendar.monthrange(leo.year, leo.month)[1]
        return leo.replace(day=siku_za_mwezi, hour=23, minute=59, second=59)
    return leo

VOCHA = {
    "JEYVAN123": {"kifurushi": "LEO", "mwisho": None},
    "JEYVAN456": {"kifurushi": "SIKU 1", "mwisho": None},
    "JEYVAN789": {"kifurushi": "WIKI HII", "mwisho": None},
}
BEI = {"500": "LEO", "1000": "SIKU 1", "5000": "WIKI HII", "15000": "MWEZI HUU"}
MALIPO_YANAYOSUBIRI = {}

def tengeneza_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def angalia_vocha(code):
    if code not in VOCHA:
        return False, f"❌ Code {code} sio sahihi. Piga 0689211924"
    info = VOCHA[code]
    kifurushi = info["kifurushi"]
    mwisho = info.get("mwisho")
    if mwisho is None:
        mwisho = tarehe_mwisho(kifurushi)
    if datetime.now() > mwisho:
        return False, f"❌ Code {code} IMESHAISHA! Ilikuwa ya {kifurushi}, iliisha {mwisho.strftime('%d/%m/%Y saa 11:59')}. Nunua nyingine."
    return True, f"✅ Karibu! Code {code} ni sahihi - {kifurushi}. Inaisha: {mwisho.strftime('%d/%m/%Y saa 11:59 usiku')}"

HTML = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>JEYVAN PREMIUM WIFI</title>
<style>
body{background:#000;color:#fff;font-family:Arial;text-align:center;margin:0;padding:15px}
h1{color:#FFD700;font-size:32px;margin:5px;line-height:1.1}
.call{background:#FFD700;color:#000;display:inline-block;padding:10px 22px;border-radius:30px;font-weight:bold;margin:10px}
h3{color:#2E86FF;margin:15px 0}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.card{border-radius:15px;padding:15px;text-align:left}
.c1{border:2px solid #FFD700;background:#111}.c2{border:2px solid #2E86FF;background:#0a1a3a}
.c3{border:2px solid #00FFAA;background:#021a12}.c4{border:2px solid #FF8C00;background:#1a1000;position:relative}
.price{font-size:26px;font-weight:bold}
.c1 .price{color:#FFD700}.c2 .price{color:#2E86FF}.c3 .price{color:#00FFAA}.c4 .price{color:#FF8C00}
.small{font-size:13px;color:#ccc}.best{background:#FF8C00;color:#000;font-size:10px;font-weight:bold;position:absolute;top:-10px;right:10px;padding:3px 8px;border-radius:10px}
.warn{background:#FFF59D;color:#333;border-radius:12px;padding:12px;text-align:left;margin:18px 0;font-size:13px}
.pay{background:#00AA55;color:#fff;border-radius:12px;padding:15px;font-weight:bold;margin:10px 0}.pay b{font-size:26px}
.box{background:#111;border:2px solid #FFD700;border-radius:15px;padding:15px;margin:15px 0}
.box2{background:#0a1a3a;border:2px solid #2E86FF;border-radius:15px;padding:15px;margin:15px 0}
input,select{width:90%;padding:14px;border-radius:12px;border:2px solid #FFD700;background:#111;color:#fff;text-align:center;font-size:16px;margin:8px 0}
button{width:95%;padding:14px;border:none;border-radius:12px;background:linear-gradient(#FFD700,#FF8C00);font-weight:bold;font-size:16px;margin:5px 0}
.btn-blue{background:linear-gradient(#2E86FF,#00CFFF);color:#fff}
.success{background:#00AA55;padding:15px;border-radius:12px;font-weight:bold;margin:10px 0;font-size:18px}
.pending{background:#FF8C00;color:#000;padding:15px;border-radius:12px;font-weight:bold;margin:10px 0}
</style></head><body>
<h1>JEYVAN<br>PREMIUM WIFI</h1><div class="call">📞 PIGA: 0689211924</div>
<h3>CHAGUA KIFURUSHI - YA KALENDA TU</h3>
<div class="grid">
<div class="card c1"><div class="price">500 TSH</div><b>LEO</b><div class="small">• Data bila kikomo<br>• 10Mbps<br>• Inaisha leo usiku</div></div>
<div class="card c2"><div class="price">1000 TSH</div><b>SIKU 1</b><div class="small">• Data bila kikomo<br>• 20Mbps<br>• Inaisha kesho usiku</div></div>
<div class="card c3"><div class="price">5000 TSH</div><b>WIKI HII</b><div class="small">• Data bila kikomo<br>• 30Mbps<br>• Inaisha Jumapili</div></div>
<div class="card c4"><span class="best">BEST SELLER</span><div class="price">15000 TSH</div><b>MWEZI HUU</b><div class="small">• Data bila kikomo<br>• 50Mbps<br>• Inaisha mwisho wa mwezi</div></div>
</div>
<div class="warn">⚠️ <b>VOCHA NI YA KALENDA TU!</b><br>
- <b>LEO</b> = Inaisha LEO usiku saa 11:59<br>
- <b>SIKU 1</b> = Inaisha KESHO usiku<br>
- <b>WIKI HII</b> = Inaisha JUMAPILI usiku<br>
- <b>MWEZI HUU</b> = Inaisha MWISHO WA MWEZI<br>
Ametumia au hajatumia, inakata muda huo huo!</div>
<div class="box"><h3 style="color:#FFD700">1. INGIA KWA CODE YA VOCHA</h3>
<form method="POST" action="/ingia-vocha"><input name="code" placeholder="Weka CODE ya vocha hapa" required><br><button>INGIA KWA VOCHA →</button></form></div>
<div class="box2"><h3 style="color:#2E86FF">2. LIPA SASA - PATA CODE MOJA KWA MOJA</h3>
<form method="POST" action="/lipa"><select name="bei" required><option value="500">500 TSH - LEO (Inaisha leo usiku)</option><option value="1000">1000 TSH - SIKU 1 (Inaisha kesho usiku)</option><option value="5000">5000 TSH - WIKI HII (Inaisha Jumapili)</option><option value="15000">15000 TSH - MWEZI HUU (Inaisha mwisho wa mwezi)</option></select><input name="simu" placeholder="Weka namba 07XX XXX XXX" required><br><button class="btn-blue">LIPA SASA NA ZENOPAY →</button></form></div>
<div class="pay">AIRTEL LIPA NAMBA<br><b>13984763</b><br>Jina: JEYVAN STUDIO</div>
{% if msg %}<div class="success">{{msg}}</div>{% endif %}
{% if pending %}<div class="pending">⏳ {{pending}}<br><br><form method="POST" action="/angalia"><input type="hidden" name="order_id" value="{{order_id}}"><button class="btn-blue">NIMEMALIZA KULIPIA - ANGALIA CODE YANGU →</button></form></div>{% endif %}
{% if code_mpya %}<div class="success">🎉 CODE YAKO MPYA:<br><span style="font-size:30px;letter-spacing:3px">{{code_mpya}}</span><br>{{mwisho_txt}}<br>Andika hii kwenye sehemu ya juu kuingia!</div>{% endif %}
</body></html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML, msg="", pending="", order_id="", code_mpya="", mwisho_txt="")

@app.route("/ingia-vocha", methods=["POST"])
def ingia_vocha():
    code = request.form.get("code","").strip().upper()
    ok, msg = angalia_vocha(code)
    return render_template_string(HTML, msg=msg, pending="", order_id="", code_mpya="", mwisho_txt="")

@app.route("/lipa", methods=["POST"])
def lipa():
    bei = request.form.get("bei")
    simu = request.form.get("simu","").strip().replace(" ","")
    if simu.startswith("0"):
        simu = "255" + simu[1:]
    kifurushi = BEI.get(bei, "LEO")
    order_id = str(uuid.uuid4())
    code_mpya = tengeneza_code()
    mwisho = tarehe_mwisho(kifurushi)
    MALIPO_YANAYOSUBIRI[order_id] = {"code": code_mpya, "bei": bei, "simu": simu, "kifurushi": kifurushi, "mwisho": mwisho}
    try:
        headers = {"x-api-key": ZENOPAY_API_KEY, "Content-Type": "application/json"}
        payload = {"order_id": order_id, "buyer_email": "jeyvanstudio@gmail.com", "buyer_name": "JEYVAN WIFI Customer", "buyer_phone": simu, "amount": int(bei), "account_id": ZENOPAY_ACCOUNT_ID, "webhook_url": "https://jeyvan-studio-wifi-39h.onrender.com/webhook"}
        r = requests.post("https://zenopay.net/api/v1/orders", json=payload, headers=headers, timeout=20)
        print("ZenoPay:", r.status_code, r.text)
        if r.status_code not in [200, 201]:
            return render_template_string(HTML, msg="⚠️ ZenoPay imeshindwa. Lipa Lipa Namba 13984763", pending="", order_id="", code_mpya="", mwisho_txt="")
    except Exception as e:
        print(e)
        return render_template_string(HTML, msg="⚠️ Imeshindwa kuungana na ZenoPay. Jaribu tena.", pending="", order_id="", code_mpya="", mwisho_txt="")
    pending = f"Angalia simu yako {simu} - umetumiwa USSD ya kulipia {bei} TSH ({kifurushi} - Inaisha {mwisho.strftime('%d/%m/%Y')}). Weka PIN yako."
    return render_template_string(HTML, msg="", pending=pending, order_id=order_id, code_mpya="", mwisho_txt="")

@app.route("/angalia", methods=["POST"])
def angalia():
    order_id = request.form.get("order_id")
    info = MALIPO_YANAYOSUBIRI.get(order_id)
    if not info:
        return render_template_string(HTML, msg="Order haikupatikana. Jaribu tena.", pending="", order_id="", code_mpya="", mwisho_txt="")
    try:
        headers = {"x-api-key": ZENOPAY_API_KEY}
        r = requests.get(f"https://zenopay.net/api/v1/orders/{order_id}", headers=headers, timeout=15)
        status = str(r.json()).lower()
        if "completed" in status or "paid" in status or "success" in status:
            code_mpya = info["code"]
            VOCHA[code_mpya] = {"kifurushi": info["kifurushi"], "mwisho": info["mwisho"]}
            mwisho_txt = f"Vocha yako ni ya {info['kifurushi']} - Inaisha: {info['mwisho'].strftime('%d/%m/%Y saa 11:59 usiku')} - Ametumia au hajatumia inakata!"
            return render_template_string(HTML, msg="✅ Malipo yamethibitishwa!", pending="", order_id="", code_mpya=code_mpya, mwisho_txt=mwisho_txt)
        else:
            pending = "Bado hujalipia. Maliza kulipia kwenye simu yako, halafu bonyeza tena hapa."
            return render_template_string(HTML, msg="", pending=pending, order_id=order_id, code_mpya="", mwisho_txt="")
    except Exception as e:
        print(e)
        return render_template_string(HTML, msg="Imeshindwa kuangalia status. Jaribu tena.", pending="", order_id="", code_mpya="", mwisho_txt="")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json or {}
    order_id = data.get("order_id") or data.get("data", {}).get("order_id")
    if order_id in MALIPO_YANAYOSUBIRI:
        info = MALIPO_YANAYOSUBIRI[order_id]
        VOCHA[info["code"]] = {"kifurushi": info["kifurushi"], "mwisho": info["mwisho"]}
    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
