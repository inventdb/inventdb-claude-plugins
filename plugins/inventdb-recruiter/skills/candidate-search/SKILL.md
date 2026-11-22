---
name: candidate-search
description: Find candidates by what their resumes say they have done, not just by keywords. Use for "who has done X?", "find me someone who has...", "do I have anyone with payments experience?", "search my resumes for...", or any question about a candidate's background.
---

# Candidate search

Uses `recruiter-basics`.

1. Put the need in plain words, as experience rather than a keyword list ("ran Kubernetes clusters in
   production and cut on-call paging"). Search `attach_search` with `namespace: "recruiting"`, `type:
   "resumes"`, `mode: "semantic"`, `limit: 15`.
2. Take the `candidate_id` from each file name (its first nine characters) and read their records
   in one `sql` call: `... FROM recruiting.candidates WHERE candidate_id IN (...)`.
3. For the strongest five to eight, `attach_read` the resume and quote the line that shows the
   experience. Drop anyone whose resume does not actually show it; say how many you dropped.
4. Show: candidate, current title and employer, the quoted evidence, years, expected salary, notice,
   location, last contacted. Order by how directly the evidence answers the need, and say so.

A search finds resumes that are similar in meaning: it can miss someone, and it can return someone
whose resume only mentions the topic. The quote is what counts. If the person asks for an exact word
(a certification, an employer), also run a `LIKE` search on the record fields and say which method
found whom.
