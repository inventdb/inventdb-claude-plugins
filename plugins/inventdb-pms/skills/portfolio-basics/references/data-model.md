# InventDB PMS data model (namespace `pms`)

One type per workbook sheet; field names are the sheet's headers in lower snake case. Query a type
as `pms.<type>`. Dates compare against `'YYYY-MM-DD'` text. `true`/`false` fields are booleans.

**properties** (`property_id` P-NNNN): owner_id, street, unit, city, state, zip, region, type, beds,
baths, sqft, year_built, lot_ac, garage, market_rent, market_value, acq_date, acq_price, annual_tax,
annual_insurance, monthly_hoa, **status** (`Occupied`, `Vacant`), notes.

**owners** (`owner_id` O-NNNN): name, type, contact, phone, email, tax_id (masked), w_9_on_file,
mailing_address, **mgmt_fee** (a fraction: 0.08 = 8% of rent collected), payout_method.

**leases** (`lease_id` L-NNNN): property_id, tenant_id, tenant_name, lease_start, lease_end, term_mo,
market_rent, **contract_rent**, pet_rent, deposit_held, pet_deposit_held, **late_fee** (dollars),
**grace_days**, renewal_type (`Auto-renew`, `Manual`), status (`Active`).

**tenants** (`tenant_id` T-NNNN): property_id, first, last, phone, email, occupants, vehicles, pets,
emergency_contact, emergency_phone, move_in, move_out.

**transactions** (the ledger, no key): date, **type** (`Income`, `Expense`), property_id, owner_id,
**account_category**, account (chart-of-accounts code and name, for example `6010 - Repairs &
Maintenance`), party_tenant_vendor, memo, amount (always positive; `type` gives the direction),
method, reference.
- Income categories: `Rent`, `Pet Rent`, `Late Fee`, `Application Fee`; and the tenant's money,
  which is **not income**: `Security Deposit`, `Pet Deposit`.
- Expense categories: `Repairs & Maintenance`, `Management Fee`, `Property Tax`, `HOA`,
  `Insurance`.
- A rent payment's memo reads `November 2026 rent`; a late fee's `5% late fee — November 2026`.

**work_orders** (`wo` WO-NNNNN): date_opened, property_id, tenant_id, category, issue, **priority**
(`High`, `Medium`, `Low`), **status** (`Open`, `In Progress`, `Completed`), vendor (company name),
est_cost, actual_cost, date_closed.

**vendors** (`vendor_id` V-NNNN): company, trade, contact, phone, email, w_9_on_file, coi_on_file,
**coi_expiry** (certificate of insurance), license, rating.

**inspections** (`inspection_id` I-NNNN): property_id, type, scheduled, inspector, **status**
(`Scheduled`, `In Progress`, `Completed`), issues_found, follow_up_wo, repair_estimate, notes.

**compliance** (one row per property): property_id, insurance_carrier, policy, coverage,
annual_premium, **policy_expiry**, smoke_test_date, co_test_date, lead_paint_pre_1978,
cert_of_occupancy, **status** (`Compliant`, `Renewal due 60d`).

**daily_tasks**: date, time, task, property_id, category, priority, **status** (`Todo`,
`In Progress`, `Done`, `Cancelled`), notes.

**receipts**: a files-only type. Receipt images and PDFs uploaded on the Files page live here
(folder `receipts/`); find them with `attach_search` (`type: "receipts"`) and read them with
`attach_read`.

## Joins

Everything about a property carries `property_id`; a property's owner is `properties.owner_id`; a
lease's tenant is `leases.tenant_id`; a work order's vendor is `work_orders.vendor` =
`vendors.company`.
