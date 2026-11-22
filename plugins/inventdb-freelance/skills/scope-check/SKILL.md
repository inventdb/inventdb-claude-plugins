---
name: scope-check
description: Check a client request, or the work already logged, against the engagement's signed SOW. Use when someone asks "is this in scope?", "can they ask for this?", "am I doing work I'm not paid for?", mentions scope creep, or wants a change request drafted.
---

# Scope check

Uses `freelance-basics`. The signed SOW decides; the consultant decides what to do about it.

## A new request

1. Find the engagement (`freelance.engagements` by client company or title; `client_id` joins
   `freelance.clients`).
2. Read the SOW: `attach_search` with `type: "documents"` and the request's words, then `attach_read`
   on the engagement's `sow_file`. Find section 1 (in scope) and section 2 (out of scope).
3. Also read `SELECT scope_item_id, item, in_scope FROM freelance.scope_items WHERE engagement_id = '...'`.
4. Answer in three lines: **In scope**, **Out of scope** or **Not mentioned**, quoting the SOW's
   words and naming the section. "Not mentioned" is not "in scope": say the SOW is silent.
5. If out of scope or not mentioned, offer a change request: hours estimate (ask the consultant if
   they have not given one), rate = the engagement's `overage_rate` (or `hourly_rate`), quoted amount
   = hours x rate, computed in SQL. After a plain yes, `propose_insert` into `change_requests`
   (`change_request_id` next after the highest, `requested_on` today, `scope_decision` `Out`, `status`
   `Pending`), then `commit`. Offer a short note to the client; the consultant sends it.

## Work already logged outside the SOW

For one engagement, list its out-of-scope items (`in_scope = false`) and look for time logs whose
`task` matches their words (`LIKE`). Report each log (key, date, task, hours) and the total hours from
`SUM`. On a fixed fee these hours are unpaid: say so, with the hours x `overage_rate` the SOW allows for
approved changes. Check `change_requests` for an approved one that covers them before calling it
scope creep.

## Pending change requests

`SELECT change_request_id, engagement_id, requested_on, request, estimate_hours, quoted_amount FROM freelance.change_requests WHERE status = 'Pending' ORDER BY requested_on`,
with days waiting from `DATEDIFF`.
