from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class HealthRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heart_rate = db.Column(db.Float, nullable=False)
    spo2 = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    glucose = db.Column(db.Float, nullable=False)
    systolic = db.Column(db.Integer, nullable=False)
    diastolic = db.Column(db.Integer, nullable=False)
    sweat_ph = db.Column(db.Float, nullable=False)
    stress_level = db.Column(db.String(20))
    prediction = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "heart_rate": self.heart_rate,
            "spo2": self.spo2,
            "temp": self.temperature,
            "glucose": self.glucose,
            "bp": f"{self.systolic}/{self.diastolic}",
            "stress": self.stress_level,
            "prediction": self.prediction,
            "time": self.timestamp.strftime("%H:%M:%S")
        }