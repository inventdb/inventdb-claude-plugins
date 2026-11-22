---
name: time-entry
description: Record time. Use when someone wants to log, enter, record or bill time on a matter ("log 0.4 on MT-2761 for a call with opposing counsel"), turn notes or a calendar of their day into time entries, or check what time they have not yet entered.
---

# Time entries

Follow `legal-practice` first. You draft time entries from what the person tells you; they
approve each one before anything is written.

## Draft each entry

| Field | Where it comes from |
|---|---|
| `time_entry_id` | next key: `SELECT time_entry_id FROM legal.time_entries ORDER BY time_entry_id DESC LIMIT 1`, plus one (`TE-134265` after `TE-134264`) |
| `date` | the day the work was done; ask if unclear |
| `timekeeper_id`, `timekeeper`, `role` | the person (or who they name), from their own past entries: `SELECT timekeeper_id, timekeeper, role FROM legal.time_entries WHERE timekeeper LIKE '%<name>%' LIMIT 1` (every timekeeper role reads time entries; `legal.timekeepers` is closed to attorneys and paralegals) |
| `matter_id`, `client_id`, `matter_caption`, `practice_area`, `phase` | the matter row |
| `hours` | **the person's number**, in tenths (0.1 h steps). Never estimate hours. If they give minutes, convert and show it ("25 min = 0.5 h, rounded up to the tenth") and let them confirm |
| `narrative` | their words, tidied into one billing sentence: what was done and why, no internal remarks |
| `task_code`, `task_description` | UTBMS task (`L-` codes) from `SELECT code, value FROM legal.lookups WHERE list = 'UTBMS Litigation Task'`; for advisory work leave blank |
| `activity_code`, `activity_description` | UTBMS activity (`A-` codes) from `list = 'UTBMS Activity'` |
| `standard_rate`, `billed_rate` | the rate on their latest entry: `SELECT standard_rate FROM legal.time_entries WHERE timekeeper_id = 'TK-..' ORDER BY date DESC LIMIT 1` (or `standard_rate_2026` from `legal.timekeepers` where the person may read it) |
| `value_at_standard_rates` | computed in SQL, not by you: `SELECT ROUND(<hours> * <rate>, 2) AS value FROM legal.lookups LIMIT 1` |
| `billable` | `true` unless they say otherwise (then `non_billable_reason`) |
| `billed` | `false`; `invoice_no` empty |
| `date_entered` | today (the as-at date in the demo); `entry_lag_days` = days from `date` to `date_entered`; `locked` = `false` |

Suggested codes are suggestions: say "suggested" beside them.

If the person cannot read cost rates or timekeepers (their access refuses it), leave the rate
and value fields out and say billing will price the entry.

## Show, confirm, write

Show the draft as a table, one row per entry, with the total hours. Wait for a plain yes, or
apply their corrections. Then, per entry, `propose_insert` into `legal.time_entries` and
`commit`. Report the `TE-` keys written.

Entries older than 7 days are locked by firm policy: if `date` is more than 7 days before
today, say it needs a billing partner's approval and do not write it.

## Unentered time

To show what someone has entered for a day:
`SELECT time_entry_id, matter_id, hours, narrative FROM legal.time_entries WHERE timekeeper_id = 'TK-..' AND date = '<date>'`.
G4 (time entered by the next business day, target 90%) is in the `docket` skill.
