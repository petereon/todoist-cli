# Todoist CLI

## DISCLAIMER
I made this for my personal needs and there are **NO TESTS** as of yet, so **PLEASE BE CAREFUL** not to obliterate your Todoist in some way. `todoist-cli` is limited to creating, listing and completing tasks and deliberately abstracts more complex operations away. My general recommendation is to create tasks with CLI specific label, so that you can at least identify or even filter and delete the tasks somewhat efficiently should something inconvenient happen.

This software is distributed under **MIT license**.

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

* `-f, --filter TEXT`: Filter for tasks e.g. '(overdue|today)' [default: '(overdue|today)']
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
