# Coding Decision Rules — Actionability Framework

This document describes the decision rules applied to each binary dimension of the actionability coding framework used in:

**Soufan, M. (2026). Visibility Without Guidance: Measuring the Actionability of Public Crisis Communication in Lebanon.**

Each item in the dataset was coded yes or no on five binary dimensions. The rules below define the conditions under which each dimension was coded positively, with annotated examples of positive and negative coding decisions.

---

## 1. Specific Location (`location`)

**Positive condition:** The item names a specific geographic area relevant to the crisis — a village, city, district, road, facility, or defined zone.

**Coded YES if:**
- A named location is mentioned in connection with a crisis event, service, or instruction
- Examples: "south Lebanon," "Nabatieh," "Bint Jbeil," "Beirut's southern suburbs," "Tyre-Sidon road"

**Coded NO if:**
- Only a general or national reference is made ("Lebanon," "the country," "affected areas")
- Location is mentioned only in an organisational byline or signature

**Examples:**

| Item | Coding | Reason |
|---|---|---|
| "WFP delivered food assistance to Ain Ebel today" | YES | Named village |
| "WFP continues to scale up operations across Lebanon" | NO | National reference only |
| "Army units responded to the incident" | NO | No location specified |
| "Civil Defense teams deployed to Kfarhatay-Sidon" | YES | Named location |

---

## 2. Clear Instruction or Action (`instruction`)

**Positive condition:** The item explicitly tells recipients what to do or not to do — a direct behavioural directive addressed to the public or a defined group.

**Coded YES if:**
- The item contains an explicit imperative or directive addressed to recipients
- Examples: "do not approach unexploded ordnance," "follow army guidance before returning south," "ensure your child's vaccinations are up to date," "call 125 if you need assistance"

**Coded NO if:**
- The item describes what the institution is doing without directing the public
- The item uses normative or advocacy language without a concrete directive ("UNICEF calls on all parties," "the situation requires urgent attention")
- The item implies what people should do without stating it explicitly

**Examples:**

| Item | Coding | Reason |
|---|---|---|
| "Citizens are urged not to approach suspicious objects" | YES | Explicit directive to public |
| "The army is working to secure the area" | NO | Describes institutional action, not public directive |
| "UNICEF calls on all parties to protect civilians" | NO | Normative advocacy, not a recipient directive |
| "Residents of the south are advised to follow official guidance before returning" | YES | Explicit directive with target group |

---

## 3. Access Channel or Contact (`contact_link`)

**Positive condition:** The item provides a functional access mechanism — a hotline number, WhatsApp number, website URL, named physical facility, or referral pathway that a recipient can use to seek help or access services.

**Coded YES if:**
- A specific phone number, hotline, or WhatsApp contact is named
- A functional website or registration link is provided
- A named physical facility where services are available is identified
- A specific referral pathway is described (e.g., "contact your nearest UNHCR registration centre")

**Coded NO if:**
- Only a general organisational website or social media handle is mentioned without directing recipients to a specific service
- The item describes services as available without specifying how to access them
- A contact is mentioned only in the post metadata (platform handle, page footer)

**Examples:**

| Item | Coding | Reason |
|---|---|---|
| "Call the Civil Defense hotline at 125" | YES | Specific hotline number |
| "UNHCR WhatsApp: +961 76 814 352 — available 24/7" | YES | Named WhatsApp contact |
| "Visit help.unhcr.org/lebanon for registration information" | YES | Functional URL for a specific service |
| "WFP is delivering food assistance to displaced families" | NO | Service described, no access mechanism |
| "Follow us on X for updates" | NO | Social media handle, not a service access point |

---

## 4. Time or Date Reference (`time_date`)

**Positive condition:** The item includes a specific time, date, or temporal marker relevant to the crisis event or the guidance provided.

**Coded YES if:**
- A specific date is mentioned (e.g., "April 8," "today," "this morning")
- A specific time is mentioned (e.g., "at 14:30," "overnight")
- A temporal window is defined (e.g., "from April 17," "during the ceasefire period")
- A deadline or scheduled event is specified

**Coded NO if:**
- No time reference appears in the item
- Only a vague temporal reference is used ("recently," "in the coming days," "soon") without a specific date or time

**Examples:**

| Item | Coding | Reason |
|---|---|---|
| "An Israeli airstrike hit the area at 09:15 this morning" | YES | Specific time |
| "WFP delivered assistance on April 22" | YES | Specific date |
| "The ceasefire entered into effect on April 17" | YES | Specific date |
| "The situation has been deteriorating in recent weeks" | NO | Vague temporal reference |
| "Convoys will resume operations soon" | NO | No specific date or time |

---

## 5. Target Group Identified (`target_group`)

**Positive condition:** The item explicitly addresses or refers to a defined population segment — displaced persons, residents of a specific area, children, families, farmers, returnees, or any other identified group.

**Coded YES if:**
- A named population group is addressed or referenced as the intended recipient of information or services
- Examples: "displaced families," "residents of south Lebanon," "children under five," "returnees," "farmers in the Bekaa"

**Coded NO if:**
- The item addresses the general public without specifying a group ("citizens," "the Lebanese people," "everyone")
- No recipient group is identified
- The item is directed at institutional actors rather than the public ("humanitarian partners," "UN agencies")

**Examples:**

| Item | Coding | Reason |
|---|---|---|
| "Displaced families in Tyre can access services at the shelter centre" | YES | Named group: displaced families |
| "Children in affected areas should receive vaccinations" | YES | Named group: children |
| "The Lebanese people are urged to remain calm" | NO | General public, no defined segment |
| "WFP calls on donors to support the response" | NO | Directed at institutional/donor audience |
| "Returnees to south Lebanon should check for UXO before entering homes" | YES | Named group: returnees |

---

## Scoring

The actionability score for each item is the arithmetic sum of the five binary fields:

```
actionability_score = location + instruction + contact_link + time_date + target_group
```

Where each field equals 1 if coded YES and 0 if coded NO. Scores range from 0 to 5.

All scores in the dataset were mechanically verified to equal this sum. No manual overrides were applied.
