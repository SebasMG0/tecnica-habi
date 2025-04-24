import os
import pytest

from mysql.connector import Error

from database import connector



class DummyCursor:
    def __init__(self):
        self.executed = None
        self.params = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def execute(self, query, params=None):
        self.executed = query
        self.params = params

    def fetchall(self):
        return [("pre_venta", "bogota", "dummy address", 2020, 120000000, "dummy description")]

class DummyConnection:
    def __init__(self):
        self.closed = False

    def cursor(self, dictionary=False):
        return DummyCursor()

    def is_connected(self):
        return True

    def close(self):
        self.closed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

def dummy_connect(*args, **kwargs):
    return DummyConnection()

def test_create_connection(monkeypatch):
    import mysql.connector
    monkeypatch.setattr(mysql.connector, "connect", dummy_connect)
    conn = connector.create_connection("localhost", "3306", "user", "pass", "db")
    assert conn.is_connected()
    conn.close()
    assert conn.closed

def test_execute_query(monkeypatch):
    dummy_conn = DummyConnection()
    query = "SELECT * FROM dummy"
    
    results = connector.execute_query(dummy_conn, query)
    
    assert isinstance(results, list)
    assert results[0] == ("pre_venta", "bogota", "dummy address", 2020, 120000000, "dummy description")
