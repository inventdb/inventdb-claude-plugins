# InventDB Legal data model (namespace `legal`)

Types and fields as imported from the InventDB Legal workbook (one type per sheet; field names
are the sheet's column headers in lower snake case). Query a type as `legal.<type>`.
Dates are stored as dates and compare against `'YYYY-MM-DD'` text. `true`/`false` fields are
booleans.

## The practice

**matters** (`matter_id` MT-NNNN): client_id, client_name, matter_caption, practice_area,
matter_type, track, fee_model, fee_terms, contingency_pre_suit, contingency_post_filing,
flat_fee_total, retainer_amount, replenish_threshold, rate_tier, volume_discount,
trust_required, court, court_short, case_number, judicial_officer, department, date_opened,
opened_at, date_filed, incident_trigger_date, limitations_authority, limitations_date,
opposing_party, opposing_counsel, insurance_carrier, claim_number, responsible_attorney (TK-),
responsible_attorney_name, originating_attorney, paralegal, legacy_status, **matter_status**,
stage, **phase**, date_closed, resolved_at, closed_at, disposition, pro_bono,
privileged_matter, fee_agreement_date, recorded_hours, recorded_value_at_standard_rates,
costs_advanced, fees_billed, collected, **trust_balance**, next_court_date.
- `matter_status`: `Opening`, `Open`, `Closing`, `Closed` (also `On Hold`, `Withdrawn` when used).
- `track`: `Civil litigation`, `Advisory and transactional`, `Family`, `Criminal defence`,
  `Probate and trusts`, `Bankruptcy`, `Workers' compensation`, `Appeals`.
- `phase` is the step inside `Open` (for example `Pleadings`, `Discovery`, `ADR`, `Trial`,
  `Drafting`, `Signing or decision`).

**clients** (`client_id` CL-NNNN): client_name, client_type, first_name, last_name,
entity_name, primary_contact, date_of_birth, preferred_language, address, city, state, zip,
phone, email, referral_source, intake_date, engagement_letter_date, conflict_check_date,
conflict_check_result, conflict_cleared_by, photo_id_verified, client_portal_enabled,
responsible_attorney, responsible_attorney_name, status, total_matters, open_matters,
last_matter_opened.

**timekeepers** (`timekeeper_id` TK-NN): name, first_name, last_name, initials, role,
billing_timekeeper, california_bar_number, bar_admission_date, date_hired,
standard_rate_2026, standard_rate_2025, standard_rate_2024, hourly_cost_rate,
annual_target_hours, utilization_target, recorded_hours_in_dataset,
billable_hours_in_dataset, recorded_value_at_standard_rates, matters_worked,
mcle_compliance_group, mcle_hours_completed, mcle_compliance_due, active.
Holds cost rates: attorneys and paralegals have no access.

**users** (`user_id` USR-NNNN): full_name, role_code, timekeeper_id, client_id, email, status,
mfa, last_login. Links a person to their timekeeper.

**matter_team**: matter_id, timekeeper_id, role_on_matter, from, to.
**ethical_walls** (`wall_id`): matter_id, timekeeper_id, reason, created_by, created_at.

## Intake and conflicts

**intake_and_leads** (`lead_id` LD-NNNN): date_received, prospect_name ("Last, First"), phone,
referral_source, potential_claim_type, limitations_date, days_to_limitations_at_intake,
disposition, **lead_status**, decline_reason, referred_to, referral_fee_arrangement,
written_client_consent_rule_1_5_1, consultation_fee, converted_client_id, matter_id,
screened_by, notes, conflict_checked_at, conflict_result, consultation_at, engagement_sent_at,
decided_at.
- `lead_status`: `New`, `Conflict Check`, `Consultation`, `Engagement Sent`, `Signed`,
  `Declined`, `Referred Out`.

**conflict_index** (`index_id` CX-NNNNNN): name, **normalised_name** ("first last", lower
case), **phonetic_key** (one 4-character sound code per name part, for example `B622` for
Barajas), **party_role**, matter_id_or_lead_id, status, since.
- `party_role`: `Client`, `Adverse party`, `Opposing counsel`, `Carrier`, `Lien holder`,
  `Prospective client`.

## Time, costs and billing

**time_entries** (`time_entry_id` TE-NNNNNN): date, timekeeper_id, timekeeper, role,
matter_id, client_id, matter_caption, practice_area, phase, task_code (UTBMS L-code),
task_description, activity_code (UTBMS A-code), activity_description, narrative, hours,
standard_rate, billed_rate, value_at_standard_rates, billable, non_billable_reason,
lodestar_eligible, gross_fee_amount, write_down, net_billed_amount, invoice_no, billed,
date_entered, entry_lag_days, locked.

**costs_and_disbursements** (`cost_id` CO-): date, matter_id, client_id, matter_caption,
practice_area, expense_code (UTBMS E-code), expense_category, vendor_payee, description,
amount, advanced_by_firm, recoverable, paid_from, receipt_reference, invoice_no,
billed_to_client, recovered_from_settlement.

**invoices** (`invoice_no` INV-YYYY-NNNN): matter_id, client_id, client_name,
matter_caption, fee_model, period_start, period_end, issue_date, due_date,
fees_at_billed_rates, write_downs, courtesy_discount, costs_billed, invoice_total,
prior_balance, applied_from_trust, payments_applied, **balance_due**, written_off,
written_off_by, **status**, days_outstanding, **aging_bucket**, delivery_method, note.
- `status`: `Open`, `Outstanding`, `Partially paid`, `Paid`, `Sent to collections`.
- `aging_bucket`: `Current (not yet due)`, `1-30 days`, `31-60 days`, `61-90 days`,
  `91-120 days`, `Over 120 days`, `Paid`.

**payments_and_receipts** (`payment_id` PY-): date, client_id, client_name, matter_id,
amount, deposited_to (operating or trust), method, payor, reference, description,
invoice_no, returned_nsf.

## Client trust account (CTA)

**trust_ledger_cta** (`transaction_id` TR-NNNNN): date, matter_id, client_id, client_name,
transaction_type, description, payee_payor, check_no, reference, amount_in, amount_out,
**matter_ledger_balance** (running, per matter), trust_account_balance (running, whole
account), bank_cleared_date, reconciliation_month.

**trust_reconciliations** (`reconciliation_id` RC-YYYY-MM): month, bank_statement_balance,
outstanding_deposits, outstanding_cheques, adjusted_bank_balance, journal_balance,
client_ledger_total, difference, status (`Signed Off`), prepared_by, signed_off_by,
signed_off_at.

**settlements_and_liens** (`settlement_id` ST-NNNN): matter_id, client_id, client_name,
matter_type, date_settled, **settlement_status** (`Agreed`, `Funds Received`,
`Funds Cleared`, `Disbursement Approved`, `Disbursed`), fee_basis, gross_settlement,
attorney_fee_rate, attorney_fee, costs_reimbursed_to_firm, liens_asserted, liens_claimed,
liens_paid, net_to_client, trust_deposit_date, funds_cleared_date, disbursement_date,
disbursement_approved_by, disbursement_approved_at, insurance_carrier, claim_number,
statutory_liens, lien_detail.

**liens** (`lien_id` LN-NNNNN): settlement_id, matter_id, lien_holder, lien_type,
amount_claimed, amount_agreed, amount_paid, status, reduction_basis, paid_on,
trust_transaction_id.

**closing_statements** (`statement_id` CS-NNNN): settlement_id, matter_id, gross, fee, costs,
liens, net_to_client, drafted_at, approved_by, approved_at, client_signed_at, document_id.

## Calendar and docket

**court_calendar** (`event_id` EV-NNNNN): date, time ("08:30"), matter_id, client_id,
matter_caption, case_number, event_type, in_court (true for a court appearance), court_location,
department, judicial_officer, appearing_timekeeper, appearing_name, deponent_witness,
outcome, continued_to, appeared, **event_status** (`Scheduled`, `Held`, `Continued`).

**deadlines_and_sol** (`deadline_id` DL-NNNNN): matter_id, client_id, matter_caption,
description, **category**, authority, trigger_event, trigger_date, computation, rule_code,
due_date, days_remaining (as at the data's snapshot), **priority** (`Critical`, `High`,
`Medium`), owner (TK-), owner_name, **status**, completed_date, vacated_reason, calendared,
rule_version, **day_type** (`Court` or `Calendar`), service_extension_days.
- `status`: `Open`, `Completed`, `Completed late`, `Vacated`.
- `category`: `Statute of Limitations`, `Court Filing`, `Pleading`, `Discovery`,
  `Disclosure`, `Case Administration`, `Criminal`, `Law and Motion`, `Post-Judgment`.

**deadline_rules** (`rule_code`): pack, authority, trigger_event, period, period_unit,
day_type, direction, service_extension, roll_rule, computation, category, priority, version,
effective_from, effective_to.
**court_holidays**: pack, date, name.

## History, risk and documents

**matter_events** (`event_id` ME-): matter_id, at, event, actor_role, actor_id, from, to,
details. A matter's status history.

**risk_signals** (`signal_id`): matter_id, code, signal, severity (`Critical`, `High`,
`Medium`), evidence, detected_at, cleared_by, cleared_at.

**documents** (`document_id` DOC-NNNNNN): matter_id, lead_id, document_type, file_name,
folder, pages, source, **privileged** (`Y`/`N`), uploaded_at, uploaded_by, sha_256,
key_fields_json, classification_confidence. One row per file in the firm's folder tree. The
files themselves are found with `attach_search` (type `documents`), by name, text inside or
meaning.

Proof records (partners only): **field_annotations**, **ai_outputs**, **decision_trace**,
**interface_messages**.

**lookups**: list, code, value, description, authority_notes. Lists include `UTBMS Litigation
Task`, `UTBMS Activity`, `UTBMS Expense`, `UTBMS Litigation Phase`, `Practice Area`,
`Matter Type`, `Calendar Event Type`, `Deadline Category`, `Trust Transaction Type`,
`Limitations Period`, `Payment Method`, `Intake Decline Reason`, `Referral Source`.

## Joins

Everything that belongs to a matter carries `matter_id`. A client's matters share
`client_id`. Time and deadlines name their person by `timekeeper_id` / `owner` (TK-). An
invoice's time and costs carry its `invoice_no`; its payments carry `invoice_no` too.
