import { useState } from 'react'
import './App.css'

// ─────────────────────────────────────────────
// ACTION REQUIRED BEFORE GOING LIVE:
//   1. Sign up at https://affiliate-program.amazon.in
//   2. Replace "YOUR_TAG-21" below with your real Associates tag
//   3. Optionally replace search-based links with direct ASIN links for better tracking
// ─────────────────────────────────────────────
const AMAZON_TAG = "YOUR_TAG-21"
const AMAZON_BASE = "https://www.amazon.in/s?k="

function amazonLink(keyword) {
  return `${AMAZON_BASE}${encodeURIComponent(keyword)}&tag=${AMAZON_TAG}`
}

const ARTICLES = [
  // ── TECH ──────────────────────────────────
  {
    id: 1, cat: "Tech", tag: "Keyboards",
    title: "Best mechanical keyboards for typing all day",
    desc: "Tactile switches, solid build, wrist-friendly layouts. Tested across 30 days of real work.",
    score: 94,
    img: "https://images.unsplash.com/photo-1595225476474-87563907a212?w=600&q=60",
    keyword: "mechanical keyboard india",
    readTime: 5
  },
  {
    id: 2, cat: "Tech", tag: "Monitors",
    title: "Ultrawide monitors that actually boost productivity",
    desc: "Stop alt-tabbing. The right ultrawide pays for itself in focus time within a month.",
    score: 91,
    img: "https://images.unsplash.com/photo-1527443154391-507e9dc6c5cc?w=600&q=60",
    keyword: "ultrawide monitor 34 inch",
    readTime: 6
  },
  {
    id: 3, cat: "Tech", tag: "Audio",
    title: "Noise-cancelling headphones worth paying for",
    desc: "We tested six pairs. Three have genuinely great ANC. Here's which one fits your budget.",
    score: 88,
    img: "https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=600&q=60",
    keyword: "noise cancelling headphones",
    readTime: 7
  },
  // ── HEALTH ────────────────────────────────
  {
    id: 4, cat: "Health", tag: "Ergonomics",
    title: "Ergonomic office chairs under ₹20,000",
    desc: "Your back is paying for a cheap chair. These picks stop the pain without breaking the bank.",
    score: 90,
    img: "https://images.unsplash.com/photo-1505843490538-5133c6c7d0e1?w=600&q=60",
    keyword: "ergonomic office chair india",
    readTime: 6
  },
  {
    id: 5, cat: "Health", tag: "Fitness",
    title: "Home gym essentials that actually get used",
    desc: "Resistance bands, adjustable dumbbells, a pull-up bar — gear people use past month one.",
    score: 87,
    img: "https://images.unsplash.com/photo-1534258936925-c58bed479fcb?w=600&q=60",
    keyword: "home gym equipment india",
    readTime: 5
  },
  {
    id: 6, cat: "Health", tag: "Wearables",
    title: "Sleep trackers that go beyond step counting",
    desc: "HRV, resting heart rate, sleep stages — wearables that give you data you can actually act on.",
    score: 85,
    img: "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=600&q=60",
    keyword: "fitness band sleep tracker",
    readTime: 7
  },
  // ── FINANCE ───────────────────────────────
  {
    id: 7, cat: "Finance", tag: "Planners",
    title: "Best budgeting planners and notebooks for 2026",
    desc: "Sometimes pen and paper beats an app. These structured planners help you actually stick to a budget.",
    score: 83,
    img: "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=600&q=60",
    keyword: "budget planner notebook india",
    readTime: 4
  },
  {
    id: 8, cat: "Finance", tag: "Books",
    title: "Finance books that changed how people think about money",
    desc: "Not get-rich-quick. Real books on compounding, frugality, and building wealth slowly.",
    score: 92,
    img: "https://images.unsplash.com/photo-1535398089889-dd807df1dfaa?w=600&q=60",
    keyword: "personal finance books india",
    readTime: 5
  },
  {
    id: 9, cat: "Finance", tag: "Calculators",
    title: "Scientific calculators for students and CA exams",
    desc: "From JEE to CA Foundation — the calculators actually allowed in Indian exams.",
    score: 86,
    img: "https://images.unsplash.com/photo-1587145820266-a5951ee6f620?w=600&q=60",
    keyword: "scientific calculator india casio",
    readTime: 4
  },
  // ── HOME ──────────────────────────────────
  {
    id: 10, cat: "Home", tag: "Kitchen",
    title: "Air fryers worth buying in India under ₹5,000",
    desc: "We cooked 30 meals across 4 models. Two are genuinely great. Here's what to buy.",
    score: 89,
    img: "https://images.unsplash.com/photo-1585325701956-60dd9c8553bc?w=600&q=60",
    keyword: "air fryer india 4 litre",
    readTime: 6
  },
  {
    id: 11, cat: "Home", tag: "Lighting",
    title: "Smart bulbs that work without a subscription",
    desc: "No monthly fees, local control, works with Alexa. Smart lighting that respects your privacy.",
    score: 84,
    img: "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&q=60",
    keyword: "smart led bulb india wifi",
    readTime: 5
  },
  {
    id: 12, cat: "Home", tag: "Storage",
    title: "Under-bed storage boxes that actually fit Indian beds",
    desc: "Indian apartments are small. These flat-pack, stackable boxes solved the problem for real homes.",
    score: 81,
    img: "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&q=60",
    keyword: "under bed storage box india",
    readTime: 4
  },
]

const CATS = ["All", "Tech", "Health", "Finance", "Home"]

const CAT_COLORS = {
  Tech: "#1d6fce",
  Health: "#0f6e56",
  Finance: "#854f0b",
  Home: "#993556",
}

export default function App() {
  const [activeCat, setActiveCat] = useState("All")

  const filtered = activeCat === "All"
    ? ARTICLES
    : ARTICLES.filter(a => a.cat === activeCat)

  return (
    <div className="app">
      <nav className="navbar">
        <div className="brand">Smart<span>Pick</span></div>
        <div className="nav-links">
          {CATS.filter(c => c !== "All").map(cat => (
            <button
              key={cat}
              className={`nav-link ${activeCat === cat ? 'active' : ''}`}
              onClick={() => setActiveCat(cat)}
            >
              {cat}
            </button>
          ))}
        </div>
      </nav>

      <div className="hero">
        <h1>Trusted reviews across every niche</h1>
        <p>Real picks. No sponsored bias. Affiliate links support this site at no cost to you.</p>
        <div className="disclosure">
          ⚠️ Affiliate disclosure: as an Amazon Associate, we earn a small commission on qualifying
          purchases. This never affects our recommendations.
        </div>
      </div>

      <div className="cat-bar">
        {CATS.map(cat => (
          <button
            key={cat}
            className={`cat-btn ${activeCat === cat ? 'active' : ''}`}
            onClick={() => setActiveCat(cat)}
          >
            {cat} {cat !== "All" && `(${ARTICLES.filter(a => a.cat === cat).length})`}
          </button>
        ))}
      </div>

      <div className="stats-bar">
        <div className="stat"><div className="stat-label">Reviews</div><div className="stat-val">{filtered.length}</div></div>
        <div className="stat"><div className="stat-label">Avg score</div><div className="stat-val">{Math.round(filtered.reduce((s,a)=>s+a.score,0)/filtered.length)}%</div></div>
        <div className="stat"><div className="stat-label">Affiliate links</div><div className="stat-val">{filtered.length}</div></div>
        <div className="stat"><div className="stat-label">Your tag</div><div className="stat-val tag-status">{AMAZON_TAG === "YOUR_TAG-21" ? "⚠ Not set" : "✓ Active"}</div></div>
      </div>

      <main className="grid">
        {filtered.map(article => (
          <article key={article.id} className="card">
            <div
              className="card-img"
              style={{ backgroundImage: `url(${article.img})` }}
            >
              <span
                className="cat-badge"
                style={{ background: CAT_COLORS[article.cat] + '22', color: CAT_COLORS[article.cat], borderColor: CAT_COLORS[article.cat] + '44' }}
              >
                {article.tag}
              </span>
              <span className="score-badge">★ {article.score}</span>
            </div>
            <div className="card-body">
              <h2 className="card-title">{article.title}</h2>
              <p className="card-desc">{article.desc}</p>
              <div className="card-meta">
                <span>{article.readTime} min read</span>
                <span>·</span>
                <span>{article.cat}</span>
              </div>
            </div>
            <div className="card-footer">
              <a
                href={amazonLink(article.keyword)}
                target="_blank"
                rel="noopener noreferrer nofollow"
                className="btn-amazon"
              >
                View on Amazon ↗
              </a>
            </div>
          </article>
        ))}
      </main>

      <footer className="footer">
        <p>© 2026 SmartPick Reviews · Independent recommendations</p>
        <p>
          Affiliate links go to Amazon India (amazon.in). Replace <code>YOUR_TAG-21</code> in{' '}
          <code>src/App.jsx</code> with your real Associates tag before going live.
        </p>
      </footer>
    </div>
  )
}
