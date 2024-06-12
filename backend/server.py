from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import socket

def get_ip_address():
    hostname = socket.gethostname()    
    ip_address = socket.gethostbyname(hostname)
    return ip_address

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            with open('Q://Runtime Caldeiraria/runtime.json', encoding='utf-8') as f:
                data = json.load(f)
                
            response = json.dumps(data, ensure_ascii=False)
            self.wfile.write(response.encode('utf-8'))

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Endpoint nao encontrado')


    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Access-Control-Allow-Headers', 'Content-type')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    ip_address = get_ip_address()
    print(f'Servidor iniciado em http://localhost:{port}')
    print(f"Outras máquinas na rede acessam em http://{ip_address}:{port}")
    print(f"Frontend (planta baixa) na URL Q://Runtime Caldeiraria/main.html")
    print("Para parar o servidor, fechar essa janela")
    httpd.serve_forever()

if __name__ == '__main__':
    run()