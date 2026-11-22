---
name: conflict-check
description: Run a conflict check. Use when someone asks to check conflicts for a prospective client, an opposing party, a company, counsel or any name before taking on work, or asks whether the firm has ever acted for or against someone.
---

# Conflict check

Follow `legal-practice` first. A conflict check searches the firm's **conflict index**
(`legal.conflict_index`), which lists every client, adverse party, opposing counsel, carrier,
lien holder and prospective client the firm has dealt with.

**You find possible conflicts. A person decides whether a conflict exists, is waivable, or
clears.** Never say "no conflict" or "cleared"; say "no matches in the conflict index" or
"possible conflicts found".

## Search each name three ways

For every name given (person or company), and every part of a person's name:
1. exact and partial spelling: `normalised_name LIKE '%<lower-case part>%'`;
2. sound: `phonetic_key LIKE '%<code>%'`, where `<code>` is the American Soundex of the
   surname (first letter, then digits: b f p v = 1; c g j k q s x z = 2; d t = 3; l = 4;
   m n = 5; r = 6; skip vowels, h, w, y; collapse repeats; pad with zeros to 4 characters,
   for example Barajas = B622, Ouyang = O520, Escobedo = E213);
3. for a company, its distinctive words (`'%kang brothers%'`), not "Inc", "LLC" or "Corp".

```sql
SELECT index_id, name, party_role, matter_id_or_lead_id, status, since
FROM legal.conflict_index
WHERE normalised_name LIKE '%barajas%' OR phonetic_key LIKE '%B622%'
```
A common surname matches many people. Then narrow by the full name and show the closest
matches first; say how many weaker matches there are.

## Report

A table, closest matches first: name as indexed, role (`Client`, `Adverse party`,
`Opposing counsel`, `Carrier`, `Lien holder`, `Prospective client`), the matter or lead key,
its status, and why it matched ("same surname, different first name", "sounds alike").

Then one line on what kind of hit it is, in plain words:
- adverse to a current client (`Adverse party` on an open matter): the most serious;
- a current or former client of the firm;
- a prior prospective client (duties to prospective clients apply even if declined);
- opposing counsel or a carrier: usually informational.

Say clearly that a person must review and decide.

## Recording the result on a lead

When the person decides and asks you to record it on an intake lead (`LD-` key): draft
`conflict_result` (their words: `Clear`, `Conflict`, `Waived`), `conflict_checked_at` (today
or the as-at date) and, if they say so, `lead_status`. Show the draft, wait for yes, then
`propose_update` and `commit` (see `legal-practice`).
