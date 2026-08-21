# emma-business — Work Queue

**This file is a queue of *concrete, executable steps*, not a state snapshot.** It lists what is being worked on right now. Finished work lives in `devlog.md` (a dated entry) and `git log`; longer-horizon, *abstract* work lives in `todo.md` and gets decomposed into items here when it's ready to execute. **When an item is done, delete it from this file AND append a dated entry to `devlog.md` in the same commit, then push.** Do not add checkmarks, "done" markers, or status indicators in place. If an item is still here, it is not done.

**Why this file exists:** when a planning step (formal planning mode or just "think before doing") produces a plan, that plan is written here BEFORE execution starts. That way an interrupted session can pick up from the queue rather than from chat context that may be gone.

The purpose of this file is also to bound scope. If a task is not in this queue, it is not in scope for the current session. New ideas go at the bottom of the queue (or to `todo.md` if they are longer-term / architectural), not silently into whatever is being worked on.

See `CLAUDE.md` § "Workflow Rules" for how this file, planning mode, and the task tool stay in sync.

**Three-cron playbook.** Extensive work runs under three local `CronCreate` jobs — **work-loop at :03** (the engine that drains `queue.md` and refills it from `todo.md`), **auto-flush at :15** (commit/push backstop), and **status-report at :42** (heartbeat). On a fresh session they are **started** as the opening step (bootstrap step 1 below); on a mid-session **large-scale re-fill** of this queue the FIRST item worked is instead to **kill** the already-running crons. Either way the **last two items are always pinned at the tail** — ensure the three crons are running, then run an end-of-session summary (see the `## Always last` section below and `CLAUDE.md` § "Autonomous productivity loop — the three-cron playbook"). Entering planning mode also disables the crons; their restart lives at the end of the queue.

---

## Active — Stand up the private business repo

The public `cleanvibe-template` repo is a forkable scaffold that regenerates itself daily
from PyPI. Business work cannot live there: it is public, and its
`regenerate-from-cleanvibe` workflow mirrors the scaffold over the working tree with
`rsync --delete` every morning, which would delete product files. So the first slice of
work is to move this tree into a private repo of its own and give the project an identity.

Work these top to bottom. **Delete each item from this file in the same commit that
completes it, and append a dated entry to `devlog.md`.** Push after every step.

1. **Create the private repo `EmmaLeonhart/emma-business` and push this tree to its `main`.**
   Private at creation — never public-then-flipped. Keep the existing scaffold history. Do
   NOT push business content to the public `cleanvibe-template` repo or any of its branches.

2. **Decompose the first `todo.md` item into a real queue.** Replace this section with
   concrete, individually-committable implementation steps, keeping the pinned tail below.
   Add `.github/workflows/ci.yml` as soon as there is testable code.

**Open decisions blocking deeper planning (NEEDS-DECISION — Emma decides):**
- Which slice is v1: the reasoning core, the audit/reproducibility substrate, or the
  deployment/control plane. Everything downstream of item 2 depends on this.
- Whether this session runs the three-cron autonomous loop (the pinned tail below). Not
  started unasked — hourly jobs that commit and push are a standing behaviour, not a side
  effect of "make me a repo".

---

## Always last — restart the three crons and summarize

**These two items stay pinned to the tail of the queue at all times** — below every bootstrap step and below every real work item. They are the closing half of the three-cron lifecycle described in `CLAUDE.md` § "Autonomous productivity loop — the three-cron playbook": the crons are **started** at the beginning of extensive work (a fresh session starts them as the opening item; a mid-session large-scale re-fill instead kills the already-running crons as its first item, and planning mode disables them), and these are always the LAST two, after everything else — they bring them back and sign off:

A. **Ensure the three crons are running** — start them if this session never did, restart them if a planning burst / queue re-fill killed them: work-loop (`3 * * * *`), auto-flush (`15 * * * *`), status-report (`42 * * * *`).
B. **Run the status-report action once more, independently** — an end-of-session summary of everything that happened this session.

(During first-session bootstrap these simply sit here at the bottom; they become load-bearing the moment the queue is filled with a large batch of created tasks.)

---

## Pointers

- Long-horizon backlog (abstract goals, source of future queue items): `todo.md`.
- Completed work (chronological, with releases): `devlog.md`.
- Narrative history: `git log`.
