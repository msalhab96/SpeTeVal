from speteval import utils
from .helpers import (
    get_n_random,
    get_random_text
    )
import pytest


@pytest.mark.parametrize(
    "test_inp,expected",
    [
        ([[1,2,3]], 1),
        ([[[[1],[2],[3]]]], 1),
        ([[1],[2],[3]], 1),
        ([], 0)
    ]
)
def test_get_min_dim(test_inp, expected):
    assert utils.get_min_dim(test_inp) == expected


@pytest.mark.parametrize(
    "test_inp,expected",
    [
        ([[1,2,3]], 3),
        ([[[[1],[2],[3]]]], 3),
        ([[1],[2],[3]], 3),
        ([], 0)
    ]
)
def test_get_max_dim(test_inp, expected):
    assert utils.get_max_dim(test_inp) == expected


@pytest.mark.parametrize(
    "test_inp,expected",
    [
        ('path_to/file.wav', 'wav'),
        ('/path_to/file.mp3', 'mp3'),
        ('custome/path_to/file.wav', 'wav'),
        ('file.ext', 'ext'),
        ('invalid path', ''),
        ('/invalidpath', ''),
        ('/invalid/path', ''),
    ]
)
def test_get_file_extension(test_inp, expected):
    assert utils.get_file_extension(test_inp) == expected


@pytest.mark.parametrize(
    "text,content,expected",
    [
        (get_random_text(10), get_n_random(10), 1.0),
        (get_random_text(10), [[get_n_random(5)]], 2.0),
        (get_random_text(5), [get_n_random(10)], 0.5),
        (get_random_text(0), get_n_random(10), 0.0),
        (get_random_text(0), get_n_random(0), 0.0),
    ]
)
def test_get_text_to_speech_ratio(text, content, expected):
    assert utils.get_text_to_speech_ratio(text, content) == expected


def test_get_text_to_speech_ratio_on_zero():
    # Tests division by zero
    assert utils.get_text_to_speech_ratio(
        get_random_text(5), [], eps=1e-9
        ) > 1e3


@pytest.mark.parametrize(
    "text,content,expected",
    [
        (get_random_text(10), get_n_random(10), 1.0),
        (get_random_text(10), get_n_random(5), 2.0),
        (get_random_text(5), get_n_random(10), 0.5),
        (get_random_text(0), get_n_random(10), 0.0),
        (get_random_text(0), get_n_random(0), 0.0),
    ]
)
def test_get_text_to_speech_ratio(text, content, expected):
    assert utils.get_text_to_speech_ratio(text, content) == expected


@pytest.mark.parametrize(
    "content,hop,expected",
    [
        (get_n_random(10), 200, 0),
        ([[get_n_random(400)]], 200, 2),
        ([get_n_random(400)], 200, 2),
        (get_n_random(400), 200, 2),
        (get_n_random(0), 350, 0),
    ]
)
def test_get_n_frames(content, hop, expected):
    assert utils.get_n_frames(content, hop) == expected


@pytest.mark.parametrize(
    "text,content,hop,expected",
    [
        (get_random_text(100), get_n_random(100), 1, 1.0),
        (get_random_text(5), get_n_random(100), 2, 0.1),
        (get_random_text(20), [get_n_random(10)], 5, 10.0),
        (get_random_text(10), get_n_random(10), 5, 5.0),
        (get_random_text(0), get_n_random(10), 20, 0.0),
        (get_random_text(0), get_n_random(0), 20, 0.0),
    ]
)
def test_get_text_to_frame_ratio(text, content, hop, expected):
    assert utils.get_text_to_frame_ratio(text, content, hop) == expected
