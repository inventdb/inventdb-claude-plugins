---
name: recruiter-basics
description: Ground rules for an independent recruiter's desk kept in InventDB (client companies, roles, candidates and their resumes, submissions, interview notes, placements and fees). Use for any question or change about candidates, resumes, roles, shortlists, the pipeline, follow-ups, placements or fees, before calling the InventDB connector.
---

# InventDB Recruiter: how to work in the desk's records

The desk lives in the recruiter's own InventDB Serverless workspace, namespace `recruiting`. You
reach it through their **InventDB** connector (tools include `sql`, `attach_search`, `attach_read`,
`propose_insert`, `propose_update`, `commit`, `bulk_upload_url`, `attach_upload_url`, `upload_check`). If
no such connector is connected, say: "Connect your InventDB workspace first: Settings > Connectors >
Add custom connector, with your workspace's /mcp address." and stop.

## Records

- Company `CO-NN` (a client that pays a fee), role `JOB-NNN`, candidate `CAND-NNNN`, submission
  `SUB-NNN` (one candidate put forward for one role), interview note `NOTE-NNN`, placement `PLC-NN`.
- Each candidate's resume is a file in the `resumes` type, named in `candidates.resume_file`
  (`CAND-0037 - Arden Thistlewood - Resume.pdf`): the first nine characters are the `candidate_id`.
- Fields and exact values are in `references/data-model.md`; SQL forms and recipes in
  `references/sql.md`.

## Finding people

- By meaning ("has run payment reconciliation at scale"): `attach_search` with `namespace:
  "recruiting"`, `type: "resumes"`, **`mode: "semantic"`**, the need in plain words, `limit` 10 to 20.
  `semantic` ranks by meaning, which is what skills and experience need.
- By name, employer or an exact skill word: `sql` on `recruiting.candidates` with `LIKE`.
- Then read the candidate's record (salary, notice, location, last contacted) with `sql`, and quote
  the resume line that shows the experience (`attach_read`). Never claim experience the resume does
  not state.

## Fair and private

- Match on the role's requirements and the resume's evidence only. Never infer or use age, gender,
  ethnicity, nationality, religion, disability, family status or anything else that is not about the
  work, and do not guess them from names, dates or places.
- Candidate details stay in the workspace. Messages you draft (to a candidate or a client) are
  drafts: the recruiter sends them, and a client sees a candidate only once the recruiter decides.

## Numbers and changes

- Counts, salaries and fees come from SQL; days from `DATEDIFF`. Money in US dollars.
- Clocks count from today, or from **20 Nov 2026** in the synthetic Ellery Search demo ("as at 20 Nov
  2026").
- Draft any change as a table, wait for a plain yes, then `propose_insert` / `propose_update` and
  `commit`. A request such as "record it" or "submit her" asks for the draft: show it and ask; the yes
  comes after the recruiter has seen it. Never delete records.
