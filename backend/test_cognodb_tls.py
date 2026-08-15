import ssl
import socket

HOST = "db-67054eba.databases.cognodb.com"
PORT = 7687

print("Python SSL:", ssl.OPENSSL_VERSION)
print("Connecting to:", HOST, PORT)

try:
    sock = socket.create_connection((HOST, PORT), timeout=10)
    print("TCP connection: SUCCESS")

    context = ssl.create_default_context()

    print("Starting TLS handshake...")

    tls_sock = context.wrap_socket(
        sock,
        server_hostname=HOST
    )

    print("TLS handshake: SUCCESS")
    print("TLS version:", tls_sock.version())
    print("Cipher:", tls_sock.cipher())

    tls_sock.close()

except Exception as e:
    print("TLS TEST FAILED")
    print("Error type:", type(e).__name__)
    print("Error:", e)