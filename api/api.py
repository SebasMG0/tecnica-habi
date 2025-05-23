#!/usr/bin/env python3
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from controller.buildings_controller import execute_query

STATUS_FILTER_CODES = {
    "pre_venta": 3,
    "en_venta": 4,
    "vendido": 5
}

QUERY_COLUMNS= ["status", "city", "address", "year", "price", "description"]

def set_response(handler, code=200):
    """
        Set the response code and headers for the HTTP response.

        Args:
            handler: The HTTP request handler.
            code: The HTTP response code to set. Default is 200 (OK).

        Returns:
            None
    """
    handler.send_response(code)
    handler.send_header('Content-Type', 'application/json')
    handler.end_headers()


class BuildingsRESTHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """
            Handle GET requests to the server.
        """
        if not self.path.startswith("/api/buildings"):
            self.send_error(404, "Endpoint is not found")
        
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            try:
                body = self.rfile.read(content_length)
                filters = json.loads(body)

            except json.JSONDecodeError:
                self.send_error(400, "The JSON body is not valid")
                return
        else:
            filters = {}

        try:
            results = execute_query(status_filter_codes= STATUS_FILTER_CODES, filters= filters, columns= QUERY_COLUMNS)
            

        except ValueError as e:
            self.send_error(400, str(e))
            return
        
        set_response(self)
        self.wfile.write(json.dumps(results).encode())         

def run(server_class = HTTPServer, handler_class = BuildingsRESTHandler, 
        port=3000, server_address='127.0.0.1') -> None:
    """
        Run the HTTP server.

        Args:
            server_class: The class of the server to run.
            handler_class: The class of the request handler to use.
            port: The port to listen on.
            server_address: The address to bind the server to. 
    """

    httpd = server_class((server_address, port), handler_class)
    print(f"Iniciando servidor en el puerto {port}...")
    
    try:
        httpd.serve_forever()

    except KeyboardInterrupt:
        print("Deteniendo el servidor...")
    
    finally:
        httpd.server_close()
        print("Servidor detenido.")