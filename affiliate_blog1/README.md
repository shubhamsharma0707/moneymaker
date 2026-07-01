# SmartPick Affiliate Blog

Multi-niche affiliate blog covering Tech, Health, Finance, and Home.
Built with React + Vite. Affiliate links go to Amazon India.

## Before you go live — CRITICAL

1. **Get your Amazon Associates tag**
   - Sign up free at https://affiliate-program.amazon.in
   - Takes ~10 minutes. You need a phone number and bank account.
   - After approval, find your "Associate ID" in the dashboard (looks like: yourname-21)

2. **Add your tag to the code**
   - Open `src/App.jsx`
   - Line 11: change `"YOUR_TAG-21"` to your real tag, e.g. `"smartpick-21"`
   - That's the only change needed — every "View on Amazon" button automatically includes it

3. **The FTC disclosure is already included**
   - It shows on every page. This is legally required in India too.
   - Do NOT remove it.

## Setup and run locally

```bash
npm install
npm run dev
```

## Build for deployment

```bash
npm run build
```
The `dist/` folder is your deployable site. Upload it to:
- **Vercel** (free): `npm i -g vercel && vercel` — easiest option
- **Netlify** (free): drag the `dist/` folder to netlify.com/drop
- **GitHub Pages**: push to a repo and enable Pages on the `dist/` folder

## Adding more articles

Open `src/App.jsx` and add an entry to the `ARTICLES` array:

```js
{
  id: 13,                          // next number
  cat: "Tech",                     // Tech | Health | Finance | Home
  tag: "Laptops",                  // shown as the badge on the card
  title: "Best laptops under ₹50,000 in 2026",
  desc: "A one or two sentence summary of the review.",
  score: 88,                       // your 0-100 recommendation score
  img: "https://...",              // Unsplash URL or your own image
  keyword: "laptop under 50000",   // what gets searched on Amazon
  readTime: 6                      // estimated read time in minutes
}
```

## How affiliate links work

Each "View on Amazon" button goes to:
`https://www.amazon.in/s?k=<search+keyword>&tag=YOUR_TAG-21`

This is a **search-based link** — it finds relevant products without you
needing individual product ASINs. Once you have real reviews live, you can
replace `keyword` with a direct ASIN link like:
`https://www.amazon.in/dp/B0XXXXXXXX?tag=your-tag-21`
Direct ASIN links earn more reliably, but search links work fine to start.

## Realistic earnings expectation

This blog earns ZERO until it has traffic.
Traffic comes from: Google (SEO), social sharing, Reddit posts, YouTube links.

A realistic timeline:
- Month 1-2: write 20+ real articles, publish, submit sitemap to Google Search Console
- Month 3-4: start seeing organic traffic if articles target low-competition keywords
- Month 6+: consistent traffic → consistent affiliate income

Amazon Associates commission rates in India: roughly 1-9% depending on category.
A visitor who buys a ₹5,000 product = ₹50-450 commission for you.
