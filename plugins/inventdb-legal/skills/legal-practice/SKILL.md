---
name: legal-practice
description: Ground rules for working in the firm's InventDB Legal workspace. Use for any question or change about matters, clients, the docket, deadlines, court dates, time, costs, invoices, payments, the client trust account (CTA), settlements, liens, intake leads, conflicts or the firm's documents, before calling the InventDB connector.
---

# InventDB Legal: how to work in the firm's records

The firm's records live in an InventDB workspace, namespace `legal`. You reach it through the
**InventDB** connector (its tools are `sql`, `search`, `get`, `describe_type`, `schema`,
`propose_insert`, `propose_update`, `commit`, `cancel`, `attach_search`, `attach_read`,
`attach_url`, `bulk_upload_url`, `attach_upload_url`, `upload_check`, `bulk_insert_commit`,
`audit_log`, `undo`). Every call runs as the person who signed in. InventDB applies their own
grants on every query, including raw SQL.

## Who sees what

- If a query is refused or a type is missing, the person has no access to it. Say so in one
  sentence ("Your access does not include invoices.") and continue with what they can see.
  One refusal is the answer: do not query that type again in this conversation, and never
  work around a refusal by querying another type.
- Never say which role or tier someone has.
- Finance never reads documents. Intake never reads existing matters' documents, time or money.
  Attorneys and paralegals never read cost rates (`timekeepers`).

## Records and keys

- The core record is the **matter**, `MT-NNNN`. Other keys: client `CL-`, timekeeper `TK-`,
  time entry `TE-`, cost `CO-`, invoice `INV-YYYY-NNNN`, payment `PY-`, trust transaction
  `TR-`, court event `EV-`, deadline `DL-`, lead `LD-`, settlement `ST-`, lien `LN-`,
  closing statement `CS-`, document `DOC-`.
- Show people business keys, never InventDB `_id` values. Use `_id` only as the `id` argument
  of `propose_update`, after looking it up by the business key.
- Field names, types and exact status strings are in `references/data-model.md`. Read it
  before writing a query on a type you have not used in this conversation.

## Numbers come from the records

- **Every count, total, balance, rate or date comes from SQL over stored records.** Add,
  average and round in the query (`SUM`, `COUNT`, `ROUND(x, 2)`), never in your head. State
  the query's scope in words ("open deadlines due by 3 Sep, all owners").
- A figure you show can always be traced: after a table of figures, offer "Show the query".
- Money: US dollars, two decimals, thousands separators. Client trust money (CTA) is never
  added to the firm's own money; show it separately and call it trust.
- Time is billed in tenths of an hour (`0.4 h`).
- Dates: "20 Aug 2026" in prose; `2026-08-20` in tables.
- Read `references/sql.md` for the SQL forms to use and the tested recipes, and write grouped
  queries only in the forms it gives.

## Clocks

- Count a clock against **today**, unless the workspace is the synthetic Alvarado & Sung LLP
  demo, whose records stop at **19 Aug 2026**. In the demo, count from 19 Aug 2026 and say
  "as at 19 Aug 2026".
- A clock is time used against its limit: "3 days left", "2 days late", "SOL in 211 days".
  Never a bare date for something due.
- Say which days you count: a deadline's `day_type` is `Court` or `Calendar`. You count
  calendar days unless the court holiday list is used; say "calendar days" when it matters.

## Changing records

You never change a record on your own judgement.

1. Draft the change and show it to the person in a short table: the record key, each field
   and its new value, and the money or hours it carries.
2. Wait for a plain yes.
3. Then call `propose_insert` / `propose_update` and, with the returned `proposal_id`,
   `commit`. If the person changes their mind, `cancel`.
4. Report the key that was written. If something went wrong, `audit_log` and `undo` exist,
   and the person decides whether to use them.

Never delete records. Never change an amount the records compute (balances, totals, values at
standard rates): those come from the firm's billing and trust processes.

## Bringing data and files in

Bytes never go through the chat. For a spreadsheet or a folder of documents, follow the
`bring-data-in` skill.

## Writing

Calm, short, factual, present tense. Sentence case. No emoji, no exclamation marks. Use the
trade's words: matter, client, timekeeper, time entry, UTBMS code, costs and disbursements,
invoice, trust ledger (CTA), settlement, lien, court calendar, deadline, statute of
limitations (SOL), intake, lead, docket.
