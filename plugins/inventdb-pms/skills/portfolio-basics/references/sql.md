# SQL on the InventDB PMS workspace

Call the connector's `sql` tool with one `SELECT`; tables are `pms.<type>`. The recipes were run on
the synthetic demo portfolio as at 20 Nov 2026; substitute your date.

## Forms to use

- `WHERE`, `AND`/`OR` with parentheses, `IN (...)`, `IN (SELECT ...)`, `NOT IN (SELECT ...)`,
  `LIKE` (case insensitive), `BETWEEN`, `JOIN ... ON`, `GROUP BY`, `ORDER BY`, `LIMIT`, `COUNT`,
  `SUM`, `AVG`, `MIN`/`MAX` on numbers and dates, `ROUND(x, 2)`.
- Not available: `CASE WHEN`; a subquery in `FROM`; `MAX`/`MIN` of a text column.
- Grouped queries: filter groups only as `HAVING SUM(col) <op> <number>`; order a grouped result by
  the aggregate itself (`ORDER BY SUM(amount) DESC`), never by its alias; round only in the select
  list. To compare two totals, return both and compare in a second step.
- Write "not yet paid" and similar filters as `IS NULL` together with a condition every row
  meets: `WHERE paid_on IS NULL AND amount > 0`.
- Day counts: `DATEDIFF(DATE('2026-11-20'), due_on)` (days from `due_on` to that date). Wrap a date
  written as text in `DATE(...)`.
- Arithmetic on two figures you already have: `SELECT ROUND(13989 - 3833.16, 2) AS net FROM pms.owners LIMIT 1`.

## Recipes

Rent roll:
`SELECT ROUND(SUM(contract_rent), 2) AS monthly_rent, COUNT(*) AS leases FROM pms.leases WHERE status = 'Active'`
and vacancies: `SELECT property_id, street, city, market_rent FROM pms.properties WHERE status = 'Vacant'`.

Who has not paid this month's rent (as at 20 Nov 2026):
```sql
SELECT lease_id, property_id, tenant_name, contract_rent, late_fee, grace_days, lease_start
FROM pms.leases
WHERE status = 'Active' AND lease_start <= '2026-11-01'
  AND property_id NOT IN (SELECT property_id FROM pms.transactions
                          WHERE account_category = 'Rent' AND date >= '2026-11-01')
```
A lease that started after the 1st owes no rent for that month on the 1st: list those apart as
"started this month". Days late = days since the 1st minus `grace_days`; a late fee applies after
the grace days.

Leases ending in the next 90 days:
`SELECT lease_id, property_id, tenant_name, lease_end, contract_rent, market_rent, renewal_type FROM pms.leases WHERE lease_end <= '2027-02-18' ORDER BY lease_end`

Open work orders, oldest first:
`SELECT wo, property_id, category, issue, priority, status, vendor, est_cost, date_opened FROM pms.work_orders WHERE status <> 'Completed' ORDER BY date_opened`

Vendors whose certificate of insurance lapses within 60 days (or has lapsed):
`SELECT company, trade, coi_expiry FROM pms.vendors WHERE coi_expiry <= '2027-01-19' ORDER BY coi_expiry`

Policy renewals due: `SELECT property_id, insurance_carrier, policy, policy_expiry, status FROM pms.compliance WHERE status <> 'Compliant'`

An owner's month (income and expenses by category, deposits apart):
```sql
SELECT type, account_category, ROUND(SUM(amount), 2) AS total
FROM pms.transactions
WHERE owner_id = 'O-1001' AND date >= '2026-10-01' AND date < '2026-11-01'
GROUP BY type, account_category
```

A property's year to date, by category (Schedule E style):
```sql
SELECT type, account_category, ROUND(SUM(amount), 2) AS total
FROM pms.transactions
WHERE property_id = 'P-5001' AND date >= '2026-01-01' AND date <= '2026-11-20'
GROUP BY type, account_category ORDER BY SUM(amount) DESC
```

A record's `_id`, for `propose_update`: `SELECT _id, wo, status FROM pms.work_orders WHERE wo = 'WO-30019'`.
