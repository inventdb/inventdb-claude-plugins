---
name: find-documents
description: Find and read the firm's documents. Use when someone asks for a document, letter, pleading, proof of service, engagement letter, invoice PDF, medical report, settlement draft or closing statement, asks what a document says, or wants documents about a topic.
---

# Find documents

Follow `legal-practice` first. The firm's files are in the workspace, filed under the
`documents` type in the firm's folder tree:
`InventDB Legal Test Documents/Clients/<client>/<MT-key caption>/<NN section>/<file>.pdf`,
plus `Firm/`, `Intake/` and `Inbox - Unsorted/`. InventDB reads every file (text, and scans
by OCR) and indexes it for search by name, by text inside and by meaning.

## Search

Use `attach_search` with `namespace: "legal"` and `type: "documents"`:
- a name or key the person gives ("proof of service Kang Brothers", "MT-3218"):
  `mode: "combined"`;
- an exact phrase or amount inside a file ("$406,300"): `mode: "fulltext"`;
- a topic ("letters about reducing a medical lien"): `mode: "semantic"`.

Show up to 10 results: file name, folder (shortened to client and matter), the snippet, and
the `view_url` as a link titled with the file name. Say how many more there are.

To know a file's matter, type or whether it is privileged, look up its row:
`SELECT document_id, matter_id, document_type, privileged FROM legal.documents WHERE file_name = '<file name>'`.
Mark privileged files "privileged" wherever you list them.

## Read

`attach_read` (by the result's `att_id`) returns a file's text. Quote what it says with the
file name, and never invent content the text does not contain. For a long file, read the part
you need (`chunk_index` or `char_range`).

InventDB reads new files in the background, a few seconds each. If a file's
`extraction_status` is `Pending`, say "InventDB is still reading this file; ask again in a few
minutes", give its view link, and stop there. Do not try to fetch the file's bytes another way.
A figure may still be on the file's `documents` row (`key_fields_json`): quote it as "indexed
for this document", not as read from the page.

## Add a file

Files never pass through the chat. To add one document to a matter, use the
`bring-data-in` skill (a one-time upload link). For a folder of files, point to the
workspace's **Files** page, **Upload folder**.

If the person's access does not include documents, `attach_search` returns nothing. Say
"Your access does not include the firm's documents."
