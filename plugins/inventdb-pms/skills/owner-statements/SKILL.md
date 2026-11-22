---
name: owner-statements
description: Owner statements and year-end figures. Use when someone asks for an owner's monthly statement, net to an owner, the management fee, profit per property, a year-to-date or year-end summary, figures for the accountant or Schedule E, or a CSV of income and expenses.
---

# Owner statements and year-end

Follow `portfolio-basics` first. Every figure is a SQL total; you never add figures yourself.

## An owner's month

For an owner and a month (all their properties):
1. Income by category: `Rent`, `Pet Rent`, `Late Fee`, `Application Fee`, from SQL.
2. Expenses by category: `Repairs & Maintenance`, `Management Fee`, `Property Tax`, `HOA`,
   `Insurance`.
3. Net to owner = income total minus expense total, computed in one SQL step from the two totals.
4. Deposits received in the month (`Security Deposit`, `Pet Deposit`), shown apart and labelled
   "held for tenants, not income".
5. The management fee check: rent collected times the owner's `mgmt_fee` (in SQL), next to the fee
   actually booked. If they differ, say by how much; do not change either.

Present it as a statement table with the owner's name and the month, and a line per property when
the owner asks.

## Year to date and year-end

Per property (or per owner), income and expenses by category from 1 Jan to the as-at date, in the
categories an accountant uses for Schedule E (rents received; repairs; management fees; taxes;
insurance; HOA). Deposits are excluded and listed apart.

When the person asks for a file, give the same figures as CSV text in a code block, one row per
property and category, columns `property_id, category, type, amount`, totals from SQL. Say the
accountant decides what is deductible.
