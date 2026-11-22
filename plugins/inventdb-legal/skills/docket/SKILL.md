---
name: docket
description: Show what is due. Use when someone asks what is on their docket, what is due today or this week, which deadlines are late or close, what hearings or court dates are coming up, or how the firm is doing on deadlines. Also use to mark a deadline complete.
---

# Today's docket

Follow `legal-practice` first (keys, clocks, numbers from SQL). Recipes are in
`legal-practice/references/sql.md`.

## Whose docket

- If the person names themself or a timekeeper ("my docket", "Anahit's docket"), scope to that
  timekeeper. Find the `TK-` key from the docket itself, which every docket role can read:
  `SELECT owner, owner_name, COUNT(*) AS n FROM legal.deadlines_and_sol WHERE owner_name LIKE '%<name>%' GROUP BY owner, owner_name`
  (`legal.timekeepers` and `legal.users` are closed to attorneys and paralegals). Then filter
  deadlines by `owner = 'TK-..'` and court events by `appearing_timekeeper = 'TK-..'`.
- If you cannot tell who they are, show the firm-wide docket and say so: "All owners. Tell me
  your name to see only yours."

## What to show, in this order

1. **Needs action**: open deadlines that are late, or due within 5 days of the as-at date.
2. **Coming up**: open deadlines due in 6 to 15 days.
3. **In court and out, next 14 days**: scheduled court calendar events. Mark in-court events
   ("in court") apart from depositions, interviews and signings.
4. **Goal measures** (only when asked how the firm or a person is doing): G1 statute of
   limitations deadlines met (target 100%, limit 0 missed), G2 deadlines met on time (target
   99.5%), G4 time entered by the next business day (target 90%, locked after 7 days). Show
   each as value, then target, then limit, then a word: "Within target" or "Under target by
   N points".

Each docket line: deadline key, matter key and caption, what is due, owner, priority, and the
clock: "due today", "1 day left", "3 days late". Add "(court days)" when `day_type` is
`Court`. Sort by due date, then priority (`Critical`, `High`, `Medium`).

If there is nothing in a group, say so in one line ("Nothing late."). Keep the list to what
fits a screen; say how many more there are and offer the rest.

## Marking a deadline done

When the person says a deadline is done:
1. Look it up by its `DL-` key and show it.
2. Draft the change: `status` = `Completed` if done on or before `due_date`, otherwise
   `Completed late` (the date decides, not you); `completed_date` = the date they give, or the
   as-at date.
3. After a plain yes: `SELECT _id ...` for the record, `propose_update` with only those two
   fields, then `commit`. Report "DL-07950 marked Completed on 19 Aug 2026."

Never mark a statute of limitations deadline `Vacated` or move a due date. Those are a
lawyer's decisions made outside this chat.
