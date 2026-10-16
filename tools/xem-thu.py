# Server xem trước ở máy: như "python -m http.server" nhưng bảo trình duyệt đừng giữ bản cũ,
# để sửa config.js / main.js xong tải lại trang là thấy ngay.
#   python tools/xem-thu.py   ->  http://127.0.0.1:4173
import functools, http.server, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class NoCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()


http.server.ThreadingHTTPServer(('127.0.0.1', 4173), functools.partial(NoCache, directory=ROOT)).serve_forever()
