# cleanvibe-template

> A cleanvibe project: an open-ended, git-tracked working session.

## How this project works
Nothing was decided up front about what this project is. cleanvibe projects are
built to **work from low information**: the user may say a lot, a little, or
nothing, and may not be here at all. Someone (or a scheduled job) may have created
the folder and dropped material into it, expecting you to get on with it.

- **The chat comes first.** Anything the user says in the conversation takes
  priority over everything else.
- **Then what is in the folder.** Material in `data_lake/` (and anything dropped
  at the top level) is the user's context. Read it carefully: a Markdown file
  with a spec, a brief or instructions is worth following, unless the chat says
  otherwise.
- **Then the folder's name and path.** A name the user chose (see `auto_named`
  in `.cleanvibe.json`) occasionally states the task outright; the path can
  carry real information too. But **a guess about why the project exists is
  not a task.** Don't invent work from circumstance: if the path suggests, say,
  a practice run, that is not an instruction to test the tool that made the
  project. But if the user *says* the tool or the chat is the subject, it is.
- **Nothing to go on is a real state, and a narrow one.** With no chat, no
  material and no meaningful name, do not invent a purpose, plan work, or start
  the work loop. Say plainly in `INTENT.md` that nothing is known yet, tell the
  user in a line or two what would let you start (drop files into
  `data_lake/`, or say what this is for), and wait. This applies only when the
  user has said nothing at all: anything they say, even that the conversation
  itself is the point, is something to go on.
- **No strict instructions is not no work.** If there is a subject (the chat, a
  name the user chose, the material) but no spec or build task, the work loop
  still runs: it researches and writes about the subject under
  `research-practice`, with the question written down as an assumption.
- **Stay inside this project.** Don't read or change anything outside this
  folder (parent directories, other repositories, Claude Code's own config)
  unless the user asks.
- **"Stop" and "don't" mean stop now.** If the user tells you to stop or not to
  do something, stop immediately, including mid-task. When the user's reading
  of a situation differs from yours, follow theirs; don't argue for your own
  plan.
- **Keep `INTENT.md` current.** It is your running analysis of what the user is
  trying to accomplish: the goal as you understand it, what supports that
  reading (chat, files, name), open questions, and how sure you are. Update it
  when your understanding changes. When you have to assume, write the
  assumption down there and carry on.
- **AskUserQuestion only when the user is clearly here.** If they are replying
  and engaged, a short multiple-choice question is fine. If they are not, don't
  stop to ask: decide, record the assumption in `INTENT.md`, and keep working.
  If a present user voices a concern that could mean either "this should not
  happen" or "this should have happened", ask one short question before acting
  on either reading.
- **Practices come from skills.** Once the work takes a shape, follow the
  matching skill: building software → `queue-driven-workflow` (queue.md,
  todo.md, devlog.md, tests, CI); researching any topic → `research-practice`;
  long autonomous stretches → `autonomous-loop`.
- **No crud.** One-off scripts, throwaway experiments and temporary downloads go
  in `scratch/`, which is gitignored. Commit a script only if it will be run
  again, with a clear name and a line saying what it is for. Delete what is no
  longer used.
- **Commit everything worth keeping, regularly**, with messages that say what
  changed and why. This repo is private and local: it has no GitHub remote unless
  the user asks for one, and then it is private
  (`gh repo create --private --source=. --push`).

## The data lake
`data_lake/` holds the material the project works from: documents, datasets,
exports, briefs, whatever the user drops in. **Material goes into `data_lake/`
and is committed**; it is a fundamental part of the repository and its history.
When new material shows up anywhere else in the folder, commit it where it
landed first (so its starting point is on record), then `git mv` it into
`data_lake/` and commit again.

## Thirty-minute intake (first session only)
In the very first session, before anything else, schedule this with
`CronCreate`: a one-time job (`recurring: false`) at the local time 30 minutes
from now, with minute, hour, day and month pinned, and this prompt:

    [cleanvibe cron] Thirty-minute intake: follow the Thirty-minute intake section of CLAUDE.md, steps 1-5.

When it fires, do this:

1. **Run** `python .claude/scripts/data_lake_intake.py` (`python3` on macOS/Linux).
   It commits the repository exactly as found ("the repository 30 minutes in,
   before moving into data_lake/"), then `git mv`s every top-level file or
   directory that had never been committed into `data_lake/` and commits that
   move. It prints a report: what moved, what is in `data_lake/`, and how much
   the user has said so far. It runs only once; it records `intake_at` in
   `.cleanvibe.json`.
2. **Investigate `data_lake/` thoroughly.** Read everything. Look especially for
   specs, briefs, outlines or instructions. Put that together with the chat and
   the directory name.
3. **Update `INTENT.md`** with what the project is for, the evidence, and your
   confidence. Commit.
4. **If the purpose is clear enough to act on, plan it.** Use the matching skill
   (`research-practice` for research, `queue-driven-workflow` for building) to
   put concrete first steps into `queue.md` / `todo.md`. Commit. Thin material
   is normal here and still worth acting on; an empty folder is not (step 5).
5. **Start the work loop** (the `autonomous-loop` skill: one cron every half
   hour that commits, pushes and keeps working the queue), depending on the
   report's verdict:
   - **Nothing to go on** (the user has said nothing at all, no material,
     generated name): do not infer a purpose, plan, or start the loop. Write in
     `INTENT.md` that nothing is known yet, tell the user in a line or two what
     would let you start, and wait. Their next message (or files appearing in
     the next session) is where work begins.
   - **The user said something, but no material:** what they said is the
     subject. Plan research on it (`research-practice`) and start the loop now.
   - **Name only** (no material, no engagement, a name the user chose): start
     only if the name plainly states a task (say, `history-of-ai-research`);
     otherwise treat it as nothing to go on.
   - **Little or no engagement, with material:** assume the user is away and
     that the folder holds the context they meant to give. Start the loop now.
   - **Substantial engagement:** the user is present (the intake counts
     messages; it can't tell steering from chatting), so don't take over yet.
     Schedule another one-time `CronCreate` job 60 minutes from now with the
     prompt `[cleanvibe cron] Start the work loop: follow step 5 of the
     Thirty-minute intake in CLAUDE.md.`, and start the loop when it fires,
     unless the user has asked you not to by then.

If the first session ended before the intake ran (`.cleanvibe.json` has no
`intake_at`), the next session schedules it again.

## Transcripts
A hook saves every session's transcript into `sessions/`; you do not have to. After
each response it refreshes `sessions/<date>_<session>.jsonl` (raw) and `.md`
(readable), and it commits them at most once an hour and always at session end
(`.claude/settings.json` → `.claude/hooks/save_session_log.py`). To catch up on
earlier sessions, read the `.md` files, newest first. Do not edit `sessions/` by
hand.

## Files
- `INTENT.md`: your running read of what this project is for.
- `data_lake/`: the material the project works from (committed).
- `README.md`: for people; fill it in once the purpose is clear.
- `sessions/`: session transcripts (automatic).
- `scratch/`: one-off work, gitignored.
- `.claude/scripts/data_lake_intake.py`: the thirty-minute intake.

## Skills

Workflow behaviors live as skills in `.claude/skills/` (auto-discovered by Claude Code):
`emergency-stop`, `cron-is-local`, `autonomous-loop`, `queue-driven-workflow`,
`research-practice`, `writing-style`, `cleanvibe-update-check`. They are vendored into this repo and kept
current by the `cleanvibe-update-check` skill.

- **Last cleanvibe update check:** `never`
- **Updates source:** <https://cleanvibe.emmaleonhart.com/updates.md>

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
Today's date is 2026-09-27.
