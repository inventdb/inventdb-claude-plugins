---
name: timesheet
description: Time entries for consulting work - logging time, weekly timesheets, budget and fee cap against hours used, unbilled time and drafting an invoice. Use for "log 2 hours on the lease review", "my timesheet this week", "how much of the budget is left on Willowmere?", "what's unbilled?", "draft the November invoice".
---

# Timesheet and budget

Uses `consulting-basics`. Hours in quarter hours; money in US dollars with two decimals; every total from SQL.

## Logging time

Draft: `entry_id` next after the highest, `date` (today unless given), consultant, engagement, workstream, task,
`hours`, `rate` (the engagement's `rate_principal` for its lead, `rate_analyst` for others, unless told), `amount` =
hours x rate computed in SQL, `billable` true, `invoice_no` empty. After a plain yes, `propose_insert` and `commit`.

## Timesheet

For a week (Monday to Sunday) or a month: hours by consultant and engagement (`GROUP BY consultant, engagement_id`),
and the entries behind them on request.

## Budget

Hours and fees used against `budget_hours` and `fee_cap`; what is left; the pace so far (hours a working day since
`start_date`) and where it lands by the deadline at that pace, computed in SQL. Over or likely over the cap: say so,
with the numbers, and offer a short note to the client before the work continues; the consultant decides.

## Unbilled and invoicing

Unbilled time by engagement (recipe in `references/sql.md`). An invoice draft for a period: the entries, hours and
amount (SQL), `due_on` = issued + 30 days unless the engagement says otherwise. Creating the invoice row and setting
`invoice_no` on its entries happen after a plain yes.
