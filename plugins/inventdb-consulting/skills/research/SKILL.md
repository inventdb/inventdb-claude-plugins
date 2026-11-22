---
name: research
description: Research outside the data room - public records, permits, zoning codes, flood maps, court and litigation searches, market facts - and the engagement's research notes. Use for "check the permit history", "is there any litigation?", "what does the zoning code say about nonconforming parking?", "record that as a research note".
---

# Research

Uses `consulting-basics`.

- **What is already known**: `SELECT note_id, date, topic, source, finding FROM consulting.research_notes WHERE engagement_id = '...' ORDER BY date`.
- **New research**: when web search or fetch is available, use it for public sources (a city code, a flood map
  service, a permit portal, a court index). Name each source and the date it was read. A web page is a lead, not a
  record: say where the official record is, and mark anything that needs a certified copy or a call to the office.
- **Record it**: draft a note (`note_id` next after the highest, `date` today, `topic`, `source` as a short name, and
  `finding` in one or two sentences with the source's own figures or words). After a plain yes, `propose_insert` and
  `commit`. A research result that changes the risk picture is also offered as a finding.
- Never present research as legal advice; say who should confirm it (counsel, the surveyor, the city).
