import pytest
from controller.buildings_controller import get_buildings_query
from controller.buildings_controller import execute_query

# Diccionario de ejemplo para códigos de estado
STATUS_FILTER_CODES = {
    "pre_venta": 3,
    "en_venta": 4,
    "vendido": 5
}

def test_get_buildings_query_year_filter_single():
    filters = {"year": [2020]}
    query = get_buildings_query(filters, STATUS_FILTER_CODES)
    assert "year = 2020" in query

def test_get_buildings_query_year_filter_range():
    filters = {"year": [2018, 2020]}
    query = get_buildings_query(filters, STATUS_FILTER_CODES)
    assert "BETWEEN 2018 AND 2020" in query

def test_get_buildings_query_year_filter_invalid():
    filters = {"year": []}
    with pytest.raises(ValueError, match="Invalid year filter"):
        get_buildings_query(filters, STATUS_FILTER_CODES)

def test_get_buildings_query_status_filter():
    filters = {"status": [3]}
    query = get_buildings_query(filters, STATUS_FILTER_CODES)
    assert "status_id = 3" in query

def test_get_buildings_query_city_filter_single():
    filters = {"city": ["bogota"]}
    query = get_buildings_query(filters, STATUS_FILTER_CODES)
    assert "city = 'bogota'" in query

def test_get_buildings_query_city_filter_multiple():
    filters = {"city": ["bogota", "medellin"]}
    query = get_buildings_query(filters, STATUS_FILTER_CODES)
    assert "city IN ('bogota', 'medellin')" in query

def dummy_execute_query(connection, query: str, params: list = None):
    # Simula retornar un resultado (lista de tuplas)
    return [("pre_venta", "bogota", "dummy address", 2020, 120000000, "dummy description")]

def dummy_create_connection(*args, **kwargs):
    class DummyConnection:
        def cursor(self, dictionary=False):
            # Retornamos un objeto cursor dummy usando la función dummy_execute_query
            class DummyCursor:
                def __enter__(self):
                    return self
                def __exit__(self, exc_type, exc_val, exc_tb):
                    pass
                def execute(self, query, params=None):
                    self._query = query
                    self._params = params
                def fetchall(self):
                    return [("pre_venta", "bogota", "dummy address", 2020, 120000000, "dummy description")]
            return DummyCursor()
        def is_connected(self):
            return True
        def close(self):
            pass
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
    return DummyConnection()

def test_execute_query(monkeypatch):
    from database import connector
    monkeypatch.setattr(connector, "create_connection", dummy_create_connection)
    monkeypatch.setattr(connector, "execute_query", dummy_execute_query)
    
    filters = {"city": ["bogota"]}
    columns = ["status", "city", "address", "year", "price", "description"]
    result = execute_query(STATUS_FILTER_CODES, filters, columns)
    
    assert isinstance(result, list)
    assert result[0]["city"] == "bogota"
