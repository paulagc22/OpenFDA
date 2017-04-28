import web
import socketserver
##
#WEB SERVER
##
PORT=8000

socketserver.TCPServer.allow_reuse_address = True
Handler = web.testHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)

print("serving at port", PORT)
httpd.serve_forever()
