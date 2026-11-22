# InventDB plugins for Claude

Claude plugins from [InventDB](https://www.inventdb.com). Each plugin runs a line of business
from Claude on the customer's own **InventDB Serverless** workspace: the records stay in the
workspace, Claude reaches them through the workspace's connector, and InventDB applies each
person's own access to every read and write.

## Add the marketplace

- **Cowork, Claude Desktop, claude.ai:** **Customize > Plugins > Add > Add marketplace**, then
  enter `inventdb/inventdb-claude-plugins`.
- **Claude Code:** `/plugin marketplace add inventdb/inventdb-claude-plugins`

## Plugins

| Plugin | What it does | Install (Claude Code) |
|---|---|---|
| [InventDB Legal](plugins/inventdb-legal/) | A law firm's docket, matters, conflict checks, time, billing, trust account and documents | `/plugin install inventdb-legal@inventdb` |
| [InventDB PMS](plugins/inventdb-pms/) | A rental portfolio's rent roll and arrears, renewals, maintenance and vendors, receipts into expenses, owner statements and year-end figures | `/plugin install inventdb-pms@inventdb` |
| [InventDB Freelance](plugins/inventdb-freelance/) | A consultant's scope checks against signed SOWs, retainer burn, effective hourly rate, unbilled time, overdue invoices and deliverables | `/plugin install inventdb-freelance@inventdb` |
| [InventDB Recruiter](plugins/inventdb-recruiter/) | An independent recruiter's resume search by meaning, role shortlists, follow-ups, placements, fees and guarantees | `/plugin install inventdb-recruiter@inventdb` |
| [InventDB Consulting](plugins/inventdb-consulting/) | Consulting work such as a buyer's due diligence: data room search and cross-checks, a cited findings register, seller requests, research, printable reports and timesheets | `/plugin install inventdb-consulting@inventdb` |

After installing, connect your InventDB workspace and sign in with your InventDB account. Each
plugin's README says how to connect it, what it sends where, and its current limits.

This repository is read-only outside InventDB: issues and pull requests are not open to outside
accounts. For questions, contact InventDB through [inventdb.com](https://www.inventdb.com).

Licensed under the [MIT License](LICENSE).
