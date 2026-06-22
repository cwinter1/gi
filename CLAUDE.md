# gi repo — Claude rules

## Git workflow

- Develop on branch `claude/winter-finance-dashboard-4mp33x`
- After finance changes: commit to feature branch AND update `gh-pages` branch
- Never push to main directly

## Finance dashboard architecture

### Encryption
- Files encrypted with AES-256-GCM via Node.js `webcrypto` (encrypt.js)
- Two password envelopes: main + recovery, stored as `WF_ENC` array in each HTML file
- Payload format: `JSON.stringify({ html: mainHtml, js: initJs })`
- `mainHtml` = innerHTML of `<main>` tag
- `initJs` = last `<script>` block (data initialization only — chart engine is a separate earlier script)

### Patching encrypted files
Never edit HTML directly — always decrypt → patch → re-encrypt:
```
node /home/user/finance/fix-<name>.js "<main-pw>" "<recovery-pw>"
```
Pattern used in all fix scripts: `readFileSync` → regex extract `WF_ENC` → `decryptPayload` → patch strings → `encryptPayload` twice → splice back → `writeFileSync`

### Deploy sequence after any finance change
1. Run fix script against `/home/user/finance/`
2. `cp /home/user/finance/index.html /home/user/gi/templates/finance/`
3. `cp /home/user/finance/budget.html /home/user/gi/templates/finance/`
4. Commit to `claude/winter-finance-dashboard-4mp33x`
5. `git checkout gh-pages` → copy files → commit → push → `git checkout claude/...`

### Current budget state (July 2026)

Income: ₪31,437 (Chris ₪16,500 + Katya ₪14,500 + allowances ₪437)

Expenses ₪30,743:
- משכנתא+הלוואות ₪8,299 (includes ריבית כה"ש ₪387 instead of loan ₪875)
- קבועים ₪3,812
- ילדים ₪2,885 (base ₪1,735 + camping ₪100 + surf ₪550 + birthdays ₪500) — צהרון ₪348 removed
- משתנה ₪8,542
- חיסכון ₪6,857 (Thailand ₪2,857 + pension ₪3,000 + emergency ₪1,000)

Surplus: ₪1,042 → overdraft paydown (3.3% of income)

Overdraft: ₪64,000 at 7.25% — no loan. Paying down from surplus (~92 months).

### What was removed vs original dashboard
- הלוואת כה"ש ₪875 (planned loan) — replaced with interest ₪387
- אסיה ₪1,500 (Asia trip savings) — removed (Thailand covers trips)
- Europe ₪1,800 — replaced by Thailand ₪2,857

### Known gotchas
- `WF_ENC` regex must use `/var WF_ENC=(\[[\s\S]*?\]);/` (multiline, lazy)
- Decrypt tries both WF_ENC entries (main pw first, then recovery)
- The `js` patch target strings must match EXACTLY including whitespace/newlines
- budget.html donut uses raw ₪ amounts; index.html donut uses percentages
- After patching, always verify with `node decrypt-inspect.js` before deploying
- overdraft.html has NOT been updated yet — still shows old loan plan
