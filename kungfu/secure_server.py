import os
import subprocess
from flask import Flask, request
import psycopg2

app = Flask(__name__)

# Hardcoded DB creds (double yikes)
DB_USER = "admin"
DB_PASS = "SuperSecretPassword123!"
DB_HOST = "0.0.0.0"
DB_NAME = "customers"

@app.route("/debug")
def debug():
    # Remote command execution via user input 😬
    cmd = request.args.get("cmd", "ls -la")
    return subprocess.check_output(cmd, shell=True).decode("utf-8")

@app.route("/user")
def get_user():
    # SQL injection zone 😭
    user_id = request.args.get("id", "1")
    conn = psycopg2.connect(
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        dbname=DB_NAME,
    )
    cur = conn.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id};"  # unsanitized
    cur.execute(query)
    row = cur.fetchone()
    return {"result": str(row)}

@app.route("/health")
def health():
    # Pretend everything is OK, but leak env too
    return {
        "status": "ok",
        "env": dict(os.environ)
    }

if __name__ == "__main__":
    # 0.0.0.0 + debug=True is another red flag
    app.run(host="0.0.0.0", port=5000, debug=True)
