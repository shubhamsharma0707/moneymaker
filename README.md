# MoneyMaker AI Suite 🚀

Welcome to the **MoneyMaker AI Suite**! This repository contains a collection of 5 legitimate, AI-powered software projects designed for monetization, passive income, and workflow automation. 

It also contains the original `money_maker` core framework, an autonomous AI agent simulation framework.

## 📂 Projects Overview

### 1. ResumeAI Pro (`/resume_ai`)
A premium SaaS web application built with React and Vite. Users input their current resume and a target job description, and the AI generates a tailored cover letter and resume improvements to bypass Applicant Tracking Systems (ATS).
- **Monetization**: Charge a monthly subscription (e.g., $9/mo) via Stripe for unlimited AI optimizations.
- **Run**: `cd resume_ai && npm install && npm run dev`

### 2. Premium AI Telegram Bot (`/telegram_ai_bot`)
An asynchronous Python-based Telegram bot (`python-telegram-bot`) that brings our AI Engine directly to users' phones.
- **Monetization**: Built-in mock credit system. Users get 3 free messages before hitting a paywall, prompting them to purchase a premium subscription via a `/buy` command.
- **Run**: Add your token to `.env` and run `python3 telegram_ai_bot/main.py`

### 3. Summarizer Pro Chrome Extension (`/chrome_ai_extension`)
A Manifest V3 compliant Chrome Web Extension that reads long web pages and generates instant, smart summaries in a beautiful glassmorphic popup.
- **Monetization**: Publish to the Chrome Web Store and offer in-app upgrades.
- **Run**: Go to `chrome://extensions/` in Google Chrome, turn on Developer Mode, and click "Load unpacked" to select the `chrome_ai_extension` folder.

### 4. Freelance Proposal Auto-Drafter (`/freelance_automator`)
A Python CLI tool designed to help *you* win more freelance gigs. It reads a local `profile.json` (containing your actual skills and portfolio) and drafts highly personalized, professional proposals for Upwork or Fiverr jobs in seconds.
- **Monetization**: Saves you hours of unbillable time writing proposals, increasing your job win rate.
- **Run**: Edit `profile.json`, then run `python3 freelance_automator/main.py`

### 5. TechTrove Affiliate Site (`/affiliate_blog`)
A high-end, responsive React blog optimized for tech and AI gear reviews. Features a magazine-style CSS Grid layout with built-in dark mode and high-converting affiliate buttons.
- **Monetization**: Amazon Associates or other affiliate programs. Add real tracking URLs to the data structure to earn commissions on clicks and purchases.
- **Run**: `cd affiliate_blog && npm install && npm run dev`

### Core AI Engine (`/money_maker`)
The original autonomous agent simulation engine that orchestrates strategies (like dynamic web search and automated marketplace listings) and provides the AI brain for the other projects.
- **Run**: `python3 money_maker/main.py --target 10`

## 🛠 Prerequisites

- **Python 3.10+** (For the Core Agent, Telegram Bot, and CLI tools)
- **Node.js 18+** (For the React web apps)
- **OpenAI API Key** (or another supported LLM provider set in your `.env` file)

## 🚀 Getting Started

Ensure you have your `.env` file configured in the root directory (or respective subdirectories) with your API keys:
```env
OPENAI_API_KEY=your_key_here
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

Navigate to any of the specific project directories to begin!
