# InventDB PMS for Claude

Run a rental portfolio from Claude: the rent roll and who is late, lease renewals and vacancies,
maintenance and vendors, receipts turned into expense lines, owner statements and year-end figures for
your accountant.

Your records live in your own **InventDB Serverless** workspace: properties, owners, leases, tenants,
the rent and expense ledger, work orders, vendors, inspections, compliance and your receipts. Claude
works on them through the workspace's connector, under your own sign-in. This plugin teaches Claude
the records, the keys and the rules: every figure comes from a query, deposits are never counted as
income, and nothing is written until you say yes.

## Install

- **Cowork, Claude Desktop, claude.ai:** **Customize > Plugins > Add > Add marketplace**,
  enter `inventdb/inventdb-claude-plugins`, then install **InventDB PMS**.
- **Claude Code:**
  ```
  /plugin marketplace add inventdb/inventdb-claude-plugins
  /plugin install inventdb-pms@inventdb
  ```

## Connect your workspace (once)

Add your InventDB workspace as a connector named **InventDB**:
- **Cowork, Claude Desktop, claude.ai:** **Settings > Connectors > Add custom connector**, URL
  `https://<your workspace>/mcp`, then **Connect** and sign in on the InventDB page that opens.
- **Claude Code:** `claude mcp add --transport http inventdb https://<your workspace>/mcp`, then
  `/mcp` to sign in.

One connector serves every InventDB plugin you install.

## Bring your data in

On your workspace's **Import** page, drop your rent roll workbook (one sheet per kind of record) or a
CSV and import it into the namespace `pms`. Put receipts and invoices on the **Files** page under
`pms` / `receipts`. Or ask Claude (`/inventdb-pms:import`) for a one-time upload link. Files never
pass through the chat.

## Use it

- "Who hasn't paid rent this month?" or `/inventdb-pms:arrears`
- "What's my rent roll?" or `/inventdb-pms:rent-roll`
- "Which leases end in the next 90 days?" or `/inventdb-pms:renewals`
- "What repairs are open, and can I send the electrician?" or `/inventdb-pms:work-orders`
- "Log the receipt from Capital City Electric" or `/inventdb-pms:log-receipt`
- "Statement for the Patterson Family Trust for October" or `/inventdb-pms:owner-statement`
- "Year-to-date figures for my accountant" or `/inventdb-pms:year-end`

## Try it on the sample portfolio

A demo workspace holds a synthetic Virginia portfolio (50 properties, 10 owners) as at 20 Nov 2026.
Every person, address and amount in it is invented. Sign-ins are available from InventDB on request.

## Current limits

- Claude asks before each connector call, because the workspace's tools do not yet mark which ones
  only read.
- Answers are text and tables; there are no interactive views inside Claude yet.
- New receipts become readable a little after upload, while InventDB reads them.

## Data

Claude sends queries and record changes to your InventDB workspace through its connector and receives
the rows and file text your sign-in allows. This plugin stores nothing itself and runs no server of
its own. Uploaded files go from your browser straight to your workspace.
