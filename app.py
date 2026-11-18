from flask import Flask, request, render_template_string
import os, random, string, requests, uuid
from datetime import datetime, timedelta

app = Flask(__name__)

ZENOPAY_API_KEY = os.getenv("ZENOPAY_API_KEY")
ZENOPAY_ACCOUNT_ID = os.getenv("ZENOPAY_ACCOUNT_ID", "zp31356735")

# ===== KILA MTEJA ANA MUDA WAKE - KUANZIA ALIPONUNUA =====
def tarehe_mwisho(kifurushi):
    leo = datetime.now()
    if kifurushi == "MASAA7":
        return leo + timedelta(hours=7)
    if kifurushi == "SIKU 1":
        return leo + timedelta(hours=24)
    if kifurushi == "WIKI HII":
        return leo + timedelta(days=7)
    if kifurushi == "MWEZI HUU":
        return leo + timedelta(days=30)
    return leo

VOCHA = {
    "JEYVAN123": {"kifurushi": "MASAA7", "mwisho": None},
    "JEYVAN456": {"kifurushi": "SIKU 1", "mwisho": None},
    "JEYVAN789": {"kifurushi": "WIKI HII", "mwisho": None},
}

BEI = {"500": "MASAA7", "1000": "SIKU 1", "5000": "WIKI HII", "15000": "MWEZI HUU"}
MALIPO_YANAYOSUBIRI = {}

def tengeneza_code():
    return "JEYVAN" + "".join(random.choices(string.digits, k=3))

def jina_nje(kifurushi):
    return {"MASAA7": "SAA 7", "SIKU 1": "SIKU 1", "WIKI HII": "WIKI", "MWEZI HUU": "MWEZI"}.get(kifurushi, kifurushi)

def angalia_vocha(code):
    info = VOCHA.get(code)
    if not info:
        return False, f"❌ Code {code} SI sahihi. Jaribu tena."
    kifurushi = info["kifurushi"]
    mwisho = info["mwisho"]
    if mwisho is None:
        mwisho = tarehe_mwisho(kifurushi)
        info["mwisho"] = mwisho
    if datetime.now() > mwisho:
        return False, f"❌ Code {code} IMESHAISHA! Nunua nyingine."
    return True, f"✅ Karibu! Code {code} ni sahihi - {jina_nje(kifurushi)} - Data bila kikomo. Inaisha: {mwisho.strftime('%d/%m/%Y saa %H:%M')}"

HTML = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>JEYVAN PREMIUM WIFI</title>
<style>
body{font-family:Arial;text-align:center;background:#000;color:#fff;padding:15px}
h1{color:#FFD700;font-size:32px;margin:5px}
.call{background:#FFD700;color:#000;padding:10px;border-radius:10px;font-weight:bold}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:15px 0}
.card{padding:15px;border-radius:12px;color:#fff}
.c1{background:#2E86FF}.c2{background:#27AE60}.c3{background:#8E44AD}.c4{background:#E67E22}
.price{font-size:22px;font-weight:bold}.small{font-size:13px;margin-top:5px}
.best{background:#FFD700;color:#000;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:bold}
.warn{background:#333;padding:12px;border-radius:10px;text-align:left;font-size:14px;margin:10px 0}
.box{background:#222;padding:15px;border-radius:12px;margin:10px 0}
.box2{background:#111;padding:15px;border-radius:12px;margin:10px 0;border:2px solid #2E86FF}
input,select{width:90%;padding:12px;margin:8px 0;border-radius:8px;border:none;font-size:16px}
button{background:#FFD700;color:#000;padding:13px 20px;border:none;border-radius:8px;font-weight:bold;font-size:16px;width:95%}
.btn-blue{background:#2E86FF;color:#fff}
.pay{background:#FFD700;color:#000;padding:12px;border-radius:10px;font-weight:bold;margin:10px 0}
.success{background:#27AE60;padding:15px;border-radius:10px;font-weight:bold;margin:10px 0}
.pending{background:#FF8C00;color:#000;padding:15px;border-radius:12px;font-weight:bold;margin:10px 0}
</style></head><body>
<h1>JEYVAN<br>PREMIUM WIFI</h1><div class="call">📞 PIGA: 0689211924</div>
<h3>CHAGUA KIFURUSHI - DATA BILA KIKOMO</h3>
<div class="grid">
<div class="card c1"><div class="price">500 TSH</div><b>SAA 7</b><div class="small">• Data bila kikomo<br>• 10Mbps<br>• Haraka sana</div></div>
<div class="card c2"><div class="price">1000 TSH</div><b>SIKU 1</b><div class="small">• Data bila kikomo<br>• 20Mbps<br>• Siku nzima</div></div>
<div class="card c3"><div class="price">5000 TSH</div><b>WIKI</b><div class="small">• Data bila kikomo<br>• 30Mbps<br>• Wiki nzima</div></div>
<div class="card c4"><span class="best">BEST SELLER</span><div class="price">15000 TSH</div><b>MWEZI</b><div class="small">• Data bila kikomo<br>• 50Mbps<br>• Mwezi mzima</div></div>
</div>
<div class="warn">🔥 <b>DATA BILA KIKOMO!</b><br>
- <b>SAA 7</b> = 500 TSH - Saa 7 kuanzia uliponunua<br>
- <b>SIKU 1</b> = 1000 TSH - Saa 24 kuanzia uliponunua<br>
- <b>WIKI</b> = 5000 TSH - Siku 7 kuanzia uliponunua<br>
- <b>MWEZI</b> = 15000 TSH - Siku 30 kuanzia uliponunua</div>
<div class="box"><h3 style="color:#FFD700">1. INGIA KWA CODE YA VOCHA</h3>
<form method="POST" action="/ingia-vocha"><input name="code" placeholder="Weka CODE ya vocha hapa" required><br><button>INGIA KWA VOCHA →</button></form></div>
<div class="box2"><h3 style="color:#2E86FF">2. LIPA SASA - PATA CODE MOJA KWA MOJA</h3>
<form method="POST" action="/lipa"><select name="bei" required><option value="500">500 TSH - SAA 7 - Data bila kikomo</option><option value="1000">1000 TSH - SIKU 1 - Data bila kikomo</option><option value="5000">5000 TSH - WIKI - Data bila kikomo</option><option value="15000">15000 TSH - MWEZI - Data bila kikomo</option></select><input name="simu" placeholder="Weka namba 07XX XXX XXX" required><br><button class="btn-blue">LIPA SASA NA ZENOPAY →</button></form></div>
<div class="pay">AIRTEL LIPA NAMBA<br><b>13984763</b><br>Jina: JEYVAN STUDIO</div>
{% if msg %}<div class="success">{{msg}}</div>{% endif %}
{% if code_mpya %}<div class="success">🎉 CODE YAKO: <h2>{{code_mpya}}</h2>{{mwisho_txt}}</div>{% endif %}
{% if pending %}<div class="pending">⏳ {{pending}}<br><br><form method="POST" action="/angalia"><input type="hidden" name="order_id" value="{{order_id}}"><button class="btn-blue">NIMEMALIZA KULIPIA - ANGALIA CODE YANGU →</button></form></div>{% endif %}
</body></html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, msg="", pending="", order_id="", code_mpya="", mwisho_txt="")

@app.route("/ingia-vocha", methods=["POST"])
def ingia_vocha():
    code = request.form.get("code", "").strip().upper()
    ok, msg = angalia_vocha(code)
    return render_template_string(HTML, msg=msg, pending="", order_id="", code_mpya="", mwisho_txt="")

@app.route("/lipa", methods=["POST"])
def lipa():
    bei = request.form.get("bei", "500")
    simu = request.form.get("simu", "").strip().replace(" ", "")
    if simu.startswith("0"):
        simu = "255" + simu[1:]
    kifurushi = BEI.get(bei, "MASAA7")
    order_id = str(uuid.uuid4())
    code_mpya = tengeneza_code()
    mwisho = tarehe_mwisho(kifurushi)
    MALIPO_YANAYOSUBIRI[order_id] = {"code": code_mpya, "kifurushi": kifurushi, "mwisho": mwisho, "bei": bei, "simu": simu}
    try:
        resp = requests.post(
            "https://api.zenopay.com/api/payments",
            json={"account_id": ZENOPAY_ACCOUNT_ID, "api_key": ZENOPAY_API_KEY, "amount": int(bei), "phone": simu, "order_id": order_id},
            timeout=20
        )
        print("ZenoPay:", resp.status_code, resp.text[:200])
    except Exception as e:
        print(e)
        return render_template_string(HTML, msg="⚠️ Imeshindwa kuungana na ZenoPay. Jaribu tena.", pending="", order_id="", code_mpya="", mwisho_txt="")
    pending = f"Angalia simu yako {simu} - umetumiwa USSD ya kulipia {bei} TSH ({jina_nje(kifurushi)} - Data bila kikomo). Weka PIN yako."
    return render_template_string(HTML, msg="", pending=pending, order_id=order_id, code_mpya="", mwisho_txt="")

@app.route("/angalia", methods=["POST"])
def angalia():
    order_id = request.form.get("order_id", "")
    info = MALIPO_YANAYOSUBIRI.get(order_id)
    if not info:
        return render_template_string(HTML, msg="⚠️ Order haikupatikana. Lipa tena.", pending="", order_id="", code_mpya="", mwisho_txt="")
    try:
        resp = requests.get(f"https://api.zenopay.com/api/payments/{order_id}", headers={"Authorization": f"Bearer {ZENOPAY_API_KEY}"}, timeout=15)
        status = resp.text.lower()
    except Exception:
        status = ""
    if "completed" in status or "paid" in status or "success" in status:
        code_mpya = info["code"]
        VOCHA[code_mpya] = {"kifurushi": info["kifurushi"], "mwisho": info["mwisho"]}
        mwisho_txt = f"Vocha yako ni ya {jina_nje(info['kifurushi'])} - Data bila kikomo!"
        return render_template_string(HTML, msg="✅ Malipo yamethibitishwa!", pending="", order_id="", code_mpya=code_mpya, mwisho_txt=mwisho_txt)
    else:
        pending = "Bado hujalipia. Maliza kulipia kwenye simu yako, halafu bonyeza tena hapa."
        return render_template_string(HTML, msg="", pending=pending, order_id=order_id, code_mpya="", mwisho_txt="")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
