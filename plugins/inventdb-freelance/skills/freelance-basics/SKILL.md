---
name: freelance-basics
description: Ground rules for a consultant's practice kept in InventDB (clients, engagements, signed SOWs, scope items, time logs, change requests, deliverables, invoices). Use for any question or change about clients, retainers, scope, hours, rates, invoices, overdue payments or deliverables, before calling the InventDB connector.
---

# InventDB Freelance: how to work in the practice's records

The practice lives in the consultant's own InventDB Serverless workspace, namespace `freelance`.
You reach it through their **InventDB** connector (tools include `sql`, `propose_insert`,
`propose_update`, `commit`, `attach_search`, `attach_read`, `bulk_upload_url`, `upload_check`). If no
such connector is connected, say: "Connect your InventDB workspace first: Settings > Connectors >
Add custom connector, with your workspace's /mcp address." and stop.

## Records

- Client `CLT-NN`, engagement `ENG-NNN` (a retainer, an hourly engagement or a fixed-fee project, each
  with a signed SOW), scope item `SCP-NNN`, time log `TL-NNNN`, change request `CR-NNN`, deliverable
  `DLV-NNN`, invoice `INV-YYYY-NNN`.
- The signed SOWs are files in the `documents` type (one per engagement, file named in
  `engagements.sow_file`). The SOW is the contract: when its text and a scope item disagree, the SOW
  wins; say so.
- Fields and exact values are in `references/data-model.md`; SQL forms and recipes in
  `references/sql.md`.

## Numbers come from the records

- Every hour, amount, rate and balance comes from SQL (`SUM`, `COUNT`, `ROUND(x, 2)`). You never add
  figures yourself. Say the scope ("ENG-001, 1 to 20 Nov 2026").
- Hours in quarter hours; money in US dollars with two decimals.
- Clocks count from today, or from **20 Nov 2026** in the synthetic Lindqvist Studio demo ("as at 20
  Nov 2026"): "invoice 51 days overdue", "29 of 40 included hours used, 11 left".

## Changing records

Draft the change as a table, wait for a plain yes, then `propose_insert` / `propose_update` and
`commit`. A request such as "record it" or "mark it paid" asks for the draft: show it and ask; the
yes comes after the consultant has seen it. Never delete records; never change an invoice's amount after it is issued. A message or
invoice email you draft is a draft: the consultant sends it.

## Scope decisions

You compare a request with the SOW and say what the SOW says, quoting it. Whether to do the work,
and at what price, is the consultant's decision.
