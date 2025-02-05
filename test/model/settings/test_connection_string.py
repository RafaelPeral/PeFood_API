import os


def test_connection_string():
    connection_string = os.getenv("DB_CONNECTION_STRING")

    assert connection_string
    assert isinstance(connection_string, str)
    assert len(connection_string) > 0
    assert "://" in connection_string
    assert "@" in connection_string
