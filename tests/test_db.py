



import sqlite3
from unittest.mock import patch
import pytest
from flaskr.db import get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)


def test_init_db_command(runner, monkeypatch):
    class Reccorder(object):
        caller = False
    def mock_init_db():
        Reccorder.caller = True
    monkeypatch.setattr('flaskr.db.init_db', mock_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'initialised' in result.output
    assert Reccorder.caller