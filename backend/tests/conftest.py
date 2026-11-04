import pytest


def pytest_collection_modifyitems(items):
    """
    Mark every test in a file ending in _e2e.py as an "e2e" test.

    E2E tests use live services (the real Google Sheet, OpenAI, a running
    backend). pytest.ini deselects the "e2e" marker by default, so plain
    `pytest` only runs mocked tests. Naming a file *_e2e.py is all that is
    needed to keep it out of the default run.
    """

    for item in items:
        if item.path.name.endswith("_e2e.py"):
            item.add_marker(pytest.mark.e2e)
