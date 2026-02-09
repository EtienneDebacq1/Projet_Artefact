import http.server
from urllib.parse import urlparse
from urllib.parse import parse_qs

#Simple class to handle HTTP requests
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
	def _set_headers(self, code):
		self.send_response(code)
		self.end_headers()

	#disable default logs
	def log_message(self, format, *args):
		pass

	def do_GET(self):
		if self.path.startswith('/api/list'):
			self._set_headers(200)
			self.wfile.write('{"markers": [6, 8, 10, 12, 14] }'.encode("utf-8"))
		else:
			self._set_headers(400)

	def do_POST(self):
		if self.path.startswith('/api/pos'):
			try:
				parsed_url = urlparse(self.path)
				user_x = int(  parse_qs(parsed_url.query)['x'][0] )
				user_y = int(  parse_qs(parsed_url.query)['y'][0] )
				print('x is ' + str(user_x) + ' y is ' + str(user_y))
				self._set_headers(200)

			except Exception as e:
				print('Failed to parse POST ' + str(self.path) + ": " + str(e) )
				self._set_headers(400)
		elif self.path.startswith('/api/marker'):
			try:
				parsed_url = urlparse(self.path)
				user_mid = int(  parse_qs(parsed_url.query)['id'][0] )
				marker_sector = parse_qs(parsed_url.query)['sector'][0]
				marker_inner =  int( parse_qs(parsed_url.query)['inner'][0] )
				print('Marker ID ' + str(user_mid) + ' secteur ' + str(marker_sector) + ' inner ' + str(marker_inner))
				self._set_headers(200)

			except Exception as e:
				print('Failed to parse POST ' + str(self.path) + ": " + str(e))
				self._set_headers(400)
		else:
			print('Unknown request ' + str(self.path) )
			self._set_headers(400)

# Create an object of the above class
handler_object = MyHttpRequestHandler

PORT = 8080
httpd = http.server.HTTPServer(("", PORT), handler_object)
httpd.serve_forever()
