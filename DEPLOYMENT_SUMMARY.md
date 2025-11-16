# Your Defence Intelligence Monitor - Deployment Summary

## 📦 What I've Built For You

A fully automated defence & security news monitoring system that:
- Scans 13 RSS feeds daily
- Filters using 135 keywords tailored to your market intelligence needs
- Sends you ONLY new articles (delta tracking)
- Delivers a professional HTML email digest
- Runs 100% free on GitHub Actions

## 📊 System Specifications

**Coverage:**
- 13 RSS feeds across publications, government sources, and international bodies
- 135 keywords including CACI-specific, procurement, emerging tech, and geopolitics
- Monitors every day at 06:00 UTC (7am UK in winter)

**CACI-Specific Monitoring:**
- 13 CACI-focused keywords including: contracts, wins, frameworks, acquisitions, partnerships
- Tracks "awarded to CACI", "CACI data platform", "CACI analytics solution"

**Keyword Categories:**
- Technologies (11): ISR, EW, CEMA, DTW, drones, PNT, digital twins, quantum
- AI & Data (34): Data platforms, analytics, fusion, AI/ML, battlefield data
- Cyber & Security (10): Cyber security, resilience, secure by design, data sovereignty
- Procurement (16): Frameworks, tenders, G-Cloud, DSP, MOD D2N2, contract awards
- Prime Contractors (6): BAE, QinetiQ, Leonardo, Thales, Raytheon, Babcock
- Tech Companies (6): Palantir, Anduril, CGI, Leidos, Serco, KBR
- Plus: Cloud providers, policy signals, geopolitical indicators, international partnerships

## 📁 Files Created (Download All)

1. **defence_news_monitor.py** - Main Python script (401 lines)
2. **requirements.txt** - Python dependencies
3. **.github/workflows/daily_digest.yml** - GitHub Actions automation
4. **README.md** - Complete documentation
5. **SETUP_CHECKLIST.md** - Quick reference for setup
6. **latest_digest.html** - Sample email output (preview)

## 🚀 Deployment Steps

### 1. Create GitHub Repository (5 mins)
- Go to github.com/new
- Name: `defence-news-monitor`
- Privacy: Private (recommended)
- Upload the 3 core files

### 2. Get Gmail App Password (5 mins)
- myaccount.google.com → Security
- Enable 2-Step Verification
- Create App Password for "Mail"
- Copy 16-character password

### 3. Add GitHub Secrets (5 mins)
- Repository → Settings → Secrets → Actions
- Add 5 secrets:
  - SENDER_EMAIL (your Gmail)
  - SENDER_PASSWORD (app password from step 2)
  - RECIPIENT_EMAIL (where you want digests)
  - SMTP_SERVER (smtp.gmail.com)
  - SMTP_PORT (587)

### 4. Enable & Test (5 mins)
- Actions tab → Enable workflows
- Run workflow manually
- Check email inbox (and spam)

**Total setup time: ~20 minutes**

## 📧 What You'll Receive

Daily email showing:
- Article count and source breakdown
- Grouped by publication
- Each article shows: title, link, date, summary, matched keywords
- Professional HTML formatting

**Example digest structure:**
```
Defence & Security Intelligence Digest
16 November 2025

5 new articles across 3 sources

US DoD Contracts (2)
├─ "CACI Awarded $47M Electronic Warfare Contract"
│  Matched: CACI, electronic warfare, contract award
└─ "Palantir Wins AI Platform Framework"
   Matched: Palantir, AI, framework awards

Defense News (2)
├─ "UK MoD Launches Digital Twin Programme"
│  Matched: MoD, digital twin, defence digital transformation
└─ "NATO Strengthens Cyber Posture"
   Matched: NATO, cyber security, cyber resilience

Breaking Defense (1)
└─ "AUKUS Partners Announce Quantum Initiative"
   Matched: AUKUS, quantum, defence innovation
```

## 🎯 RSS Feeds Monitored

**Defence Publications:**
1. Defense News
2. Breaking Defense
3. C4ISRNET
4. The War Zone

**Think Tanks:**
5. RUSI
6. IISS

**UK Government:**
7. Gov.uk Ministry of Defence
8. Gov.uk Home Office
9. Gov.uk Strategic Command
10. Gov.uk General News (defence-filtered)

**US Government:**
11. US Department of Defense (News)
12. US Department of Defense (Contracts) ← Key for CACI wins

**International:**
13. NATO

## 🔧 Easy Customization

**Add more sources:**
Edit RSS_FEEDS dictionary (line ~20)

**Add/remove keywords:**
Edit KEYWORDS list (line ~37)

**Change schedule:**
Edit .github/workflows/daily_digest.yml (line 5)
- Current: 06:00 UTC daily
- For 09:00 Mon-Fri: `'0 9 * * 1-5'`
- For every 6 hours: `'0 */6 * * *'`

**Add recipients:**
Can modify script to send to multiple emails

## 💡 Why This Approach?

**vs. Manual RSS Reader (Feedly):**
- ✅ Automated filtering by keywords
- ✅ Email delivery (no app needed)
- ✅ Delta tracking (only new items)
- ✅ Customizable output format

**vs. Google Alerts:**
- ✅ More reliable RSS feeds
- ✅ Better control over sources
- ✅ Professional formatting
- ✅ No Google rate limits

**vs. Paid Services:**
- ✅ 100% free
- ✅ Full control over data
- ✅ Customizable to your exact needs
- ✅ No vendor lock-in

## ⚠️ Important Notes

**Database Persistence:**
- First run: Creates database, shows no articles
- Second run onwards: Only NEW articles (delta)
- Database stored in GitHub repo
- To reset: Delete defence_news.db file

**Email Limitations:**
- Gmail: 500 emails/day (plenty for daily digest)
- If you need more recipients, consider Slack integration

**RSS Feed Reliability:**
- Some sources may change feed URLs
- Script includes error handling
- Check GitHub Actions logs if issues

**Keywords:**
- Case-insensitive matching
- Word boundary detection (won't match "CACI" in "acacia")
- Shows up to 5 matched keywords per article

## 🎓 How It Works

```
06:00 UTC Daily
    ↓
GitHub Actions Triggers
    ↓
Python Script Runs:
1. Fetch all 13 RSS feeds
2. Parse articles
3. Check against 135 keywords
4. Query SQLite for unseen articles
5. Generate HTML digest
6. Send via Gmail SMTP
7. Mark articles as seen
8. Commit database to repo
    ↓
Email Arrives in Inbox
```

## 📈 Next Steps After Deployment

**Week 1:**
- Monitor email delivery
- Check if keyword matches are relevant
- Adjust keywords as needed

**Week 2:**
- Review coverage - are you missing sources?
- Consider adding industry-specific RSS feeds
- Fine-tune keywords (add/remove based on relevance)

**Month 1:**
- Evaluate article volume
- Consider schedule adjustments
- Share with team if valuable

**Future Enhancements:**
- Export to Google Sheets for trend analysis
- Slack integration for team sharing
- Add web scraping for non-RSS sources (LinkedIn, Defence IQ)
- Sentiment analysis on CACI mentions
- Automated keyword extraction from new articles

## 🆘 Support Resources

**If things go wrong:**
1. Check README.md troubleshooting section
2. View GitHub Actions logs (Actions tab)
3. Test email credentials locally
4. Verify all 5 secrets are set correctly

**Useful links:**
- Cron schedule generator: https://crontab.guru/
- Gmail app passwords: https://support.google.com/accounts/answer/185833
- GitHub Actions docs: https://docs.github.com/en/actions

## ✅ Success Checklist

After deployment, you should have:
- [ ] Daily emails at 06:00 UTC
- [ ] CACI-specific articles highlighted
- [ ] Procurement and framework news
- [ ] Emerging tech intelligence (AI, cyber, digital twins)
- [ ] Geopolitical signals (Ukraine, China, Indo-Pacific)
- [ ] Competitor activity (Palantir, Anduril, primes)
- [ ] Zero ongoing costs
- [ ] Full control over your intelligence gathering

---

## Ready to Deploy?

1. Download all files from this chat
2. Follow SETUP_CHECKLIST.md
3. First email arrives tomorrow at 06:00 UTC
4. Refine keywords based on results

**Questions?** Everything is documented in README.md

**Working well?** Consider expanding to web scraping for LinkedIn and other non-RSS sources.

Good luck with your market intelligence gathering! 🎯
