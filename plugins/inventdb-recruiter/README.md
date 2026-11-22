# InventDB Recruiter for Claude

Run an independent recruiting desk from Claude: who in my own resumes has actually done this, who fits
the open role, who do I need to chase, and who owes me a fee.

Your records live in your own **InventDB Serverless** workspace: client companies, roles, candidates and
their resumes, submissions, interview notes and placements. Claude works on them through the
workspace's connector, under your own sign-in. This plugin teaches Claude the records and the rules:
search resumes by meaning and quote the evidence, match only on what the work needs, every count and
fee comes from a query, drafts are drafts, and nothing is written until you say yes.

## Install

- **Cowork, Claude Desktop, claude.ai:** **Customize > Plugins > Add > Add marketplace**,
  enter `inventdb/inventdb-claude-plugins`, then install **InventDB Recruiter**.
- **Claude Code:**
  ```
  /plugin marketplace add inventdb/inventdb-claude-plugins
  /plugin install inventdb-recruiter@inventdb
  ```

## Connect your workspace (once)

Add your InventDB workspace as a connector named **InventDB**:
- **Cowork, Claude Desktop, claude.ai:** **Settings > Connectors > Add custom connector**, URL
  `https://<your workspace>/mcp`, then **Connect** and sign in on the InventDB page that opens.
- **Claude Code:** `claude mcp add --transport http inventdb https://<your workspace>/mcp`, then
  `/mcp` to sign in.

One connector serves every InventDB plugin you install.

## Bring your data in

On your workspace's **Import** page, drop your workbook (one sheet per kind of record) or a candidate
CSV and import it into the namespace `recruiting`. Put resumes on the **Files** page with **Upload
folder**, under `recruiting` / `resumes`. Or ask Claude (`/inventdb-recruiter:import`) for a one-time
upload link. Files never pass through the chat.

## Use it

- "Who has run payment reconciliation at scale?" or `/inventdb-recruiter:find`
- "Shortlist for the Senior DevOps role" or `/inventdb-recruiter:shortlist JOB-104`
- "Who do I need to chase?" or `/inventdb-recruiter:follow-ups`
- "What's happening on the security role?" or `/inventdb-recruiter:role JOB-108`
- "Who owes me a fee?" or `/inventdb-recruiter:fees`
- "Who haven't I spoken to in a while?" or `/inventdb-recruiter:quiet`

## Try it on the sample desk

A demo workspace holds a synthetic desk (Ellery Search: 10 client companies, 15 roles, 120 candidates
with one resume each) as at 20 Nov 2026. Every person, company and resume in it is invented. Sign-ins
are available from InventDB on request.

## Current limits

- Claude asks before each connector call, because the workspace's tools do not yet mark which ones
  only read.
- Answers are text and tables; there are no interactive views inside Claude yet.
- A new resume becomes searchable a little after upload, while InventDB reads it.
- Search by meaning finds similar resumes; it can miss one. Claude quotes the evidence so you can judge.

## Data

Claude sends queries and record changes to your InventDB workspace through its connector and receives
the rows and resume text your sign-in allows. This plugin stores nothing itself and runs no server of
its own. Uploaded files go from your browser straight to your workspace.
