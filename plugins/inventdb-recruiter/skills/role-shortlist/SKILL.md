---
name: role-shortlist
description: Build a shortlist for an open role from the recruiter's own candidates and resumes, check fit against the must-haves, the salary band and location, and put chosen candidates forward. Use for "shortlist for JOB-104", "who fits the DevOps role?", "submit these three", or "who should I send to Palisade?".
---

# Role shortlist

Uses `recruiter-basics` and `candidate-search`.

1. Read the role: `SELECT role_id, company_id, title, must_have, location, remote, salary_min, salary_max, status FROM recruiting.roles WHERE role_id = '...'`.
   A `Filled` role takes no new candidates: say so and stop.
2. Search the resumes by meaning for the must-haves (one search per distinct requirement if they are
   unrelated), as in `candidate-search`.
3. Remove anyone already put forward for this role (the "not yet put forward" recipe in
   `references/sql.md`), and show the band check: expected salary against `salary_max` (above the band
   is not a no, but say it), location against the role's location and `remote`, notice weeks.
4. Present the shortlist as a table: candidate, evidence quoted from the resume for each must-have
   (or "not shown"), salary against band, location fit, notice, last contacted. The recruiter chooses.
5. Putting someone forward: after a plain yes, `propose_insert` into `submissions` (`submission_id`
   next after the highest, `submitted_on` today, `stage` `Submitted`, `next_step_on` today + 5 days),
   then `commit`. Offer the client email with each candidate's evidence; the recruiter sends it.
