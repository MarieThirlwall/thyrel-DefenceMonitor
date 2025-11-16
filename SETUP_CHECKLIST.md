# Quick Setup Checklist

## Files to Upload to GitHub
- [ ] defence_news_monitor.py
- [ ] requirements.txt  
- [ ] .github/workflows/daily_digest.yml

## GitHub Secrets to Add

Go to: Repository → Settings → Secrets and variables → Actions → New repository secret

| Secret Name | Get It From | Example Value |
|------------|-------------|---------------|
| SENDER_EMAIL | Your Gmail address | marie.example@gmail.com |
| SENDER_PASSWORD | Gmail → Security → App passwords | abcdefghijklmnop |
| RECIPIENT_EMAIL | Where you want emails sent | marie.work@company.com |
| SMTP_SERVER | Fixed value for Gmail | smtp.gmail.com |
| SMTP_PORT | Fixed value for Gmail | 587 |

## Gmail App Password Steps

1. https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Click "App passwords"
4. Select: Mail + Other (Custom)
5. Name it: "Defence News"
6. Copy the 16-character password
7. Paste into SENDER_PASSWORD secret (no spaces)

## Test It

1. Go to Actions tab
2. Click "Daily Defence News Digest"
3. "Run workflow" button
4. Wait 2 minutes
5. Check your email!

## Schedule

Default: 06:00 UTC daily (7am UK winter, 6am UK summer)

To change: Edit `.github/workflows/daily_digest.yml` line 5

## Current Keyword Count: 120+

Including:
- CACI-specific: contracts, wins, frameworks, acquisitions
- Tech: ISR, EW, cyber, AI, digital twins, quantum
- Procurement: frameworks, tenders, G-Cloud, DSP
- Companies: Palantir, Anduril, BAE, QinetiQ, Thales, etc.
- Policy: AUKUS, Five Eyes, defence budgets
- Geopolitical: Ukraine, China, Russia, Indo-Pacific

## Current RSS Feeds: 13

- Defense News, Breaking Defense, C4ISRNET, War Zone
- RUSI, IISS
- Gov.uk: MOD, Home Office, Strategic Command
- US DoD: News + Contracts
- NATO

## Cost: £0

GitHub Actions free tier: 2,000 minutes/month (you'll use ~5)

---

## Common Issues

**No email?**
- Check spam folder
- Verify all 5 secrets are set
- Check Actions tab for error logs
- Ensure app password (not Gmail password)

**0 articles every day?**
- First run creates database
- Only NEW articles shown (that's the point!)
- To reset: delete defence_news.db file

**Want different time?**
- 09:00 UTC: `'0 9 * * *'`
- Mon-Fri only: `'0 6 * * 1-5'`  
- Every 6 hours: `'0 */6 * * *'`

---

Ready to deploy? See README.md for full instructions.
