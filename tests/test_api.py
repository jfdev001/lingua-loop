"""Test api endpoints using mocks

You also need to mock/monkeypatch the fetch transcript logic since this
should not actually be called to avoid querying something on youtube actually...
you might initially query and then store some of the results as a fixture...
since it should ideally be used also in the comptue score (i.e., knowledge
of the expected transcripts is needed...)
"""


def test_load_video(test_api):
    assert False


def test_compute_score(test_api):
    assert False
