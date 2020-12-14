def pytest_ignore_collect(path):
    if str(path).endswith("app.py"):
        return True
