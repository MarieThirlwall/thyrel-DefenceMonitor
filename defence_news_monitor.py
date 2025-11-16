#!/usr/bin/env python3
"""
Defence & Security News Aggregator
Monitors multiple RSS feeds, filters by keywords, tracks deltas, sends email digest
"""

import feedparser
import sqlite3
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import os
import re
from typing import List, Dict, Set
import time

# RSS Feed Sources
RSS_FEEDS = {
    "Defense News": "https://www.defensenews.com/arc/outboundfeeds/rss/",
    "Breaking Defense": "https://breakingdefense.com/feed/",
    "C4ISRNET": "https://www.c4isrnet.com/arc/outboundfeeds/rss/",
    "The War Zone": "https://www.thedrive.com/the-war-zone/rss",
    "RUSI": "https://rusi.org/rss.xml",
    "IISS": "https://www.iiss.org/news-insights/rss/",
    "Gov.uk MOD": "https://www.gov.uk/government/organisations/ministry-of-defence.atom",
    "Gov.uk News": "https://www.gov.uk/search/news-and-communications.atom",
    "Gov.uk Home Office": "https://www.gov.uk/government/organisations/home-office.atom",
    "UK Strategic Command": "https://www.gov.uk/government/organisations/strategic-command.atom",
    "US DoD": "https://www.defense.gov/DesktopModules/ArticleCS/RSS.ashx?ContentType=1&Site=945",
    "US DoD Contracts": "https://www.defense.gov/DesktopModules/ArticleCS/RSS.ashx?ContentType=1&Site=3",
    "NATO": "https://www.nato.int/cps/en/natohq/news.rss",
}

# Keyword filters (case-insensitive matching)
KEYWORDS = [
    # Primary keywords
    "ISR", "electronic warfare", "procurement", "Digital Targeting Web", "DTW",
    "CEMA", "Digital Secure Access", "Cyber", "Data", "Data Integration",
    "Digital Twin", "Simulation", "Synthetic data", "Drone", "PNT",
    
    # === CACI Specific ===
    "CACI", "CACI International", "CACI Ltd", "CACI UK",
    "CACI contract", "awarded to CACI", "CACI win", "CACI framework",
    "CACI acquisition", "CACI expansion", "CACI partnership",
    "CACI data platform", "CACI analytics solution",
    
    # === Data & Analytics ===
    "data analytics", "data fusion", "data management", "data integration",
    "defence data platform", "battlefield data", 
    "national security analytics", "intelligence modernisation",
    
    # === Digital Transformation ===
    "digital services", "digital transformation", "digital twins",
    "secure digital twin", "defence digital transformation",
    "MoD digital transformation", "Home Office data modernisation",
    "public sector digital", "defence digital service",
    
    # === AI & Machine Learning ===
    "AI", "artificial intelligence", "machine learning",
    "defence AI", "AI-enabled decision support", "national security AI",
    "defence AI regulation", "AI assurance", "ethical AI", "AI arms race",
    "data ethics",
    
    # === Command & Control ===
    "joint all-domain command and control", "JADC2",
    "mission systems", "command and control",
    "multi-domain operations",
    
    # === Security & Resilience ===
    "cyber security", "secure by design", "cyber resilience",
    "data sovereignty", "cyber act",
    
    # === Geospatial ===
    "geospatial data", "GIS", "mapping", "location intelligence",
    
    # === Emerging Technologies ===
    "quantum", "edge computing", "space domain awareness",
    "dual-use technology",
    
    # === Services & Capabilities ===
    "defence consulting", "systems engineering", "enterprise architecture",
    
    # === Government Organizations & Programs ===
    "NATO", "Ministry of Defence", "MoD", "Home Office",
    "UK Strategic Command", "Data Strategy for Defence",
    "NATO innovation fund", "Defence AI Centre", "DSTL",
    "Crown Commercial Service", "CCS frameworks",
    
    # === Data Strategies ===
    "MoD data strategy", "NATO data strategy",
    
    # === Procurement & Frameworks ===
    "defence procurement", "framework", "contract award", "tender",
    "defence procurement reform", "digital framework", "G-Cloud", "DSP",
    "framework awards", "Digital Outcomes", "MOD D2N2",
    "MOD contracts", "government framework award",
    
    # === International Partnerships ===
    "AUKUS", "Five Eyes", "defence tech collaboration",
    
    # === Major Defence Contractors ===
    "Palantir", "Anduril",
    "BAE Systems", "QinetiQ", "Leonardo", "Thales", "Raytheon", "Babcock",
    "CGI", "Leidos", "KBR", "Serco",
    
    # === Cloud Providers in Defence ===
    "AWS Defence", "Microsoft Defence", "Google Cloud Defence",
    
    # === Policy & Budget ===
    "defence budget", "MoD funding", "Integrated Review", "Strategic Defence Review",
    "national security legislation", "defence innovation",
    "sovereign capability", "trusted supplier", "defence supply chain",
    
    # === Geopolitical Signals ===
    "Ukraine", "Indo-Pacific", "China", "Russia", "semiconductors",
]

# Database setup
DB_PATH = "defence_news.db"

def init_db():
    """Initialize SQLite database for tracking seen articles"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id TEXT PRIMARY KEY,
            source TEXT,
            title TEXT,
            link TEXT,
            published TEXT,
            summary TEXT,
            seen_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_article_hash(title: str, link: str) -> str:
    """Generate unique hash for article"""
    return hashlib.md5(f"{title}{link}".encode()).hexdigest()

def is_article_seen(article_id: str) -> bool:
    """Check if article has been seen before"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id FROM articles WHERE id = ?", (article_id,))
    result = c.fetchone()
    conn.close()
    return result is not None

def mark_article_seen(article_id: str, source: str, title: str, link: str, 
                     published: str, summary: str):
    """Mark article as seen in database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT OR IGNORE INTO articles (id, source, title, link, published, summary, seen_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (article_id, source, title, link, published, summary, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def matches_keywords(text: str, keywords: List[str]) -> List[str]:
    """Check if text contains any keywords (case-insensitive), return matched keywords"""
    text_lower = text.lower()
    matched = []
    for keyword in keywords:
        # Use word boundaries for better matching
        pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
        if re.search(pattern, text_lower):
            matched.append(keyword)
    return matched

def fetch_feed(source_name: str, feed_url: str) -> List[Dict]:
    """Fetch and parse RSS feed"""
    try:
        print(f"Fetching {source_name}...")
        feed = feedparser.parse(feed_url)
        
        articles = []
        for entry in feed.entries:
            title = entry.get('title', 'No title')
            link = entry.get('link', '')
            summary = entry.get('summary', entry.get('description', ''))
            published = entry.get('published', entry.get('updated', ''))
            
            # Combine title and summary for keyword matching
            search_text = f"{title} {summary}"
            
            # Check if matches any keywords
            matched_keywords = matches_keywords(search_text, KEYWORDS)
            
            if matched_keywords:
                article_id = get_article_hash(title, link)
                
                # Only include if not seen before (delta)
                if not is_article_seen(article_id):
                    articles.append({
                        'id': article_id,
                        'source': source_name,
                        'title': title,
                        'link': link,
                        'summary': summary[:300],  # Truncate long summaries
                        'published': published,
                        'matched_keywords': matched_keywords
                    })
                    
                    # Mark as seen
                    mark_article_seen(article_id, source_name, title, link, published, summary)
        
        print(f"  Found {len(articles)} new matching articles")
        return articles
        
    except Exception as e:
        print(f"  Error fetching {source_name}: {e}")
        return []

def generate_html_digest(articles: List[Dict]) -> str:
    """Generate HTML email digest"""
    
    if not articles:
        html = """
        <html>
        <body>
            <h2>Defence & Security Intelligence Digest</h2>
            <p><em>{date}</em></p>
            <p>No new articles matching your keywords today.</p>
        </body>
        </html>
        """.format(date=datetime.now().strftime("%d %B %Y"))
        return html
    
    # Group by source
    by_source = {}
    for article in articles:
        source = article['source']
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(article)
    
    html = """
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; }}
            h2 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            h3 {{ color: #34495e; margin-top: 30px; }}
            .article {{ 
                margin: 20px 0; 
                padding: 15px; 
                background-color: #f8f9fa; 
                border-left: 4px solid #3498db;
            }}
            .article-title {{ 
                font-size: 16px; 
                font-weight: bold; 
                color: #2c3e50; 
                margin-bottom: 8px;
            }}
            .article-title a {{ color: #2c3e50; text-decoration: none; }}
            .article-title a:hover {{ color: #3498db; }}
            .article-meta {{ 
                font-size: 12px; 
                color: #7f8c8d; 
                margin-bottom: 8px;
            }}
            .article-summary {{ 
                font-size: 14px; 
                color: #34495e; 
                line-height: 1.6;
            }}
            .keywords {{ 
                font-size: 11px; 
                color: #16a085; 
                font-weight: bold;
                margin-top: 8px;
            }}
            .stats {{
                background-color: #ecf0f1;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 20px;
            }}
        </style>
    </head>
    <body>
        <h2>Defence & Security Intelligence Digest</h2>
        <p><em>{date}</em></p>
        
        <div class="stats">
            <strong>{count} new articles</strong> across {sources} sources
        </div>
    """.format(
        date=datetime.now().strftime("%d %B %Y"),
        count=len(articles),
        sources=len(by_source)
    )
    
    # Add articles grouped by source
    for source in sorted(by_source.keys()):
        html += f"\n        <h3>{source} ({len(by_source[source])})</h3>"
        
        for article in by_source[source]:
            keywords_str = ", ".join(article['matched_keywords'][:5])  # Show first 5 matches
            if len(article['matched_keywords']) > 5:
                keywords_str += f" +{len(article['matched_keywords']) - 5} more"
            
            html += f"""
        <div class="article">
            <div class="article-title">
                <a href="{article['link']}" target="_blank">{article['title']}</a>
            </div>
            <div class="article-meta">{article['published']}</div>
            <div class="article-summary">{article['summary']}</div>
            <div class="keywords">Matched: {keywords_str}</div>
        </div>
            """
    
    html += """
    </body>
    </html>
    """
    
    return html

def send_email_digest(html_content: str, recipient_email: str):
    """Send email digest via SMTP"""

    # Email configuration from environment variables
    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', '587'))
    sender_email = os.environ.get('SENDER_EMAIL', '').strip()
    sender_password = os.environ.get('SENDER_PASSWORD', '').replace(' ', '').replace('\xa0', '').strip()

    print(f"\n[EMAIL CONFIG]")
    print(f"  SMTP Server: {smtp_server}")
    print(f"  SMTP Port: {smtp_port}")
    print(f"  Sender Email: {sender_email if sender_email else 'NOT SET'}")
    print(f"  Sender Password: {'SET' if sender_password else 'NOT SET'}")
    print(f"  Recipient Email: {recipient_email}")

    if not sender_email or not sender_password:
        print("ERROR: Email credentials not set. Set SENDER_EMAIL and SENDER_PASSWORD environment variables.")
        print("\nHTML digest preview:")
        print(html_content)
        raise ValueError("Email credentials not configured")
    
    # Create message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Defence Intelligence Digest - {datetime.now().strftime('%d %B %Y')}"
    msg['From'] = sender_email
    msg['To'] = recipient_email
    
    # Attach HTML content
    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)
    
    try:
        # Send email
        print(f"\n[EMAIL SENDING]")
        print(f"  Connecting to {smtp_server}:{smtp_port}...")
        with smtplib.SMTP(smtp_server, smtp_port, timeout=30) as server:
            print(f"  Starting TLS...")
            server.starttls()
            print(f"  Logging in as {sender_email}...")
            server.login(sender_email, sender_password)
            print(f"  Sending message...")
            server.send_message(msg)

        print(f"\n✓ Email digest sent successfully to {recipient_email}")

    except smtplib.SMTPAuthenticationError as e:
        print(f"\n✗ SMTP Authentication Error: {e}")
        print("  Check that your Gmail App Password is correct (16 characters)")
        print("  Verify 2-Step Verification is enabled in Google Account")
        raise
    except smtplib.SMTPException as e:
        print(f"\n✗ SMTP Error: {e}")
        print(f"  Server: {smtp_server}:{smtp_port}")
        raise
    except Exception as e:
        print(f"\n✗ Unexpected error sending email: {type(e).__name__}: {e}")
        raise

def main():
    """Main execution function"""
    print(f"\n{'='*60}")
    print(f"Defence & Security News Monitor - {datetime.now().strftime('%d %B %Y %H:%M')}")
    print(f"{'='*60}\n")
    
    # Initialize database
    init_db()
    
    # Fetch all feeds
    all_articles = []
    for source_name, feed_url in RSS_FEEDS.items():
        articles = fetch_feed(source_name, feed_url)
        all_articles.extend(articles)
        time.sleep(1)  # Be polite to servers
    
    print(f"\n{'='*60}")
    print(f"Total new articles found: {len(all_articles)}")
    print(f"{'='*60}\n")
    
    # Generate and send digest
    html_digest = generate_html_digest(all_articles)

    recipient = os.environ.get('RECIPIENT_EMAIL', 'your-email@example.com')
    print(f"\n[RECIPIENT] {recipient}")

    send_email_digest(html_digest, recipient)

    # Save HTML digest to file for review (optional, may fail in some environments)
    try:
        digest_path = 'latest_digest.html'
        with open(digest_path, 'w', encoding='utf-8') as f:
            f.write(html_digest)
        print(f"✓ Digest saved to {digest_path}")
    except Exception as e:
        print(f"Note: Could not save digest file ({e})")

    print(f"\n{'='*60}")
    print("✓ Defence News Monitor completed successfully")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
