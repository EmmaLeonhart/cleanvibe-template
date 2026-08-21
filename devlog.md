# cleanvibe-template — Devlog

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
