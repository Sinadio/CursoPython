"""
Sistema de Monitorização das Culturas — Starter Kit
Stack: FastAPI (Python) + HTML/JS (frontend leve)

Funcionalidades incluídas:
1) Dados meteorológicos (OpenWeather API)
2) Sensores em tempo real (WebSocket com dados simulados + gancho MQTT)
3) Deteção simples de pragas (upload de imagem; análise básica de manchas/lesões)
4) Análises de saúde da cultura (NDVI/VARI/GLI a partir de bandas ou imagem RGB)

Como executar:
- Python 3.10+
- pip install -r requirements.txt
- Defina a variável de ambiente OPENWEATHER_API_KEY
- uvicorn app:app --reload

Ficheiros gerados dinamicamente:
- /static/* (frontend leve)

Nota: Este é um starter focado em clareza. Em produção, separar frontend, usar build tool, filas, DB, e segurança.
"""

import os
import asyncio
import base64
import io
import json
import math
import random
from datetime import datetime, timezone
from typing import List, Optional

import numpy as np
from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import httpx
from PIL import Image

app = FastAPI(title="Crop Monitor Starter", version="0.1.0")

# CORS (ajuste conforme necessário)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Static Frontend ---
STATIC_INDEX = """
<!doctype html>
<html lang="pt">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Sistema de Monitorização das Culturas</title>
  <style>
    body{font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; margin:0; background:#0b1220; color:#e8eefc}
    header{padding:16px 24px; display:flex; gap:12px; align-items:center; border-bottom:1px solid #1f2a44}
    .badge{background:#12223f; padding:4px 8px; border-radius:999px; font-size:12px; color:#9db4ff}
    main{display:grid; grid-template-columns: 320px 1fr; gap:16px; padding:16px}
    aside, section{background:#0f1830; border:1px solid #1f2a44; border-radius:16px; padding:16px}
    h2{margin:0 0 8px 0; font-size:18px}
    h3{margin:16px 0 8px 0; font-size:16px}
    label{font-size:12px; color:#9db4ff}
    input, button, select{background:#101a34; color:#e8eefc; border:1px solid #253457; border-radius:10px; padding:8px 10px}
    button{cursor:pointer}
    .grid{display:grid; gap:12px}
    .kpi{display:grid; grid-template-columns: repeat(3,1fr); gap:12px}
    .card{background:#0c1428; border:1px solid #1f2a44; border-radius:12px; padding:12px}
    canvas{width:100%; max-height:220px}
    .pill{padding:3px 8px; border-radius:999px; border:1px solid #2d3b63; font-size:12px}
    footer{padding:8px; text-align:center; color:#6b7fb1}
    .row{display:flex; gap:8px; align-items:center}
    .hint{color:#9db4ff; font-size:12px}
    .ok{color:#61d095}
    .warn{color:#ffd56b}
    .err{color:#ff7a7a}
  </style>
</head>
<body>
  <header>
    <div style="font-weight:700">🌾 Crop Monitor</div>
    <div class="badge">Starter</div>
    <div style="margin-left:auto; font-size:12px" id="clock"></div>
  </header>

  <main>
    <aside class="grid">
      <div>
        <h2>Localização & Meteo</h2>
        <div class="grid">
          <div class="row">
            <label>Latitude</label>
            <input id="lat" type="number" step="any" value="-19.8"/>
          </div>
          <div class="row">
            <label>Longitude</label>
            <input id="lon" type="number" step="any" value="34.9"/>
          </div>
          <button id="btnWeather">Obter Meteorologia</button>
          <div id="weather" class="hint">—</div>
        </div>
      </div>

      <div>
        <h2>Sensores em Tempo Real</h2>
        <div class="grid">
          <div class="row"><span class="pill">Solo</span><span id="soil">—</span></div>
          <div class="row"><span class="pill">Temp</span><span id="temp">—</span></div>
          <div class="row"><span class="pill">Humidade</span><span id="hum">—</span></div>
          <button id="btnWS">Conectar</button>
          <div class="hint">Use /ws para simulação. Substitua por MQTT no backend.</div>
        </div>
      </div>

      <div>
        <h2>Deteção de Pragas (Beta)</h2>
        <div class="grid">
          <input type="file" id="img" accept="image/*" />
          <button id="btnPest">Analisar Imagem</button>
          <div id="pest" class="hint">—</div>
        </div>
      </div>

      <div>
        <h2>Saúde da Cultura</h2>
        <div class="grid">
          <label>Upload de imagem RGB (folha/parcel):</label>
          <input type="file" id="imgHealth" accept="image/*"/>
          <button id="btnHealth">Calcular Índices</button>
          <div id="health" class="hint">—</div>
        </div>
      </div>
    </aside>

    <section>
      <h2>Visão Geral</h2>
      <div class="kpi">
        <div class="card">
          <div class="hint">Precipitação (próx. 24h)</div>
          <div id="kpi_rain" style="font-size:28px">—</div>
        </div>
        <div class="card">
          <div class="hint">Índice de Stress (heurístico)</div>
          <div id="kpi_stress" style="font-size:28px">—</div>
        </div>
        <div class="card">
          <div class="hint">Risco de Praga</div>
          <div id="kpi_pest" style="font-size:28px">—</div>
        </div>
      </div>

      <h3>Logs</h3>
      <pre id="log" style="background:#0b1220; border:1px solid #1f2a44; padding:12px; border-radius:8px; max-height:240px; overflow:auto"></pre>
    </section>
  </main>

  <footer>Feito com FastAPI · Este é um protótipo educativo.</footer>

<script>
const $ = (id)=>document.getElementById(id);
const log = (t)=>{$('log').textContent += `[${new Date().toLocaleTimeString()}] ${t}\n`;}

// Relógio
setInterval(()=>{$('clock').textContent = new Date().toLocaleString();},1000);

// Meteo
$('btnWeather').onclick = async ()=>{
  const lat = parseFloat($('lat').value), lon = parseFloat($('lon').value);
  try{
    const res = await fetch(`/api/weather?lat=${lat}&lon=${lon}`);
    const data = await res.json();
    if(data.error){ $('weather').textContent = data.error; return; }
    $('weather').textContent = `Temp: ${data.current.temp}°C · Hum: ${data.current.humidity}% · Vento: ${data.current.wind_speed} m/s`;
    $('kpi_rain').textContent = (data.next24h_rain_mm).toFixed(1)+" mm";
    const stress = heuristicStress(data);
    $('kpi_stress').textContent = stress.label;
  }catch(e){ $('weather').textContent = 'Falha na meteorologia'; log(e); }
}

function heuristicStress(w){
  const t = w.current.temp, h = w.current.humidity, wind = w.current.wind_speed;
  const s = Math.max(0, Math.min(100, (t-18)*3 + (50-h)*0.5 + wind*2));
  let label = 'Baixo'; if(s>35) label='Médio'; if(s>65) label='Alto';
  return {score:s, label};
}

// WebSocket sensores (simulado)
let ws;
$('btnWS').onclick = ()=>{
  if(ws && ws.readyState===1){ ws.close(); return; }
  ws = new WebSocket((location.protocol==='https:'?'wss':'ws')+`://${location.host}/ws`);
  ws.onopen = ()=>{ log('WS conectado'); $('btnWS').textContent='Desconectar'; };
  ws.onmessage = (ev)=>{
    const s = JSON.parse(ev.data);
    $('soil').textContent = s.soil_moisture.toFixed(1)+'%';
    $('temp').textContent = s.air_temp.toFixed(1)+'°C';
    $('hum').textContent = s.air_hum.toFixed(0)+'%';
    $('kpi_pest').textContent = s.pest_risk;
  }
  ws.onclose = ()=>{ log('WS fechado'); $('btnWS').textContent='Conectar'; };
}

// Deteção de pragas (upload)
$('btnPest').onclick = async ()=>{
  const f = $('img').files[0]; if(!f){ alert('Selecione uma imagem'); return; }
  const fd = new FormData(); fd.append('file', f);
  const res = await fetch('/api/pests/analyze', {method:'POST', body:fd});
  const data = await res.json();
  $('pest').innerHTML = `Prob. praga: <b>${(data.prob*100).toFixed(1)}%</b> · Sinais: ${data.signals.join(', ')||'—'}`;
}

// Saúde da cultura (índices RGB)
$('btnHealth').onclick = async ()=>{
  const f = $('imgHealth').files[0]; if(!f){ alert('Selecione uma imagem'); return; }
  const fd = new FormData(); fd.append('file', f);
  const res = await fetch('/api/health/indices', {method:'POST', body:fd});
  const d = await res.json();
  $('health').innerHTML = `VARI: <b>${d.VARI.toFixed(3)}</b> · GLI: <b>${d.GLI.toFixed(3)}</b> · ExG: <b>${d.ExG.toFixed(3)}</b>`;
}
</script>
</body>
</html>
"""

# Monta rota simples para servir o frontend sem ficheiros físicos
@app.get("/", response_class=HTMLResponse)
def index():
    return HTMLResponse(STATIC_INDEX)

# --- Meteorologia (OpenWeather) ---
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

@app.get("/api/weather")
async def get_weather(lat: float = Query(...), lon: float = Query(...)):
    if not OPENWEATHER_API_KEY:
        return JSONResponse({"error": "Defina OPENWEATHER_API_KEY"}, status_code=400)
    url = (
        "https://api.openweathermap.org/data/3.0/onecall"
        f"?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric&exclude=minutely,alerts"
    )
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url)
        r.raise_for_status()
        data = r.json()
    # Previsão de precipitação nas próximas 24h
    next24 = data.get("hourly", [])[:24]
    rain_mm = 0.0
    for h in next24:
        # OpenWeather traz rain:{"1h":mm}
        rain_mm += float(h.get("rain", {}).get("1h", 0.0))
    return {
        "current": {
            "temp": data.get("current", {}).get("temp"),
            "humidity": data.get("current", {}).get("humidity"),
            "wind_speed": data.get("current", {}).get("wind_speed"),
            "dt": data.get("current", {}).get("dt"),
        },
        "next24h_rain_mm": rain_mm,
    }

# --- WebSocket Sensores (simulado) ---
class ConnectionManager:
    def __init__(self):
        self.active: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        if ws in self.active:
            self.active.remove(ws)

    async def broadcast(self, message: dict):
        for ws in list(self.active):
            try:
                await ws.send_json(message)
            except Exception:
                self.disconnect(ws)

manager = ConnectionManager()

@app.websocket("/ws")
async def sensor_ws(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            # Simulação de 1 leitura/segundo
            await asyncio.sleep(1.0)
            reading = {
                "soil_moisture": max(0, min(100, random.gauss(45, 10))),
                "air_temp": random.gauss(28, 3),
                "air_hum": max(0, min(100, random.gauss(60, 8))),
                "pest_risk": random.choice(["Baixo","Médio","Alto"]),
            }
            await manager.broadcast(reading)
    except WebSocketDisconnect:
        manager.disconnect(ws)

# Gancho para MQTT (exemplo de como integrar)
"""
# Exemplo: substitua o simulador por MQTT real
# pip install paho-mqtt
#
# import paho.mqtt.client as mqtt
# mqttc = mqtt.Client()
# mqttc.connect("broker.hivemq.com", 1883)
# mqttc.subscribe("farm/sensor/#")
# def on_message(client, userdata, msg):
#     payload = json.loads(msg.payload)
#     asyncio.create_task(manager.broadcast(payload))
# mqttc.on_message = on_message
# mqttc.loop_start()
"""

# --- Deteção simples de pragas ---
# Heurística: detectar proporção de pixels castanho-escuros/vermelhos (lesões),
# e desvio de canais que sugiram padrões manchados.

def analyze_pest_image(img: Image.Image) -> dict:
    img = img.convert("RGB").resize((512, 512))
    arr = np.asarray(img).astype(np.float32) / 255.0
    R, G, B = arr[...,0], arr[...,1], arr[...,2]

    # Máscara de possíveis lesões (tons castanhos/avermelhados, baixa G)
    lesion_mask = (R>0.35) & (G<0.35) & (R>G) & (R>B*0.9)
    lesion_ratio = float(lesion_mask.mean())

    # Variança local aproximada via gradiente (bordas de manchas)
    gx = np.abs(np.gradient(R)[0]) + np.abs(np.gradient(G)[0]) + np.abs(np.gradient(B)[0])
    gy = np.abs(np.gradient(R)[1]) + np.abs(np.gradient(G)[1]) + np.abs(np.gradient(B)[1])
    texture = float(np.clip((gx+gy).mean()*2.0, 0, 1))

    # Probabilidade heurística
    prob = np.clip(lesion_ratio*2.5 + texture*0.5, 0, 1)
    signals = []
    if lesion_ratio>0.03: signals.append("manchas")
    if texture>0.15: signals.append("padrão irregular")
    return {"prob": prob, "signals": signals}

@app.post("/api/pests/analyze")
async def pests_analyze(file: UploadFile = File(...)):
    content = await file.read()
    img = Image.open(io.BytesIO(content))
    result = analyze_pest_image(img)
    return result

# --- Saúde da cultura (índices com base em RGB) ---
# Índices úteis para RGB: VARI, GLI, Excess Green (ExG)
# Referências:
#  VARI = (G - R) / (G + R - B)
#  GLI  = (2G - R - B) / (2G + R + B)
#  ExG  = 2G - R - B (normalizado aqui)

def rgb_indices(img: Image.Image) -> dict:
    img = img.convert("RGB").resize((512,512))
    arr = np.asarray(img).astype(np.float32)
    R, G, B = arr[...,0], arr[...,1], arr[...,2]
    denom_vari = (G + R - B)
    denom_vari[denom_vari==0] = 1
    VARI = np.mean((G - R) / denom_vari)
    GLI = np.mean((2*G - R - B) / (2*G + R + B + 1e-6))
    ExG = np.mean((2*G - R - B) / 255.0)
    return {"VARI": float(VARI), "GLI": float(GLI), "ExG": float(ExG)}

@app.post("/api/health/indices")
async def health_indices(file: UploadFile = File(...)):
    content = await file.read()
    img = Image.open(io.BytesIO(content))
    return rgb_indices(img)

# --- Pequena rota de saúde do servidor ---
@app.get("/api/status")
def status():
    return {"ok": True, "server_time": datetime.now(timezone.utc).isoformat()}

# --- requirements.txt helper ---
@app.get("/requirements.txt", response_class=HTMLResponse)
def reqs():
    return HTMLResponse(
        "\n".join([
            "fastapi==0.111.0",
            "uvicorn[standard]==0.30.1",
            "httpx==0.27.0",
            "pillow==10.3.0",
            "numpy==1.26.4",
            # "paho-mqtt==1.6.1"  # opcional se for integrar MQTT
        ])
    )
