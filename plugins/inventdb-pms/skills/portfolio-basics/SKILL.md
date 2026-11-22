---
name: portfolio-basics
description: Ground rules for working in a rental portfolio kept in InventDB (properties, owners, leases, tenants, rent and expense ledger, work orders, vendors, inspections, compliance, receipts). Use for any question or change about rents, arrears, leases, renewals, vacancies, maintenance, vendors, receipts, owner statements or year-end figures, before calling the InventDB connector.
---

# InventDB PMS: how to work in the portfolio's records

The portfolio lives in the person's own InventDB Serverless workspace, namespace `pms`. You reach
it through their **InventDB** connector (the one whose tools include `sql`, `search`,
`propose_insert`, `propose_update`, `commit`, `attach_search`, `attach_read`, `bulk_upload_url`,
`upload_check`). If no such connector is connected, say: "Connect your InventDB workspace first:
Settings > Connectors > Add custom connector, with your workspace's /mcp address." and stop.

## Records and keys

- Property `P-NNNN`, owner `O-NNNN`, lease `L-NNNN`, tenant `T-NNNN`, work order `WO-NNNNN`,
  vendor `V-NNNN`, inspection `I-NNNN`. Ledger lines (`pms.transactions`) have no key of their own;
  their `reference` names what they came from (a work order, a payment).
- Show business keys and addresses, never InventDB `_id` values. Use an `_id` only as the `id` of
  `propose_update`, after looking it up by the business key.
- Field names and exact status strings are in `references/data-model.md`. Read it before querying a
  type you have not used in this conversation.

## Numbers come from the records

- **Every count, total, balance and rate comes from SQL over stored records.** Add and round in the
  query (`SUM`, `COUNT`, `ROUND(x, 2)`), never in your head. Say the scope in words ("November 2026,
  all 50 properties"). Offer "show the query" after a table of figures.
- **Deposits are the tenant's money, not income.** The ledger books security and pet deposits as
  `Income` lines (`account_category` `Security Deposit`, `Pet Deposit`). Leave them out of every
  income, profit or owner-payout figure, and show deposits held as their own line.
- US dollars, two decimals, thousands separators. Dates "20 Nov 2026" in prose, `2026-11-20` in
  tables.
- Write grouped queries only in the forms `references/sql.md` gives.

## Clocks

Count against **today**, unless the workspace is the synthetic Virginia demo portfolio, whose
records stop at **20 Nov 2026**: then today is 20 Nov 2026 for every clock and every date you write, whatever
the calendar says, and you say "as at 20 Nov 2026". A clock is
time against its limit: "lease ends in 3 days", "rent 15 days late (grace 5)", "certificate lapsed
12 days ago". Never a bare date for something due.

## Changing records

Nothing is written on your own judgement:
1. Draft the change as a short table: the record, each field and its new value, and the money.
2. Wait for a plain yes. A request such as "record it" asks for the draft: show it and ask; the yes
   comes after the person has seen it.
3. `propose_insert` / `propose_update`, then `commit` with the returned `proposal_id` (`cancel` if
   they change their mind). Report what was written.

Never delete records. Never change an amount the records already settle (a paid rent line, an owner
payout).

## Bringing data and files in

Files never pass through the chat. For spreadsheets, receipts or lease PDFs, follow the
`bring-data-in` skill.

## Writing

Short, factual, present tense, sentence case, no emoji. A notice or letter you draft is a draft:
say "Draft for your review"; the person sends it. Never threaten eviction or legal action, and never
state what the law requires; name the lease term instead (grace days, late fee).
