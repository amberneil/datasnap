import pytest
import os
from unittest.mock import MagicMock
from datasnap.buildresult import buildresult
from datasnap.shallow_walk import shallow_walk
from datasnap.tests.inputs.path_mock import mock_data, mock_path_structure

def test_shallow_walk_return_value(tmp_path, monkeypatch):
    mock_path_structure(tmp_path)

    # Build expected return sets.
    expected_path_set = set(
        os.path.join(str(tmp_path), i.path) for i in mock_data if i.isdir)
    expected_name_set = set(
        os.path.split(i.path)[1] for i in mock_data if i.isdir)

    results = list(shallow_walk(tmp_path))
    results_path_set = set(os.path.join(par, name) for name, par, _ in results)
    results_name_set = set(name for name, _p, _d in results)

    # Check all returns are directories.
    assert all(isdir for n, s, isdir in results)
    # Check all expected paths and names are present.
    assert expected_path_set == results_path_set
    assert expected_name_set == results_name_set
    # Check to make sure stats are not mutated.
    # Popping out certain keys that may change value upon re-inspection.
    for result in results:
        name, parent, stats = result
        compare = buildresult(parent, name)
        compare_name, compare_parent, compare_stats = compare
        assert compare_name == name
        assert compare_parent == parent
        assert os.path.exists(os.path.join(parent, name))
        for key in ['st_mtime_ns', 'st_mtime', 'st_atime', 'st_atime_ns']:
            compare_stats.pop(key)
            stats.pop(key)
        assert set(compare_stats.items()) == set(stats.items())
    