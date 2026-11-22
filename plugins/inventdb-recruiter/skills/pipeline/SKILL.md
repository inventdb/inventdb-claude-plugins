---
name: pipeline
description: The recruiter's pipeline and follow-ups: overdue and upcoming next steps, each role's stages, candidates gone quiet, and moving a submission to its next stage. Use for "who do I need to chase?", "what's happening on JOB-108?", "my week", "move Quinn to offer", "who haven't I spoken to in a while?".
---

# Pipeline and follow-ups

Uses `recruiter-basics`.

## Who to chase

The overdue recipe in `references/sql.md`, oldest first, with days overdue (`DATEDIFF`) and the role
title. Offers first, then later interviews, then the rest: an offer left waiting is the likeliest to be
lost. Then what is due in the next 7 days. Offer a short follow-up draft for each (to the candidate or
the client contact, whichever owes the next step); the recruiter sends them.

## One role

Stage counts for the role, each live candidate with their stage and next step, and the latest
interview notes (`recruiting.interview_notes` for the role, newest first). Say plainly if nothing is
past `Submitted` for a role open more than 30 days.

## Gone quiet

Candidates not contacted in 90 days, with their current title. Offer a short check-in draft.

## Moving a stage

Find the submission's `_id` (`SELECT _id, submission_id, stage, next_step_on FROM recruiting.submissions WHERE submission_id = '...'`),
show the change (new stage, new next step date; `Rejected` and `Withdrawn` clear the next step), and
after a plain yes `propose_update` and `commit`. An interview note from the recruiter goes in
`interview_notes` the same way. `Placed` is recorded with a placement (see `placements-and-fees`).
