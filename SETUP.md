# GI Food Analyser — Setup Guide

## Step 1: Get an Anthropic API Key

1. Go to https://console.anthropic.com
2. Sign in or create an account
3. Navigate to **API Keys** → **Create Key**
4. Copy the key — you'll need it in Step 3

---

## Step 2: Clone the repo locally (optional, for local testing)

```bash
git clone https://github.com/cwinter1/gi.git
cd gi
```

---

## Step 3: Set up environment variables

Copy the example file and fill it in:

```bash
cp .env.example .env
```

Edit `.env`:

```
ANTHROPIC_API_KEY=sk-ant-...        # from Step 1
FLASK_SECRET_KEY=some-long-random-string
SITE_USERNAME=admin                  # your chosen login username
SITE_PASSWORD=your-chosen-password   # your chosen login password
FLASK_ENV=development                # use 'production' on Railway
```

---

## Step 4: Run locally (optional)

```bash
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000 — log in with the username/password you set above.

---

## Step 5: Deploy to Railway

1. Go to https://railway.app and sign in
2. Click **New Project** → **Deploy from GitHub repo**
3. Select `cwinter1/gi`
4. Railway will detect `railway.toml` and build automatically
5. Once the build finishes, go to **Variables** and add:

   | Key | Value |
   |-----|-------|
   | `ANTHROPIC_API_KEY` | your key from Step 1 |
   | `FLASK_SECRET_KEY` | a long random string |
   | `SITE_USERNAME` | your chosen username |
   | `SITE_PASSWORD` | your chosen password |
   | `FLASK_ENV` | `production` |

6. Click **Deploy** (or Railway will redeploy automatically after adding variables)
7. Go to **Settings** → **Domains** → **Generate Domain** to get a public URL

---

## Step 6: Use the app

1. Open your Railway URL
2. Log in with the `SITE_USERNAME` / `SITE_PASSWORD` you set
3. Take or upload a photo of a meal
4. Click **נתח את הצלחת** — results appear in ~5–10 seconds

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ANTHROPIC_API_KEY is not configured` | Add the key in Railway Variables |
| Login fails | Double-check `SITE_USERNAME` and `SITE_PASSWORD` variables |
| App crashes on deploy | Check Railway build logs — usually a missing variable |
| Timeout on analysis | Normal for large images; Railway timeout is set to 120s |
