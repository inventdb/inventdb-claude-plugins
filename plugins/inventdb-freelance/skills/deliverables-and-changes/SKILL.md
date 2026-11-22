---
name: deliverables-and-changes
description: Deliverables due, late or delivered per engagement, logging time, and a weekly client update. Use for "what's due this week?", "what's late?", "mark the dashboard delivered", "log 2 hours on Brightmoor", "weekly client update".
---

# Deliverables and time

Uses `freelance-basics`.

## Deliverables

- Due soon: `SELECT deliverable_id, engagement_id, title, due_date, status FROM freelance.deliverables WHERE status <> 'Delivered' ORDER BY due_date`,
  with days to go (or days late) from `DATEDIFF`.
- A deliverable past its due date and not delivered is late whatever its `status` says; list it as
  late.
- Marking one delivered: `propose_update` of `status` `Delivered` and `delivered_on` today, after a plain
  yes.

## Logging time

Draft the log: next `time_log_id` (`SELECT time_log_id FROM freelance.time_logs ORDER BY time_log_id DESC LIMIT 1`),
date (today unless given), engagement, task, hours in quarter hours, `billable` true. Check the task
against the engagement's out-of-scope items first (`scope-check`) and warn if it matches one. After a
plain yes, `propose_insert` and `commit`.

## Weekly client update

For one engagement: hours this week and this month (`SUM`), deliverables delivered and due, pending
change requests, and the retainer's hours left. A draft; the consultant sends it.
