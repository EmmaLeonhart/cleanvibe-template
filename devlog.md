# emma-business — Devlog

**This file is where "done" lives.** `queue.md` is delete-only: when a queue
item is finished, the item is **deleted from `queue.md`** and a dated entry
is **appended here**, in the same commit as the work, then pushed. Never
tick a box in place — a checked box left in `queue.md` is the failure mode
this file exists to prevent.

Also record releases (tag + a one-line note), notable milestones, and
anything else worth a chronological trail. Newest entries at the bottom.

This is the **same convention as the cleanvibe repo's own `devlog.md`** —
every cleanvibe-scaffolded project gets one for the same reason.

See `CLAUDE.md` § "Workflow Rules" and `queue.md`'s preamble.

---

## 2026-07-12 — Project scaffolded

Scaffolded with `cleanvibe new` (cleanvibe v1.17.0). Future entries
land here as queue items get deleted.

## 2026-08-21 — Stripped the template-only regeneration workflow

Deleted `.github/workflows/regenerate-from-cleanvibe.yml`. It exists to keep the
public `cleanvibe-template` snapshot current: daily, it reinstalls cleanvibe from
PyPI and `rsync -a --delete`s a fresh scaffold over the working tree, preserving
only `.git/`, `.github/` and `.cleanvibe-version`. In a template that is the whole
point; in a product repo it deletes every file the product adds. Removed rather
than disabled so no future push can re-arm it by accident.

`.cleanvibe-version` (1.17.0) and `.claude/skills/` stay. The `cleanvibe-update-check`
skill is the non-destructive path for pulling scaffold updates forward.

## 2026-08-21 — Project identity written down

`README.md` and `CLAUDE.md` now describe the actual project instead of the template
placeholders: a sovereign AI product for enterprise, run on customer servers or on
our cloud under a high level of customer control, with local auditability and
reproducibility as the core claim, a neuro-symbolic leaning so the audit trail runs
over real structure, and interpretability in scope as part of that story. Renamed the
`queue.md` and `devlog.md` headers off `cleanvibe-template`.

Source is Emma's own description this session, not inference from a data lake —
`data_lake/` is empty apart from its `.gitkeep`, so the bootstrap's "infer the project
from dropped files" step had nothing to read and was answered directly instead.

## 2026-08-21 — `todo.md` created — the long-horizon backlog

Wrote the project's horizon as six abstract destinations: deployment and control
plane, audit and reproducibility substrate, neuro-symbolic reasoning core,
interpretability surface, enterprise readiness, and the commercial track. Future
queues get decomposed from these.

Two assumptions are named in the file rather than buried: that on-premise and
managed cloud are one product with two deployment modes, and that the compliance
regimes customers are held to are not yet known. Both change the shape of the work
if wrong.
