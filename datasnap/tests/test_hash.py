import pytest
from pathlib import Path
from datasnap.hash import md5
from datasnap.tests.inputs.path_mock import mock_data, mock_path_structure

def test_md5_return_value(tmp_path):
    mock_path_structure(tmp_path)
    for i in mock_data:
        if i.isdir:
            continue
        fullpath = str(tmp_path.joinpath(Path(i.path)))
        result = md5(fullpath)
        assert isinstance(result, str)
        assert len(result) == 32
        assert result.lower() == result

def test_correct_md5():
    test = Path(__file__).parent.joinpath('inputs/hash_input.txt').resolve()
    expected_hash = 'C7DA63AFDDEBBED3EA3CCB73486A6C33'
    assert md5(test) == expected_hash.lower()

def test_md5_callback():
    test = Path(__file__).parent.joinpath('inputs/hash_input.txt').resolve()
    byte_parts = []
    def callback(byts):
        byte_parts.append(byts)
    md5(test, callback=callback)
    assert test.stat().st_size == sum(byte_parts)


