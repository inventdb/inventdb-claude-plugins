# SQL on the InventDB Legal workspace

Call the connector's `sql` tool with one `SELECT`. Tables are `legal.<type>`. Every recipe
below was run against the synthetic demo workspace (as at 19 Aug 2026); substitute your date.

## Dialect

- Works: `WHERE`, `AND`/`OR` with parentheses, `IN (...)`, `IN (SELECT ...)`, `LIKE` (case
  insensitive, `%` wildcard), `BETWEEN`, `JOIN ... ON`, `GROUP BY`, `ORDER BY`, `LIMIT`,
  `COUNT`, `SUM`, `AVG`, `MIN`/`MAX` on numbers and dates, `ROUND(x, 2)`.
- Dates compare as text: `due_date <= '2026-09-03'`.
- Booleans: `billable = true`, `billed = false`, `in_court = true`.
- **Not available**: `CASE WHEN`; a subquery in `FROM`; `MAX`/`MIN` of a text column. To find
  the highest key, `ORDER BY time_entry_id DESC LIMIT 1`.
- **Write grouped queries in exactly these forms:**
  - Filter groups only as `HAVING SUM(col) <op> <number>` (or `COUNT(*)`, `AVG(col)`). To compare
    two totals per group, or filter on a computed value, return the per-group totals and compare
    them in a second step.
  - Order a grouped result by the aggregate expression itself (`ORDER BY SUM(x) DESC`), never by
    its alias, and round only in the select list.
  - A grouped total that goes into a report is reconciled once against the ungrouped `SUM` with
    the same `WHERE`, and both are shown to agree.
- Write "not yet billed" and similar filters as `IS NULL` together with a condition every row
  meets: `WHERE invoice_no IS NULL AND hours > 0`.
- Day counts: `DATEDIFF(DATE('2026-11-20'), due_on)` (days from `due_on` to that date). Wrap a date
  written as text in `DATE(...)`.
- Search record fields with `LIKE`. Search files by meaning with `attach_search`; `MEANING()`
  is not for record fields.
- Count rates as two queries (the part and the whole); do not compute them in SQL with
  `CASE`. Then divide the two counts in one more query, for example
  `SELECT ROUND(22599 * 100.0 / 34269, 1) AS pct FROM legal.lookups LIMIT 1`.

## Recipes

Docket, next 15 days (as at 19 Aug 2026):
```sql
SELECT deadline_id, matter_id, matter_caption, description, due_date, priority, owner, owner_name, day_type, authority
FROM legal.deadlines_and_sol
WHERE status = 'Open' AND due_date <= '2026-09-03'
ORDER BY due_date LIMIT 100
```
Late (open and past due): `... WHERE status = 'Open' AND due_date < '2026-08-19'`.

Court calendar, next 14 days:
```sql
SELECT event_id, date, time, matter_id, matter_caption, event_type, in_court, court_location, appearing_name
FROM legal.court_calendar
WHERE event_status = 'Scheduled' AND date BETWEEN '2026-08-20' AND '2026-09-02'
ORDER BY date, time LIMIT 100
```

Goal measures:
- G1, statute of limitations deadlines met (target 100%, limit 0 missed):
  `SELECT status, COUNT(*) AS n FROM legal.deadlines_and_sol WHERE category = 'Statute of Limitations' GROUP BY status`
  Missed = `Completed late`, plus `Open` ones past due.
- G2, deadlines met on time (target 99.5%): `Completed` over `Completed` + `Completed late`,
  from `SELECT status, COUNT(*) AS n FROM legal.deadlines_and_sol GROUP BY status`.
- G4, time entered by the next business day (target 90%, entries lock after 7 days):
  `SELECT COUNT(*) AS n FROM legal.time_entries WHERE entry_lag_days <= 1` over
  `SELECT COUNT(*) AS n FROM legal.time_entries`.

One matter's money:
```sql
SELECT ROUND(SUM(hours), 1) AS hours, ROUND(SUM(value_at_standard_rates), 2) AS value
FROM legal.time_entries WHERE matter_id = 'MT-3218' AND billable = true AND billed = false
```
```sql
SELECT ROUND(SUM(balance_due), 2) AS due, COUNT(*) AS invoices
FROM legal.invoices WHERE matter_id = 'MT-3218' AND balance_due > 0
```
Trust for one matter: `SELECT trust_balance FROM legal.matters WHERE matter_id = 'MT-3218'`,
and its ledger: `SELECT transaction_id, date, transaction_type, amount_in, amount_out,
matter_ledger_balance FROM legal.trust_ledger_cta WHERE matter_id = 'MT-3218' ORDER BY date DESC LIMIT 20`.

Receivables by age:
```sql
SELECT aging_bucket, COUNT(*) AS invoices, ROUND(SUM(balance_due), 2) AS due
FROM legal.invoices WHERE balance_due > 0 GROUP BY aging_bucket
```

Unbilled work (WIP) by matter, largest first:
```sql
SELECT matter_id, ROUND(SUM(value_at_standard_rates), 2) AS value, ROUND(SUM(hours), 1) AS hours
FROM legal.time_entries WHERE billable = true AND billed = false
GROUP BY matter_id ORDER BY SUM(value_at_standard_rates) DESC LIMIT 20
```

Trust: client ledgers below zero (G7, limit 0):
`SELECT COUNT(*) AS n FROM legal.trust_ledger_cta WHERE matter_ledger_balance < 0` and
`SELECT matter_id, matter_caption, trust_balance FROM legal.matters WHERE trust_balance < 0`.
Monthly reconciliation (G6, by the 10th, difference 0):
`SELECT reconciliation_id, month, difference, status, signed_off_at FROM legal.trust_reconciliations ORDER BY month DESC LIMIT 3`.

Conflict search on a name (both spellings and sound):
```sql
SELECT index_id, name, party_role, matter_id_or_lead_id, status
FROM legal.conflict_index
WHERE normalised_name LIKE '%ouyang%' OR phonetic_key LIKE '%O520%'
```

A record's `_id`, for `propose_update`:
`SELECT _id, deadline_id, status FROM legal.deadlines_and_sol WHERE deadline_id = 'DL-07950'`.
