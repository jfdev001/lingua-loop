import pytest
import tomllib
from pathlib import Path


def get_opt_in_markers():
    root = Path(__file__).resolve().parents[1]
    with open(Path(root, "pyproject.toml"), "rb") as f:
        data = tomllib.load(f)

    # NOTE: coupled to pyproject...
    markers = data["tool"]["pytest"]["ini_options"]["markers"]
    return [m.split(":")[0].strip() for m in markers]


OPT_IN_MARKERS = get_opt_in_markers()


def pytest_collection_modifyitems(config, items):
    """Must explicitly pass `-m MARKEXPR` to run marked tests

    References:
    [1] Related to https://doc.pytest.org/en/latest/example/simple.html#control-skipping-of-tests-according-to-command-line-option
    """
    markexpr = config.option.markexpr or ""  # `pytest -m MARKEXPR`

    for item in items:
        item_marker_names = {m.name for m in item.iter_markers()}
        for marker in OPT_IN_MARKERS:
            if marker in item_marker_names and marker not in markexpr:
                reason = f"{marker} test, requires 'pytest -m {marker}'"
                item.add_marker(pytest.mark.skip(reason=reason))
