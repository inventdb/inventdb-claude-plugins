---
name: intake
description: New business. Use when a prospective client calls or writes, someone wants to open an intake lead, check where leads stand, see which leads wait for a decision, or decline or refer a lead.
---

# Intake and leads

Follow `legal-practice` first. A lead (`LD-` key) is a prospective client. Duties are owed to
prospective clients even if the firm declines, so a lead is never deleted.

## Open a lead

1. Run the `conflict-check` skill on the prospect and every other party they name, first.
2. Draft the lead: `lead_id` (next key: `SELECT lead_id FROM legal.intake_and_leads ORDER BY lead_id DESC LIMIT 1`, plus one),
   `date_received` (today, or the as-at date in the demo), `prospect_name` as "Last, First",
   `phone`, `referral_source`, `potential_claim_type`, `limitations_date` only if the person
   states it, `lead_status` = `New` (or `Conflict Check` while the check is open), `notes`.
3. Show it, wait for a plain yes, then `propose_insert` into `legal.intake_and_leads` and
   `commit`.

Never compute a statute of limitations date yourself. If the person asks, show the matching
rules from `legal.deadline_rules` (authority, period, computation) and say a lawyer confirms
the date.

## Where leads stand

`SELECT lead_status, COUNT(*) AS n FROM legal.intake_and_leads GROUP BY lead_status`, then the
open ones (`New`, `Conflict Check`, `Consultation`, `Engagement Sent`) with their age:
"received 2 days ago · SOL in 140 days" (G3: decision within 2 business days of receipt).

## Decline or refer

The decision is a lawyer's. When asked to record it: `lead_status` `Declined` (with
`decline_reason` from `SELECT value FROM legal.lookups WHERE list = 'Intake Decline Reason'`)
or `Referred Out` (with `referred_to`), and `decided_at`. Remind the person that a
non-engagement letter goes to the prospect.
