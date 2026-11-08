
from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Thread

''' ============================= '''
''' TERMINAL:   CTRL + `          '''
''' RUN WITH:   python servers.py '''
''' STOP WITH:  CTRL + C          '''
''' ============================= '''

HOST = "localhost"
PORT = 2000
TRUSTED_PORT = 3000

pages = {
    "/notesite.html": "notesite.html",
    "/iframe.html": "iframe.html",
    "/demo_fullsizeDiv.html": "demo_fullsizeDiv.html",
    "/demo_fakeBtn.html": "demo_fakeBtn.html",
    "/demo_CJ.html": "demo_CJ.html",
    "/demo_Cursor.html": "demo_Cursor.html",
    "/trusted.html": "trusted.html"
}


class Handler(SimpleHTTPRequestHandler):

    ''' Dodawanie sposobów ochrony przed CJ:'''
    ''' self.send_header("X-Frame-Options", "DENY") '''
    ''' self.send_header("X-Frame-Options", "SAMEORIGIN") '''
    ''' self.send_header("Content-Security-Policy", "frame-ancestors 'self'") '''
    ''' self.send_header("Content-Security-Policy", "frame-ancestors 'none'") '''
    ''' self.send_header("Content-Security-Policy", "frame-ancestors 'self' http://127.0.0.1:3000/trusted.html") '''

    '''
    def end_headers(self):
        if self.path.split("?")[0] == "/notesite.html":
            UNCOMMENT THIS FUNCTION AND ADD POLICIES FROM ABOVE HERE
        super().end_headers()
    '''
    

    def do_GET(self):
        # Strona domyślna
        if self.path == "/":
            if self.server.server_port == TRUSTED_PORT:
                self.path = "/trusted.html"
            else:
                self.path = "/notesite.html"

        # Obsługa nieznanych ścieżek
        requested_path = self.path.split("?")[0]

        if self.server.server_port == TRUSTED_PORT:
            if requested_path != "/trusted.html":
                self.send_error(404, "Nie znaleziono strony")
                return
        else:
            if requested_path not in pages:
                self.send_error(404, "Nie znaleziono strony")
                return

        return super().do_GET()


server = HTTPServer((HOST, PORT), Handler)
trusted_server = HTTPServer((HOST, TRUSTED_PORT), Handler)

print(f"Serwer działa pod adresem: http://{HOST}:{PORT}")
for path in pages:
    print(f"http://{HOST}:{PORT}{path}")
print(f"Zaufana strona: http://{HOST}:{TRUSTED_PORT}/trusted.html")

server_thread = Thread(target=server.serve_forever)
trusted_server_thread = Thread(target=trusted_server.serve_forever)
server_thread.start()
trusted_server_thread.start()
try:
    server_thread.join()
    trusted_server_thread.join()
except KeyboardInterrupt:
    print("\nZatrzymywanie serwera...")
finally:
    server.shutdown()
    trusted_server.shutdown()
    server.server_close()
    trusted_server.server_close()
