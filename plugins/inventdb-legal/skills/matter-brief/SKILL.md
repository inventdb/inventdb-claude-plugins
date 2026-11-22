---
name: matter-brief
description: Brief someone on one matter. Use when asked about a specific matter (by MT- number, caption, client or opposing party), its status, what's next, its money, its trust balance, its deadlines, court dates, team or documents, or to prepare for a call or hearing on it.
---

# Matter brief

Follow `legal-practice` first. One matter at a time. If the person names a party or caption,
find the matter:
`SELECT matter_id, matter_caption, client_name, matter_status FROM legal.matters WHERE matter_caption LIKE '%<words>%' OR client_name LIKE '%<words>%' OR opposing_party LIKE '%<words>%' LIMIT 10`
and ask which one when there is more than one.

## The brief, in this order

1. **Header**: `MT-` key, caption, client (`CL-` key), track and practice area, responsible
   attorney, court and case number when litigated.
2. **The matter spine**: Intake → Opening → Open · <phase> → Resolved → Closing → Closed, with
   the current stage named from `matter_status` and, on Open, its `phase`. Write it as one
   line, for example `Intake ✓ → Opening ✓ → Open ✓ → Closing ● → Closed`.
3. **Next**: the next open deadline (key, what, due date, clock) and the next scheduled court
   event (date, time, type, in court or not). Then the statute of limitations date as a clock
   when the matter is not closed ("SOL in 189 days").
4. **Money** (only the parts the person's access allows; skip a part that is refused, saying
   so once):
   - unbilled time: hours and value at standard rates (billable, not yet billed);
   - receivables: balance due on open invoices, oldest age;
   - trust (CTA): the matter's trust balance, shown apart from the firm's money;
   - settlement, when there is one: status, gross, fee, liens, net to client, and the
     disbursement clock (funds cleared to disbursed: target under 10 days, limit 21).
5. **Team**: from `matter_team` (who, role on the matter).
6. **Watch**: open risk signals for the matter (code, signal, severity) when the person can
   read them.
7. **Files**: how many documents the matter has and the latest few (name, type, date), with
   privileged ones marked "privileged". Use `attach_search` with `type: "documents"` and the
   matter key as the query, or `legal.documents` by `matter_id`.

Every figure comes from a query (recipes in `legal-practice/references/sql.md`). About a dozen
queries make a brief; run the independent ones in parallel, and fetch rows once rather than
asking the same type several times:

1. the matter row (`SELECT * FROM legal.matters WHERE matter_id = 'MT-..'`);
2. its open deadlines (`status = 'Open'`, by `due_date`, `LIMIT 5`) and its statute of
   limitations deadline (`category = 'Statute of Limitations'`);
3. its scheduled court events (`event_status = 'Scheduled'`, by `date`, `LIMIT 3`);
4. time by timekeeper in one grouped query (`timekeeper`, `SUM(hours)`, unbilled value), with
   `ORDER BY SUM(hours) DESC` if you sort it;
5. open invoices (`balance_due > 0`);
6. when `trust_balance` is not 0 or the matter is settled: its settlement row, its liens and its
   closing statement (three queries);
7. `matter_team`, open `risk_signals`, and its `documents` rows (newest first, `LIMIT 5`).

Keep the brief to one screen. End with the single most useful next step for this matter, stated as a
fact ("The closing statement waits for approval; funds cleared 13 Aug.") and never as advice
on the law.
