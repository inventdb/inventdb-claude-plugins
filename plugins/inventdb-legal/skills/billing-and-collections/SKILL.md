---
name: billing-and-collections
description: Money in. Use when someone asks about receivables, aging, overdue or unpaid invoices, collections, unbilled work (WIP), lockup, what a client owes, what was paid, or wants a payment reminder drafted.
---

# Billing and collections

Follow `legal-practice` first. Recipes are in `legal-practice/references/sql.md`.

## What to show

- **Receivables by age**: invoices with `balance_due > 0`, grouped by `aging_bucket`
  (`Current (not yet due)`, `1-30 days`, `31-60 days`, `61-90 days`, `91-120 days`,
  `Over 120 days`), each with count and total due, oldest last. Give the total.
- **Who to chase**: the largest and oldest balances, one line each: invoice key, matter key
  and caption, client, balance due, days outstanding, status. `Sent to collections` invoices
  are listed apart: they are already with collections.
- **Unbilled work (WIP)**: billable, not-yet-billed time by matter (hours and value at
  standard rates), largest first.
- **One client or matter**: its open invoices, payments received (`payments_and_receipts`)
  and anything applied from trust.

Lockup (G5, target under 90 days) needs both WIP days and debtor days; give it only when the
person asks, show how each part was counted, and label it "estimate" if any input is missing.

## Reminder letters

You may draft the wording of a payment reminder. The facts in it (invoice key, dates, amount
due) come from the invoice row, quoted exactly. Say "Draft for your review"; the person sends
it. Never threaten collections or interest unless the person says the firm's terms allow it.

## Changes

Recording a payment, a write-off or a write-down changes the firm's books. Draft it only when
asked, show it, wait for a plain yes, then `propose_insert` / `propose_update` and `commit`.
Never change `balance_due`, `invoice_total` or other totals directly: say billing recalculates
them.
