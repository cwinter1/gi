# Personal Finance Dashboard — Methodology & Architecture

A fully offline personal finance dashboard built as 3 standalone HTML files. No server, no login, no internet required to view — all data is hardcoded in the files.

---

## The 3 Files

| File | Purpose |
|------|--------|
| `index.html` | Main dashboard: monthly trend charts, income vs. expenses, waterfall, donut, habits, milestones |
| `budget.html` | Detailed budget: accordion sections per category, line-bar progress bars, utility verification |
| `overdraft.html` | Debt exit plan: trajectory charts, savings milestones, action items |

All files are in Hebrew (RTL), dark-themed, mobile-friendly, and self-contained.

---

## Tech Stack

- **Plain HTML + CSS + JS** — zero build tools, zero dependencies except Chart.js
- **Chart.js 4.4.1** via cdnjs CDN (bar, line, doughnut, horizontal bar)
- **Fonts** via Google Fonts: Bebas Neue (headings), IBM Plex Mono (numbers), Space Grotesk (body)
- **RTL layout**: `dir="rtl"` on `<html>`, `direction:rtl` in CSS
- **Offline fallback**: `typeof Chart === 'undefined'` check replaces blank canvases with a Hebrew message when offline

---

## Design System

Derived from the cwinter1.github.io design language:

```css
:root {
  --bg: #0a0a0a;       /* page background */
  --s: #1a1a1a;        /* card surface */
  --el: #242424;       /* elevated element */
  --ac: #ff6b35;       /* accent orange */
  --ac2: #f7931e;      /* accent amber */
  --g: #4ade80;        /* green (positive) */
  --r: #f87171;        /* red (negative) */
  --blue: #60a5fa;     /* info/loan */
  --purple: #a78bfa;   /* investment */
  --text: #f5f5f5;     /* body text */
  --muted: #999;       /* secondary text */
  --border: #333;      /* dividers */
  --radius: 12px;
}
```

Key layout rules:
- `max-width: 840px` on `<main>` — keeps it readable
- Nav active state: `border-bottom: 2px solid var(--ac)` (no background)
- Hero: `radial-gradient(ellipse at top left, rgba(74,222,128,.05) 0%, transparent 60%)`
- Chart defaults: `color: '#999'`, `borderColor: '#333'`

---

## Category Tree

### Food (מזון)
- Supermarket: Shufersal, Rami Levy, Victory, Osher Ad, Yochananof
- Restaurants & Takeout: sit-down, pizza, Wolt/Ten Bis, coffee
- Fresh market / specialty (butcher, fish)

### Housing (דיור)
- Arnona (municipal property tax, billed bi-monthly in 6 installments)
- Va'ad Bayit (building committee, monthly direct debit)
- Electricity (bi-monthly, IEC or Ogen)
- Gas (cylinder replacement, irregular)
- Water (bi-monthly, municipality)
- Internet, Cable/HOT/YES
- Renters insurance (annual, sometimes installments)
- Repairs / maintenance (irregular)

### Transport (תחבורה)
- Fuel: 3–5 fill-ups per month typical; stations: Paz, Sonol, Delek, Ten, Yellow
- Car insurance (annual, sometimes installments)
- Car inspection (annual)
- Parking (Pango, Cellopark, municipal)
- Public transport (Rav-Kav)
- Car maintenance (irregular)

### Health (בריאות)
- Health fund (קופת חולים, salary deduction)
- Pharmacy (vitamins vs. prescriptions — different subcategories)
- Dental, optician (irregular)
- Gym / sports (monthly membership)
- Therapy / mental health

### Kids (ילדים)
- Daycare / kindergarten (monthly bank standing order)
- School fees (annual, installments)
- School supplies (back-to-school spike Aug/Sep)
- After-school activities / חוגים (monthly per child)
- Clothing (seasonal spikes before Rosh Hashana)
- Tutoring (if ongoing, monthly)
- Bat/Bar Mitzvah savings (tracked as separate savings goal)
- Summer camp (קייטנה, lump sum or installments)

### Entertainment & Subscriptions (בידור)
- Streaming: Netflix, Spotify, Apple, Google
- Cinema, theater, books
- Gifts (seasonal: Hanukkah, Passover, birthdays)
- Vacation / travel (large, plan separately)

### Financial (פיננסי)
- Bank fees (monthly)
- Loan repayment (fixed monthly installment)
- Overdraft interest (monthly, check bank statement)
- Insurance policies (life, disability, critical illness)
- Pension / provident fund (salary deduction)

### Irregular / One-time
- Holiday shopping, appliances, medical, legal, moving

---

## Data Source: Israeli Credit Card PDFs

### Amex PDF Structure
- Each transaction: `[date] | [merchant name] | [NIS amount]`
- Foreign charges: show original currency + NIS total — use the NIS total
- Installments: `תשלום X מתוך Y` — record only the monthly installment, not the full amount
- Fuel vs. food: merchant code disambiguates (e.g., fuel station shop ≠ fuel fill-up)
- SuperPharm = Health (pharmacy), not Supermarket

### CAL PDF Structure
- Similar layout to Amex
- More recurring subscription charges (Netflix, Spotify, Apple, Google)
- Watch for `נדחו לחיוב הבא` (deferred charges) — avoid double-counting
- Wolt / Ten Bis charges: Food > Restaurants
- PayBox / Bit transfers: check description (may be rent split or personal payment)

### Installment Tracking
Maintain a running table of active installment plans:
```
Item | Monthly Amount | Remaining Months | Card | Start Date
```
Decrement remaining months by 1 each month. Remove when reaching 0.

### Parsing Hebrew PDFs in Python
```python
from pdfminer.high_level import extract_text
text = extract_text('statement.pdf')  # handles Hebrew RTL correctly
```
- Always use `encoding='utf-8'` when writing output files
- Numbers are LTR even in Hebrew PDFs
- Merchant names may be Latin-transliterated (e.g., `SUPER-PHARM`)

---

## Israeli Utility Billing Patterns

| Utility | Billing Cycle | Notes |
|---------|--------------|-------|
| Electricity | Bi-monthly | Summer bills significantly higher (A/C); 3-tier pricing |
| Water | Bi-monthly | Includes sewage (ביוב); tiered pricing |
| Arnona | Bi-monthly (6 payments) | Annual tax split into 6 installments; discounts for eligible families |
| Va'ad Bayit | Monthly | Fixed direct debit; set by building committee vote |
| Gas (cylinder) | Irregular | ~1 cylinder per 2–4 months; more in winter |
| Internet | Monthly | Via credit card or direct debit |

---

## UI Components

### Chart.js Setup
```js
// Always check before initializing — enables offline use
if (typeof Chart === 'undefined') {
  document.querySelectorAll('.chart-wrap').forEach(el => {
    el.innerHTML = '<span style="color:#555">גרף לא זמין — נדרש חיבור לאינטרנט</span>';
  });
} else {
  Chart.defaults.color = '#999';
  Chart.defaults.borderColor = '#333';
  // chart initializations here...
}
```
- Chart containers need explicit height (e.g., `height:240px`) — Chart.js ignores implicit height
- Always set `responsive: true, maintainAspectRatio: false`

### Accordion
```html
<div class="acc-item">
  <button onclick="toggle(this)">Section Title</button>
  <div class="acc-body">Content here</div>
</div>
```
```css
.acc-body { display: none; }
.acc-item.open .acc-body { display: block; }
```
```js
// Must be defined BEFORE the Chart.js check block
function toggle(btn) { btn.parentElement.classList.toggle('open'); }
```

### Progress Bars
```html
<div class="prog-bar"><div class="prog-fill" style="width:73%"></div></div>
```
```css
.prog-bar { background:#333; border-radius:4px; height:6px; overflow:hidden; }
.prog-fill { height:100%; border-radius:4px; transition:width .3s ease; }
```
For compact line items, use `height:3px`.

---

## Data Schema (embedded in HTML)

Data lives directly in `<script>` blocks inside each HTML file. Approximate structure:

```js
const months = ['ינואר', 'פברואר', ...];  // array of month labels
const income = [/* monthly net income */];
const expenses = [/* monthly total expenses */];
const savings = [/* income - expenses per month */];

// Expense breakdown by category (current month)
const categories = {
  food: 0,
  housing: 0,
  transport: 0,
  health: 0,
  kids: 0,
  subscriptions: 0,
};

// Budget line items (per section)
const budgetItems = [
  { name: 'Item name (Hebrew)', spent: 0, budget: 0, frequency: 'monthly' },
  // ...
];
```

---

## Monthly Update Process

1. Download Amex PDF + CAL PDF + bank statement
2. Parse each PDF — extract and categorize all transactions
3. Update `index.html` — append new month to arrays, update KPI cards
4. Update `budget.html` — update each line item's `spent` value
5. Update `overdraft.html` — update balance, savings progress percentages
6. Open all 3 files in browser and verify visually
7. Upload updated files to Google Drive `analysis/` folder
8. Archive raw PDFs to a monthly subfolder in Drive

---

## Lessons Learned / Gotchas

### Google Drive MCP
- `create_file` only creates NEW files — there is no update or overwrite
- No `delete_file`, no `move_file` available via MCP
- Every "update" creates a duplicate — track the latest file ID per name
- Use `disableConversionToGoogleType: true` for HTML files to prevent Drive converting them to Google Docs
- Folder creation: set `contentMimeType` to `application/vnd.google-apps.folder`

### Chart.js
- Version 4.x changed plugin registration (no `Chart.plugins.register` — use `plugins:{}` in config)
- Combo bar+line chart: use `type:'bar'` on the Chart, add a dataset with `type:'line'`
- RTL doesn't affect chart rendering — axis text stays LTR, which is fine for numbers

### Hebrew / RTL
- `dir="rtl"` on `<html>` flips all layout including flex direction
- Google Fonts: load Bebas Neue, IBM Plex Mono, Space Grotesk with `display=swap`
- `toLocaleString('he-IL')` formats numbers with commas for Israeli locale

### PDF Parsing
- Use `pdfminer.six` for Hebrew — handles RTL text extraction best
- Always specify `encoding='utf-8'` in Python file operations
- On Israeli Windows: default encoding is cp1255 — `open(f, encoding='utf-8')` is mandatory
- Avoid Unicode arrows/symbols in `print()` on Windows — use `->` instead of `→`

### GitHub Pages / CDN
- GitHub Pages URLs may be blocked by cloud egress proxies
- `raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}` usually works even when Pages is blocked
- CDN fallbacks are essential for static offline-first dashboards
