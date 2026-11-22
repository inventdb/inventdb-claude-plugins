---
name: placements-and-fees
description: Placements, placement fees invoiced and unpaid, overdue fees, replacement guarantees still running, and recording a new placement or a fee payment. Use for "who owes me a fee?", "which placements are still in guarantee?", "record the placement", "Ledgerline paid".
---

# Placements and fees

Uses `recruiter-basics`.

## Fees

The "fees not yet paid" recipe in `references/sql.md`: each unpaid fee with the company, amount,
invoiced date and days since. Overdue when days since invoice is more than the company's
`terms_days`: say "N days overdue" (days since minus terms). Not yet due: say when it falls due.
Totals with `SUM`. Offer a polite reminder to the client contact for the overdue ones; the recruiter
sends it.

## Guarantees

Placements whose `guarantee_end` has not passed, with days left. If the person has left, the
recruiter owes a replacement: suggest a check-in with the placed candidate and the client before the
guarantee ends.

## Recording a placement

Draft it: `placement_id` next after the highest, the submission, role and candidate, start date,
salary, the company's `fee_pct`, `fee_amount` = salary x fee_pct (computed in SQL), `invoiced_on`,
`guarantee_end` = start + 90 days unless the recruiter says otherwise. With it, the submission moves to
`Placed` and the role to `Filled`. After a plain yes, `propose_insert` / `propose_update` and `commit`.

## A fee paid

`propose_update` of `paid_on` on the placement, after a plain yes. A part payment is not a payment: ask
how to record it.
