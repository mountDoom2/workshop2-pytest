import pytest


@pytest.mark.parametrize("message", ["message", "mail", "error"])
def test_ValueError(message):
    raise ValueError(message)


@pytest.mark.parametrize("message", ["message", "mail", "error"])
def test_RuntimeError(message):
    raise RuntimeError(message)


def test_NotImplementedError():
    raise NotImplementedError()


def test_passing():
    pass
