import csv
from pathlib import Path
from collections import defaultdict

ROOT  = Path(__file__).resolve().parent
INPUT = ROOT / "master_dataset_fixed.csv"
OUT   = ROOT

rows = []
with open(INPUT, encoding="utf-8") as f:
    for row in csv.DictReader(f):
        row["actionability_score"] = int(row["actionability_score"])
        rows.append(row)

N = len(rows)
print(f"Loaded {N} rows\n")

SOURCE_TYPE_MAP = {
    "DRM Lebanon":                "state/ministry",
    "Ministry of Social Affairs": "state/ministry",
    "Ministry of Public Health":  "state/ministry",
    "Lebanese Civil Defense":     "emergency responder",
    "Lebanese Army":              "emergency responder",
    "Lebanese Red Cross":         "emergency responder",
    "UNHCR Lebanon":              "humanitarian/UN",
    "UNICEF Lebanon":             "humanitarian/UN",
    "WFP Lebanon":                "humanitarian/UN",
}

def pct(n, total):
    return round(100 * n / total, 1) if total else 0

def avg(values):
    return round(sum(values) / len(values), 2) if values else 0

def write_csv(path, fieldnames, data_rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(data_rows)
    print(f"Saved: {path.name}")


# 1. Overall actionability
scores = [r["actionability_score"] for r in rows]
low    = sum(1 for s in scores if s <= 1)
mid    = sum(1 for s in scores if 2 <= s <= 3)
high   = sum(1 for s in scores if s >= 4)

result1 = [{
    "total_items":     N,
    "average_score":   avg(scores),
    "pct_score_0_1":   pct(low,  N),
    "pct_score_2_3":   pct(mid,  N),
    "pct_score_4_5":   pct(high, N),
    "count_score_0_1": low,
    "count_score_2_3": mid,
    "count_score_4_5": high,
}]

write_csv(OUT / "analysis_1_overall_actionability.csv", list(result1[0].keys()), result1)
print("1. Overall actionability")
print(f"   Average score : {result1[0]['average_score']}")
print(f"   Score 0-1     : {result1[0]['count_score_0_1']} items ({result1[0]['pct_score_0_1']}%)")
print(f"   Score 2-3     : {result1[0]['count_score_2_3']} items ({result1[0]['pct_score_2_3']}%)")
print(f"   Score 4-5     : {result1[0]['count_score_4_5']} items ({result1[0]['pct_score_4_5']}%)\n")


# 2. Actionability elements
fields = ["location", "instruction", "contact_link", "time_date", "target_group"]
field_labels = {
    "location":     "Specific location",
    "instruction":  "Clear instruction/action",
    "contact_link": "Access channel / contact",
    "time_date":    "Time or date",
    "target_group": "Target group identified",
}

result2 = []
print("2. Actionability elements present")
for f in fields:
    yes_count = sum(1 for r in rows if r[f] == "yes")
    no_count  = N - yes_count
    result2.append({
        "element":     field_labels[f],
        "field":       f,
        "present_yes": yes_count,
        "missing_no":  no_count,
        "pct_present": pct(yes_count, N),
        "pct_missing": pct(no_count,  N),
    })
    print(f"   {field_labels[f]:<35} present: {yes_count:3d} ({pct(yes_count,N):5.1f}%)  missing: {no_count:3d} ({pct(no_count,N):5.1f}%)")

write_csv(OUT / "analysis_2_missing_elements.csv",
          ["element","field","present_yes","missing_no","pct_present","pct_missing"], result2)
print()


# 3. Communication type vs actionability
by_type = defaultdict(list)
for r in rows:
    ct = r["communication_type"].strip() or "unspecified"
    by_type[ct].append(r["actionability_score"])

result3 = []
print("3. Communication type vs actionability")
for ct, s_list in sorted(by_type.items(), key=lambda x: -avg(x[1])):
    result3.append({
        "communication_type": ct,
        "count":              len(s_list),
        "pct_of_total":       pct(len(s_list), N),
        "average_score":      avg(s_list),
        "pct_high_4_5":       pct(sum(1 for s in s_list if s >= 4), len(s_list)),
    })
    print(f"   {ct:<45} n={len(s_list):3d}  avg={avg(s_list):.2f}  high={pct(sum(1 for s in s_list if s>=4),len(s_list)):.0f}%")

write_csv(OUT / "analysis_3_commtype_vs_actionability.csv",
          ["communication_type","count","pct_of_total","average_score","pct_high_4_5"], result3)
print()


# 4. Source comparison
by_source      = defaultdict(list)
source_commtypes = defaultdict(list)
for r in rows:
    src = r["source"]
    by_source[src].append(r["actionability_score"])
    source_commtypes[src].append(r["communication_type"].strip())

def most_common(lst):
    return max(set(lst), key=lst.count) if lst else ""

result4 = []
print("4. Source comparison")
for src, s_list in sorted(by_source.items(), key=lambda x: -avg(x[1])):
    mc = most_common(source_commtypes[src])
    result4.append({
        "source":               src,
        "source_group":         SOURCE_TYPE_MAP.get(src, "other"),
        "count":                len(s_list),
        "average_score":        avg(s_list),
        "pct_high_4_5":         pct(sum(1 for s in s_list if s >= 4), len(s_list)),
        "pct_low_0_1":          pct(sum(1 for s in s_list if s <= 1), len(s_list)),
        "most_common_commtype": mc,
    })
    print(f"   {src:<35} n={len(s_list):3d}  avg={avg(s_list):.2f}  high={pct(sum(1 for s in s_list if s>=4),len(s_list)):4.0f}%  [{mc}]")

write_csv(OUT / "analysis_4_source_comparison.csv",
          ["source","source_group","count","average_score","pct_high_4_5","pct_low_0_1","most_common_commtype"], result4)
print()


# 5. Source-type comparison
by_stype = defaultdict(list)
for r in rows:
    stype = SOURCE_TYPE_MAP.get(r["source"], "other")
    by_stype[stype].append(r["actionability_score"])

result5 = []
print("5. Source-type comparison")
for stype, s_list in sorted(by_stype.items(), key=lambda x: -avg(x[1])):
    result5.append({
        "source_type":   stype,
        "count":         len(s_list),
        "pct_of_total":  pct(len(s_list), N),
        "average_score": avg(s_list),
        "pct_high_4_5":  pct(sum(1 for s in s_list if s >= 4), len(s_list)),
        "pct_low_0_1":   pct(sum(1 for s in s_list if s <= 1), len(s_list)),
    })
    print(f"   {stype:<25} n={len(s_list):3d} ({pct(len(s_list),N):4.1f}%)  avg={avg(s_list):.2f}  high={pct(sum(1 for s in s_list if s>=4),len(s_list)):4.0f}%  low={pct(sum(1 for s in s_list if s<=1),len(s_list)):4.0f}%")

write_csv(OUT / "analysis_5_sourcetype_comparison.csv",
          ["source_type","count","pct_of_total","average_score","pct_high_4_5","pct_low_0_1"], result5)

print("\nDone. 5 CSV files written to data/coding/")
