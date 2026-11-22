---
name: billing
description: Unbilled hours, what to invoice next, overdue invoices and payment reminders, and recording a payment. Use for "what haven't I billed?", "who owes me money?", "draft the November invoice", "Quillmere paid INV-2026-006", "chase late payments".
---

# Billing

Uses `freelance-basics`. Amounts from SQL; drafts are drafts; writes only after yes.

## Unbilled time

The unbilled recipe in `references/sql.md`, one row per engagement with its hours, its oldest unbilled
date and the days since then. Flag anything older than 30 days first: it should already have been
invoiced. Fixed-fee work (`FIXED FEE`) is billed by milestone, not by hours: leave it out.

## What to invoice next

- Hourly: unbilled hours x `hourly_rate` (in SQL) for the months that have ended.
- Retainer: `monthly_fee` for the month that ended, plus overage (see `burn-and-rate`).
- Fixed fee: the SOW's milestone split (read the SOW: 30% at start, 40% at the milestone, 30% on
  completion, unless it says otherwise) against the milestone invoices already issued.

Show the draft lines and the total. Creating the invoice record (`propose_insert` into `invoices`,
next `invoice_no`, `status` `Sent`, `due_on` = issued + the client's `payment_terms_days`) and marking
its time logs (`propose_update` of each `invoice_no`) happen after a plain yes.

## Overdue

The overdue recipe in `references/sql.md`: invoice, client company, amount, due date, days overdue,
and the total owed by each client (`SUM`). Offer a reminder email per client, polite on the first,
firmer past 30 days, quoting the invoice numbers and amounts; the consultant sends it.

## Recording a payment

Find the invoice's `_id`
(`SELECT _id, invoice_no, amount, paid_on FROM freelance.invoices WHERE invoice_no = 'INV-2026-006'`), show
the change (`paid_on`, `status` `Paid`), and after a plain yes `propose_update` and `commit`. A part
payment is not a payment: say so and ask how to record it.
