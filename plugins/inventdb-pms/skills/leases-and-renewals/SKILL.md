---
name: leases-and-renewals
description: Leases, renewals and vacancies. Use when someone asks which leases end soon, what to renew and at what rent, how far rents sit below market, which units are vacant, or wants a renewal offer drafted.
---

# Leases and renewals

Follow `portfolio-basics` first.

## Leases ending

List active leases ending in the next 30, 60 and 90 days (by `lease_end`), each with tenant,
property, contract rent, market rent, the gap (market minus contract, from SQL) and
`renewal_type`. Put `Manual` renewals first: nothing happens unless the person acts. An
`Auto-renew` lease rolls over by its terms; say so.

The clock is "ends in N days" against `lease_end`.

## Renewal rent

Show the contract and market rent side by side. Any new rent is the person's decision: you may show
what a stated percentage gives (computed in SQL), never choose one.

## Renewal offer

Draft the letter: tenant, property address, current lease end, the new term and rent the person
chose, the date to reply by. "Draft for your review." When the person says the renewal is signed,
draft the lease update (`lease_end`, `contract_rent`, `term_mo`) as a table, wait for yes, then
`propose_update` and `commit`.

## Vacancies

Vacant properties with their market rent, and how long each has been empty (the last lease's
`lease_end`, or the property's notes). Give the monthly rent the vacancies cost at market, from SQL.
