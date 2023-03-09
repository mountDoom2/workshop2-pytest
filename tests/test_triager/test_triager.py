import pytest

from pytest_triage import triager


@pytest.fixture
def empty_triager():
    return triager.Triager()


@pytest.fixture
def filled_triager():
    trg = triager.Triager()
    trg.register_signature(("test", "error", "error"))


@pytest.mark.parametrize(
    "signature",
    [
        ("name", "Exception", "pattern"),
    ],
)
def test_register_signature(empty_triager, signature):
    empty_triager.register_signature(*signature)


def test_register_signature_duplicates(empty_triager):
    signature = ("name", "Exception", "pattern")
    empty_triager.register_signature(*signature)
    with pytest.raises(ValueError):
        empty_triager.register_signature(*signature)


@pytest.mark.parametrize(
    "signature",
    [
        # At least one of exception/pattern must be entered
        ("name",),
        ("name", None, None),
        ("name", "", ""),
        # Name must not be empty
        ("", "Exception", "pattern"),
        (None, "Exception", "pattern"),
    ],
)
def test_register_signature_invalid(empty_triager, signature):
    with pytest.raises(ValueError):
        empty_triager.register_signature(*signature)


@pytest.mark.triage_register
@pytest.mark.parametrize(
    "raw_signature,expected",
    [
        ("name:ValueError", ("name", "ValueError", None)),
        ("name:ValueError:", ("name", "ValueError", None)),
        ("name::pattern", ("name", None, "pattern")),
        ("name::pattern:", ("name", None, "pattern:")),
        ("name::pattern:", ("name", None, "pattern:")),
        ("name:exception:pattern", ("name", "exception", "pattern")),
        ("name:exception:pattern:", ("name", "exception", "pattern:")),
    ],
)
def test_register_raw_signature(empty_triager, raw_signature, expected):
    empty_triager.register_raw_signature(raw_signature) == expected


@pytest.mark.triage_register
@pytest.mark.parametrize(
    "raw_signature",
    [
        "",
        "name",
        ":name",
        "name:",
    ],
)
def test_parse_signature_invalid(empty_triager, raw_signature):
    with pytest.raises(ValueError):
        empty_triager.register_raw_signature(raw_signature)
