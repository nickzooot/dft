import unittest
import hashlib
import random
from ecdsa import EllipticCurve, ECPoint, ECDSA

class TestEllipticCurve(unittest.TestCase):
    def setUp(self):
        # Create secp256k1 curve for testing
        self.p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
        self.a = 0
        self.b = 7
        self.Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
        self.Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
        self.n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        
        # Create curve and generator point
        self.curve = EllipticCurve(self.p, self.a, self.b, self.Gx, self.Gy, self.n)
        
    def test_point_on_curve(self):
        """Test if the generator point is on the curve"""
        G = self.curve.G
        self.assertTrue(self.curve.is_on_curve(G))
        
    def test_point_not_on_curve(self):
        """Test a point that is not on the curve"""
        # Create a point with coordinates that don't satisfy the curve equation
        bad_point = ECPoint(self.curve, 1, 1)
        self.assertFalse(self.curve.is_on_curve(bad_point))
        
    def test_point_at_infinity(self):
        """Test point at infinity"""
        infinity_point = ECPoint(self.curve, None, None, infinity=True)
        self.assertTrue(self.curve.is_on_curve(infinity_point))
        
    def test_curve_creation(self):
        """Test that curve parameters are set correctly"""
        self.assertEqual(self.curve.p, self.p)
        self.assertEqual(self.curve.a, self.a)
        self.assertEqual(self.curve.b, self.b)
        self.assertEqual(self.curve.n, self.n)
        self.assertEqual(self.curve.G.x, self.Gx)
        self.assertEqual(self.curve.G.y, self.Gy)


class TestECPoint(unittest.TestCase):
    def setUp(self):
        # Create secp256k1 curve for testing
        self.p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
        self.a = 0
        self.b = 7
        self.Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
        self.Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
        self.n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        
        # Create curve and points
        self.curve = EllipticCurve(self.p, self.a, self.b, self.Gx, self.Gy, self.n)
        self.G = self.curve.G
        self.infinity = ECPoint(self.curve, None, None, infinity=True)
        
    def test_point_addition(self):
        """Test adding two distinct points"""
        # Add G to itself to get 2G
        G2 = self.G + self.G
        # Verify that 2G is on the curve
        self.assertTrue(self.curve.is_on_curve(G2))
        
    def test_point_addition_with_infinity(self):
        """Test adding a point to the point at infinity"""
        # G + O = G
        result = self.G + self.infinity
        self.assertEqual(result.x, self.G.x)
        self.assertEqual(result.y, self.G.y)
        
        # O + G = G
        result = self.infinity + self.G
        self.assertEqual(result.x, self.G.x)
        self.assertEqual(result.y, self.G.y)
        
    def test_point_addition_inverse(self):
        """Test adding a point to its inverse"""
        # Create a point with the same x but negative y (mod p)
        neg_G = ECPoint(self.curve, self.G.x, (-self.G.y) % self.p)
        # G + (-G) should equal the point at infinity
        result = self.G + neg_G
        self.assertTrue(result.infinity)
        
    def test_scalar_multiplication(self):
        """Test scalar multiplication of a point"""
        # 1 * G = G
        result = 1 * self.G
        self.assertEqual(result.x, self.G.x)
        self.assertEqual(result.y, self.G.y)
        
        # 2 * G = G + G
        result1 = 2 * self.G
        result2 = self.G + self.G
        self.assertEqual(result1.x, result2.x)
        self.assertEqual(result1.y, result2.y)
        
        # 0 * G = O (point at infinity)
        result = 0 * self.G
        self.assertTrue(result.infinity)
        
    def test_associativity(self):
        """Test that point addition is associative: (P + Q) + R = P + (Q + R)"""
        # Create points 2G and 3G
        G2 = self.G + self.G
        G3 = G2 + self.G
        
        # Test (G + G) + G = G + (G + G)
        result1 = (self.G + self.G) + self.G
        result2 = self.G + (self.G + self.G)
        self.assertEqual(result1.x, result2.x)
        self.assertEqual(result1.y, result2.y)
        
    def test_string_representation(self):
        """Test the string representation of points"""
        # Test regular point
        point_str = str(self.G)
        self.assertTrue("Point(" in point_str)
        
        # Test point at infinity
        infinity_str = str(self.infinity)
        self.assertEqual(infinity_str, "Point(infinity)")


class TestECDSA(unittest.TestCase):
    def setUp(self):
        # Create secp256k1 curve for testing
        p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
        a = 0
        b = 7
        Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
        Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
        n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        
        # Create curve and ECDSA instance
        self.curve = EllipticCurve(p, a, b, Gx, Gy, n)
        self.ecdsa = ECDSA(self.curve)
        
        # Generate a key pair
        self.private_key, self.public_key = self.ecdsa.keygen()
        
        # Message for testing
        self.message = b"Test message for ECDSA signature and verification"
        
    def test_key_generation(self):
        """Test that key generation produces valid keys"""
        # Private key should be in the range [1, n-1]
        self.assertTrue(1 <= self.private_key < self.curve.n)
        
        # Public key should be on the curve
        self.assertTrue(self.curve.is_on_curve(self.public_key))
        
        # Public key should equal private_key * G
        expected_public_key = self.private_key * self.curve.G
        self.assertEqual(self.public_key.x, expected_public_key.x)
        self.assertEqual(self.public_key.y, expected_public_key.y)
        
    def test_signature_and_verification(self):
        """Test signature creation and verification"""
        # Sign a message
        signature = self.ecdsa.sign(self.message)
        r, s = signature
        
        # Signature components should be in the range [1, n-1]
        self.assertTrue(1 <= r < self.curve.n)
        self.assertTrue(1 <= s < self.curve.n)
        
        # Verify the signature
        is_valid = self.ecdsa.verify(self.message, signature)
        self.assertTrue(is_valid)
        
    def test_verification_with_explicit_public_key(self):
        """Test verification using an explicitly provided public key"""
        # Sign a message
        signature = self.ecdsa.sign(self.message)
        
        # Verify using the explicit public key
        is_valid = self.ecdsa.verify(self.message, signature, self.public_key)
        self.assertTrue(is_valid)
        
    def test_invalid_signature(self):
        """Test that an invalid signature is rejected"""
        # Sign a message
        signature = self.ecdsa.sign(self.message)
        r, s = signature
        
        # Create an invalid signature by modifying r
        invalid_signature = (r + 1, s)
        
        # Verify the invalid signature
        is_valid = self.ecdsa.verify(self.message, invalid_signature)
        self.assertFalse(is_valid)
        
    def test_wrong_message(self):
        """Test that a signature doesn't verify for a different message"""
        # Sign a message
        signature = self.ecdsa.sign(self.message)
        
        # Verify with a different message
        different_message = b"This is a different message"
        is_valid = self.ecdsa.verify(different_message, signature)
        self.assertFalse(is_valid)
        
    def test_wrong_public_key(self):
        """Test that a signature doesn't verify with the wrong public key"""
        # Sign a message with the original key pair
        signature = self.ecdsa.sign(self.message)
        
        # Create a new key pair
        new_ecdsa = ECDSA(self.curve)
        _, new_public_key = new_ecdsa.keygen()
        
        # Verify with the wrong public key
        is_valid = self.ecdsa.verify(self.message, signature, new_public_key)
        self.assertFalse(is_valid)
        
    def test_signature_with_zero_r_or_s(self):
        """Test handling of invalid signatures with r or s equal to 0"""
        # Create invalid signatures with r or s equal to 0
        invalid_sig1 = (0, 123)
        invalid_sig2 = (123, 0)
        
        # Verify with invalid signatures
        is_valid1 = self.ecdsa.verify(self.message, invalid_sig1)
        is_valid2 = self.ecdsa.verify(self.message, invalid_sig2)
        
        self.assertFalse(is_valid1)
        self.assertFalse(is_valid2)
        
    def test_signature_with_out_of_range_values(self):
        """Test handling of invalid signatures with r or s outside the valid range"""
        # Create invalid signatures with r or s outside [1, n-1]
        invalid_sig1 = (self.curve.n, 123)
        invalid_sig2 = (123, self.curve.n)
        
        # Verify with invalid signatures
        is_valid1 = self.ecdsa.verify(self.message, invalid_sig1)
        is_valid2 = self.ecdsa.verify(self.message, invalid_sig2)
        
        self.assertFalse(is_valid1)
        self.assertFalse(is_valid2)
        
    def test_different_signatures_for_same_message(self):
        """Test that multiple signatures of the same message are all valid but different"""
        # Sign the message multiple times
        signature1 = self.ecdsa.sign(self.message)
        signature2 = self.ecdsa.sign(self.message)
        
        # Signatures should be different (due to random k)
        self.assertNotEqual(signature1, signature2)
        
        # Both signatures should verify correctly
        is_valid1 = self.ecdsa.verify(self.message, signature1)
        is_valid2 = self.ecdsa.verify(self.message, signature2)
        
        self.assertTrue(is_valid1)
        self.assertTrue(is_valid2)


if __name__ == '__main__':
    unittest.main() 