# CLI

A CLI tool listing and creating a Todoist tasks.

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
