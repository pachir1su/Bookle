import os
import sqlite3
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

from gemini_client import infer_genre

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

DB_PATH = os.path.join(os.path.dirname(__file__), "db.sqlite3")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/api/ping")
def ping():
    return jsonify({"ok": True, "ts": datetime.utcnow().isoformat()})

@app.post("/api/scan")
def scan():
    data = request.get_json(silent=True) or {}
    code = str(data.get("code", "")).strip()
    return jsonify({"student_id": code})

@app.get("/api/student/<sid>/summary")
def student_summary(sid: str):
    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM students WHERE id = ?", (sid,))
        student = cur.fetchone()
        if not student:
            return jsonify({"error": "student_not_found"}), 404

        cur.execute(
            '''
            SELECT b.id, b.title, b.author, b.description, b.genre, h.borrowed_at
            FROM borrow_history h
            JOIN books b ON b.id = h.book_id
            WHERE h.student_id = ?
            ORDER BY h.borrowed_at DESC
            LIMIT 5
            ''',
            (sid,),
        )
        history = [dict(r) for r in cur.fetchall()]

        # pick user-preferred genre from history, else fallback
        genres = [h["genre"] for h in history if h.get("genre")]
        main_genre = genres[0] if genres else None

        if main_genre:
            cur.execute(
                '''
                SELECT id, title, author, description, genre
                FROM books
                WHERE genre = ?
                AND id NOT IN (SELECT book_id FROM borrow_history WHERE student_id = ?)
                LIMIT 3
                ''',
                (main_genre, sid),
            )
        else:
            cur.execute(
                '''
                SELECT id, title, author, description, genre
                FROM books ORDER BY RANDOM() LIMIT 3
                '''
            )
        recs = [dict(r) for r in cur.fetchall()]

        # Gemini (or heuristic) to predict genre for each recommendation
        for r in recs:
            text = f"{r['title']} - {r.get('description','')}"
            genre, provider = infer_genre(text)
            r["predicted_genre"] = genre
            r["predicted_by"] = provider

        # random quote
        cur.execute("SELECT text, author FROM quotes ORDER BY RANDOM() LIMIT 1")
        q = cur.fetchone()
        quote = dict(q) if q else {"text": "Keep reading.", "author": "—"}

        # printable receipt
        receipt_lines = [
            f"[영수증] {student['name']} 님",
            f"- 학번: {student['id']}  학급: {student['class']}  학년: {student['grade']}",
            f"- 최근 대출 {len(history)}권",
        ]
        for h in history:
            receipt_lines.append(f"  • {h['title']} ({h['author']}) — {h['borrowed_at'][:10]}")

        receipt_lines.append("- 추천 도서")
        for r in recs:
            receipt_lines.append(f"  • {r['title']}  [{r.get('predicted_genre') or r.get('genre')}]")
        receipt_lines.append(f'명언: "{quote["text"]}" — {quote["author"]}')

        return jsonify({
            "student": {"id": student["id"], "name": student["name"], "grade": student["grade"], "class": student["class"]},
            "history": history,
            "recommendations": recs,
            "quote": quote,
            "receipt_text": "\n".join(receipt_lines),
        })
    except Exception as e:
        return jsonify({"error": "internal_error", "detail": str(e)}), 500

@app.post("/api/genre")
def genre_api():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "text_required"}), 400
    genre, provider = infer_genre(text)
    return jsonify({"genre": genre, "provider": provider})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="127.0.0.1", port=port, debug=True)