---
name: burn-and-rate
description: Retainer burn (hours used against included hours this month, overage to bill) and effective hourly rate per engagement against the consultant's target rate. Use for "how much of the retainer is left?", "am I over on Quillmere?", "what am I really earning per hour?", "which client pays worst?".
---

# Retainer burn and effective rate

Uses `freelance-basics`. All hours and amounts from SQL.

## Retainer burn this month

For each `Active` engagement with `kind = 'Retainer'`:
- hours used this month: `SUM(hours)` from `time_logs` with `date >= '<first of month>'`;
- included hours: `included_hours_per_month`; left = included minus used (one more query if needed);
- working days left in the month, counted from today;
- over the included hours: overage hours x `overage_rate` is what to bill on the next invoice, and
  the SOW says the client gets notice first. Offer the notice as a draft.

Show one row per retainer: engagement, client, used, included, left, overage to bill.

## Effective hourly rate

Use the recipe in `references/sql.md` (`freelance-basics`): billed amount over the hours billed for
retainer and hourly work; fixed fee over every hour logged for fixed-fee work (a completed fixed fee is
final; an active one is "so far"). Show each engagement with its rate, its `target_hourly_rate` and
"above" or "below target". Name the hours and the amount behind each rate.

Retainer hours not used in a month are not carried over unless the SOW says so; read the SOW before
saying otherwise.
