#!/usr/bin/env python3
"""Thirty-minute data-lake intake for a cleanvibe project.

The first session schedules this for 30 minutes after it starts (see CLAUDE.md,
"Thirty-minute intake"). It runs once and does the mechanical part without
judgment, so the history is exact:

1. Commit everything in the repository as it is found: "the repository 30
   minutes in, before moving into data_lake/". This records where every file
   the user dropped in started out.
2. `git mv` each top-level file or directory that had never been committed
   (the user's drops, new directories), except the project's own files, into
   `data_lake/`, and commit that move on its own.
3. Print a report for the agent: the two commits, what moved where, the files
   now in `data_lake/`, and how much the user has said in the chat so far
   (counted from the transcripts in `sessions/`).

It records `intake_at` in `.cleanvibe.json` and does nothing on later runs.
Stdlib only. Exit code 0 on success, 1 if a git step failed.
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MARKER = ROOT / ".cleanvibe.json"
LAKE = "data_lake"

# The project's own files and directories: never moved into the data lake.
KEEP = {
    ".git", ".claude", ".cleanvibe.json", ".gitignore", "!runClaude.bat",
    "CLAUDE.md", "README.md", "INTENT.md",
    "sessions", LAKE, "scratch",
    "queue.md", "todo.md", "devlog.md", "research",
}

# Messages that come from cleanvibe itself, not from the user.
_NOT_USER = (
    "[cleanvibe",
    "This is the first ever session in a new project",
    "This is a new session in an existing cleanvibe project",
)
SUBSTANTIAL_MESSAGES = 2
SUBSTANTIAL_CHARS = 300


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)


def fail(step, result):
    print(f"data_lake_intake: {step} failed: {result.stderr.strip() or result.stdout.strip()}")
    sys.exit(1)


def load_marker():
    try:
        return json.loads(MARKER.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def never_committed_entries():
    """Top-level entries with nothing tracked under them, minus KEEP."""
    status = git("status", "--porcelain", "-uall", "-z")
    if status.returncode != 0:
        fail("git status", status)
    tops = set()
    records = status.stdout.split("\0")
    i = 0
    while i < len(records):
        rec = records[i]
        i += 1
        if len(rec) < 4:
            continue
        code, path = rec[:2], rec[3:]
        if code[0] in "RC":  # rename/copy: the next record is the old path
            i += 1
        tops.add(path.split("/")[0])
    out = []
    for top in sorted(tops):
        if top in KEEP:
            continue
        if git("ls-files", "--", top).stdout.strip():
            continue  # something under it is already committed: leave it
        out.append(top)
    return out


def _text(entry):
    if entry.get("type") == "attachment":
        att = entry.get("attachment") or {}
        return att.get("prompt", "") if att.get("type") == "queued_command" else ""
    if entry.get("type") != "user" or entry.get("isMeta"):
        return ""
    content = (entry.get("message") or {}).get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(b.get("text", "") for b in content
                         if isinstance(b, dict) and b.get("type") == "text")
    return ""


def engagement():
    """(messages, characters) the user sent, from sessions/*.jsonl."""
    messages = chars = 0
    for log in sorted((ROOT / "sessions").glob("*.jsonl")):
        try:
            lines = log.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        for line in lines:
            try:
                text = _text(json.loads(line)).strip()
            except ValueError:
                continue
            if not text or text.startswith("<") or text.startswith(_NOT_USER):
                continue
            messages += 1
            chars += len(text)
    return messages, chars


def free_name(name):
    dest = Path(LAKE) / name
    n = 2
    while (ROOT / dest).exists():
        stem, dot, ext = name.partition(".")
        dest = Path(LAKE) / (f"{stem}-{n}{dot}{ext}" if dot and stem else f"{name}-{n}")
        n += 1
    return dest.as_posix()


def main():
    marker = load_marker()
    if marker.get("intake_at"):
        print(f"Intake already done at {marker['intake_at']}; nothing to do.")
        return 0

    moving = never_committed_entries()
    messages, chars = engagement()

    git("add", "-A")
    first = None
    if git("diff", "--cached", "--quiet").returncode != 0:
        body = "\n".join(f"- {name}" for name in moving) or "- (no new top-level files)"
        done = git("commit", "-q", "-m",
                   "Intake: the repository 30 minutes in, before moving into data_lake/\n\n"
                   "Everything as found, so each file's starting point is recorded.\n"
                   "Not yet committed before this, to be moved next:\n" + body)
        if done.returncode != 0:
            fail("first commit", done)
        first = git("rev-parse", "--short", "HEAD").stdout.strip()

    moves = []
    (ROOT / LAKE).mkdir(exist_ok=True)
    for name in moving:
        dest = free_name(name)
        moved = git("mv", "--", name, dest)
        if moved.returncode != 0:
            fail(f"git mv {name}", moved)
        moves.append((name, dest))

    marker["intake_at"] = datetime.now().isoformat(timespec="seconds")
    MARKER.write_text(json.dumps(marker, indent=2) + "\n", encoding="utf-8")
    git("add", "--", MARKER.name)
    body = "\n".join(f"- {a} -> {b}" for a, b in moves) or "- (nothing to move)"
    done = git("commit", "-q", "-m", "Intake: move uncommitted material into data_lake/\n\n" + body)
    if done.returncode != 0:
        fail("move commit", done)
    second = git("rev-parse", "--short", "HEAD").stdout.strip()

    lake_files = [p for p in git("ls-files", "--", LAKE).stdout.splitlines()
                  if not p.endswith(".gitkeep")]
    substantial = messages >= SUBSTANTIAL_MESSAGES or chars >= SUBSTANTIAL_CHARS

    print("# Thirty-minute intake report\n")
    print(f"- Snapshot commit: {first or '(nothing new to commit)'}")
    print(f"- Move commit: {second}")
    print(f"- Moved into {LAKE}/: " + (", ".join(f"{a} -> {b}" for a, b in moves) or "nothing"))
    print(f"- Files in {LAKE}/ ({len(lake_files)}):")
    for path in lake_files[:200]:
        print(f"  - {path}")
    if len(lake_files) > 200:
        print(f"  - ... and {len(lake_files) - 200} more")
    print(f"- User engagement so far: {messages} message(s), {chars} characters "
          f"(not counting cleanvibe's own prompts)")
    print(f"- Material in {LAKE}/: {'yes' if lake_files else 'none'}; folder name: "
          f"{'generated (says nothing)' if marker.get('auto_named') else 'chosen by the user'}")
    if substantial:
        print("- Verdict: SUBSTANTIAL engagement. The user is present (this counts "
              "messages; it cannot tell steering from chatting): schedule the work loop "
              "to start in 60 minutes rather than now.")
    elif messages and not lake_files:
        print("- Verdict: SOME ENGAGEMENT, no material. What the user said is the subject: "
              "plan research on it and start the work loop now.")
    elif lake_files:
        print("- Verdict: LITTLE OR NO engagement, but there is material. Assume the user "
              "is away and that the folder holds the context they meant to give: start "
              "the work loop now.")
    elif not marker.get("auto_named"):
        print("- Verdict: NAME ONLY. No material and no engagement. Start work only if the "
              "folder name plainly states a task; otherwise treat this as NOTHING TO GO ON.")
    else:
        print("- Verdict: NOTHING TO GO ON. No material, no engagement, and a generated "
              "name. Do not invent work from circumstance (a guess about why the project "
              "exists is not a task), do not plan, do not start the work loop. Say so in "
              "INTENT.md and wait "
              "for the user.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
