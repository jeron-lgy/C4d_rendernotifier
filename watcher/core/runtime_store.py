import config


def load_state():
    return config.load_runtime_state()


def save_state(state):
    config.save_runtime_state(state)


def update_flags(timeout_notified=None, completion_notified=None, status=None, ended_at=None):
    state = load_state()
    if timeout_notified is not None:
        state["timeout_notified"] = bool(timeout_notified)
    if completion_notified is not None:
        state["completion_notified"] = bool(completion_notified)
    if status is not None:
        state["status"] = status
    if ended_at is not None:
        state["ended_at"] = ended_at
    save_state(state)
    return state

