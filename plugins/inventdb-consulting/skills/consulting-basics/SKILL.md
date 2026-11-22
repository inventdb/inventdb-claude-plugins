---
name: consulting-basics
description: Ground rules for a consulting practice kept in InventDB (engagements such as a buyer's due diligence, the data room and document register, findings, requests to the other side, research notes, rent rolls, time entries, invoices and reports). Use for any question or change about an engagement, its documents, findings, deadlines, seller requests, research, time, budget or reports, before calling the InventDB connector.
---

# InventDB Consulting: how to work in the practice's records

The practice lives in the consultant's own InventDB Serverless workspace, namespace `consulting`. You reach it through
their **InventDB** connector (tools include `sql`, `attach_search`, `attach_read`, `attach_url`, `propose_insert`,
`propose_update`, `commit`, `bulk_upload_url`, `attach_upload_url`, `upload_check`). If no such connector is connected,
say: "Connect your InventDB workspace first: Settings > Connectors > Add custom connector, with your workspace's /mcp
address." and stop.

## The work

An engagement (`ENG-YYYY-NN`) is a piece of advisory work for a client, for example a buyer's due diligence on a
property under contract. Its goal: a decision-ready report for the client **before the deadline** (for due diligence,
the end of the due diligence period in the purchase agreement), with **every finding cited to a document and page**.
Everything else serves that: the document register, the findings register, the requests to the other side, the
research notes, the timesheet.

## Records

- Keys: engagement `ENG-YYYY-NN`, checklist item `DD-NN`, document `DOC-NNN`, finding `F-NNN`, request `RFI-NNN`,
  research note `RN-NN`, time entry `TE-NNNN`, invoice `INV-YYYY-NNN`, report `REP-<engagement>-<n>`.
- The files themselves: the seller's and third parties' documents in the files type `data_room`; the consultant's
  own reports in `deliverables`. The `documents` type is the register: one row per file, with its workstream, source,
  pages and review status.
- Fields and exact values: `references/data-model.md`. SQL forms and recipes: `references/sql.md`.

## Clocks

In the synthetic Willowmere Plaza demo (Marrow & Finch Advisory), **today is 20 Nov 2026**: use that date for every
clock, every "as at" and every date you write, whatever the calendar says, and say "as at 20 Nov 2026". In a real
workspace, today is today. Name the
deadline and the days left: "due diligence period ends 25 Nov 2026, 5 days left". A date in a document (an option
notice, an auto-renewal, an objection deadline) is checked against today and the closing date, and a date already
passed is said plainly.

## Numbers and quotes

- Counts, hours, fees and totals from the records come from SQL. A figure read from a document is quoted with its
  document key and page. Arithmetic on figures you already have goes through `sql` too
  (`SELECT ROUND(9350000 * 0.008865, 2) AS tax FROM consulting.engagements LIMIT 1`).
- Quote a document's exact words for every finding. Never state a term, amount or date a document does not show.

## Judgement

You read, compare, find and draft. Severity is a suggestion with its reason; the consultant decides. Legal
conclusions (whether a title exception is acceptable, whether a right of first refusal applies) are for the client's
counsel: say what the document says and who should decide. Drafts (emails to the seller, reports) are drafts until
the consultant says otherwise.

## Changing records

Draft the change as a table, wait for a plain yes, then `propose_insert` / `propose_update` and `commit`. A request such
as "record it" or "log it" asks for the draft: show it and ask; the yes comes after the consultant has seen it. Never
delete records or files.
