# SQL on the InventDB Recruiter workspace

One `SELECT` per call to the connector's `sql` tool; tables are `recruiting.<type>`. Recipes were run on the
synthetic demo as at 20 Nov 2026.

## Forms to use

- `WHERE`, `AND`/`OR` with parentheses, `IN`, `NOT IN (SELECT ...)`, `LIKE` (case insensitive), `BETWEEN`,
  `JOIN ... ON`, `GROUP BY`, `ORDER BY`, `LIMIT`, `COUNT`, `SUM`, `AVG`, `MIN`/`MAX` on numbers and dates,
  `ROUND(x, 2)`.
- Not available: `CASE WHEN`; a subquery in `FROM`; `MAX`/`MIN` of a text column.
- Grouped queries: filter groups only as `HAVING COUNT(*) <op> <number>`; order by the aggregate itself
  (`ORDER BY COUNT(*) DESC`), never its alias.
- Write "unpaid" and similar filters as `IS NULL` together with a condition every row meets:
  `WHERE paid_on IS NULL AND fee_amount > 0`.
- In a join, columns come back named with their table alias (`p.fee_amount`); add `AS fee_amount` to name them.
- Day counts: `DATEDIFF(DATE('2026-11-20'), invoiced_on)` (days since), `DATEDIFF(guarantee_end, DATE('2026-11-20'))`
  (days to go).

## Recipes

The highest key, for the next one: `SELECT submission_id FROM recruiting.submissions ORDER BY submission_id DESC LIMIT 1`
(the same for `candidate_id`, `note_id`, `placement_id`).

Follow-ups overdue (live submissions whose next step has passed):
```sql
SELECT s.submission_id AS submission_id, s.role_id AS role_id, d.name AS candidate, s.stage AS stage, s.next_step_on AS next_step_on
FROM recruiting.submissions s JOIN recruiting.candidates d ON s.candidate_id = d.candidate_id
WHERE s.next_step_on < '2026-11-20' AND s.stage IN ('Screen', 'Submitted', 'Interview 1', 'Interview 2', 'Offer')
ORDER BY s.next_step_on
```
Due in the next 7 days: the same with `s.next_step_on BETWEEN '2026-11-20' AND '2026-11-27'`.

A role's pipeline: `SELECT stage, COUNT(*) AS n FROM recruiting.submissions WHERE role_id = 'JOB-104' GROUP BY stage`.

Candidates not yet put forward for a role, within its band:
`SELECT candidate_id, name, expected_salary, location, notice_weeks FROM recruiting.candidates WHERE candidate_id NOT IN (SELECT candidate_id FROM recruiting.submissions WHERE role_id = 'JOB-104') AND expected_salary <= 205000`
(narrow it with the ids from a meaning search: `AND candidate_id IN ('CAND-0004', 'CAND-0064')`).

Fees not yet paid, with the client's terms:
```sql
SELECT p.placement_id AS placement_id, c.company AS company, p.fee_amount AS fee, p.invoiced_on AS invoiced_on,
       c.terms_days AS terms_days, DATEDIFF(DATE('2026-11-20'), p.invoiced_on) AS days_since_invoice
FROM recruiting.placements p JOIN recruiting.roles r ON p.role_id = r.role_id JOIN recruiting.companies c ON r.company_id = c.company_id
WHERE p.paid_on IS NULL
```
Overdue when `days_since_invoice` is more than `terms_days`.

Guarantees still running: `SELECT placement_id, candidate_id, guarantee_end, DATEDIFF(guarantee_end, DATE('2026-11-20')) AS days_left FROM recruiting.placements WHERE guarantee_end >= '2026-11-20' ORDER BY guarantee_end`

Candidates gone quiet (not contacted in 90 days): `SELECT candidate_id, name, current_title, last_contacted FROM recruiting.candidates WHERE last_contacted < '2026-08-22' ORDER BY last_contacted`
