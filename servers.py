
from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Thread

''' ============================= '''
''' TERMINAL:   CTRL + `          '''
''' RUN WITH:   python servers.py '''
''' STOP WITH:  CTRL + C          '''
''' ============================= '''

HOST = "localhost"
PORT = 2000

pages = {
    "/notesite.html": "notesite.html",
    "/iframe.html": "iframe.html",
    "/demo_fullsizeDiv.html": "demo_fullsizeDiv.html",
    "/demo_fakeBtn.html": "demo_fakeBtn.html",
    "/demo_CJ.html": "demo_CJ.html",
    "/demo_Cursor.html": "demo_Cursor.html",
}


class Handler(SimpleHTTPRequestHandler):

    ''' Dodawanie sposobów ochrony przed CJ:'''
    ''' self.send_header("X-Frame-Options", "DENY") '''
    ''' self.send_header("X-Frame-Options", "SAMEORIGIN") '''
    ''' self.send_header("Content-Security-Policy", "frame-ancestors 'self'") '''
    ''' self.send_header("Content-Security-Policy", "frame-ancestors 'none'") '''
    ''' self.send_header("Content-Security-Policy", "frame-ancestors http://127.0.0.1:8000/") '''

    '''
    def end_headers(self):
        if self.path.split("?")[0] == "/notesite.html":
            UNCOMMENT AND ADD POLICIES FROM ABOVE HERE
        super().end_headers()
    '''

    def do_GET(self):
        # Strona domyślna
        if self.path == "/":
            self.path = "/notesite.html"

        # Obsługa nieznanych ścieżek
        requested_path = self.path.split("?")[0]

        if requested_path not in pages and requested_path != "/":
            self.send_error(404, "Nie znaleziono strony")
            return

        return super().do_GET()


server = HTTPServer((HOST, PORT), Handler)

print(f"Serwer działa pod adresem: http://{HOST}:{PORT}")

for path in pages:
    print(f"http://{HOST}:{PORT}{path}")

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\nZatrzymywanie serwera...")
finally:
    server.server_close()
