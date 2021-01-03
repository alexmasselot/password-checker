def pytest_ignore_collect(path):
    if str(path).endswith("main.py"):
        return True
