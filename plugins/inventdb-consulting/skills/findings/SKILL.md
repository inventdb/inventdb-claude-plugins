---
name: findings
description: The findings register and the engagement's status against its deadline - red flags by severity, checklist coverage, documents not yet reviewed, overdue requests, and recording or updating a finding. Use for "red flags", "where are we on Willowmere?", "what's still open before the deadline?", "record that as a finding", "mark F-002 resolved".
---

# Findings and status

Uses `consulting-basics`.

## Status of an engagement

In one answer, as at today, each part from SQL (recipes in `references/sql.md`):
1. The clock: days to the due diligence deadline, and to closing. Any checklist item past its due date and not done is
   the first thing said, with what it means (for example a title objection deadline that has passed).
2. Open findings by severity, highest first, each with its key, title and source.
3. Checklist: items not done by workstream; documents received and not yet reviewed.
4. Requests to the seller overdue, with days late.
5. Budget: hours and fees used against the budget and the fee cap.
End with the three things that most need doing before the deadline.

## Severity (a suggestion; the consultant decides)

- **High**: could stop the deal, or materially change the price, or leaves a liability that survives closing
  (a purchase right held by a tenant, a rent the documents contradict, a known contamination).
- **Medium**: a cost or risk to price, negotiate or fix before closing.
- **Low**: housekeeping, or a point to confirm.

## Recording a finding

Draft: `finding_id` (next after the highest), engagement, workstream, severity with its reason, title, `doc_id`,
`page`, `quote` (the document's exact words), impact, `amount` (from the document or computed in SQL, or empty),
recommendation, `status` `Open`, `raised_on` today. Check the register for a finding that already covers it first.
After a plain yes, `propose_insert` and `commit`. Updating a status (`Raised with seller`, `Resolved` with
`resolved_on`, `Accepted risk`) is the same, with `propose_update`.

A report shows the register: an issue that is not in the register is not in the report.
