# InventDB Consulting for Claude

Run consulting work from Claude, for example a buyer's due diligence on a property under contract: search the data
room by meaning, cross-check the leases, estoppels and rent roll, keep a findings register where every finding is
quoted and cited to its page, chase the seller's outstanding documents, record research, produce a printable report,
and keep the timesheet against the budget.

Your records and documents live in your own **InventDB Serverless** workspace: engagements, the data room and its
register, findings, requests, research notes, time entries, invoices and reports. Claude works on them through the
workspace's connector, under your own sign-in. This plugin teaches Claude the records and the rules: documents are
quoted and cited, figures come from queries, severity is a suggestion and you decide, drafts are drafts, and nothing
is written until you say yes.

## Install

- **Cowork, Claude Desktop, claude.ai:** **Customize > Plugins > Add > Add marketplace**,
  enter `inventdb/inventdb-claude-plugins`, then install **InventDB Consulting**.
- **Claude Code:**
  ```
  /plugin marketplace add inventdb/inventdb-claude-plugins
  /plugin install inventdb-consulting@inventdb
  ```

## Connect your workspace (once)

Add your InventDB workspace as a connector named **InventDB**:
- **Cowork, Claude Desktop, claude.ai:** **Settings > Connectors > Add custom connector**, URL
  `https://<your workspace>/mcp`, then **Connect** and sign in on the InventDB page that opens.
- **Claude Code:** `claude mcp add --transport http inventdb https://<your workspace>/mcp`, then
  `/mcp` to sign in.

One connector serves every InventDB plugin you install.

## Bring your data in

Upload the data room folder on your workspace's **Files** page under `consulting` / `data_room`, and import your
workbook (engagements, checklist, rent roll, time) on the **Import** page into the namespace `consulting`. Or ask
Claude (`/inventdb-consulting:import`) for a one-time upload link. Files never pass through the chat.

## Use it

- "Where are we on Willowmere?" or `/inventdb-consulting:status ENG-2026-07`
- "Is there anything in the leases that could stop the sale?" or `/inventdb-consulting:find`
- "Compare the estoppels with the rent roll" or `/inventdb-consulting:cross-check`
- "Review the T-12" or `/inventdb-consulting:review`
- "What is the seller still owing us?" or `/inventdb-consulting:requests`
- "Check the permit history for Unit 105" or `/inventdb-consulting:research`
- "Draft the due diligence report" or `/inventdb-consulting:report ENG-2026-07 Draft`
- "Log 2.5 hours for Imogen on the lease review" or `/inventdb-consulting:log-time`
- "How much of the budget is left?" or `/inventdb-consulting:timesheet`

## Printable reports

Reports are built as PDF from a fixed template in the plugin, with the facts from your records and findings. Every
page carries the engagement key, the version and status, "Page x of y", and a QR code (also a link) that opens the
engagement in your workspace after sign-in. A draft carries a DRAFT watermark until you issue it as final. Building
the PDF needs code execution (Cowork, Claude Code, or claude.ai with file creation on).

## Try it on the sample engagement

A demo workspace holds a synthetic buyer's due diligence on Willowmere Plaza, a seven-tenant retail centre under
contract, as at 20 Nov 2026, with its data room of 28 documents. Every person, company and figure in it is invented.
Sign-ins are available from InventDB on request.

## Current limits

- Claude asks before each connector call, because the workspace's tools do not yet mark which ones only read.
- The QR code opens the engagement in SQL Studio; the workspace has no record page yet.
- A new document becomes searchable a little after upload, while InventDB reads it.
- Claude cites pages from the page numbers printed in a document; a document without them is cited by section.

## Data

Claude sends queries and record changes to your InventDB workspace through its connector and receives the rows and
document text your sign-in allows. This plugin stores nothing itself and runs no server of its own. Uploaded files go
from your browser straight to your workspace.
