from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "<html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>body{font-family:Arial;background:#0f172a;color:white;text-align:center;padding:20px}.box{background:white;color:#0f172a;max-width:400px;margin:auto;padding:20px;border-radius:15px}.lipa{background:#22c55e;color:white;padding:15px;border-radius:10px;margin-top:20px;font-size:20px;font-weight:bold}</style></head><body><div class='box'><h1>JEYVAN STUDIO</h1><h3>WIFI YA KASI MBULU</h3><p>500 - 7 Hours</p><p>1000 - 1 Day</p><p>5000 - 1 Week</p><p>15000 - 1 Month</p><div class='lipa'>AIRTEL LIPA NAMBA<br><span style='font-size:32px'>13984763</span><br>Jina: JEYVAN STUDIO</div></div></body></html>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
