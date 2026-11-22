---
name: bring-data-in
description: Bring a timesheet, client list, invoice export or signed SOWs into the consultant's workspace. Use when someone wants to import or upload a CSV or Excel file (time logs, clients, invoices), a whole workbook, or SOW and contract PDFs.
---

# Bring data and files in

Files go from the person's browser straight into their workspace, never through the chat.

## A workbook

The workspace's **Import** page (`<workspace address>/import`): drop the Excel file, choose **All
sheets → types**, namespace `freelance`, untick any sheet that is not records, then **Import**. To
match this plugin, name the sheets Clients, Engagements, Scope Items, Time Logs, Change Requests,
Deliverables and Invoices, with the columns in `freelance-basics/references/data-model.md`. Write dates
as dates (not text).

## One CSV (a timesheet export)

`bulk_upload_url` with `namespace: "freelance"` and the type (for example `time_logs`). Give the link
("it works once, for 15 minutes"). When they say it is uploaded, `upload_check`; show the preview (rows,
matching and unmatched columns, warnings); after a plain yes, `bulk_insert_commit`. Report the row count
before and after, and the hours added (`SUM`).

## SOWs and contracts

- Several files: the **Files** page, **Upload files** or **Upload folder**, namespace `freelance`, type
  `documents`. Keep files in `documents`: never upload them into a records type.
- One file: `attach_upload_url` with `namespace: "freelance"`, `type: "documents"`; give the link; then
  `upload_check`. Put the file name in the engagement's `sow_file` (after yes).

InventDB reads each file in the background (text, OCR, meaning) before `scope-check` can quote it.
