---
name: bring-data-in
description: Bring spreadsheets or files into the firm's workspace. Use when someone wants to import or upload a CSV, an Excel workbook, a list of new time entries, clients, contacts or invoices, a document for a matter, or a folder of documents.
---

# Bring data and files in

Bytes never pass through the chat: files go from the person's browser straight into the
workspace. There are two ways in.

## One spreadsheet into one type: an upload link

For a CSV, TSV, JSON or a one-sheet Excel file of records of one kind (time entries, clients,
leads, costs):
1. `bulk_upload_url` with `namespace: "legal"` and the target `type` (for example
   `time_entries`). Give the person the `upload_url` as a link: "Open this link and drop the
   file. It works once, for 15 minutes."
2. When they say it is done, `upload_check` with the `upload_token`. Its `result` holds a
   preview: the inferred columns, sample rows, warnings and the row count.
3. Compare the columns with the type's fields in `legal-practice/references/data-model.md`.
   Show the person: rows to import, columns that match, columns that do not, and any warnings.
4. After a plain yes, `bulk_insert_commit` with the `proposal_id` (and column-type
   corrections if needed).
5. Count the rows now in the type and report the before and after counts.

## One document onto a matter: an upload link

`attach_upload_url` with `namespace: "legal"`, `type: "matters"` or `"documents"`, and the
record's `_id` as `record_id` when it belongs to one record. Give the link; after they upload,
`upload_check` returns the new attachment. InventDB reads it in the background (text, OCR,
meaning), so search finds it a little later.

## A whole workbook or a folder: the workspace pages

For a workbook with many sheets, or a folder of many files, the workspace's own pages are
faster. Tell the person, with the workspace address (the connector's address without `/mcp`):
- **Import** (`/import`): drop the CSV or Excel file; choose **All sheets → types**, the
  namespace `legal`, untick sheets that are not records (a README, a change log), then
  **Import**. Each sheet becomes a type; each column a field.
- **Files** (`/files`): **Upload folder**, choose the folder, set where the files live
  (namespace `legal`, type `documents`), leave "Analyze images and videos with AI" off, then
  **Upload**. Folders keep their structure.

Afterwards, check the result in SQL (rows per type, or
`attach_search` with `query: "*"` and the folder) and report what arrived.
