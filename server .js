const express = require('express');
const app = express();
app.use(express.json());

const MANUAL_CODES = ["JEYVAN-1234", "JEYVAN-5678"]; // CODE zako za mkono zinabaki hapa

app.get('/', (req, res) => {
  res.send('JEYVAN API Iko Sawa - Kalenda Vifurushi');
});

app.post('/api/payment', (req, res) => {
  const { phone, amount, code } = req.body;
  console.log(`Malipo: ${phone} - ${amount} - Code: ${code}`);
  // Hapa ndipo CODE inatengenezwa kiotomatiki
  const newCode = "JEY-" + Math.floor(1000 + Math.random() * 9000);
  res.json({ success: true, code: newCode, message: "CODE imetengenezwa" });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log('Server inafanya kazi kwenye ' + PORT));