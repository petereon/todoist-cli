import cutie


def read_and_close(f):
    s = f.read()
    f.close()
    return s


def get_token():
    import os

    home = os.getenv("HOME")
    path = f"{home}/.todoist_token"
    if not os.getenv("TODOIST_API_TOKEN") and not os.path.exists(path):
        token = cutie.secure_input("Todoist API token:")
        if cutie.prompt_yes_or_no("Save to file?"):

            print(f"Saving the token to {path}")
            f = open(path, "w")
            f.write(token)
            f.close()
        else:
            print("Saving the token to environment variable `TODOIST_API_TOKEN`")
            os.environ["TODOIST_API_TOKEN"] = token
    else:
        token = os.getenv("TODOIST_API_TOKEN") or read_and_close(open(path, "r"))

    return token


def mayber_start_spinner(message, interactive, console):
    status_context = console.status("Creating task...")
    if interactive:
        status_context.__enter__()
    return status_context


def maybe_end_spinner(status_context, interactive):
    if interactive:
        status_context.__exit__(None, None, None)
