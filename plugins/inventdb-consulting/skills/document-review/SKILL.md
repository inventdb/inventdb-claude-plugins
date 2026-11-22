---
name: document-review
description: Search, read, abstract and cross-check the documents in an engagement's data room (leases, estoppels, title, survey, zoning letters, environmental and condition reports, operating statements, tax bills, contracts). Use for "find anything about...", "what does the lease say", "review this document", "compare the estoppels with the rent roll", "is the T-12 clean?", "anything that could stop the sale?".
---

# Document review

Uses `consulting-basics`. The documents are evidence: quote them, cite them, never fill a gap from memory.

## Finding documents

- By meaning ("anything that could stop or delay the sale", "who maintains the roof"): `attach_search` with
  `namespace: "consulting"`, `type: "data_room"`, `mode: "semantic"`, `limit` 10 to 20.
- By exact words ("right of first refusal", a tenant's name, a section number): the same with `mode: "keyword"`.
- Then the register row for each file (`... FROM consulting.documents WHERE file_name = '...'`) for its key and status.

## Reading and citing

`attach_read` returns the text without page breaks. Page footers ("Page 2 of 3") mark the pages: cite the page from
them, or the section number when a document has none. Every point you make carries `DOC-NNN p.N` and the exact words.

## Abstracting a document

Key terms as a table: term, what the document says (quoted), page. For a lease: parties, premises and area, term and
expiry, rent now, deposit, options and their notice dates, repairs, co-tenancy, exclusives, assignment, any purchase
right. For a report (environmental, condition, title, survey, zoning): its conclusions, every exception, cost or
recommendation, with page.

## Cross-checks (where most findings come from)

- **Rent roll against leases and estoppels**, unit by unit: rent, expiry, deposit. A difference is a finding: show both
  sources, the difference per month and per year (computed in SQL), and what document would settle it.
- **Seller's statements against documents**: the purchase agreement's representations (for example "no tenant holds
  any right to purchase", "the rent roll is true") against the leases, estoppels and title.
- **Dates against the deal's clock**: option notice dates, auto-renewals, lease expiries, objection deadlines, against
  today, the due diligence deadline and closing.
- **Income quality**: one-off items in the trailing twelve months (termination fees, settlements) against the prior
  years; the recurring figure computed in SQL.
- **Reports against each other**: an estoppel's roof complaint against the condition report and the loss runs.
- **Coverage**: estoppels received against the purchase agreement's threshold (from `rent_roll`, in SQL).

Say what you checked and found nothing in, as well as what you found.

## After a review

- Offer each new issue as a finding (see `findings`), with suggested severity and its reason.
- Offer to mark the document `Reviewed` (`status`, `reviewed_on` today, `reviewed_by`), after a plain yes.
