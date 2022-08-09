# Todoist CLI

## DISCLAIMER
I made this for my personal need and did not bother to write **NO TESTS** yet, so **PLEASE BE CAREFUL** not to obliterate your Todoist in some way. Ideally create tasks with CLI specific label so that you can at least identify, filter and delete them somewhat efficiently would something
unexpected or sad happen. This is **MIT licensed** and as such I will not be held liable for any damages resulting from use of this software.

---


A CLI tool scoped for listing, creating and completing Todoist tasks.

**Usage**:

```console
$ [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `complete`
* `list`
* `new`

## `complete`

**Usage**:

```console
$ complete [OPTIONS] [TASK_ID]
```

**Arguments**:

* `[TASK_ID]`: ID of the task to complete

**Options**:

* `-i, --interactive / -n, --no-interactive`: Interactive mode  [default: True]
* `--help`: Show this message and exit.

## `list`

**Usage**:

```console
$ list [OPTIONS]
```

**Options**:

* `-f, --filter TEXT`: Filter for tasks e.g. '(overdue|today)'
* `-o, --order TEXT`: Ordering(s) for the tasks, accepted values are `time` or `t` and `priority` or `p`
* `-s, --short`: Will display only short version of table (date, task content, priority and labels)  [default: False]
* `--help`: Show this message and exit.

## `new`

**Usage**:

```console
$ new [OPTIONS] [CONTENT]
```

**Arguments**:

* `[CONTENT]`: Content of the task

**Options**:

* `-s, --desc, --description TEXT`: Long description for the task
* `-p, --prio, --priority TEXT`: Priority for the task, accepted values are `P1`, `P2`, `P3` and `P4`
* `-l, --label TEXT`: Label(s) for the task
* `-r, --project TEXT`: Project that task should belong under, default is Inbox
* `-d, --date TEXT`: Date time for tasks (accepts all the date formats allowed in Todoist interface in plain text)
* `-i, --interactive / -n, --no-interactive`: Interactive mode  [default: True]
* `--help`: Show this message and exit.
