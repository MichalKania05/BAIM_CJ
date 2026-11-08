
from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Thread

''' ============================= '''
''' TERMINAL:   CTRL + `          '''
''' RUN WITH:   python servers.py '''
''' STOP WITH:  CTRL + C          '''
''' ============================= '''

HOST = "localhost"

PORT_NOTES = 1000
PORT_MAIN = 2000
PARTNER_PORT = 3000

# Strony przypisane do poszczególnych portów
pages = {
    1000: [
        "/notesite.html",
        "/othersite.html"
    ],
    2000: [
        "/attacker.html",
        "/demo_fullsizeDiv.html",
        "/demo_fakeBtn.html",
        "/demo_CJ.html",
        "/demo_Cursor.html"
    ],
    3000: [
        "/partner.html"
    ]
}


class Handler(SimpleHTTPRequestHandler):

    ''' Dodawanie sposobów ochrony przed CJ:'''
    ''' UNCOMMENT THIS FUNCTION AND ADD POLICIES FROM ABOVE HERE '''
    ''' self.send_header("X-Frame-Options", "DENY") '''
    ''' self.send_header("X-Frame-Options", "SAMEORIGIN") '''
    ''' self.send_header("Content-Security-Policy", "frame-ancestors 'none'") '''
    ''' self.send_header("Content-Security-Policy", "frame-ancestors 'self'") '''
    ''' self.send_header("Content-Security-Policy", "frame-ancestors 'self' http://127.0.0.1:3000/partner.html") '''

    
    def end_headers(self):
        if self.path.split("?")[0] == "/notesite.html":
            self.send_header("X-Frame-Options", "SAMEORIGIN")
        super().end_headers()
    

    def do_GET(self):
        # Usunięcie parametrów URL
        requested_path = self.path.split("?")[0]

        # Strona domyślna
        if requested_path == "/":
            if self.server.server_port == PORT_NOTES:
                self.path = "/notesite.html"
            elif self.server.server_port == PARTNER_PORT:
                self.path = "/partner.html"
            else:
                self.path = "/attacker.html"

            requested_path = self.path

        # Sprawdzenie, czy strona jest przypisana do portu
        allowed_pages = pages.get(self.server.server_port, [])

        if requested_path not in allowed_pages:
            self.send_error(404, "Nie znaleziono strony")
            return

        return super().do_GET()


# Tworzenie serwerów
servers = {
    PORT_NOTES: HTTPServer((HOST, PORT_NOTES), Handler),
    PORT_MAIN: HTTPServer((HOST, PORT_MAIN), Handler),
    PARTNER_PORT: HTTPServer((HOST, PARTNER_PORT), Handler)
}

print("\nSerwery działają pod adresami:")

for port, server in servers.items():
    print(f"\nPort {port}:")
    for path in pages[port]:
        print(f"http://{HOST}:{port}{path}")

# Uruchamianie serwerów w osobnych wątkach
threads = []

for server in servers.values():
    thread = Thread(target=server.serve_forever)
    thread.start()
    threads.append(thread)

try:
    for thread in threads:
        thread.join()

except KeyboardInterrupt:
    print("\nZatrzymywanie serwerów...")

finally:
    for server in servers.values():
        server.shutdown()
        server.server_close()

    print("Wszystkie serwery zostały zatrzymane.")
