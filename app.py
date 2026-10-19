import os
import pymysql
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_conn():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "rootpass"),
        database=os.getenv("DB_NAME", "praktikum"),
        cursorclass=pymysql.cursors.DictCursor,
    )

def init_table(conn):
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS notes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            content VARCHAR(255) NOT NULL)""")
    conn.commit()

@app.route("/")
def hello():
    return "Halo dari Flask + MySQL + Docker + Jenkins!"

@app.route("/notes", methods=["GET", "POST"])
def notes():
    conn = get_conn()
    init_table(conn)
    with conn.cursor() as cur:
        if request.method == "POST":
            cur.execute("INSERT INTO notes (content) VALUES (%s)",
                        (request.json.get("content", ""),))
            conn.commit()
        cur.execute("SELECT * FROM notes")
        data = cur.fetchall()
    conn.close()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)