# emma-business

## Skills

Workflow behaviors live as skills in `.claude/skills/` (auto-discovered by Claude Code):
`emergency-stop`, `cron-is-local`, `autonomous-loop`, `queue-driven-workflow`,
`writing-style`, `cleanvibe-update-check`. They are vendored into this repo and kept
current by the `cleanvibe-update-check` skill.

- **Last cleanvibe update check:** `never`
- **Updates source:** <https://cleanvibe.emmaleonhart.com/updates.md>

## Project Description

Private working repo for a **sovereign AI product for enterprise**. Enterprise customers
run the system under their own control — on their own servers, or on our cloud service
configured to give them a high level of control over it. The customer keeps custody of the
deployment, the data, and the evidence trail.

The core product claim is **local auditability and reproducibility**: the record of how an
output was produced lives inside the customer's perimeter and is inspectable there without
us; the same inputs on the same pinned versions reproduce the same outputs, and a past run
can be replayed rather than re-narrated. The approach leans **neuro-symbolic** — symbolic
structure carries the parts of the reasoning that must be inspectable, so the audit trail
is over real structure rather than a post-hoc explanation of a black box.
**Interpretability** is in scope as a component of that auditability story, not as a
separate research goal.

This framing comes from Emma directly (2026-08-21) and is the spec until she narrows it.
Do not quietly widen it: "sovereign" means customer-custody of deployment, data and
evidence, and every architectural choice is judged against whether it survives running
entirely inside someone else's perimeter.

## Architecture and Conventions

Nothing is built yet, so there is no architecture to document — this section fills in as
decisions get made, and an empty section is the honest state, not an oversight.

Settled so far:

- **This repo is private and stays private.** It was moved off the public
  `cleanvibe-template` scaffold precisely so business work is not published. Never push its
  contents to `cleanvibe-template` or any other public remote.
- **No scaffold auto-regeneration.** `.github/workflows/regenerate-from-cleanvibe.yml` was
  deleted: it `rsync --delete`s a fresh cleanvibe scaffold over the tree daily, which is
  correct for a template snapshot and destructive for a product repo. Pull scaffold updates
  forward with the `cleanvibe-update-check` skill instead.
- **Air-gap-first is a design constraint, not a feature flag.** Anything that only works
  with a call home to us fails the sovereign claim; assume the deployment cannot reach us.
- **Reproducibility is enforced, not asserted.** Version and seed pinning, content-addressed
  artifacts, and replayable runs are architecture, and belong in tests as soon as there is
  code to test.

Open: the v1 slice (reasoning core vs. audit substrate vs. control plane), and the language
and deployment-target stack — both are NEEDS-DECISION in `queue.md`.

## Long command series run in strict order
When the user gives a long series of commands, treat it as a long series of commands to be
executed in relatively STRICT ORDER, one after another, EVEN IF the order seems not to make
sense or seems inefficient. The sequencing is intentional — the user organizes the steps so
states change in the order they want. Do not reorder, merge, or skip steps.

## Not-done taxonomy (never "deliberately deferred")
When work is NOT done, tag it with exactly ONE of: **NEEDS-DECISION** (name the decision +
who decides), **BLOCKED-ON-USER-ACTION** (a real-world action only the user can take — name
it), **BLOCKED-ON-EXTERNAL** (CI / a remote / a third party / another session's unpushed
commit — name it + the unblock signal), **NEEDS-INVESTIGATION** (not understood yet — a
to-do for the next tick, never a resting place), **UNSAFE-TO-GUESS** (could cause damage —
name the risk + what makes it safe), or **OUT-OF-SCOPE** (another repo's job — name it).
LOAD-BEARING DEFAULT: if it fits none of these with a specifically-named blocker, it is NOT
deferred — DO IT NOW. Bare "deliberately not done" / "blocked on <person>" is banned.

# currentDate
Today's date is 2026-07-12.
