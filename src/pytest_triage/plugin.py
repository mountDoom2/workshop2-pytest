import pytest

from pytest_triage import hooks, triager


def pytest_addhooks(pluginmanager):
    """This example assumes the hooks are grouped in the 'sample_hook' module."""

    pluginmanager.add_hookspecs(hooks)


def pytest_addoption(parser):
    parser.addoption("--signature", action="append")
    parser.addoption("--most-common", type=int, action="store")


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "signature(name,exception,pattern): mark for signature"
    )
    # Step 1
    # Initialize Triager and store it to config object
    config._triager = triager.Triager()
    # Step 2
    # Register "signature" marker using config.addinivalue_line("markers", "signature(name,exception,pattern): Mark for signature definition.")
    config.addinivalue_line(
        "markers", "signature(name,exception,pattern): mark for signature"
    )

    # Step 3
    # Store options value of --signature and --most-common
    # Parse and register signatures
    # Store all loaded signatures from commandline to config object, so we add them later as test markers in pytest_collection_modifyitems
    config._most_common = config.getoption("most_common")
    cmdline_signatures = config.getoption("signature")
    config._global_sigs = []

    if cmdline_signatures:
        config._global_sigs.extend(config._triager.parse_signatures(cmdline_signatures))
        for sig in config._global_sigs:
            config._triager.register_signature(*sig)
    # Step 4
    # Call pytest_register_signatures hook with config object as parameter
    # Register signatures from hooks' results.
    # Store all loaded signatures from hooks to config object, so we add them later as test markers in pytest_collection_modifyitems
    results = config.hook.pytest_register_signatures(config=config)

    if results:
        for signatures in results:
            config._global_sigs.extend(signatures)
            for sig in signatures:
                config._triager.register_signature(*sig)


def pytest_collection_modifyitems(items):

    for item in items:
        # Step 2
        # find all "signature" markers using item.iter_markers.
        # Read marker parameters using marker.kwargs.get method.
        # Register them into Triager using Triager.register_signature (access Triager via config object (item.config))
        for marker in item.iter_markers(name="signature"):
            name, exception, pattern = (
                marker.kwargs.get("name"),
                marker.kwargs.get("exception"),
                marker.kwargs.get("pattern"),
            )
            if name not in item.config._triager.signatures:
                item.config._triager.register_signature(name, exception, pattern)
        # Step 3
        # Add all global signatures (set in pytest_configure) to all items using item.add_marker
        for name, exception, pattern in item.config._global_sigs:
            item.add_marker(
                pytest.mark.signature(name=name, exception=exception, pattern=pattern)
            )


def pytest_runtest_makereport(item, call):
    if call.when != "call":
        return
    # Step 2
    # Triage test result in case of failure using Triager.find_bin
    if call.excinfo:
        sig_names = [
            marker.kwargs.get("name") for marker in item.iter_markers(name="signature")
        ]

        item.config._triager.find_bin(
            call.excinfo.typename, str(call.excinfo.value), names=sig_names
        )


def pytest_terminal_summary(terminalreporter, config):
    # Step 1
    # Use Triager.bins (dict-like object) to print detected signatures. Since we have no signatures now, all failured will be Unknown.
    # To print the output, use terminalreporter.write_line method.
    # Example output: Unknown Errors: 10
    if config._triager.bins:
        terminalreporter.write_line("===SIGNATURES===")
        for signature_name, count in config._triager.most_common(config._most_common):
            terminalreporter.write_line(f"{signature_name}: {count}")
