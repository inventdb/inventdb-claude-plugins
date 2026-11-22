---
name: reports
description: Prepare a printable report (PDF) for an engagement - for example a due diligence report for a buyer - from the findings register, the records and the documents, with every page carrying the engagement key, page x of y and a QR code back to the engagement; save it to the workspace. Use for "draft the DD report", "printable report", "issue the final report", "report for the client".
---

# Printable reports

Uses `consulting-basics` and `findings`. The layout is fixed by `scripts/build_report.py` in this skill; you supply
the facts and draft the wording. Facts come from the records (SQL) and the findings register; nothing appears that is
not in them.

## 1. Gather

- The engagement row; today's date for "as at"; the report's version (`SELECT version FROM consulting.reports WHERE engagement_id = '...' ORDER BY version DESC LIMIT 1`, plus one, or 1).
- Every finding of the engagement, by workstream, with `doc_id`, `page`, `quote`, impact, amount, recommendation and
  status. If document review has found issues not yet in the register, say so and offer to record them first.
- Key figures from SQL, each with its source: price, area, rent roll monthly total, estoppel coverage, and whatever
  the findings rely on (a recurring NOI, a tax at the price).
- Open requests with due dates and status; the documents reviewed (key, title, pages, status).
- The workspace address: the host of any file link the connector returns (`attach_url`, or `view_url` in
  `attach_search` results), or ask. The QR target is SQL Studio on the engagement:
  `<workspace>/studio?q=` + the URL-encoded `SELECT * FROM consulting.engagements WHERE engagement_id = '<key>'`.

## 2. Write the spec (JSON) and build

```json
{"title": "Due diligence report: Willowmere Plaza",
 "engagement": {"id": "ENG-2026-07", "title": "...", "client": "...", "property": "...", "prepared_by": "...",
                "purchase_price": "$9,350,000.00", "dd_deadline": "25 November 2026", "closing_date": "18 December 2026"},
 "as_at": "20 Nov 2026", "version": 1, "status": "Draft", "synthetic": false,
 "record_url": "https://<workspace>/studio?q=...",
 "summary": ["two to four short paragraphs: the answer first, then what it rests on"],
 "red_flags": [{"key": "F-001", "severity": "High", "title": "...", "source": "DOC-006 p.2"}],
 "figures": [{"label": "...", "value": "...", "source": "..."}],
 "sections": [{"heading": "Leases & Income", "notes": ["optional"],
               "findings": [{"key": "F-007", "severity": "High", "title": "...", "quote": "exact words",
                             "source": "DOC-009 p.3", "impact": "...", "amount": "...", "recommendation": "...",
                             "status": "Open"}]}],
 "open_requests": [{"key": "RFI-014", "request": "...", "due": "18 Nov 2026", "status": "Open, 2 days late"}],
 "documents": [{"key": "DOC-001", "title": "...", "pages": 2, "status": "Reviewed"}],
 "limitations": ["optional; a standard scope statement is used if omitted"]}
```

Set `"synthetic": true` for the synthetic demo workspace. Then run, with Python 3 and reportlab:
`python <this skill's folder>/scripts/build_report.py report.json "<key> v<n> <Draft|Final>.pdf"`.
Every page then carries the engagement key, version, status, "Page x of y" and the QR code (also a clickable link);
a Draft carries a DRAFT watermark. Give the person the PDF.

Without code execution (no Python available), say so, and give the same report as a document with the same sections,
headed with the engagement key, version and status.

## 3. Save it

After a plain yes: `propose_insert` the `reports` row (`report_id` `REP-<engagement>-<n>`, version, title, status,
`issued_on` today, `prepared_by`, `file_name`), `commit`, and give an `attach_upload_url` link (`namespace:
"consulting"`, `type: "deliverables"`) so the person drops the PDF into the workspace; then `upload_check`.

A report is `Final` only when the consultant says so. A Final report is never changed: a correction is a new version.
