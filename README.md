# emma-business

Private working repo for a **sovereign AI product for enterprise**.

## What this is

The product is an AI system that enterprise customers run under their own control:
on their own servers, or on our cloud service configured to give them a high level
of control over it. "Sovereign" is the load-bearing word — the customer keeps
custody of the deployment, the data, and the evidence trail.

The core product claim is **local auditability and reproducibility**:

- **Local auditability** — the record of how an output was produced lives with the
  customer, inspectable inside their own perimeter, with no dependency on us to
  explain what the system did.
- **Reproducibility** — the same inputs, on the same pinned versions, produce the
  same outputs, and a past run can be replayed rather than re-narrated.
- **Neuro-symbolic leaning** — symbolic structure carries the parts of the reasoning
  that need to be inspectable, so the audit trail is over real structure rather than
  a post-hoc explanation of a black box.
- **Interpretability** — in scope, as a component of that auditability story rather
  than as a separate research goal.

## Status

Early. The repo currently holds project identity, a long-horizon backlog
(`todo.md`), and the active work queue (`queue.md`). There is no product code yet,
and the v1 slice is still an open decision — see the NEEDS-DECISION block at the
bottom of `queue.md`.

## How this repo is worked

Scaffolded with [cleanvibe](https://github.com/EmmaLeonhart/cleanvibe) and developed
with AI-assisted coding via Claude Code.

- `todo.md` — long-horizon, abstract destinations.
- `queue.md` — concrete steps currently in scope. Delete-only: finishing an item
  means deleting it here and appending a dated entry to `devlog.md`, same commit.
- `devlog.md` — where "done" lives, plus releases and milestones.

```
cd emma-business
claude
```
