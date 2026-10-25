
from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from functools import partial

''' ============================= '''
''' TERMINAL:   CTRL + `          '''
''' RUN WITH:   python servers.py '''
''' STOP WITH:  ENTER in terminal '''
''' ============================= '''

pages = {
    8000: "notesite.html",
    8001: "iframe.html",
    8002: "demo_fakeBtn.html",
    8003: "demo_CJ.html",
    8004: "demo_Cursor.html"
}

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, page="index.html", **kwargs):
        self.page = page
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == "/":
            self.path = "/" + self.page
        return super().do_GET()

for port, page in pages.items():
    handler = partial(Handler, page=page)
    server = HTTPServer(("localhost", port), handler)
    Thread(target=server.serve_forever, daemon=True).start()
    print(f"http://localhost:{port} -> {page}")

input("Naciśnij Enter, aby zatrzymać serwery...")