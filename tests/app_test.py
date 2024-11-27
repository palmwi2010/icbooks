# Tests to query the API


from app import process_query


def test_pi():
    # Should fail
    assert process_query("pi") == "i is an irrational number"

def test_knows_lotr():
    # Should pass
    assert process_query("Who is the author of LOTR") == "JRR Tolkein"


api = 0
expected_format = 0


def test_book_api():
    assert process_query(api) == expected_format
