from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import sqlite3
from models import get_conn, init_db

app = Flask(__name__)
CORS(app)

# Ensure DB exists
init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/spots", methods=["GET"])
def get_spots():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, spot_name, occupied FROM spots ORDER BY id")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route("/api/spots/<int:spot_id>", methods=["POST"])
def set_spot(spot_id):
    data = request.json or {}
    occupied = int(data.get("occupied", 0))
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE spots SET occupied=? WHERE id=?", (occupied, spot_id))
    conn.commit()
    conn.close()
    return jsonify({"status":"ok", "id": spot_id, "occupied": occupied})

# Endpoint sensors can call: POST /api/sensor with {"spot": 3, "occupied": 1}
@app.route("/api/sensor", methods=["POST"])
def sensor_update():
    data = request.json or {}
    spot_id = int(data.get("spot"))
    occupied = int(data.get("occupied", 0))
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE spots SET occupied=? WHERE id=?", (occupied, spot_id))
    conn.commit()
    conn.close()
    return jsonify({"status":"ok"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
