# Freelance Proposal Auto-Drafter

Generates a tailored freelance proposal from a job description, using one of
your skill-specific profiles. You review and send the proposal yourself —
this tool does not auto-apply to anything or touch any platform.

## Setup (one-time)

1. Install dependencies:
   ```
   pip install -r requirements.txt --break-system-packages
   ```
   (drop `--break-system-packages` if you're using a virtualenv)

2. Copy `.env.example` to `.env` and paste in your real OpenAI API key:
   ```
   cp .env.example .env
   ```
   Then edit `.env` and replace `your_key_here` with your actual key from
   https://platform.openai.com/api-keys

3. Fill in your real details in each file under `profiles/`:
   - `profiles/coding.json`
   - `profiles/writing.json`
   - `profiles/design.json`
   - `profiles/data_va.json`

   Every field marked `FILL_IN` needs your real info: your name (or the name
   that account operates under), title, years of experience, actual skills,
   your real hourly rate, and `platform_account` (just a note to yourself —
   e.g. "Upwork: yourname_dev" — so you remember which account this profile
   is for). `portfolio_links` is an empty list right now; add links as you
   build up a portfolio — you don't need any to start.

   You only need to fill in the profiles for skill areas you're actually
   pursuing right now. Leave the others as-is until you're ready to use them
   — the tool will just flag them as needing setup.

## Running it

```
python3 main.py
```

It will:
1. Ask which profile/account this proposal is for.
2. Ask you to paste the job description (press Enter twice when done).
3. Generate a tailored proposal you can copy and paste into Upwork/Fiverr/etc.

## What this tool does NOT do

- It does not auto-apply to jobs or submit anything on your behalf.
- It does not create or manage platform accounts.
- It does not guarantee you'll be hired — it drafts a starting point you
  should review, fact-check, and personalize further before sending.
- It does not track applications or earnings (that's on you, for now).

## Cost

Each proposal costs a small fraction of a cent in OpenAI API usage
(gpt-4o-mini is the default model). You pay OpenAI directly for API usage —
there's no subscription on top of that from this tool.
