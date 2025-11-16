# Defence & Security News Monitor

Automated RSS aggregator for defence and security market intelligence. Monitors 13+ news sources, filters by 120+ keywords (ISR, CACI, procurement, AI, cyber, etc.), tracks deltas (only new articles), and sends daily email digests.

## 🎯 What This Does

- ✅ Monitors Defense News, Breaking Defense, C4ISRNET, War Zone, RUSI, IISS, Gov.uk, US DoD, NATO
- 🔍 Filters for CACI-specific news, procurement, emerging tech, geopolitical signals
- 📧 Daily email digest at 06:00 UTC
- 💾 SQLite database tracks what you've seen (delta only)
- 🤖 Runs automatically on GitHub Actions (100% free)
- 🎨 Professional HTML email with matched keywords highlighted

## 📋 Monitored Sources (13 feeds)

**Publications:**
- Defense News, Breaking Defense, C4ISRNET, The War Zone
- RUSI, IISS

**Government:**
- Gov.uk MOD, Home Office, UK Strategic Command
- US Department of Defense (News + Contracts feed)
- NATO

## 🔍 Keyword Coverage (120+ terms)

**CACI Specific:**
- CACI contracts, wins, frameworks, acquisitions, partnerships

**Technologies:**
- ISR, Electronic Warfare, CEMA, DTW, Cyber, AI/ML
- Data platforms, analytics, fusion, integration
- Digital twins, quantum, edge computing

**Procurement:**
- Framework awards, G-Cloud, DSP, MOD D2N2
- Contract awards, tenders, procurement reform

**Companies:**
- Primes: BAE Systems, QinetiQ, Leonardo, Thales, Raytheon, Babcock
- Tech: Palantir, Anduril, CGI, Leidos, Serco
- Cloud: AWS Defence, Microsoft Defence, Google Cloud

**Strategy & Policy:**
- MoD/NATO data strategies, AI regulation, AUKUS
- Defence budgets, Integrated Review, sovereign capability

**Geopolitical:**
- Ukraine, China, Russia, Indo-Pacific, semiconductors

[Full keyword list in script]

---

## 🚀 Quick Setup (20 minutes)

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Name it: `defence-news-monitor` (or your choice)
3. Set to **Private** (recommended for business intelligence)
4. **Do NOT** initialize with README (we have files)
5. Click "Create repository"

### Step 2: Upload Your Files

**Option A - Web Upload (Easiest):**
1. Download the 3 files I've created
2. On your new GitHub repo page, click "uploading an existing file"
3. Drag and drop:
   - `defence_news_monitor.py`
   - `requirements.txt`
   - `.github/workflows/daily_digest.yml`
4. Commit files

**Option B - Git Command Line:**
```bash
git clone https://github.com/YOUR-USERNAME/defence-news-monitor.git
cd defence-news-monitor

# Copy the files I created into this directory
# Then:
git add .
git commit -m "Initial commit"
git push
```

### Step 3: Set Up Email (Gmail)

1. Go to https://myaccount.google.com/
2. Security → 2-Step Verification (enable if not already)
3. Security → App passwords
4. Select app: **Mail**, device: **Other (Custom)**
5. Name it "Defence News Monitor"
6. Click **Generate**
7. **Copy the 16-character password** (e.g., `abcd efgh ijkl mnop`)

### Step 4: Configure GitHub Secrets

1. Go to your repository
2. Settings → Secrets and variables → Actions
3. Click **New repository secret**
4. Add these **5 secrets** one by one:

| Secret Name | Value | Example |
|------------|-------|---------|
| `SENDER_EMAIL` | Your Gmail address | `marie.example@gmail.com` |
| `SENDER_PASSWORD` | App password from Step 3 | `abcdefghijklmnop` |
| `RECIPIENT_EMAIL` | Where to send digest | `marie.work@email.com` |
| `SMTP_SERVER` | Gmail SMTP | `smtp.gmail.com` |
| `SMTP_PORT` | Port number | `587` |

**Important:** 
- Use the **app password**, NOT your regular Gmail password
- No spaces in SENDER_PASSWORD (remove spaces from the app password)

### Step 5: Enable GitHub Actions

1. Go to **Actions** tab in your repo
2. Click "I understand my workflows, go ahead and enable them"
3. Done! It will run daily at 06:00 UTC

### Step 6: Test It Now (Optional)

1. Actions tab → "Daily Defence News Digest"
2. Click **Run workflow** → **Run workflow**
3. Wait ~2 minutes
4. Check your email inbox

---

## 📧 What You'll Receive

Daily email digest showing:
- **Header:** Date and total article count
- **Grouped by source:** Articles organized by publication
- **Each article:**
  - Clickable title linking to full article
  - Publication date
  - Summary excerpt (first 300 chars)
  - Matched keywords (shows which terms triggered the match)

**Example:**
```
Defence & Security Intelligence Digest
16 November 2025

3 new articles across 2 sources

Defense News (2)
├─ "CACI Wins $47M Electronic Warfare Contract"
│  Published: 15 Nov 2025
│  Summary: CACI International has been awarded...
│  Matched: CACI, electronic warfare, contract award
│
└─ "UK MoD Launches Digital Twin Programme"
   Published: 15 Nov 2025
   Summary: The Ministry of Defence announced...
   Matched: MoD, digital twin, defence digital transformation

NATO (1)
└─ "Alliance Strengthens Cyber Defence Posture"
   ...
```

---

## ⚙️ Customization

### Change Email Schedule

Edit `.github/workflows/daily_digest.yml`:

```yaml
schedule:
  - cron: '0 6 * * *'  # Currently 06:00 UTC daily
```

**Common schedules:**
- `'0 9 * * *'` = 09:00 UTC daily
- `'0 6 * * 1-5'` = 06:00 UTC Mon-Fri only
- `'0 */6 * * *'` = Every 6 hours
- `'0 6,18 * * *'` = 06:00 and 18:00 UTC

Use https://crontab.guru/ to create custom schedules.

### Add More RSS Feeds

Edit `defence_news_monitor.py`, find `RSS_FEEDS` dictionary (~line 20):

```python
RSS_FEEDS = {
    "Source Name": "https://example.com/rss",
    "Janes": "https://janes.com/rss",  # Add like this
}
```

### Add/Remove Keywords

Edit `KEYWORDS` list (~line 37):

```python
KEYWORDS = [
    "your new keyword",
    "another term",
]
```

### Change Email Recipient

Update the `RECIPIENT_EMAIL` secret in GitHub Settings

---

## 🔧 Troubleshooting

### No email received?

1. **Check GitHub Actions logs:**
   - Actions tab → Latest run → Check for errors
   
2. **Verify secrets:**
   - Settings → Secrets → Ensure all 5 are set correctly
   - SENDER_PASSWORD must be app password (16 chars, no spaces)
   
3. **Check spam folder**

4. **Test credentials locally:**
   ```python
   import smtplib
   server = smtplib.SMTP('smtp.gmail.com', 587)
   server.starttls()
   server.login('your@gmail.com', 'your-app-password')
   print("Success!")
   ```

### Getting "0 new articles" every day?

The first run creates the database. All subsequent runs only show **new** articles (delta).

**To reset and see all articles again:**
- Delete `defence_news.db` from your repository
- Next run will show everything

### Want to run manually?

```bash
# Clone your repo
git clone https://github.com/YOUR-USERNAME/defence-news-monitor.git
cd defence-news-monitor

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SENDER_EMAIL="your@gmail.com"
export SENDER_PASSWORD="your-app-password"
export RECIPIENT_EMAIL="recipient@email.com"

# Run
python defence_news_monitor.py
```

### Database not updating?

GitHub Actions automatically commits the database back to the repo.

**Check:**
- Repository Settings → Actions → General
- Workflow permissions = "Read and write permissions"

---

## 💰 Cost

**100% FREE** 

- GitHub Actions: 2,000 minutes/month free tier
- This uses ~5 minutes/month
- No credit card required

---

## 🔐 Security Notes

1. **Keep repository private** - contains market intelligence
2. **Never commit secrets** - always use GitHub Secrets
3. **App passwords only** - never use your main Gmail password
4. **Revoke app passwords** if you suspect compromise

---

## 📊 Advanced Features

### Multiple Recipients

To send to multiple people, edit the script:

```python
recipients = [
    "person1@email.com",
    "person2@email.com"
]

for recipient in recipients:
    send_email_digest(html_digest, recipient)
```

### Export to Google Sheets

Install `gspread` and modify the script to write to Sheets instead of/in addition to email.

### Slack Integration

Replace email function with Slack webhook for team channels.

### Add Web Scraping (for non-RSS sources)

For sites without RSS (like LinkedIn):
```python
from bs4 import BeautifulSoup
import requests

# Add scraping logic for specific pages
```

---

## 📞 Support

**RSS Feed Issues:**
- Check if feed URL still works: paste into browser
- Many defense sites change their RSS URLs

**Email Issues:**
- Gmail app passwords documentation: https://support.google.com/accounts/answer/185833
- For Outlook/other: update SMTP_SERVER and SMTP_PORT secrets

**GitHub Actions Issues:**
- https://docs.github.com/en/actions

---

## 🎓 How It Works

1. **Daily trigger:** GitHub Actions runs at 06:00 UTC
2. **Fetch feeds:** Python pulls all RSS feeds
3. **Filter:** Checks each article against 120+ keywords
4. **Delta check:** SQLite database tracks seen articles
5. **Generate:** Creates HTML digest of NEW matches only
6. **Send:** SMTP email with digest
7. **Persist:** Commits database back to GitHub

---

## ✅ Next Steps

1. ✓ Create GitHub repository
2. ✓ Upload files
3. ✓ Set up Gmail app password
4. ✓ Add 5 GitHub secrets
5. ✓ Enable Actions
6. ✓ Test manually
7. ✓ Wait for tomorrow's 06:00 UTC run
8. ✓ Check your inbox!

---

**Questions?** Check the troubleshooting section or GitHub Actions logs.

**Working well?** Consider adding more RSS feeds specific to your market.
