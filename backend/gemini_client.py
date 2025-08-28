import os, re

GENRES = [
    "과학", "공상과학", "판타지", "추리", "로맨스", "역사", "철학",
    "자기계발", "에세이", "인문", "컴퓨터/IT", "경제/경영", "사회", "예술", "문학", "기타",
]

def heuristic(text: str) -> str:
    t = (text or "").lower()
    pairs = [
        ("ai", "컴퓨터/IT"), ("python", "컴퓨터/IT"), ("javascript", "컴퓨터/IT"),
        ("quantum", "과학"), ("space", "공상과학"), ("galaxy", "공상과학"),
        ("magic", "판타지"), ("dragon", "판타지"),
        ("detective", "추리"), ("murder", "추리"),
        ("love", "로맨스"), ("romance", "로맨스"),
        ("history", "역사"), ("ancient", "역사"),
        ("philosophy", "철학"), ("stoic", "철학"),
        ("habit", "자기계발"), ("productivity", "자기계발"),
        ("essay", "에세이"),
        ("humanities", "인문"),
        ("economics", "경제/경영"), ("business", "경제/경영"),
        ("society", "사회"),
        ("art", "예술"),
        ("novel", "문학"), ("poem", "문학"),
    ]
    for kw, g in pairs:
        if kw in t:
            return g
    return "기타"

def infer_genre(text: str):
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        return heuristic(text), "heuristic"
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = (
            "다음 문장의 책 장르를 한 단어로 예측하라. 후보: " + ", ".join(GENRES) +
            "\\n문장: " + (text or "") + "\\n반환 형식: 후보 중 하나만 출력."
        )
        resp = model.generate_content(prompt)
        out = resp.text.strip() if hasattr(resp, "text") else ""
        # 정규화
        out = out.replace("IT", "컴퓨터/IT")
        out = out.replace("컴퓨터", "컴퓨터/IT") if out == "컴퓨터" else out
        # 후보군 이외면 휴리스틱
        if out not in GENRES:
            out = heuristic(text)
        return out, "gemini"
    except Exception as e:
        return heuristic(text), "heuristic"