import pytest
import os
from datasnap.datasnap import datasnap
from datasnap.deep_walk import deep_walk
from datasnap.shallow_walk import shallow_walk
from datasnap.tests.inputs.path_mock import mock_data, mock_path_structure
from pathlib import Path

def test_raises_not_dir_error(monkeypatch):
    monkeypatch.setattr(Path, 'is_dir', lambda self: False)
    with pytest.raises(NotADirectoryError):
        datasnap('fakefolder')

def test_returns_shallow(tmp_path):
    mock_path_structure(tmp_path)
    result = list(datasnap(str(tmp_path), shallow=True))
    
    result_name_set = set(name for name, _, _ in result)
    result_parent_set = set(parent for _, parent, _ in result)
    expected_name_set = set()
    expected_parent_set = set()
    for i in mock_data:
        if i.isdir:
            parent, name = os.path.split(i.path)
            expected_name_set.add(name)
            fullparent = str(tmp_path.joinpath(parent))
            expected_parent_set.add(fullparent)

    # Check stats output for mutation.
    # Popping certain stats keys that mutate on re-inspection.
    result_stats = [stats for _, _, stats in result]
    expected_stats = [stats for _, _, stats in shallow_walk(tmp_path)]
    for key in ['st_mtime_ns', 'st_mtime', 'st_atime', 'st_atime_ns']:
        for st in result_stats + expected_stats:
            st.pop(key)
    for count, st in enumerate(result_stats):
        result_set = set(st.items())
        expected_set = set(expected_stats[count].items())
        assert result_set == expected_set

    # Check that names and parents are as expected.
    assert expected_name_set == result_name_set
    assert expected_parent_set == result_parent_set

def test_returns_deep(tmp_path):
    mock_path_structure(tmp_path)
    result = list(datasnap(str(tmp_path)))
    
    result_name_set = set(name for name, _, isdir in result)
    result_parent_set = set(parent for _, parent, _ in result)
    expected_name_set = set()
    expected_parent_set = set()
    for i in mock_data:
        parent, name = os.path.split(i.path)
        expected_name_set.add(name)
        fullparent = str(tmp_path.joinpath(parent))
        expected_parent_set.add(fullparent)

    # Check that names and parents are as expected.
    assert expected_name_set == result_name_set
    assert expected_parent_set == result_parent_set