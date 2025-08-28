
# Bookle Fullstack

## 빠른 실행
```bash
# 1) 루트에서
npm install

# 2) 의존성 + 더미 DB 시드
# Windows
npm run setup:win
# macOS/Linux
npm run setup:posix

# 3) 프론트/백 동시 실행
# Windows
npm run dev:win
# macOS/Linux
npm run dev
```

- 프론트: http://localhost:5173
- 백엔드: http://127.0.0.1:5000/api/ping

> Gemini 키가 없으면 휴리스틱으로 장르를 예측합니다.
```
set GOOGLE_API_KEY=YOUR_KEY   # Windows PowerShell은 $env:GOOGLE_API_KEY="..."
export GOOGLE_API_KEY=YOUR_KEY
```
