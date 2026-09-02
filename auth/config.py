import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30





# HS256 -> for using same server or single server
# H - HMAC -> Hash-based Message Authentication Code
# S - SHA -> Secure Hash Algorithm
# 256 -> 256 bit(32 bytes)
# Together — HS256:
# HMAC + SHA-256
# Use SHA-256 hashing + your SECRET_KEY to sign the token

# RS256 = RSA Signature with SHA-256 -> for using multiple server like (private key, public key)
# RSA = Rivest–Shamir–Adleman
# hese are the three people who invented the RSA algorithm in 1977 — Ron Rivest, Adi Shamir, and Leonard Adleman. 
# The algorithm is named after them.