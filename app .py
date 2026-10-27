from flask import Flask, request, jsonify, render_template_string
import random, string, datetime, json, os

app = Flask(__name__)

# Hifadhi ya vocha - itatengenezwa yenyewe
VOUCHERS_FILE = "vouchers.json"
VOUCHERS = {}

# Pakia vocha zilizopo
if os.path.exists(VOUCHERS_FILE):
    try:
        with open(VOUCHERS_FILE, 'r') as f:
            VOUCHERS = json.load(f)
    except:
        VOUCHERS = {}

def save_vouchers():
    with open(VOUCHERS_FILE, 'w') as f:
        json.dump(VOUCHERS, f)

def generate_code():
    return "JV-" + ''.join(random.choices(string.digits, k=4)) + "-" + ''.join(random.choices(string.digits, k=4))

# Page ya malipo - mteja akitoka hotspot yako
PAYMENT_PAGE = """
<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Lipa JEYVAN WIFI</title>
<style>
body{background:#0f0f0f;color:white;font-family:Arial;padding:20px;text-align:center}
.card{background:#1a1a2e;border-radius:20px;padding:25px;max-width:400px;margin:20px auto;border:2px solid #ff9f00}
h1{color:#ff9f00} .price{font-size:40px;color:#00ff88;font-weight:900;margin:15px 0}
button{width:100%;padding:16px;background:#ff9f00;border:none;border-radius:12px;font-weight:900;font-size:18px;margin-top:15px;cursor:pointer}
.info{background:#222;padding:12px;border-radius:10px;margin:15px 0;font-size:13px;text-align:left}
input{width:100%;padding:12px;border-radius:10px;border:1px solid #333;background:#0f0f0f;color:white;margin:8px 0}
</style></head><body>
<div class="card">
<h1>JEYVAN PREMIUM WIFI</h1>
<p>Unaenda kununua kifurushi:</p>
<div class="price">{{bei}} TSH</div>
<p>Masaa: {{masaa}} | Airtel Lipa: 13984763</p>
<div class="info">
<b>Jinsi ya kulipa:</b><br>
1. Ingiza namba yako ya Airtel Money<br>
2. Bonyeza LIPA SASA<br>
3. Thibitisha kwenye simu yako *150*60#<br>
4. Utapata CODE ya kuingia WiFi hapa!
</div>
<form method="POST" action="/lipa">
<input type="hidden" name="bei" value="{{bei}}">
<input type="hidden" name="masaa" value="{{masaa}}">
<input name="phone" placeholder="Namba yako Airtel - 068xxxxxxx" required>
<button type="submit">LIPA SASA {{bei}} TSH →</button>
</form>
<p style="margin-top:15px;font-size:11px;color:#777">Mfumo wa majaribio - Kwa sasa utapewa CODE mara moja baada ya kubonyeza</p>
</div></body></html>
"""

SUCCESS_PAGE = """
<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vocha Yako</title>
<style>body{background:#0f0f0f;color:white;font-family:Arial;padding:20px;text-align:center}
.card{background:#1a1a2e;border-radius:20px;padding:25px;max-width:400px;margin:20px auto;border:2px solid #00ff88}
.code{font-size:32px;background:#000;padding:15px;border-radius:12px;letter-spacing:3px;color:#00ff88;font-weight:900;margin:15px 0;border:2px dashed #00ff88}
button{width:100%;padding:14px;background:#00ff88;border:none;border-radius:10px;font-weight:900;margin-top:10px}</style></head><body>
<div class="card">
<h1 style="color:#00ff88">✓ MALIPO YAMEPOKELEWA!</h1>
<p>Vocha yako ya {{masaa}} Masaa:</p>
<div class="code">{{code}}</div>
<p>Bei: {{bei}} TSH | Muda: {{masaa}}H</p>
<p style="font-size:13px;color:#aaa">Nakili hii CODE na weka kwenye page ya JEYVAN WIFI pale chini "Weka CODE yako hapa"</p>
<button onclick="copyCode()">NAKILI CODE</button>
<button onclick="window.location.href='http://login.hotspot.co.tz'" style="background:#ff9f00">RUDI KUINGIA WIFI →</button>
</div>
<script>function copyCode(){navigator.clipboard.writeText("{{code}}");alert("CODE Imenakiliwa: {{code}}")}</script>
</body></html>
"""

@app.route('/')
def home():
    bei = request.args.get('bei', '500')
    masaa = request.args.get('masaa', '7')
    return render_template_string(PAYMENT_PAGE, bei=bei, masaa=masaa)

@app.route('/lipa', methods=['GET','POST'])
def lipa():
    if request.method == 'GET':
        bei = request.args.get('bei', '500')
        masaa = request.args.get('masaa', '7')
        return render_template_string(PAYMENT_PAGE, bei=bei, masaa=masaa)
    
    bei = request.form.get('bei', '500')
    masaa = request.form.get('masaa', '7')
    phone = request.form.get('phone', '')
    
    code = generate_code()
    now = datetime.datetime.now()
    
    VOUCHERS[code] = {
        "code": code,
        "bei": bei,
        "masaa": masaa,
        "phone": phone,
        "created": now.strftime("%Y-%m-%d %H:%M:%S"),
        "used": False
    }
    save_vouchers()
    
    # HAPA NDIPO AZAMPAY ITAUNGANISHWA BAADAYE
    # Kwa sasa tunatengeneza code mara moja kwa majaribio
    
    return render_template_string(SUCCESS_PAGE, code=code, bei=bei, masaa=masaa)

@app.route('/api/vouchers')
def list_vouchers():
    return jsonify(VOUCHERS)

@app.route('/api/validate/<code>')
def validate(code):
    v = VOUCHERS.get(code)
    if not v:
        return jsonify({"valid": False, "msg": "CODE SI SAHIHI"})
    if v.get("used"):
        return jsonify({"valid": False, "msg": "CODE IMESHATUMIKA"})
    return jsonify({"valid": True, "masaa": v["masaa"], "bei": v["bei"]})

# Hii ndiyo AzamPay itaita baada ya malipo ya Airtel Lipa 13984763
@app.route('/callback/azampay', methods=['POST'])
def azam_callback():
    data = request.json
    # Hapa ndipo tutathibitisha malipo ya kweli
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
