# InventDB Legal for Claude

Run a law firm's practice from Claude: today's docket, matter briefs, conflict checks, time
entries, billing and collections, the client trust account (CTA) and the firm's documents.

The firm's records live in its own **InventDB Serverless** workspace, which Claude reaches through
the workspace's connector. This plugin teaches Claude the firm's records, keys, statuses and rules.
InventDB checks every read and write against the signed-in person's own access, so Claude sees
and changes only what that person may.

## Install

- **Cowork, Claude Desktop, claude.ai:** **Customize > Plugins > Add > Add marketplace**,
  enter `inventdb/inventdb-claude-plugins`, then install **InventDB Legal**.
- **Claude Code:**
  ```
  /plugin marketplace add inventdb/inventdb-claude-plugins
  /plugin install inventdb-legal@inventdb
  ```

## Connect your workspace (once)

Add your firm's InventDB workspace as a connector named **InventDB**:
- **Cowork, Claude Desktop, claude.ai:** **Settings > Connectors > Add custom connector**, URL
  `https://<your workspace>/mcp`, then **Connect**, sign in on the InventDB page that opens, and
  choose **Allow**.
- **Claude Code:** `claude mcp add --transport http inventdb https://<your workspace>/mcp`, then
  `/mcp` to sign in.

The workspace needs the `legal` namespace and the InventDB Legal roles; InventDB sets these up
with you. One connector serves every InventDB plugin you install.

## Use it

Ask, for example:
- "What's on my docket this week?" or `/inventdb-legal:docket`
- "Brief me on MT-3218" or `/inventdb-legal:matter MT-3218`
- "Run a conflict check on Dulce Barajas" or `/inventdb-legal:conflict-check Dulce Barajas`
- "Log 0.4 h on MT-2761: call with opposing counsel about the meet-and-confer" or `/inventdb-legal:log-time`
- "Which invoices are over 90 days?" or `/inventdb-legal:aging`
- "Is any client ledger below zero?" or `/inventdb-legal:trust`
- "Find the proof of service for Kang Brothers" or `/inventdb-legal:find-docs`
- "Import this CSV of time entries" or `/inventdb-legal:import`

Changes are proposed first. Claude shows the exact record and fields it would write, and writes
only after you say yes. Every figure comes from a query over the records, never from the model.

To bring in a spreadsheet or a folder of documents, Claude hands you a one-time upload link, or
points you to the workspace's **Import** and **Files** pages. Files never pass through the chat.

## Try it on the sample firm

A demo workspace holds a synthetic California litigation firm (Alvarado & Sung LLP) as at
19 Aug 2026. Every person, matter and amount in it is invented. Sign-ins for the demo, one per
role, are available from InventDB on request.

## Current limits

- Signing in through the connector is available for workspace administrator accounts for now;
  role-limited accounts use the workspace directly until it is extended to them.
- Claude asks before each connector call, because the workspace's tools do not yet mark which
  ones only read.
- Answers are text and tables; there are no interactive views inside Claude yet.
- New files become searchable by text and meaning a little after upload, while InventDB reads
  them.

## Data

Claude sends queries and record changes to your InventDB workspace through its connector, and
receives the rows, file text and search results your access allows. This plugin stores nothing
itself and runs no server of its own. Uploaded files go from your browser straight to your
workspace.
