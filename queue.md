# emma-business — Work Queue

**This file is a queue of *concrete, executable steps*, not a state snapshot.** It lists what is being worked on right now. Finished work lives in `devlog.md` (a dated entry) and `git log`; longer-horizon, *abstract* work lives in `todo.md` and gets decomposed into items here when it's ready to execute. **When an item is done, delete it from this file AND append a dated entry to `devlog.md` in the same commit, then push.** Do not add checkmarks, "done" markers, or status indicators in place. If an item is still here, it is not done.

**Why this file exists:** when a planning step (formal planning mode or just "think before doing") produces a plan, that plan is written here BEFORE execution starts. That way an interrupted session can pick up from the queue rather than from chat context that may be gone.

The purpose of this file is also to bound scope. If a task is not in this queue, it is not in scope for the current session. New ideas go at the bottom of the queue (or to `todo.md` if they are longer-term / architectural), not silently into whatever is being worked on.

See `CLAUDE.md` § "Workflow Rules" for how this file, planning mode, and the task tool stay in sync.

**Three-cron playbook.** Extensive work runs under three local `CronCreate` jobs — **work-loop at :03** (the engine that drains `queue.md` and refills it from `todo.md`), **auto-flush at :15** (commit/push backstop), and **status-report at :42** (heartbeat). On a fresh session they are **started** as the opening step (bootstrap step 1 below); on a mid-session **large-scale re-fill** of this queue the FIRST item worked is instead to **kill** the already-running crons. Either way the **last two items are always pinned at the tail** — ensure the three crons are running, then run an end-of-session summary (see the `## Always last` section below and `CLAUDE.md` § "Autonomous productivity loop — the three-cron playbook"). Entering planning mode also disables the crons; their restart lives at the end of the queue.

---

## Active — Get this tree onto its private remote

Everything that could be done from this session is done: the destructive scaffold
workflow is gone, the project identity is written, `todo.md` holds the horizon. What is
left needs either a credential this session does not have, or a decision only Emma can
make. Both are recorded here with a named blocker rather than left as "in progress".

1. **BLOCKED-ON-USER-ACTION — create the private repo `EmmaLeonhart/emma-business`.**
   This Claude session's GitHub token is bound to the `emmaleonhart/cleanvibe-template`
   repository; `POST /user/repos` returns 403 (`sessions are bound to their configured
   repositories`). Repo creation has to happen from Emma's own account.

   ```
   gh repo create emma-business --private
   ```

   or via github.com/new with visibility set to **Private** at creation — not created
   public and flipped afterwards, since a public moment is a permanent one.

   **Unblock signal:** the repo exists at `github.com/EmmaLeonhart/emma-business`. Then a
   Claude session can `add_repo` it and push, or push from a local clone:

   ```
   git remote add business https://github.com/EmmaLeonhart/emma-business.git
   git push -u business HEAD:main
   ```

   Until then this tree is only in the ephemeral session container and in the bundle
   handed back to Emma. **Do NOT push it to `cleanvibe-template` or any public remote —
   that is the exact outcome the move exists to avoid.**

2. **NEEDS-DECISION (Emma) — which `todo.md` item is the v1 slice.** The three candidates
   are the audit/reproducibility substrate (item 2), the neuro-symbolic reasoning core
   (item 3), and the deployment/control plane (item 1). This is not a sequencing
   preference: it decides what the first code is, what the first tests assert, and which
   of the two named assumptions in `todo.md` gets tested first. Nothing concrete can be
   queued under it without the answer, so this is where planning stops rather than
   continuing on a guess.

   Also open, and cheaper to answer: the implementation language and target platform, and
   which compliance regimes the audit story has to satisfy.

3. **NEEDS-DECISION (Emma) — whether this project runs the three-cron autonomous loop**
   (the pinned tail below). Not started unasked: hourly jobs that commit and push are a
   standing behaviour, and "make me a repo and a plan" does not authorise one.

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
