import http.server
import socketserver
import os
import random
import string
import hashlib
from io import BytesIO
from zipfile import ZipFile

PORT = 8000
OUTPUT_DIR = '/serverdata'

# Ensure output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/generate':
            # Generate random 1KB text content
            random_text = ''.join(random.choices(string.ascii_letters + string.digits, k=1024))
            text_file_path = os.path.join(OUTPUT_DIR, 'random_file.txt')
            
            # Save the random text to a file
            with open(text_file_path, 'w') as text_file:
                text_file.write(random_text)
            
            # Compute SHA-256 hash of the file
            file_hash = hashlib.sha256(random_text.encode('utf-8')).hexdigest()
            hash_file_path = os.path.join(OUTPUT_DIR, 'file_hash.txt')
            
            # Save the hash to another file
            with open(hash_file_path, 'w') as hash_file:
                hash_file.write(file_hash)
            
            # Create a zip file containing both the text and hash files
            zip_buffer = BytesIO()
            with ZipFile(zip_buffer, 'w') as zip_file:
                zip_file.write(text_file_path, 'random_file.txt')
                zip_file.write(hash_file_path, 'file_hash.txt')
            
            # Prepare response
            zip_buffer.seek(0)
            self.send_response(200)
            self.send_header('Content-Type', 'application/zip')
            self.send_header('Content-Disposition', 'attachment; filename="files.zip"')
            self.send_header('Content-Length', str(len(zip_buffer.getvalue())))
            self.end_headers()
            self.wfile.write(zip_buffer.getvalue())

        else:
            # Handle other paths
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Path not found')

# Set up and start the server
with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
