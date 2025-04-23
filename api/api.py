#!/usr/bin/env python3
import json

from http.server import BaseHTTPRequestHandler, HTTPServer
from controller.buildings_controller import execute_query

STATUS_FILTER_CODES = {
    "pre_venta": 3,
    "en_venta": 4,
    "vendido": 5
}

# Función auxiliar para establecer cabeceras
def set_response(handler, code=200):
    handler.send_response(code)
    handler.send_header('Content-Type', 'application/json')

    # handler.send_header('Access-Control-Allow-Origin', '*')
    handler.end_headers()

class SimpleRESTHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
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
            filters = {} # YEAR, STATUS, CITY

        try:
            query = execute_query(status_filter_codes= STATUS_FILTER_CODES, filters= filters)
            print(query)

        except ValueError as e:
            self.send_error(400, str(e))
            print(str(e))
            return
            
        response = [
            {"id": "1", "name": "Recurso 1"},
            {"id": "2", "name": "Recurso 2"}
        ]
        set_response(self)
        self.wfile.write(json.dumps(response).encode())
            

def run(server_class=HTTPServer, handler_class=SimpleRESTHandler, 
        port=3000, server_address='127.0.0.1'):
    httpd = server_class((server_address, port), handler_class)
    print(f"Iniciando servidor en el puerto {port}...")
    
    try:
        httpd.serve_forever()

    except KeyboardInterrupt:
        print("Deteniendo el servidor...")
        pass

    httpd.server_close()

if __name__ == "__main__":
    run()
