import pytest

pytestmark = [
    pytest.mark.signature(name="Global NotImplemented", exception="NotImplementedError")
]


@pytest.mark.parametrize("message", ["message", "mail", "error"])
@pytest.mark.signature(name="Function ValueError", exception="ValueError")
def test_ValueError(message):
    raise ValueError(message)


@pytest.mark.parametrize("message", ["message", "mail", "error"])
def test_RuntimeError(message):
    raise RuntimeError(message)


def test_NotImplementedError():
    raise NotImplementedError()


def test_passing():
    pass
