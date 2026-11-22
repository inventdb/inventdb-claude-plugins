---
name: bring-data-in
description: Bring spreadsheets, receipts and lease documents into the portfolio's workspace. Use when someone wants to import or upload a rent roll, a CSV or Excel file of tenants, leases or transactions, receipts, invoices or lease PDFs, or a whole workbook.
---

# Bring data and files in

Files go from the person's browser straight into their workspace, never through the chat.

## Starting from a spreadsheet

The workspace's **Import** page (`<workspace address>/import`): drop the CSV or Excel file. For a
workbook with one sheet per kind of record, choose **All sheets → types** and the namespace `pms`;
untick any sheet that is not records (a README); then **Import**. Each sheet becomes a type and each
column a field. To match this plugin, name the sheets Properties, Owners, Leases, Tenants,
Transactions, Work Orders, Vendors, Inspections, Compliance and Daily Tasks, with the columns listed in
`portfolio-basics/references/data-model.md`.

## One file of records: an upload link

For one CSV or one-sheet Excel file into one type: `bulk_upload_url` with `namespace: "pms"` and the
type (for example `transactions`). Give the link ("it works once, for 15 minutes"). When they say it
is uploaded, `upload_check`; show the preview (rows, matching and unmatched columns, warnings); after
a plain yes, `bulk_insert_commit`. Report the type's row count before and after.

## Receipts, invoices, lease PDFs

- Several files: the **Files** page, **Upload files** or **Upload folder**, with namespace `pms` and
  type `receipts` (receipts and invoices). Keep files in a files type: never upload into a records
  type such as `transactions`.
- One file: `attach_upload_url` with `namespace: "pms"`, `type: "receipts"`; give the link; then
  `upload_check`.

InventDB reads each file in the background (text, OCR, meaning); then the `receipts-and-expenses`
skill can turn it into an expense line.
