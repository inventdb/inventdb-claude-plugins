---
name: receipts-and-expenses
description: Turn receipts and vendor invoices into expense lines. Use when someone uploads or mentions a receipt, a vendor invoice or a bill, asks to log an expense, or asks which receipts are not yet recorded.
---

# Receipts and expenses

Follow `portfolio-basics` first. Receipts live in the `receipts` type; InventDB reads each one (text,
and OCR for photos) in the background after upload.

## Find and read

`attach_search` with `namespace: "pms"`, `type: "receipts"` (`query: "*"` lists them all, or a vendor
name or work order key). Read one with `attach_read`. If its text is not ready yet, say "InventDB is
still reading this receipt; ask again in a minute" and stop.

## Match it to the records

From the receipt's text take the vendor, the date, the work order key if printed, the service address
and the total. Then match in SQL:
- the vendor: `SELECT company FROM pms.vendors WHERE company LIKE '%<name>%'`;
- the work order: by its key, or by vendor and property;
- the property: by the work order, or by the street in `pms.properties`;
- whether it is already in the ledger: `SELECT date, amount, reference FROM pms.transactions WHERE reference = '<WO key>' OR (party_tenant_vendor = '<vendor>' AND amount = <total>)`.

Say what matched and what did not. If the receipt's address matches no property, stop and ask.

## Draft the expense

One `pms.transactions` line: `date` (the receipt's), `type` `Expense`, `property_id`, `owner_id`
(the property's), `account_category` `Repairs & Maintenance`, `account` as the other repair lines
read, `party_tenant_vendor` the vendor, `memo` "<WO key> — <issue>", `amount` **exactly the receipt's
total, as printed**, `method` as printed, `reference` the work order key.

The amount is read from the receipt, not computed: quote the line you read it from. Show the draft
next to the receipt's file name, wait for yes, then `propose_insert` and `commit`. Offer to close the
work order with the same amount as `actual_cost` (see `maintenance-and-vendors`), as a separate yes.

## Not yet recorded

For "which receipts are not in the books": list the receipts, match each as above, and list those with
no ledger line.
