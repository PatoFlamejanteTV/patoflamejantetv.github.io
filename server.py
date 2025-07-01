import http.server
import socketserver
import os

PORT = 8000

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.headers.get('User-Agent') and 'curl' in self.headers.get('User-Agent'):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            with open('index.txt', 'r', encoding='utf-8') as f:
                self.wfile.write(f.read().encode())
                self.wfile.write(b'\n')  # Add newline after index.txt

            # Sort blog posts by filename in reverse order (e.g., post3, post2, post1)
            blog_posts = sorted(os.listdir('blog'), reverse=True)

            for post in blog_posts[:3]:
                # Write the post filename before its content
                self.wfile.write(post.encode())
                self.wfile.write(b'\n')
                with open(os.path.join('blog', post), 'r', encoding='utf-8') as f:
                    self.wfile.write(f.read().encode())
                    self.wfile.write(b'\n')  # Add newline after each blog post
        else:
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b'Forbidden: Access only via curl')

Handler = MyHttpRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
