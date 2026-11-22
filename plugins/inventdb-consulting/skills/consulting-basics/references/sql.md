# SQL on the InventDB Consulting workspace

One `SELECT` per call to the connector's `sql` tool; tables are `consulting.<type>`. Recipes were run on the synthetic
demo as at 20 Nov 2026.

## Forms to use

- `WHERE`, `AND`/`OR` with parentheses, `IN`, `NOT IN (SELECT ...)`, `LIKE` (case insensitive), `BETWEEN`,
  `JOIN ... ON`, `GROUP BY`, `ORDER BY`, `LIMIT`, `COUNT`, `SUM`, `AVG`, `MIN`/`MAX` on numbers and dates, `ROUND(x, 2)`.
- Not available: `CASE WHEN`; a subquery in `FROM`; `MAX`/`MIN` of a text column. The highest key, for the next one:
  `SELECT finding_id FROM consulting.findings ORDER BY finding_id DESC LIMIT 1`.
- Grouped queries: filter groups only as `HAVING COUNT(*) <op> <number>` or `HAVING SUM(col) <op> <number>`; order by
  the aggregate itself (`ORDER BY SUM(hours) DESC`), never its alias.
- Write "not yet invoiced" and similar filters as `IS NULL` together with a condition every row meets:
  `WHERE invoice_no IS NULL AND hours > 0`.
- In a join, columns come back named with their table alias; add `AS` to name them.
- Day counts: `DATEDIFF(dd_deadline, DATE('2026-11-20'))` (days left), `DATEDIFF(DATE('2026-11-20'), due_on)` (days late).
- Arithmetic on figures you already have: `SELECT ROUND(752400 + 118400, 2) AS x FROM consulting.engagements LIMIT 1`.

## Recipes

The engagement and its clock:
`SELECT engagement_id, title, purchase_price, dd_deadline, closing_date, budget_hours, fee_cap, DATEDIFF(dd_deadline, DATE('2026-11-20')) AS days_left FROM consulting.engagements WHERE engagement_id = 'ENG-2026-07'`

Open findings by severity: `SELECT severity, COUNT(*) AS n FROM consulting.findings WHERE engagement_id = 'ENG-2026-07' AND status <> 'Resolved' GROUP BY severity`

Checklist items not done, earliest due first:
`SELECT item_id, workstream, item, status, due_date FROM consulting.checklist WHERE engagement_id = 'ENG-2026-07' AND status <> 'Done' ORDER BY due_date`

Documents received but not reviewed:
`SELECT doc_id, title, workstream, received_on FROM consulting.documents WHERE engagement_id = 'ENG-2026-07' AND status = 'Received' ORDER BY received_on`

Requests overdue:
`SELECT request_id, request, due_on, DATEDIFF(DATE('2026-11-20'), due_on) AS days_late FROM consulting.requests WHERE engagement_id = 'ENG-2026-07' AND status IN ('Open', 'Partially received') AND due_on < '2026-11-20' ORDER BY due_on`

Rent roll totals and estoppel coverage (share of area with an estoppel):
`SELECT ROUND(SUM(monthly_rent), 2) AS monthly, SUM(sf) AS sf FROM consulting.rent_roll WHERE engagement_id = 'ENG-2026-07'`
and the same with `AND estoppel_received = true`; divide the two in one more query.

Budget: hours and fees used against `budget_hours` and `fee_cap`:
`SELECT ROUND(SUM(hours), 2) AS hours, ROUND(SUM(amount), 2) AS fees FROM consulting.time_entries WHERE engagement_id = 'ENG-2026-07'`

Unbilled time: `SELECT engagement_id, SUM(hours) AS hours, ROUND(SUM(amount), 2) AS fees FROM consulting.time_entries WHERE invoice_no IS NULL AND hours > 0 GROUP BY engagement_id`

A file's register row: `SELECT doc_id, title, status FROM consulting.documents WHERE file_name = '<file name from attach_search>'`
