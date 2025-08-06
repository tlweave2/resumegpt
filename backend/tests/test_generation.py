from backend.services.generation_service import gen_cover_letter


def test_cover_letter():
    out = gen_cover_letter("Backend Engineer at FooCorp")
    assert "FooCorp" in out
