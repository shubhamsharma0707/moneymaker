import React from 'react'
import './index.css'

// Mock Database of Affiliate Articles
const ARTICLES = [
  {
    id: 1,
    title: "Top 5 Mechanical Keyboards for Coders in 2026",
    description: "We tested the most popular mechanical keyboards on the market. If you spend 8+ hours a day typing code, these ergonomic, tactile masterpieces will save your wrists and boost your WPM.",
    image: "https://images.unsplash.com/photo-1595225476474-87563907a212?auto=format&fit=crop&w=800&q=80",
    tag: "Hardware",
    affiliateLink: "https://amazon.com/mock-affiliate-link-1",
    featured: true
  },
  {
    id: 2,
    title: "Best Ultrawide Monitors for Productivity",
    description: "Stop alt-tabbing. An ultrawide monitor is the single biggest productivity upgrade you can make to your setup. Here are our top picks.",
    image: "https://images.unsplash.com/photo-1527443154391-507e9dc6c5cc?auto=format&fit=crop&w=800&q=80",
    tag: "Displays",
    affiliateLink: "https://amazon.com/mock-affiliate-link-2",
    featured: false
  },
  {
    id: 3,
    title: "Noise-Cancelling Headphones That Actually Work",
    description: "Open-plan offices are loud. Block out the noise and get into the flow state with these premium ANC headphones.",
    image: "https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?auto=format&fit=crop&w=800&q=80",
    tag: "Audio",
    affiliateLink: "https://amazon.com/mock-affiliate-link-3",
    featured: false
  },
  {
    id: 4,
    title: "The Ultimate Ergonomic Chair Review",
    description: "Your back will thank you. We spent 30 days testing the Herman Miller Aeron against budget alternatives.",
    image: "https://images.unsplash.com/photo-1505843490538-5133c6c7d0e1?auto=format&fit=crop&w=800&q=80",
    tag: "Office Gear",
    affiliateLink: "https://amazon.com/mock-affiliate-link-4",
    featured: false
  }
];

function App() {
  return (
    <>
      <nav className="navbar">
        <div className="logo">TechTrove</div>
        <div style={{ display: 'flex', gap: '1rem', fontWeight: 500 }}>
          <a href="#" style={{ color: 'inherit', textDecoration: 'none' }}>Reviews</a>
          <a href="#" style={{ color: 'inherit', textDecoration: 'none' }}>Guides</a>
          <a href="#" style={{ color: 'inherit', textDecoration: 'none' }}>Deals</a>
        </div>
      </nav>

      <main className="container">
        <header style={{ marginBottom: '3rem' }}>
          <h1 style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>Latest Gear Reviews</h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '1.1rem' }}>
            In-depth analysis of the best tech for developers and creators.
          </p>
        </header>

        <div className="magazine-grid">
          {ARTICLES.map((article) => (
            <article 
              key={article.id} 
              className={`article-card ${article.featured ? 'featured' : ''}`}
            >
              <div 
                className="article-img" 
                style={{ backgroundImage: `url(${article.image})` }}
              />
              <div className="article-content">
                <span className="tag">{article.tag}</span>
                <h2 className="article-title">{article.title}</h2>
                <p className="article-desc">{article.description}</p>
                <a 
                  href={article.affiliateLink} 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="btn-affiliate"
                >
                  🛒 Check Price on Amazon
                </a>
              </div>
            </article>
          ))}
        </div>
      </main>

      <footer className="footer">
        <p>© 2026 TechTrove Reviews. All rights reserved.</p>
        <p style={{ fontSize: '0.75rem', marginTop: '0.5rem' }}>
          Disclosure: As an Amazon Associate, we earn from qualifying purchases. 
          This helps support our review team at no extra cost to you.
        </p>
      </footer>
    </>
  )
}

export default App
