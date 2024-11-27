# Tests to query the API


from app import process_query


def test_pi_lower():
    assert process_query("pi") == "pi is an irrational number"

def test_pi_upper():
    assert process_query("PI") == "pi is an irrational number"

def test_knows_lotr_author():
    assert process_query("Who is the author of LOTR") == "JRR Tolkein"


# api = 0
# expected_format = 0


# def test_book_api():
#     assert process_query(api) == expected_format
