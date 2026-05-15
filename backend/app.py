import random
import time
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class HealthRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heart_rate = db.Column(db.Float)
    spo2 = db.Column(db.Float)
    temperature = db.Column(db.Float)
    blood_pressure = db.Column(db.String(20))
    glucose = db.Column(db.Float)
    sweat_ph = db.Column(db.Float)
    stress_level = db.Column(db.String(50))
    prediction = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

def ai_diagnostic_logic(data):
    """Simulated AI Prediction Logic based on clinical thresholds"""
    alerts = []
    prediction = "Stable"
    
    if data['heart_rate'] > 100: alerts.append("Tachycardia Detected")
    if data['spo2'] < 94: alerts.append("Oxygen Abnormality")
    if data['temp'] > 38.0: alerts.append("Fever Detected")
    if data['glucose'] > 140: alerts.append("High Glucose Alert")
    
    # Stress detection logic (HRV/Sweat Proxy)
    stress = "Low"
    if data['heart_rate'] > 90 and data['sweat_ph'] < 5.0:
        stress = "High"
    
    if alerts:
        prediction = " / ".join(alerts)
    
    return prediction, stress

@app.route('/api/telemetry', methods=['GET'])
def get_telemetry():
    # Simulate Real-time Biosensor Data
    data = {
        "heart_rate": round(random.uniform(65, 110), 1),
        "spo2": round(random.uniform(92, 100), 1),
        "temp": round(random.uniform(36.5, 39.5), 1),
        "systolic": random.randint(110, 145),
        "diastolic": random.randint(70, 95),
        "glucose": round(random.uniform(80, 160), 1),
        "sweat_ph": round(random.uniform(4.5, 7.0), 1)
    }
    
    prediction, stress = ai_diagnostic_logic(data)
    
    # Save to history
    new_record = HealthRecord(
        heart_rate=data['heart_rate'],
        spo2=data['spo2'],
        temperature=data['temp'],
        blood_pressure=f"{data['systolic']}/{data['diastolic']}",
        glucose=data['glucose'],
        sweat_ph=data['sweat_ph'],
        stress_level=stress,
        prediction=prediction
    )
    db.session.add(new_record)
    db.session.commit()

    return jsonify({
        **data,
        "prediction": prediction,
        "stress": stress,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })

@app.route('/api/history', methods=['GET'])
def get_history():
    records = HealthRecord.query.order_by(HealthRecord.timestamp.desc()).limit(10).all()
    return jsonify([{
        "time": r.timestamp.strftime("%H:%M:%S"),
        "hr": r.heart_rate,
        "spo2": r.spo2,
        "temp": r.temperature
    } for r in reversed(records)])

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
