import { useState } from 'react'
import './index.css'

function App() {
  const [jobDescription, setJobDescription] = useState('')
  const [resumeText, setResumeText] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [result, setResult] = useState(null)

  const handleGenerate = () => {
    if (!jobDescription || !resumeText) return;
    
    setIsGenerating(true);
    
    // Fetch from real backend
    fetch('http://localhost:3001/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ jobDescription, resumeText })
    })
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        alert("Error: " + data.error);
        setIsGenerating(false);
        return;
      }
      setResult(data);
      setIsGenerating(false);
    })
    .catch(err => {
      alert("Failed to connect to backend: " + err.message);
      setIsGenerating(false);
    });
  }

  return (
    <div className="animate-slide-up">
      <header className="text-center mb-2 mt-8">
        <h1 className="gradient-text" style={{ fontSize: '3rem' }}>ResumeAI Pro</h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '1.125rem' }}>
          Instantly tailor your resume and generate the perfect cover letter.
        </p>
      </header>

      <main className="mt-8">
        {!result ? (
          <div className="grid grid-cols-2">
            <div className="glass-panel">
              <h2 className="mb-2 text-center">Your Details</h2>
              <div className="input-group">
                <label>Target Job Description</label>
                <textarea 
                  placeholder="Paste the job description here..."
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                />
              </div>
              <div className="input-group">
                <label>Your Current Resume</label>
                <textarea 
                  placeholder="Paste your current resume text here..."
                  style={{ minHeight: '200px' }}
                  value={resumeText}
                  onChange={(e) => setResumeText(e.target.value)}
                />
              </div>
              <button 
                className="btn btn-primary" 
                style={{ width: '100%' }}
                onClick={handleGenerate}
                disabled={isGenerating || !jobDescription || !resumeText}
              >
                {isGenerating ? (
                  <span className="animate-pulse">Analyzing with AI...</span>
                ) : (
                  'Generate Application Package'
                )}
              </button>
            </div>
            
            <div className="glass-panel flex flex-col justify-center items-center text-center" style={{ borderStyle: 'solid', borderColor: 'var(--primary-color)' }}>
              <h3>AI-Powered Optimization</h3>
              <p style={{ color: 'var(--text-secondary)' }}>
                Our advanced AI analyzes the job description keywords and rewrites your resume bullet points to bypass ATS filters, while generating a highly personalized cover letter.
              </p>
              
              <div className="mt-8 p-4" style={{ background: 'rgba(255,255,255,0.05)', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.1)' }}>
                <h4 style={{ marginBottom: '0.5rem' }}>Pro Plan Required</h4>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '1rem' }}>
                  Unlimited AI generations for $9/month.
                </p>
                <a 
                  href="https://buy.stripe.com/test_premium_plan" 
                  target="_blank" 
                  rel="noreferrer" 
                  className="btn btn-secondary" 
                  style={{ display: 'inline-block', width: '100%', textDecoration: 'none' }}
                >
                  Upgrade via Stripe
                </a>
              </div>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-2 animate-slide-up">
            <div className="glass-panel">
              <div className="flex justify-between items-center mb-2">
                <h2>Generated Cover Letter</h2>
                <button className="btn btn-secondary" onClick={() => navigator.clipboard.writeText(result.coverLetter)}>
                  Copy Text
                </button>
              </div>
              <textarea 
                readOnly 
                value={result.coverLetter} 
                style={{ minHeight: '400px', background: 'rgba(0,0,0,0.2)' }} 
              />
            </div>
            
            <div className="flex flex-col gap-6">
              <div className="glass-panel">
                <h2>Resume Improvements</h2>
                <ul style={{ color: 'var(--text-secondary)', lineHeight: '1.6' }}>
                  {result.improvements.map((imp, idx) => (
                    <li key={idx} className="mb-2">{imp}</li>
                  ))}
                </ul>
              </div>
              
              <button className="btn btn-secondary" onClick={() => setResult(null)}>
                ← Start New Application
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
