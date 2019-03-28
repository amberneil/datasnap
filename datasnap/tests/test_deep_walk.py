import pytest
from pathlib import Path
from datasnap.buildresult import buildresult
from datasnap.deep_walk import deep_walk
from datasnap.tests.inputs.path_mock import mock_data, mock_path_structure

def test_deep_walk_return_value(tmp_path):
    mock_path_structure(tmp_path)

    expected_name_set = set(Path(i.path).name for i in mock_data)
    expected_parent_set = set(
        str(tmp_path.joinpath(Path(i.path).parent)) for i in mock_data)
    
    results = list(deep_walk(tmp_path))
    result_name_set = set(r.name for r in results)
    result_parent_set = set(r.parent for r in results)
    assert result_name_set == expected_name_set
    assert result_parent_set == expected_parent_set

    results = [(name, par, frozenset(stats.keys())) for name, par, stats in results]
    expected = []
    for i in mock_data:
        name = Path(i.path).name
        parent = str(tmp_path.joinpath(Path(i.path).parent)) 
        build = buildresult(parent, name)
        expected.append((build.name, build.parent, frozenset(build.stats.keys())))
    assert set(results) == set(expected)

def test_deep_walk_hash(tmp_path):
    mock_path_structure(tmp_path)
    results = list(deep_walk(tmp_path, hash=True))
    assert all([r.stats.get('md5') for r in results if not r.stats['isdir']])

def test_deep_walk_callback(tmp_path):
    mock_path_structure(tmp_path)
    collector = []
    def callback(increment):
        collector.append(increment)
    results = list(deep_walk(tmp_path, callback=callback))
    assert sum(collector) == len(mock_data)


