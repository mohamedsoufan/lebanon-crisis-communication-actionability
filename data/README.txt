STUDY: Visibility Without Guidance — Lebanon Public Crisis Communication Audit
COLLECTION WINDOW: April 1 – May 7, 2026
LAST UPDATED: 2026-05-08

FOLDER STRUCTURE
----------------
data/
  raw/       Original source data, one subfolder per source
  cleaned/   Cleaned CSVs, one row per item, one subfolder per source
  coding/    Coded dataset, analysis scripts, output CSVs, and figures


SOURCES
-------
01  DRM Lebanon (Disaster Risk Management Unit)    Facebook
02  Ministry of Social Affairs                     Facebook
03  Ministry of Public Health                      Facebook / website
04  Lebanese Civil Defense                         Facebook
05  Lebanese Army                                  X (formerly Twitter)
06  Lebanese Red Cross                             X (formerly Twitter)
07  UNHCR Lebanon                                  Flash updates (PDF)
08  UNICEF Lebanon                                 Press releases / reports
09  WFP Lebanon                                    X (formerly Twitter) / website


STATUS
------
Source                         Raw    Cleaned    Coded
01 DRM Lebanon                 YES    YES        YES
02 Ministry of Social Affairs  YES    YES        YES
03 Ministry of Public Health   YES    YES        YES
04 Lebanese Civil Defense      YES    YES        YES
05 Lebanese Army               YES    YES        YES
06 Lebanese Red Cross          YES    YES        YES
07 UNHCR Lebanon               YES    YES        YES
08 UNICEF Lebanon              YES    YES        YES
09 WFP Lebanon                 YES    YES        YES

Total coded items: 182


SOURCE NOTES
------------

01 DRM Lebanon
- 30 posts collected (April 1 – May 6, 2026)
- 27 are daily situation reports
- 3 non-situation-report posts: UXO warning (Apr 17), missing child guidance (Apr 09),
  missing persons hotline Beirut (Apr 08, truncated)
- 27 of 30 posts truncated in scrape; full text not captured
- Mean actionability score: 1.20

02 Ministry of Social Affairs
- 5 crisis-related posts within window
- Mean actionability score: 1.00

03 Ministry of Public Health
- 42 items (Facebook posts + website)
- Mean actionability score: 1.50

04 Lebanese Civil Defense
- 27 unique posts within window (April 1 – May 7, 2026)
- Dates inferred from comment ages (scrape date May 7)
- Excluded: 5 non-crisis posts, 4 video-only duplicates, 16 public comments
- Mean actionability score: 1.44

05 Lebanese Army
- Platform: X (@LebarmyOfficial)
- 40 crisis-related posts within window
- Excluded: routine arrests, diplomatic meetings, ceremonial posts
- High-actionability posts driven by UXO disposal and return advisory content
- Mean actionability score: 2.80

06 Lebanese Red Cross
- Platform: X (@RedCrossLebanon)
- Source JSON: 743 entries (2020–2026); filtered to window
- 7 crisis-related posts retained; 3 excluded (slogan, retweet, fundraising)
- Posts cluster around Apr 8 mass emergency response and Apr 12–17 drone attack on LRC team
- Mean actionability score: 1.29

07 UNHCR Lebanon
- Flash Update PDFs (weekly, publicly available)
- Flash Update #6 not available; excluded
- 4 documents included: FU#5, FU#7, FU#8, FU#9
- Each document coded as one unit of analysis
- Mean actionability score: 4.75

08 UNICEF Lebanon
- 3 website press releases + 3 Flash Update PDFs (FU#6, #7, #8)
- Most actionable item: vaccination guidance post (5/5)
- Mean actionability score: 4.50

09 WFP Lebanon
- Platform: X (@WFPLebanon) + website
- 21 posts within window; no non-crisis posts in window
- Content: convoy updates, food insecurity data, media appearances
- No citizen-facing action channels or instructions in any post
- Mean actionability score: 2.38


CODING COLUMNS
--------------
source_id, source, source_type, platform, date, clean_text, language,
crisis_related, crisis_topic, communication_type,
location, instruction, contact_link, time_date, target_group,
actionability_score, notes

Actionability score = sum of five binary fields (location + instruction +
contact_link + time_date + target_group). Range: 0–5.
