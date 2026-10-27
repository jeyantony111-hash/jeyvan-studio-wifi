from flask import Flask, request, render_template_string, redirect
import datetime

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>JEYVAN STUDIO - WIFI MBULU</title>
<style>
body{font-family:Arial;background:linear-gradient(135deg,#0f172a,#1e3a8a);color:white;margin:0;padding:20px;min-height:100vh}
.container{max-width:400px;margin:auto;background:rgba(255,255,255,0.1);backdrop-filter:blur(10px);border-radius:20px;padding:25px;box-shadow:0 10px 30px rgba(0,0,0,0.3)}
h1{text-align:center;color:#facc15;margin-bottom:5px}
.sub{text-align:center;opacity:0.8;margin-bottom:20px}
.card{background:white;color:#0f172a;border-radius:15px;padding:15px;margin:12px 0;display:flex;justify-content:space-between;align-items:center;transition:0.3s}
.card:hover{transform:scale(1.02)}
.price{font-weight:bold;font-size:18px}
.time{font-size:13px;opacity:0.7}
.btn{background:#facc15;color:#0f172a;border:none;padding:10px 18px;border-radius:10px;font-weight:bold;cursor:pointer}
.btn:hover{background:#fde047}
.lipa{background:#00a651;color:white;text-align:center;padding:12px;border-radius:12px;margin-top:20px;font-weight:bold}
</style>
</head>
<body>
<div class="container">
<h1>JEYVAN STUDIO</h1>
<div class="sub">WIFI YA KASI MBULU - Karibu Mteja!</div>

<div class="card">
<div><div class="price">TZS 500</div><div class="time">Masaa 7 - Browsing</div></div>
<a href="/lipa?amount=500"><button class="btn">Nunua</button></a>
</div>

<div class="card">
<div><div class="price">TZS 1,000</div><div class="time">Masaa 24 - Siku 1</div></div>
<a href="/lipa?amount=1000"><button class="btn">Nunua</button></a>
</div>

<div class="card">
<div><div class="price">TZS 5,000</div><div class="time">Wiki 1 - Unlimited</div></div>
<a href="/lipa?amount=5000"><button class="btn">Nunua</button></a>
</div>

<div class="card">
<div><div class="price">TZS 15,000</div><div class="time">Mwezi 1 - Family</div></div>
<a href="/lipa?amount=15000"><button class="btn">Nunua</button></a>
</div>

<div class="lipa">
Airtel Lipa Namba: 13984763<br>
Jina: JEYVAN STUDIO<br>
Lipa kisha weka Code ya Muamala
</div>

</div>
</body>
</html>
"""

LIPA_PAGE = """
<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width,initial-scale=1.0">
<style>body{font-family:Arial;background:#0f172a;color:white;padding:20px;text-align:center}
.box{max-width:400px;margin:auto;background:white;color:#0f172a;padding:25px;border-radius:20px}
input{width:90%;padding:12px;margin:10px 0;border-radius:10px;border:1px solid #ccc}
.btn{background:#00a651;color:white;padding:12px 25px;border:none;border-radius:10px;font-weight:bold;width:100%}</style>
</head><body>
<div class="box">
<h2>Lipa TZS {{amount}} - JEYVAN</h2>
<p>1. Piga *150*60# Airtel<br>2. Chagua Lipa Namba<br>3. Weka: <b>13984763</b><br>4. Weka Kiasi: <b>{{amount}}</b></p>
<form action="/verify" method="post">
<input type="hidden" name="amount" value="{{amount}}">
<input type="text" name="code" placeholder="Weka Code ya Muamala hapa (mf: CI...)" required>
<button class="btn">THIBITISHA MALIPO</button>
</form>
<p style="font-size:12px;opacity:0.7">Baada ya kuthibitisha utaunganishwa moja kwa moja</p>
</div>
</body></html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/lipa')
def lipa():
    amount = request.args.get('amount','500')
    return render_template_string(LIPA_PAGE, amount=amount)

@app.route('/verify', methods=['POST'])
def verify():
    code = request.form.get('code')
    amount = request.form.get('amount')
    # Hapa ndipo tunaruhusu mtumiaji aingie - Kwa sasa tunakubali code yoyote
    # Baadaye tutaunganisha na API ya Airtel
    return f"""
    <html><head><meta name="viewport" content="width=device-width,initial-scale=1.0">
    <style>body{{background:#0f172a;color:white;text-align:center;padding:40px;font-family:Arial}}
    .ok{{background:#00a651;padding:20px;border-radius:20px;max-width:400px;margin:auto}}
    </style></head><body>
    <div class="ok">
    <h1>✅ MALIPO YAMEPOKELEWA!</h1>
    <p>Kiasi: TZS {amount}</p>
    <p>Code: {code}</p>
    <p>Umeunganishwa kwenye JEYVAN STUDIO WIFI!</p>
    <p>Enjoy - Muda wako umeanza kuhesabiwa.</p>
    <hr>
    <p style="font-size:12px">Mteja atapata internet moja kwa moja. Password ya WiFi itaonekana hapa.</p>
    </div>
    </body></html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
