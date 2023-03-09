from collections import Counter
import re
import typing as t


class Triager:
    def __init__(self):
        # Dict-like object for grouping failure count by signature.
        self.bins = Counter()
        self.signatures = {}

    def find_bin(self, exc: str, message: str, names: t.List[str] = None):
        """Find whether exception and/or message matches registered signatures.

        If no signature found, put it in "Unknown errors" bin.
        """
        is_unknown = True
        for name, (exception, pattern) in self.signatures.items():
            if names and name not in names:
                continue
            match_exc = (exception == exc) if exception else True
            match_pattern = re.search(pattern, message) if pattern else True

            if match_exc and match_pattern:
                self.bins[name] += 1
                is_unknown = False
        if is_unknown:
            self.bins["Unknown Errors"] += 1

    def most_common(self, n: int = None):
        """Return N most-common failures."""
        return self.bins.most_common(n)

    def _parse_signature(self, raw_signature: str):
        """Parse signature.

        Format: name:exception:pattern

        name: required
        exception: optional
        pattern: optional

        Either one of exception/pattern must be entered.

        Return tuple (name, exception, pattern)
        """
        name, *split = raw_signature.split(":", 2)
        pattern, exception = None, None
        if len(split) == 2:
            exception, pattern = split
        elif len(split) == 1:
            exception = split[0]
        # Normalize empty strings to None
        pattern = pattern or None
        exception = exception or None

        return name, exception, pattern

    def parse_signatures(self, signatures: t.List[str]):
        """Parse list of signatures."""
        parsed = []
        for raw_signature in signatures:
            name, exception, pattern = self._parse_signature(raw_signature)
            parsed.append(
                (
                    name,
                    exception,
                    pattern,
                )
            )
        return parsed

    def register_raw_signature(self, raw_signature: str):
        """Parse and register signature from string."""
        name, exception, pattern = self._parse_signature(raw_signature)
        self.register_signature(name, exception, pattern)
        return name, exception, pattern

    def register_signature(self, name: str, exception: str = None, pattern: str = None):
        """Register signature.

        Duplicated names are invalid.
        Either one of exception/pattern must be entered.
        """
        if name in self.signatures:
            raise ValueError(f"Signature '{name}' already registered.")
        if not name:
            raise ValueError("Missing signature name.")
        if not exception and not pattern:
            raise ValueError(
                f"Error while registering signature '{name}'. Exception or pattern is required."
            )
        self.signatures[name] = (exception, pattern)
