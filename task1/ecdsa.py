import hashlib
import random

class EllipticCurve:
    """Represents an elliptic curve over a finite field along with its generator point."""
    def __init__(self, p, a, b, Gx, Gy, n, h=1):
        self.p = p      # prime modulus of the finite field
        self.a = a      # curve coefficient a
        self.b = b      # curve coefficient b
        self.n = n      # order of the generator point
        self.h = h      # cofactor
        self.G = ECPoint(self, Gx, Gy) 
    def is_on_curve(self, point):
        """Returns True if the given point lies on the elliptic curve."""
        if point.infinity:
            return True
        x, y = point.x, point.y
        return (y * y - x * x * x - self.a * x - self.b) % self.p == 0

class ECPoint:
    """Represents a point on an elliptic curve."""
    def __init__(self, curve, x, y, infinity=False):
        self.curve = curve
        self.x = x
        self.y = y
        self.infinity = infinity  # flag for the point at infinity

    def __add__(self, other):
        if self.infinity:
            return other
        if other.infinity:
            return self

        # If points are inverses, return point at infinity.
        if self.x == other.x and (self.y != other.y or self.y == 0):
            return ECPoint(self.curve, None, None, infinity=True)

        if self.x == other.x:
            # Point doubling: slope = (3*x^2 + a) / (2*y)
            s = (3 * self.x * self.x + self.curve.a) * pow(2 * self.y, -1, self.curve.p)
        else:
            # Point addition: slope = (y2 - y1) / (x2 - x1)
            s = (other.y - self.y) * pow(other.x - self.x, -1, self.curve.p)
        s %= self.curve.p
        x_r = (s * s - self.x - other.x) % self.curve.p
        y_r = (s * (self.x - x_r) - self.y) % self.curve.p
        point = ECPoint(self.curve, x_r, y_r)
        assert self.curve.is_on_curve(point)
        return point 

    def __mul__(self, scalar):
        """Performs scalar multiplication using the double-and-add algorithm."""
        scalar = scalar % self.curve.n  # ensure scalar is within the valid range
        result = ECPoint(self.curve, None, None, infinity=True)  # initialize to point at infinity
        addend = self

        while scalar:
            if scalar & 1:
                result = result + addend
            addend = addend + addend
            scalar //= 2
        assert(self.curve.is_on_curve(result)) 
        return result

    __rmul__ = __mul__

    def __str__(self):
        if self.infinity:
            return "Point(infinity)"
        return f"Point({self.x}, {self.y})"

class ECDSA:
    """Encapsulates ECDSA operations: key generation, signing, and signature verification."""
    def __init__(self, curve):
        self.curve = curve
        self.private_key = None
        self.public_key = None

    def keygen(self):
        """Generates a private/public key pair."""
        self.private_key = random.randint(1, self.curve.n - 1)
        self.public_key = self.private_key * self.curve.G
        if self.public_key.infinity:
            raise ValueError("Invalid public key generated.")
        return self.private_key, self.public_key

    def sign(self, message):
        """Signs a message using the private key.
        
        Returns:
            A tuple (r, s) representing the signature.
        """
        if self.private_key is None:
            raise ValueError("Private key not generated.")
        # Hash the message with SHA-256 and convert to an integer.
        e = int.from_bytes(hashlib.sha256(message).digest(), byteorder='big')
        while True:
            k = random.randint(1, self.curve.n - 1)
            R = k * self.curve.G
            r = R.x % self.curve.n
            if r == 0:
                continue
            try:
                k_inv = pow(k, -1, self.curve.n)
            except ValueError:
                continue  # if k has no modular inverse, choose another
            s = (k_inv * (e + self.private_key * r)) % self.curve.n
            if s == 0:
                continue
            return (r, s)

    def verify(self, message, signature, public_key=None):
        """Verifies the signature of a message.
        
        Args:
            message (bytes): The original message.
            signature (tuple): The (r, s) tuple.
            public_key (ECPoint, optional): Public key to verify against. Defaults to the instance's public key.
        
        Returns:
            bool: True if the signature is valid, otherwise False.
        """
        if public_key is None:
            public_key = self.public_key
        r, s = signature
        if not (1 <= r < self.curve.n and 1 <= s < self.curve.n):
            return False
        e = int.from_bytes(hashlib.sha256(message).digest(), byteorder='big')
        try:
            s_inv = pow(s, -1, self.curve.n)
        except ValueError:
            return False
        u1 = (e * s_inv) % self.curve.n
        u2 = (r * s_inv) % self.curve.n
        R = u1 * self.curve.G + u2 * public_key
        if R.infinity:
            return False
        return (R.x % self.curve.n) == r

# Example usage
if __name__ == '__main__':
    # secp256k1 curve parameters (widely used in Bitcoin)
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    a = 0
    b = 7
    Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
    Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
    n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

    # Create generator point G.
    # Temporarily set its curve to None; we assign the curve object immediately after.
    # Create the curve object and then update G's curve.
    curve = EllipticCurve(p, a, b, Gx, Gy, n)
    G = ECPoint(curve, Gx, Gy)
    curve.G = G

    # Instantiate ECDSA with the defined curve.
    ecdsa = ECDSA(curve)
    private_key, public_key = ecdsa.keygen()
    print("Private key:", private_key)
    print("Public key:", public_key)

    # Sign and verify a message.
    message = b"Hello, this is a test message for ECDSA."
    signature = ecdsa.sign(message)
    print("Signature:", signature)
    valid = ecdsa.verify(message, signature)
    print("Signature valid?", valid)
