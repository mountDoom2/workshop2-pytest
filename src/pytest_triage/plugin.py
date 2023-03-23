import pytest

from pytest_triage import hooks, triager


def pytest_addhooks(pluginmanager):
    """Register new hooks"""
    # Step 4
    # Register new hooks


def pytest_addoption(parser):
    ...
    # Step 3
    # Register options:
    # * --signature (list of strings)
    # * --most-common (int)


def pytest_configure(config):
    ...
    # Step 1
    # Initialize Triager and store it to config object

    # Step 2
    # Register "signature" marker using config.addinivalue_line("markers", "signature(name,exception,pattern): Mark for signature definition.")

    # Step 3
    # Store options value of --signature and --most-common
    # Parse and register signatures
    # Store all loaded signatures from commandline to config object, so we add them later as test markers in pytest_collection_modifyitems

    # Step 4
    # Call pytest_register_signatures hook with config object as parameter
    # Register signatures from hooks' results.
    # Store all loaded signatures from hooks to config object, so we add them later as test markers in pytest_collection_modifyitems


def pytest_collection_modifyitems(items):
    ...
    # Step 2
    # find all "signature" markers using item.iter_markers.
    # Read marker parameters using marker.kwargs.get method.
    # Register them into Triager using Triager.register_signature (access Triager via config object (item.config)) - verify that marker is not already registered.

    # Step 3
    # Add all global signatures (set in pytest_configure) to all items using item.add_marker


def pytest_runtest_makereport(item, call):
    if call.when != "call":
        return
    # Step 1
    # Triage test result in case of failure using Triager.find_bin


def pytest_terminal_summary(terminalreporter, config):
    ...
    # Step 1
    # Use Triager.bins (dict-like object) to print detected signatures. Since we have no signatures now, all failured will be Unknown.
    # To print the output, use terminalreporter.write_line method.
    # Example output: Unknown Errors: 10
