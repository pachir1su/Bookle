import os, sqlite3, random, datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "db.sqlite3")

def main():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("CREATE TABLE students (id TEXT PRIMARY KEY, name TEXT, grade INTEGER, class TEXT)")
    cur.execute("CREATE TABLE books (id TEXT PRIMARY KEY, title TEXT, author TEXT, description TEXT, genre TEXT)")
    cur.execute("CREATE TABLE borrow_history (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id TEXT, book_id TEXT, borrowed_at TEXT)")
    cur.execute("CREATE TABLE quotes (text TEXT, author TEXT)")

    students = [
        ("30216", "홍길동", 3, "02"),
        ("10101", "김아라", 1, "01"),
    ]
    cur.executemany("INSERT INTO students VALUES (?,?,?,?)", students)

    books = [
        ("b1", "파이썬으로 시작하는 AI", "김개발", "AI와 파이썬 실습 가이드", "컴퓨터/IT"),
        ("b2", "양자 세계의 비밀", "이과학", "양자역학 입문 소개", "과학"),
        ("b3", "마법사의 유산", "박환상", "고대 마법서와 모험", "판타지"),
        ("b4", "사라진 목격자", "최추리", "형사와 미스터리 사건", "추리"),
        ("b5", "로마 제국 연대기", "정역사", "고대 로마 이야기", "역사"),
        ("b6", "사랑의 온도", "윤로맨스", "두 청춘의 사랑 이야기", "로맨스"),
        ("b7", "비즈니스 모델의 정석", "한경영", "성장 전략과 수익화", "경제/경영"),
        ("b8", "엔트로피와 삶", "류철학", "과학과 철학의 교차점", "철학"),
    ]
    cur.executemany("INSERT INTO books VALUES (?,?,?,?,?)", books)

    borrows = [
        ("30216", "b7", "2025-06-04"),
        ("30216", "b1", "2025-05-21"),
        ("30216", "b4", "2025-04-17"),
        ("10101", "b3", "2025-05-09"),
    ]
    cur.executemany("INSERT INTO borrow_history (student_id, book_id, borrowed_at) VALUES (?,?,?)", borrows)

    quotes = [
        ("책은 들고 다니는 주머니 속의 정원이다.", "중국 속담"),
        ("네 꿈을 설계하라. 그렇지 않으면 누군가의 꿈을 위해 일하게 될 것이다.", "짐 론"),
        ("읽는다는 것은 새로운 세계를 사는 일이다.", "나탈리 사루트"),
    ]
    cur.executemany("INSERT INTO quotes VALUES (?,?)", quotes)

    conn.commit()
    conn.close()
    print("Seeded:", DB_PATH)

if __name__ == "__main__":
    main()