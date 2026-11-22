# InventDB Freelance for Claude

Run a consulting practice from Claude: is this request in the SOW, how much of the retainer is left,
what am I really earning per hour, what have I not billed, who owes me, and what is due this week.

Your records live in your own **InventDB Serverless** workspace: clients, engagements, the signed SOWs,
scope items, time logs, change requests, deliverables and invoices. Claude works on them through the
workspace's connector, under your own sign-in. This plugin teaches Claude the records and the rules:
the signed SOW decides what is in scope, every hour and amount comes from a query, drafts are drafts,
and nothing is written until you say yes.

## Install

- **Cowork, Claude Desktop, claude.ai:** **Customize > Plugins > Add > Add marketplace**,
  enter `inventdb/inventdb-claude-plugins`, then install **InventDB Freelance**.
- **Claude Code:**
  ```
  /plugin marketplace add inventdb/inventdb-claude-plugins
  /plugin install inventdb-freelance@inventdb
  ```

## Connect your workspace (once)

Add your InventDB workspace as a connector named **InventDB**:
- **Cowork, Claude Desktop, claude.ai:** **Settings > Connectors > Add custom connector**, URL
  `https://<your workspace>/mcp`, then **Connect** and sign in on the InventDB page that opens.
- **Claude Code:** `claude mcp add --transport http inventdb https://<your workspace>/mcp`, then
  `/mcp` to sign in.

One connector serves every InventDB plugin you install.

## Bring your data in

On your workspace's **Import** page, drop your workbook (one sheet per kind of record) or a timesheet
CSV and import it into the namespace `freelance`. Put signed SOWs on the **Files** page under
`freelance` / `documents`. Or ask Claude (`/inventdb-freelance:import`) for a one-time upload link.
Files never pass through the chat.

## Use it

- "Tidewell want a mobile app for the intake form. Is that in the SOW?" or `/inventdb-freelance:scope-check`
- "Am I doing work I'm not paid for?" or `/inventdb-freelance:scope-creep`
- "How much of each retainer is left this month?" or `/inventdb-freelance:retainers`
- "What am I really earning per hour?" or `/inventdb-freelance:rates`
- "What haven't I billed?" or `/inventdb-freelance:unbilled`
- "Who owes me money?" or `/inventdb-freelance:overdue`
- "What's due or late?" or `/inventdb-freelance:deliverables`
- "Log 2.5 hours on Brightmoor, LP report automation" or `/inventdb-freelance:log-time`

## Try it on the sample practice

A demo workspace holds a synthetic consulting practice (Lindqvist Studio: 8 clients, 8 engagements,
their signed SOWs) as at 20 Nov 2026. Every person, company and amount in it is invented. Sign-ins are
available from InventDB on request.

## Current limits

- Claude asks before each connector call, because the workspace's tools do not yet mark which ones
  only read.
- Answers are text and tables; there are no interactive views inside Claude yet.
- A new SOW becomes searchable a little after upload, while InventDB reads it.

## Data

Claude sends queries and record changes to your InventDB workspace through its connector and receives
the rows and file text your sign-in allows. This plugin stores nothing itself and runs no server of
its own. Uploaded files go from your browser straight to your workspace.
