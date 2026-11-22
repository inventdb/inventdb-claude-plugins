# SQL on the InventDB Freelance workspace

One `SELECT` per call to the connector's `sql` tool; tables are `freelance.<type>`. Recipes were run on the
synthetic demo as at 20 Nov 2026.

## Forms to use

- `WHERE`, `AND`/`OR` with parentheses, `IN`, `LIKE` (case insensitive), `BETWEEN`, `JOIN ... ON`,
  `GROUP BY`, `ORDER BY`, `LIMIT`, `COUNT`, `SUM`, `AVG`, `MIN`/`MAX` on numbers and dates, `ROUND(x, 2)`.
- Not available: `CASE WHEN`; a subquery in `FROM`; `MAX`/`MIN` of a text column.
- Grouped queries: filter groups only as `HAVING SUM(col) <op> <number>`; order by the aggregate itself
  (`ORDER BY SUM(hours) DESC`), never its alias; round only in the select list.
- Write "not yet invoiced" and "unpaid" filters as `IS NULL` together with a condition every row
  meets: `WHERE invoice_no IS NULL AND hours > 0`, `WHERE paid_on IS NULL AND amount > 0`.
- Day counts: `DATEDIFF(DATE('2026-11-20'), due_on)`. A rate is two figures: return both, then divide in
  one more query (`SELECT ROUND(56000 / 312.5, 2) AS rate FROM freelance.clients LIMIT 1`).

## Recipes

Unbilled hours by engagement, and the oldest unbilled date:
```sql
SELECT engagement_id, SUM(hours) AS hours, MIN(date) AS oldest
FROM freelance.time_logs WHERE invoice_no IS NULL AND hours > 0
GROUP BY engagement_id
```

A retainer's month against its included hours:
`SELECT ROUND(SUM(hours), 2) AS used FROM freelance.time_logs WHERE engagement_id = 'ENG-001' AND date >= '2026-11-01'`
with `included_hours_per_month` and `overage_rate` from `freelance.engagements`.

Effective hourly rate on retainer and hourly work: billed amount over the hours those invoices cover
`SELECT engagement_id, ROUND(SUM(amount), 2) AS billed, SUM(hours) AS hours FROM freelance.invoices WHERE hours > 0 GROUP BY engagement_id`;
on a fixed fee, `fixed_fee` over every hour logged on it
(`SELECT ROUND(SUM(hours), 2) AS h FROM freelance.time_logs WHERE engagement_id = 'ENG-004'`). Compare with
`target_hourly_rate`.

Overdue invoices:
`SELECT invoice_no, engagement_id, amount, due_on, DATEDIFF(DATE('2026-11-20'), due_on) AS days_overdue FROM freelance.invoices WHERE paid_on IS NULL AND due_on < '2026-11-20' ORDER BY due_on`

Hours logged against excluded work: compare `time_logs.task` with the engagement's out-of-scope items
`SELECT item FROM freelance.scope_items WHERE engagement_id = 'ENG-004' AND in_scope = false`, matching words
(`task LIKE '%SMS%'`).
