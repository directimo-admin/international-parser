__version__ = '1.0.1'
__prog__ = 'sauth'

from http.server import SimpleHTTPRequestHandler
import os
import base64
import socketserver
import click


class SimpleHTTPAuthHandler(SimpleHTTPRequestHandler):
    """Main class to present webpages and authentication."""
    username = ''
    password = ''

    def __init__(self, request, client_address, server):
        key = '{}:{}'.format(self.username, self.password).encode('ascii')
        self.key = base64.b64encode(key)
        self.valid_header = b'Basic ' + self.key
        super().__init__(request, client_address, server)

    def do_HEAD(self):
        """head method"""
        print("send header")
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_authhead(self):
        """do authentication"""
        print("send header")
        self.send_response(401)
        self.send_header("WWW-Authenticate", "Basic realm=\"Test\"")
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """Present frontpage with user authentication."""
        auth_header = self.headers.get('Authorization', '').encode('ascii')
        if auth_header is None:
            self.do_authhead()
            self.wfile.write(b"no auth header received")
        elif auth_header == self.valid_header:
            SimpleHTTPRequestHandler.do_GET(self)
        else:
            self.do_authhead()
            self.wfile.write(auth_header)
            self.wfile.write(b"not authenticated")


def serve_http(ip="", port=80, start_dir=None, handler_class=SimpleHTTPAuthHandler):
    """setting up server"""
    httpd = socketserver.TCPServer((ip, port), handler_class)

    if start_dir:
        print("Changing dir to {cd}".format(cd=start_dir))
        os.chdir(start_dir)

    socket_addr = httpd.socket.getsockname()
    print('Serving "{}" directory on {}://{}:{}'.format(
        os.getcwd(), 'http', socket_addr[0], socket_addr[1])
    )
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Server stopped.")


@click.command()
@click.argument('username')
@click.argument('password')
@click.argument('ip', default='0.0.0.0')
@click.argument('port', default=9000)
@click.option('--dir', help='use different directory')
def main(dir, ip, port, username, password):
    """
    Start http server with basic authentication current directory.
    """
    SimpleHTTPAuthHandler.username = username
    SimpleHTTPAuthHandler.password = password
    serve_http(ip=ip, port=port,
               start_dir=dir, handler_class=SimpleHTTPAuthHandler)


if __name__ == "__main__":
    main()
