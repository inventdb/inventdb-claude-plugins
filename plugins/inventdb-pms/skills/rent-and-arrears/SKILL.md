---
name: rent-and-arrears
description: Rent roll and arrears. Use when someone asks who has paid or not paid rent, who is late, what is owed, the monthly rent roll, vacancies, or wants late notices drafted or a rent payment recorded.
---

# Rent and arrears

Follow `portfolio-basics` first. Recipes are in `portfolio-basics/references/sql.md`.

## Who is late

1. Find active leases that started on or before the 1st and have no `Rent` ledger line dated in the
   current month (the as-at month in the demo). That list is the arrears for this month. Leases that
   started after the 1st owe nothing on the 1st: list them apart as "started this month".
2. For each: tenant, property (key and street), contract rent, and the clock: days since the 1st,
   against the lease's `grace_days`. Past the grace days, the lease's `late_fee` applies; say "late
   fee $110 applies (5 days' grace ended 6 Nov)". Before it, say "due, within grace".
3. Total the rent outstanding in SQL. Sort by amount, largest first.
4. Earlier months: a tenant may also owe earlier months. Check with the same query per month when the
   person asks for a full arrears history.

## Rent roll

Monthly contract rent of active leases, the count of leases, vacancies with their market rent, and
the gap between contract and market rent across the portfolio (SQL: `SUM(market_rent) -
SUM(contract_rent)` as two sums, then subtract).

## Notices

Draft a polite payment reminder per late tenant: amount, the month, the late fee and grace days as
the lease states them, and how to pay. "Draft for your review"; the person sends it. Never threaten
eviction and never cite law.

## Recording a payment

When the person says a tenant paid: draft one `pms.transactions` line: `date`, `type` `Income`,
`property_id`, `owner_id` (from the property), `account_category` `Rent`, `account` as the other
rent lines read (`SELECT account FROM pms.transactions WHERE account_category = 'Rent' LIMIT 1`),
`party_tenant_vendor` the tenant's name, `memo` "November 2026 rent", `amount`, `method`,
`reference`. Show it, wait for yes, then `propose_insert` and `commit`. A late fee is a separate
`Late Fee` line, only when the person says to charge it.
