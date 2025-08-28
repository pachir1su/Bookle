import React, { useEffect, useState } from 'react'

const Panel = ({children}) => (
  <div style={{background:'#121a2a',border:'1px solid #26324a',borderRadius:12,padding:20,marginTop:20}}>
    {children}
  </div>
)

export default function App(){
  const [sid, setSid] = useState('30216')
  const [error, setError] = useState(null)
  const [data, setData] = useState(null)
  const [genreText, setGenreText] = useState('공학이란 무엇인가')

  useEffect(() => {
    fetch('/api/ping').catch(()=>{})
  }, [])

  const fetchSummary = async () => {
    setError(null); setData(null)
    try{
      const res = await fetch(`/api/student/${encodeURIComponent(sid)}/summary`)
      if(!res.ok) throw new Error(`status ${res.status}`)
      const json = await res.json()
      setData(json)
    }catch(e){
      setError(`Request failed with ${e.message}`)
    }
  }

  const analyzeGenre = async () => {
    try{
      const res = await fetch('/api/genre', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({text: genreText})
      })
      const json = await res.json()
      alert(`장르: ${json.genre} (${json.provider})`)
    }catch(e){
      alert('분석 실패: ' + e.message)
    }
  }

  return (
    <div style={{maxWidth:880,margin:'40px auto',padding:'0 16px'}}>
      <h1 style={{display:'flex',alignItems:'center',gap:10,marginBottom:8}}>
        <span style={{fontSize:28}}>📚 Library Quote Receipt</span>
      </h1>
      <div style={{opacity:.8,marginBottom:18}}>바코드/학번 입력 → 추천 도서 & 글귀를 영수증으로 출력</div>

      <div style={{display:'flex',gap:10}}>
        <input
          value={sid}
          onChange={e=>setSid(e.target.value)}
          placeholder="학번을 입력하세요"
          style={{flex:1,background:'#0f1724',border:'1px solid #294063',borderRadius:14,padding:'14px 16px',color:'#cfe3ff',outline:'none'}}
        />
        <button onClick={fetchSummary} style={{background:'#243043',border:'1px solid #304a72',borderRadius:12,padding:'10px 16px',color:'#d9e6ff',cursor:'pointer'}}>조회</button>
      </div>

      {error && <div style={{color:'#ff8b8b',marginTop:12}}>⚠ {error}</div>}

      {data && (
        <Panel>
          <h2 style={{marginTop:0}}>요약</h2>
          <div style={{margin:'6px 0 12px 0'}}>
            {data.student.name} • 학번 {data.student.id} • {data.student.grade}학년 {data.student.class}반
          </div>

          <h3>최근 대출</h3>
          <ul>
            {data.history.map((h, i)=>(
              <li key={i}>{h.title} ({h.author}) — {h.borrowed_at?.slice(0,10)} [{h.genre}]</li>
            ))}
          </ul>

          <h3>추천 도서</h3>
          <ul>
            {data.recommendations.map((r)=>(
              <li key={r.id}>
                {r.title} ({r.author}) — 예측 장르: <b>{r.predicted_genre || r.genre}</b> <small style={{opacity:.7}}>by {r.predicted_by}</small>
              </li>
            ))}
          </ul>

          <h3>영수증 미리보기</h3>
          <pre style={{whiteSpace:'pre-wrap',background:'#0f1724',padding:14,borderRadius:12,border:'1px solid #233553'}}>{data.receipt_text}</pre>
        </Panel>
      )}

      <Panel>
        <h2>🧠 Gemini Genre Analyzer</h2>
        <div style={{opacity:.8,marginBottom:6}}>책 제목 또는 소개 문단을 입력하면 장르를 예측합니다.</div>
        <textarea
          value={genreText}
          onChange={e=>setGenreText(e.target.value)}
          rows={6}
          style={{width:'100%',background:'#0f1724',border:'1px solid #294063',borderRadius:12,padding:12,color:'#cfe3ff'}}
        />
        <div style={{marginTop:10,display:'flex',gap:10}}>
          <button onClick={analyzeGenre} style={{background:'#243043',border:'1px solid #304a72',borderRadius:12,padding:'10px 16px',color:'#d9e6ff',cursor:'pointer'}}>분석</button>
          <div style={{opacity:.6}}>결과: 분석 실패 · by client</div>
        </div>
      </Panel>

      <div style={{opacity:.5,marginTop:26}}>Made with React + Flask · Dummy DB</div>
    </div>
  )
}