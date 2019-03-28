import pytest
import datasnap
import os
from unittest.mock import Mock
from datasnap.buildresult import buildresult, getstats, DataSnapItem

def test_buildresult_return_value(monkeypatch):
    parent_path, name, isdir = 'fakepath', 'fakename', True
    fakestats = {'exists': True, 'realpath': 'fakepath',
                'islink': 'fakename', 'parent': 'fakeparent'}
    monkeypatch.setattr(datasnap.buildresult, 'getstats', lambda *args: fakestats)
    result = buildresult(parent_path, name)
    assert isinstance(result, DataSnapItem)
    assert result.parent == parent_path
    assert result.name == name
    assert result.stats == fakestats

def test_getstats_return_value(monkeypatch):
    from datasnap.tests.inputs.stats_mock import stats_mock
    monkeypatch.setattr(os, 'path', Mock())
    monkeypatch.setattr(os, 'stat', lambda x: stats_mock)
    expected_values = {'isdir', 'exists', 'islink', 'realpath', 'count',
        'index', 'n_fields', 'n_sequence_fields',
        'n_unnamed_fields', 'st_atime', 'st_atime_ns', 'st_birthtime',
        'st_blksize', 'st_blocks', 'st_ctime', 'st_ctime_ns', 'st_dev',
        'st_flags', 'st_gen', 'st_gid', 'st_ino', 'st_mode', 'st_mtime',
        'st_mtime_ns', 'st_nlink', 'st_rdev', 'st_size', 'st_ui'}
    parent, name = 'fakeparent', 'fakename'
    result = getstats(parent, name)
    assert expected_values.difference(set(result.keys())) == set()

def test_getstats_exception_handling(monkeypatch):
    from datasnap.tests.inputs.stats_mock import stats_mock
    parent, name = 'fakeparent', 'fakename'
    def raise_caught(x):
        raise EnvironmentError(1, 'No such file or directory')
    def raise_uncaught(x):
        raise EnvironmentError(2, 'Some other error that could happen')
    monkeypatch.setattr(os, 'path', Mock())
    monkeypatch.setattr(os, 'stat', raise_caught)
    assert isinstance(getstats(parent, name), dict)
    monkeypatch.setattr(os, 'stat', raise_uncaught)
    with pytest.raises(EnvironmentError):
        getstats(parent, name)


         



    

    






