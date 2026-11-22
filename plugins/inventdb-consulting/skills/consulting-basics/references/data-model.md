# InventDB Consulting data model (namespace `consulting`)

Query a type as `consulting.<type>`. Dates compare against `'YYYY-MM-DD'` text. `true`/`false` fields are booleans.

**clients** (`client_id` CL-NN): name, contact, email, phone, kind.

**engagements** (`engagement_id` ENG-YYYY-NN): client_id, title, kind (`Buyer due diligence`, `Vendor due diligence`),
property, property_type, gla_sf, units, purchase_price, seller, psa_date, **dd_deadline** (end of the due diligence
period), **closing_date**, deposit, fee_basis, rate_principal, rate_analyst, **budget_hours**, **fee_cap**, lead,
**status** (`Active`, `Completed`), start_date.

**checklist** (`item_id` DD-NN): engagement_id, workstream, item, **status** (`Not started`, `Requested`, `In review`,
`Done`), owner, **due_date**, doc_id.

**documents** (`doc_id` DOC-NNN): engagement_id, title, workstream, **file_name** (the file in `data_room`), source
(`Seller data room`, `Title company`, `Surveyor`, `Public record`, `Third-party report`), received_on, pages,
**status** (`Received`, `Reviewed`), reviewed_on, reviewed_by.

**findings** (`finding_id` F-NNN): engagement_id, workstream, **severity** (`High`, `Medium`, `Low`), title, doc_id,
page, quote, impact, amount, recommendation, **status** (`Open`, `Raised with seller`, `Resolved`, `Accepted risk`),
raised_on, resolved_on.

**requests** (`request_id` RFI-NNN): engagement_id, workstream, request, requested_on, **due_on**, **status** (`Open`,
`Received`, `Partially received`, `Not available`), received_on, doc_id.

**research_notes** (`note_id` RN-NN): engagement_id, date, topic, source, finding.

**rent_roll** (`unit`): engagement_id, tenant, sf, lease_start, lease_end, monthly_rent, annual_rent,
security_deposit, **estoppel_received**, lease_doc_id. This is the seller's rent roll as delivered: check it against
the leases and estoppels, never treat it as proof.

**time_entries** (`entry_id` TE-NNNN): engagement_id, date, consultant, workstream, task, hours, rate, amount,
billable, **invoice_no** (empty = not yet invoiced).

**invoices** (`invoice_no` INV-YYYY-NNN): engagement_id, client_id, issued_on, due_on, hours, amount, paid_on, status.

**reports** (`report_id` REP-...): engagement_id, version, title, **status** (`Draft`, `Final`), issued_on,
prepared_by, file_name (the PDF in `deliverables`).

Files types: **data_room** (documents received) and **deliverables** (the consultant's reports). Find files with
`attach_search` and read them with `attach_read`.

Workstreams: `Title & Survey`, `Zoning & Permits`, `Environmental`, `Physical condition`, `Leases & Income`,
`Financials & Tax`, `Insurance`, `Service contracts`, `Legal & Litigation`, `Report`.
