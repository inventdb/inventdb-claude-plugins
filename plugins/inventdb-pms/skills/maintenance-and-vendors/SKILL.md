---
name: maintenance-and-vendors
description: Maintenance, vendors, inspections and property compliance. Use when someone asks about open work orders, repairs, which vendor to send, vendor insurance certificates, upcoming inspections, insurance policy renewals, smoke or CO tests, or wants a work order opened or closed.
---

# Maintenance, vendors and compliance

Follow `portfolio-basics` first.

## Open work orders

Open and in-progress work orders, oldest first: key, property, issue, priority, vendor, estimate,
and age ("opened 108 days ago"). `High` priority first when the person asks what to do today.

## Which vendor

A vendor may be sent only with a current certificate of insurance (`coi_expiry` after today) and a
W-9 on file. For a trade, list matching vendors with rating and certificate date; mark a lapsed
certificate "certificate lapsed 12 Oct, do not dispatch until renewed". Never pick for the person
when two qualify; show both.

## Opening and closing a work order

- Open: draft `wo` (next key: `SELECT wo FROM pms.work_orders ORDER BY wo DESC LIMIT 1`, plus one),
  `date_opened`, `property_id`, `tenant_id` if a tenant reported it, `category`, `issue`,
  `priority`, `status` `Open`, `vendor`, `est_cost` (the person's or the vendor's figure). Yes, then
  `propose_insert`, `commit`.
- Close: `status` `Completed`, `actual_cost` (from the vendor's receipt or invoice, see
  `receipts-and-expenses`), `date_closed`. Yes, then `propose_update`, `commit`.

## Inspections and compliance

- Scheduled inspections in the next 30 days, with property and inspector.
- Insurance policies with `status` `Renewal due 60d`, with carrier, policy and expiry ("renews in
  34 days").
- Smoke and CO tests older than a year, and pre-1978 properties' lead paint records.

Say plainly what is due; the person decides what to book.
