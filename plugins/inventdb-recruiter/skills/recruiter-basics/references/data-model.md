# InventDB Recruiter data model (namespace `recruiting`)

Query a type as `recruiting.<type>`. Dates compare against `'YYYY-MM-DD'` text.

**companies** (`company_id` CO-NN): company, industry, **fee_pct** (the placement fee, 0.20 = 20% of first-year
salary), contact, email, phone, **terms_days** (days to pay a fee invoice).

**roles** (`role_id` JOB-NNN): company_id, title, **must_have** (the requirements, separated by `;`),
location, remote (`Remote`, `Hybrid`, `On site`), salary_min, salary_max, opened_on, **status** (`Open`,
`Filled`).

**candidates** (`candidate_id` CAND-NNNN): name, email, phone, current_title, current_employer, location,
years_experience, skills (comma separated), expected_salary, notice_weeks, source (`Referral`, `Inbound`,
`Sourced`, `Event`), **last_contacted**, status, **resume_file** (file name in `resumes`).

**submissions** (`submission_id` SUB-NNN): role_id, candidate_id, submitted_on, **stage** (`Screen`,
`Submitted`, `Interview 1`, `Interview 2`, `Offer`, `Placed`, `Rejected`, `Withdrawn`), **next_step_on**
(empty once closed). Live = Screen, Submitted, Interview 1, Interview 2 or Offer.

**interview_notes** (`note_id` NOTE-NNN): candidate_id, role_id, date, note.

**placements** (`placement_id` PLC-NN): submission_id, role_id, candidate_id, start_date, salary, fee_pct,
**fee_amount**, invoiced_on, **paid_on** (empty = unpaid), **guarantee_end** (the replacement guarantee:
if the person leaves before this date, the recruiter owes a replacement).

**resumes**: a files-only type holding one resume per candidate (find with `attach_search`, read with
`attach_read`).
