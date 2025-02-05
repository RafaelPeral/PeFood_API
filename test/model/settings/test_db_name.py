import os


def test_db_name():
    db_name = os.getenv("DB_NAME")

    assert db_name
    assert isinstance(db_name, str)
    assert len(db_name) > 0
