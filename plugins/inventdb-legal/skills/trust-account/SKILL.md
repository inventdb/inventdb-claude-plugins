---
name: trust-account
description: The client trust account (CTA). Use when someone asks about trust balances, a client's or matter's trust ledger, whether any client ledger is below zero, the monthly three-way reconciliation, settlement funds, liens, closing statements or disbursements.
---

# Client trust account (CTA)

Follow `legal-practice` first. Trust money belongs to clients. **Never add it to, or show it
in the same total as, the firm's own money.** Call it "trust" every time.

## Checks to answer with

- **Client ledgers below zero** (G7, limit 0): count ledger rows with
  `matter_ledger_balance < 0` and matters with `trust_balance < 0`. If both are 0, say "No
  client ledger is below zero." If not, list each matter and its balance, and say it must be
  corrected today and reported to the responsible partner.
- **Monthly three-way reconciliation** (G6, signed off by the 10th, difference 0.00): the last
  three `trust_reconciliations` rows: month, difference, status, signed off when and by whom.
  Say "Within target" or "Late by N days" (signed off after the 10th of the next month).
- **One matter's ledger**: its transactions, newest first (date, type, in, out, running
  balance), and the matter's `trust_balance`.
- **Largest balances held**: `SELECT matter_id, matter_caption, trust_balance FROM legal.matters WHERE trust_balance > 0 ORDER BY trust_balance DESC LIMIT 10`.

## Settlements

For a settled matter: `settlements_and_liens` (status, gross, fee basis and rate, fee, costs
reimbursed, liens, net to client), its `liens` (holder, claimed, agreed, paid, status) and its
`closing_statements` (drafted, approved by, client signed). The disbursement clock runs from
`funds_cleared_date` to `disbursement_date`: target under 10 days, limit 21 days (firm policy
on "promptly", Rule 1.15). State it as "Cleared 13 Aug · 6 days · limit 21".

Approving a closing statement or a disbursement is a partner's decision. You show the
figures, exactly as stored; you never approve, and you never compute a different net.
