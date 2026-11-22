---
name: bring-data-in
description: Bring a data room, single documents, a document index or other spreadsheets into the consultant's workspace. Use when someone wants to upload a folder of documents from the seller, one new document, a rent roll or document index in CSV or Excel, or a whole workbook.
---

# Bring data and files in

Files go from the person's browser straight into their workspace, never through the chat.

## A data room (a folder of files)

The workspace's **Files** page (`<workspace address>/files`): **Upload folder**, namespace `consulting`, type
`data_room`. Keep documents in `data_room` and reports in `deliverables`: never upload files into a records type.
InventDB reads each file in the background (text, OCR, meaning); it becomes searchable a little after upload.

Then register them: one `documents` row per file (next `doc_id`, `engagement_id`, title, workstream, `file_name`
exactly as uploaded, source, `received_on`, pages, `status` `Received`). Draft the rows from the file names and
`attach_search` results; write after a plain yes.

## One new document

`attach_upload_url` with `namespace: "consulting"`, `type: "data_room"`. Give the link ("it works once, for 15
minutes"); when they say it is uploaded, `upload_check`, wait until the file is read, then register it and offer a
review (`document-review`). If it answers an open request, offer to mark the request received.

## A spreadsheet

- A workbook with one sheet per kind of record: the **Import** page (`<workspace address>/import`), **All sheets →
  types**, namespace `consulting`. Sheet names to match this plugin: Clients, Engagements, Checklist, Documents,
  Findings, Requests, Research Notes, Rent Roll, Time Entries, Invoices, Reports (columns in
  `consulting-basics/references/data-model.md`). Dates as dates.
- One CSV (a rent roll, a timesheet export): `bulk_upload_url` with `namespace: "consulting"` and the type; after the
  upload, `upload_check`, show the preview, and `bulk_insert_commit` after a plain yes.
