import requests
import csv
import time
import re
from datetime import datetime, timedelta
from pathlib import Path

ROOT   = Path(__file__).resolve().parent.parent.parent.parent
OUTPUT = ROOT / "data" / "raw" / "10_GDELT" / "gdelt_lebanon_raw.csv"

QUERIES = [
    (
        'Lebanon AND (crisis OR emergency OR displacement OR displaced OR shelter OR aid OR relief '
        'OR health OR hospital OR casualties OR wounded OR killed OR strike OR attack OR border '
        'OR "South Lebanon" OR refugees OR electricity OR water OR "Civil Defense" OR "Red Cross")',
        "english"
    )
]

START            = datetime(2026, 4,  1,  0,  0,  0)
END              = datetime(2026, 5,  7, 23, 59, 59)
CAP              = 250
MIN_WINDOW_HOURS = 6

ALLOWED_DOMAINS = {
    "lbcgroup.tv", "mtv.com.lb", "aljadeed.tv", "otv.com.lb",
    "almayadeen.net", "almanar.com.lb", "nna-leb.gov.lb",
    "annahar.com", "al-akhbar.com", "addiyar.com", "aljoumhouria.com",
    "aliwaa.com.lb", "mustaqbalweb.com", "elnashra.com", "lebanon24.com",
    "naharnet.com", "lorientlejour.com", "lorienttoday.com", "tayyar.org",
    "beirut-today.com", "the961.com", "961themix.com", "daraj.media",
    "nowlebanon.com", "kataeb.org", "janoubia.com", "saidaonline.com",
    "imlebanon.org", "cedarnews.net", "alahednews.com.lb",
    "lebanondebate.com", "lebanonfiles.com",
}

DOMAIN_TO_SOURCE = {
    "lbcgroup.tv":       "LBCI",
    "mtv.com.lb":        "MTV Lebanon",
    "aljadeed.tv":       "Al Jadeed",
    "otv.com.lb":        "OTV",
    "almayadeen.net":    "Al Mayadeen",
    "almanar.com.lb":    "Al Manar",
    "nna-leb.gov.lb":    "NNA",
    "annahar.com":       "An Nahar",
    "al-akhbar.com":     "Al Akhbar",
    "addiyar.com":       "Ad Diyar",
    "aljoumhouria.com":  "Al Joumhouria",
    "aliwaa.com.lb":     "Al Liwaa",
    "mustaqbalweb.com":  "Al Mustaqbal",
    "elnashra.com":      "Elnashra",
    "lebanon24.com":     "Lebanon 24",
    "naharnet.com":      "Naharnet",
    "lorientlejour.com": "L'Orient Le Jour",
    "lorienttoday.com":  "L'Orient Today",
    "tayyar.org":        "Tayyar",
    "beirut-today.com":  "Beirut Today",
    "the961.com":        "The961",
    "961themix.com":     "961 The Mix",
    "daraj.media":       "Daraj",
    "nowlebanon.com":    "Now Lebanon",
    "kataeb.org":        "Kataeb",
    "janoubia.com":      "Janoubia",
    "saidaonline.com":   "Saida Online",
    "imlebanon.org":     "IM Lebanon",
    "cedarnews.net":     "Cedar News",
    "alahednews.com.lb": "Al Ahed News",
    "lebanondebate.com": "Lebanon Debate",
    "lebanonfiles.com":  "Lebanon Files",
}

FIELDNAMES = [
    "source_id", "source", "source_type", "platform",
    "date", "title", "url", "domain", "language",
    "snippet", "full_text", "raw_query", "clean_text",
    "crisis_related", "crisis_topic", "communication_type",
    "location", "instruction", "contact_link", "time_date", "target_group",
    "actionability_score", "notes",
]


def build_windows(start_date, end_date, interval_days=1):
    windows = []
    current = start_date
    while current < end_date:
        window_end = min(
            current + timedelta(days=interval_days) - timedelta(seconds=1),
            end_date
        )
        windows.append((
            current.strftime("%Y%m%d%H%M%S"),
            window_end.strftime("%Y%m%d%H%M%S")
        ))
        current += timedelta(days=interval_days)
    return windows

def normalize_title(title):
    title = title.lower()
    title = re.sub(r"[^\w\s]", "", title)
    title = re.sub(r"\s+", " ", title).strip()
    return title

def clean_text(title, snippet):
    parts = [p.strip() for p in [title, snippet] if p and p.strip()]
    text  = " | ".join(parts)
    text  = re.sub(r"\s+", " ", text).strip()
    return text

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "Mozilla/5.0"})


def query_gdelt(query_text, lang_code, start_dt, end_dt, max_records=250, retries=3):
    params = {
        "query":         f"{query_text} sourcelang:{lang_code}",
        "mode":          "artlist",
        "maxrecords":    max_records,
        "startdatetime": start_dt,
        "enddatetime":   end_dt,
        "sort":          "DateDesc",
        "format":        "json",
    }
    for attempt in range(1, retries + 1):
        try:
            r = SESSION.get(
                "https://api.gdeltproject.org/api/v2/doc/doc",
                params=params,
                timeout=60
            )
            r.raise_for_status()
            if not r.text.strip():
                return []
            return r.json().get("articles", [])
        except requests.exceptions.JSONDecodeError:
            return []
        except Exception as e:
            if attempt < retries:
                wait = attempt * 30
                print(f"  retrying in {wait}s ({e})", flush=True)
                time.sleep(wait)
            else:
                print(f"ERROR: {e}")
                return []


all_articles    = []
seen_urls       = set()
seen_titles     = set()
total_requests  = 0
article_counter = 0


def process_window(query_text, lang_code, start_dt, end_dt):
    global total_requests, article_counter

    articles = query_gdelt(query_text, lang_code, start_dt, end_dt)
    total_requests += 1

    kept           = 0
    skipped_domain = 0

    for a in articles:
        url    = a.get("url",    "").strip()
        title  = a.get("title",  "").strip()
        domain = a.get("domain", "").strip().lower()

        if not url or not title:
            continue

        if domain not in ALLOWED_DOMAINS:
            skipped_domain += 1
            continue

        norm_title = normalize_title(title)
        if url in seen_urls or norm_title in seen_titles:
            continue

        language = a.get("language", "").strip()
        if language and language.lower() != lang_code.lower():
            continue

        seen_urls.add(url)
        seen_titles.add(norm_title)

        raw_date   = a.get("seendate", "")
        date_clean = (
            f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:8]}"
            if len(raw_date) >= 8 else ""
        )

        snippet   = a.get("seendescription", a.get("description", "")).strip()
        full_text = a.get("content", "").strip()

        article_counter += 1
        source_id = f"GDELT_{article_counter:03d}"
        source    = DOMAIN_TO_SOURCE.get(domain, domain)

        all_articles.append({
            "source_id":           source_id,
            "source":              source,
            "source_type":         "media",
            "platform":            "GDELT",
            "date":                date_clean,
            "title":               title,
            "url":                 url,
            "domain":              domain,
            "language":            language,
            "snippet":             snippet,
            "full_text":           full_text,
            "raw_query":           query_text,
            "clean_text":          clean_text(title, snippet),
            "crisis_related":      "",
            "crisis_topic":        "",
            "communication_type":  "media report",
            "location":            "",
            "instruction":         "",
            "contact_link":        "",
            "time_date":           "",
            "target_group":        "",
            "actionability_score": "",
            "notes":               "",
        })
        kept += 1

    print(f"  {start_dt[:8]}: {len(articles)} returned | {kept} kept | {skipped_domain} non-Lebanese dropped",
          flush=True)

    if len(articles) == CAP:
        start_obj    = datetime.strptime(start_dt, "%Y%m%d%H%M%S")
        end_obj      = datetime.strptime(end_dt,   "%Y%m%d%H%M%S")
        window_hours = (end_obj - start_obj).total_seconds() / 3600
        if window_hours > MIN_WINDOW_HOURS:
            mid = start_obj + (end_obj - start_obj) / 2
            process_window(query_text, lang_code,
                           start_obj.strftime("%Y%m%d%H%M%S"),
                           mid.strftime("%Y%m%d%H%M%S"))
            process_window(query_text, lang_code,
                           (mid + timedelta(seconds=1)).strftime("%Y%m%d%H%M%S"),
                           end_dt)


WINDOWS = build_windows(START, END)

for query_text, lang_code in QUERIES:
    print(f"\nQuery  : {query_text[:80]}...")
    print(f"Lang   : {lang_code}")
    print(f"Window : {START.date()} to {END.date()}  ({len(WINDOWS)} days)")
    print(f"Domains: {len(ALLOWED_DOMAINS)} Lebanese outlets whitelisted\n")

    for start, end in WINDOWS:
        process_window(query_text, lang_code, start, end)
        time.sleep(2)
        with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(sorted(all_articles, key=lambda x: x["date"]))

all_articles.sort(key=lambda x: x["date"])
with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
    writer.writeheader()
    writer.writerows(all_articles)

print(f"\nDone.")
print(f"Total articles kept : {len(all_articles):,}")
print(f"Total API requests  : {total_requests:,}")
print(f"Saved to            : {OUTPUT}")
