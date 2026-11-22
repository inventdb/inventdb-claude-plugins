---
name: bring-data-in
description: Bring candidates, roles or a pipeline export and a folder of resumes into the recruiter's workspace. Use when someone wants to import or upload a CSV or Excel file of candidates, roles or submissions, a whole workbook, or resume PDFs and Word files.
---

# Bring data and files in

Files go from the person's browser straight into their workspace, never through the chat.

## A workbook

The workspace's **Import** page (`<workspace address>/import`): drop the Excel file, choose **All
sheets → types**, namespace `recruiting`, untick any sheet that is not records, then **Import**. To
match this plugin, name the sheets Companies, Roles, Candidates, Submissions, Interview Notes and
Placements, with the columns in `recruiter-basics/references/data-model.md`.

## One CSV (an export from a job board or an ATS)

`bulk_upload_url` with `namespace: "recruiting"` and the type (for example `candidates`). Give the link
("it works once, for 15 minutes"). When they say it is uploaded, `upload_check`; show the preview (rows,
matching and unmatched columns, warnings, and any `candidate_id` that already exists); after a plain
yes, `bulk_insert_commit`. Report the row count before and after.

## Resumes

- A folder of resumes: the **Files** page, **Upload folder**, namespace `recruiting`, type `resumes`.
  Name each file `<candidate_id> - <name> - Resume.pdf` so it joins to its record, and put the file name
  in the candidate's `resume_file`. Keep resumes in `resumes`: never upload them into a records type.
- One resume: `attach_upload_url` with `namespace: "recruiting"`, `type: "resumes"`; give the link; then
  `upload_check`.

InventDB reads each resume in the background (text, OCR, meaning); it is searchable by meaning a little
after upload.
