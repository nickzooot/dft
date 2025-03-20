# ECDSA Implementation

This project provides a pure Python implementation of the Elliptic Curve Digital Signature Algorithm (ECDSA) using the secp256k1 curve (the same curve used in Bitcoin).

## Project Files

- `ecdsa.py` - Core implementation of the ECDSA algorithm
- `test_ecdsa.py` - Comprehensive test suite for the ECDSA implementation
- `Digital Signature Practiсe.pdf` - Reference document for digital signature implementation


## Implementation Overview

The ECDSA implementation consists of three main classes:

1. **EllipticCurve**: Represents an elliptic curve over a finite field along with its generator point
2. **ECPoint**: Represents a point on an elliptic curve, with methods for point addition and scalar multiplication
3. **ECDSA**: Encapsulates ECDSA operations such as key generation, signing, and signature verification

## Features

- Complete elliptic curve operations (point addition, doubling, scalar multiplication)
- Key pair generation using the secp256k1 curve
- Message signing using ECDSA
- Signature verification
- Comprehensive test suite to verify correctness
- Example usage includes file signing and verification (in ecdsa.py)


## Getting Started

### Basic Usage

```python
from ecdsa import EllipticCurve, ECPoint, ECDSA

# secp256k1 curve parameters (used in Bitcoin). Here can be used other curve.
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
a = 0
b = 7
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# Create curve and ECDSA instance
curve = EllipticCurve(p, a, b, Gx, Gy, n)
ecdsa = ECDSA(curve)

# Generate a key pair
private_key, public_key = ecdsa.keygen()
print(f"Private key: {private_key}")
print(f"Public key: ({public_key.x}, {public_key.y})")

# Sign a message
message = b"Hello, ECDSA!"
signature = ecdsa.sign(message)
print(f"Signature (r, s): {signature}")

# Verify the signature
is_valid = ecdsa.verify(message, signature, public_key)
print(f"Signature valid: {is_valid}")
```

### Running the Tests

To run the comprehensive test suite:

```
python -m unittest test_ecdsa.py
```

The test suite verifies:
- Elliptic curve point operations
- Key generation
- Signature creation and verification
- Edge cases and invalid inputs

