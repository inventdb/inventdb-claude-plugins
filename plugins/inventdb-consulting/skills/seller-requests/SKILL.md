---
name: seller-requests
description: Requests for information to the seller or other side - what is open, overdue or not available, follow-up emails, marking a request received and linking the document, and adding a new request. Use for "what's the seller still owing us?", "chase the estoppels", "RFI list", "we got the CAM reconciliations".
---

# Requests to the seller

Uses `consulting-basics`.

- **Open and overdue**: the overdue recipe in `references/sql.md`, then those due in the next seven days. For each,
  why it matters for the deadline (an estoppel the purchase agreement requires, a document a finding depends on).
- **Follow-up**: one short email per counterparty (usually the seller's broker or counsel), listing the requests by key
  with their original due dates and the due diligence deadline. A draft; the consultant sends it.
- **Received**: when a document arrives, mark the request `Received` (`received_on` today, `doc_id` of the register
  row) after a plain yes; if the file is not in the data room yet, give an upload link first (see `bring-data-in`).
- **New request**: draft it (next `request_id`, workstream, request, `requested_on` today, `due_on`, `status` `Open`);
  write after a plain yes. A finding that needs a missing document (an amendment named in an estoppel, a waiver) is a
  reason for a request: offer one.
