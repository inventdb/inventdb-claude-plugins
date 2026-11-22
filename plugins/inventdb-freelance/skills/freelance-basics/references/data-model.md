# InventDB Freelance data model (namespace `freelance`)

Query a type as `freelance.<type>`. Dates compare against `'YYYY-MM-DD'` text. Retainers and hourly work
are invoiced on the 1st for the month before; the current month is not invoiced yet. `true`/`false` fields are booleans.

**clients** (`client_id` CLT-NN): company, contact, email, phone, industry, payment_terms_days, status.

**engagements** (`engagement_id` ENG-NNN): client_id, **kind** (`Retainer`, `Hourly`, `Fixed`), title,
start_date, end_date, monthly_fee, **included_hours_per_month** (retainers), hourly_rate (hourly),
overage_rate (hours beyond a retainer's included hours, or approved changes on a fixed fee),
fixed_fee, **target_hourly_rate** (the consultant's goal), **status** (`Active`, `Completed`),
sow_file (the signed SOW's file name in `documents`).

**scope_items** (`scope_item_id` SCP-NNN): engagement_id, item, **in_scope** (true: listed in the SOW's
scope; false: listed in its exclusions), notes.

**time_logs** (`time_log_id` TL-NNNN): date, engagement_id, task, hours, billable, **invoice_no** (the
invoice that billed it; `FIXED FEE` on fixed-fee work; empty = not yet invoiced).

**change_requests** (`change_request_id` CR-NNN): engagement_id, requested_on, request,
**scope_decision** (`In`, `Out`), estimate_hours, quoted_amount, **status** (`Pending`, `Approved`,
`Declined`).

**deliverables** (`deliverable_id` DLV-NNN): engagement_id, title, due_date, **status** (`In progress`,
`Delivered`, `Late`), delivered_on.

**invoices** (`invoice_no` INV-YYYY-NNN): engagement_id, client_id, period_start, period_end, **hours** (the
hours the invoice covers; empty on fixed-fee milestone invoices), amount, issued_on, due_on, paid_on (empty = unpaid), **status** (`Sent`, `Paid`).

**documents**: a files-only type holding the signed SOWs (find with `attach_search`, `type:
"documents"`; read with `attach_read`).
