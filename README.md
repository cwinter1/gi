# gi

Two things live in this repo:

1. **Flask app** — image analysis tool (`app.py`, served via Railway)
2. **Finance dashboard** — encrypted family budget, served via GitHub Pages (`gh-pages` branch)

---

## Finance Dashboard

**URL:** `https://cwinter1.github.io/gi/`

Three pages, all AES-256-GCM encrypted in the browser (Web Crypto API, PBKDF2 key derivation). No server needed — static HTML only.

| Page | Description |
|---|---|
| `index.html` | Main dashboard — KPIs, monthly chart, income sources, upcoming events |
| `budget.html` | Full budget accordion — all categories with line items |
| `overdraft.html` | Overdraft exit plan (pending update) |

### Monthly budget (July 2026)

| קטגוריה | ₪/חודש |
|---|---|
| הכנסה (כריס + קטיה + קצבה) | 31,437 |
| משכנתא + הלוואות | 8,299 |
| קבועים | 3,812 |
| ילדים | 2,885 |
| משתנה | 8,542 |
| חיסכון | 6,857 |
| **עודף → למינוס** | **1,042** |

### Savings (חיסכון ₪6,857)

| | ₪/חודש |
|---|---|
| תאילנד 2027 (₪40,000 ÷ 14 mo) | 2,857 |
| פנסיה תגמולים | 3,000 |
| חירום בל"מ | 1,000 |

### Kids (ילדים ₪3,233) — annual costs spread ÷12

| | ₪/חודש |
|---|---|
| בלט, צהרון, 5 Fingers, תפירה, צופים, בית ספר | 2,083 |
| קמפינג שנתי אמה+מאיה (₪1,200÷12) | 100 |
| גלישה קיץ 3 ילדים (₪6,600÷12) | 550 |
| יום הולדת 3 ילדות (₪6,000÷12) | 500 |

### Overdraft

₪64,000 at 7.25% — no loan plan. Reducing from ₪694/month surplus. Interest cost ₪387/month included in משכנתא line.

---

## Flask App

Login required (Railway env: `SITE_USERNAME`, `SITE_PASSWORD`). Finance routes are public (no `@require_login`).

Routes: `/` (image upload), `/analyse` (POST → Anthropic API), `/finance/` `/finance/budget.html` `/finance/overdraft.html`

Railway env vars: `FLASK_SECRET_KEY`, `SITE_USERNAME`, `SITE_PASSWORD`, `ANTHROPIC_API_KEY`

---

## Encryption workflow

Source files live at `/home/user/finance/` (not committed to main branch).

```
# Initial encrypt
node /home/user/finance/encrypt.js "<main-pw>" "<recovery-pw>"

# Update data (decrypt → patch → re-encrypt)
node /home/user/finance/update.js "<main-pw>" "<recovery-pw>"

# After any change:
cp /home/user/finance/*.html /home/user/gi/templates/finance/   # Flask
git checkout gh-pages && cp ... && git push                      # GitHub Pages
```
