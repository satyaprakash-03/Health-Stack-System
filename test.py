"""
test.py — SSLCommerz Integration Test Suite
============================================
Tests the SSLCOMMERZ Python library functions:
  - IPN hash validation
  - Transaction query by session key
  - Transaction query by tran_id
  - Refund status query
  - Object initialization (sandbox vs live)

Run with:
    python test.py
    python -m pytest test.py -v
"""

import unittest
from sslcommerz_lib import SSLCOMMERZ


# ── Shared test credentials (Sandbox) ─────────────────────────────────────────
SANDBOX_CONFIG = {
    'store_id'  : 'testbox',
    'store_pass': 'test_testemi@ssl',
    'issandbox' : True,
}

LIVE_CONFIG = {
    'store_id'  : 'your_live_store_id',
    'store_pass': 'your_live_store_pass',
    'issandbox' : False,
}


class TestSSLCommerzInit(unittest.TestCase):
    """Test SSLCOMMERZ object initialization."""

    def test_sandbox_mode_urls(self):
        """Sandbox mode should use sandbox.sslcommerz.com URLs."""
        gateway = SSLCOMMERZ(SANDBOX_CONFIG)
        self.assertEqual(gateway.mode, 'sandbox')
        self.assertIn('sandbox.sslcommerz.com', gateway.createSessionUrl)
        self.assertIn('sandbox.sslcommerz.com', gateway.validation_url)
        self.assertIn('sandbox.sslcommerz.com', gateway.transaction_url)

    def test_live_mode_urls(self):
        """Live mode should use securepay.sslcommerz.com URLs."""
        gateway = SSLCOMMERZ(LIVE_CONFIG)
        self.assertEqual(gateway.mode, 'securepay')
        self.assertIn('securepay.sslcommerz.com', gateway.createSessionUrl)

    def test_store_credentials_stored(self):
        """Store ID and password should be stored on the object."""
        gateway = SSLCOMMERZ(SANDBOX_CONFIG)
        self.assertEqual(gateway.store_id,   SANDBOX_CONFIG['store_id'])
        self.assertEqual(gateway.store_pass, SANDBOX_CONFIG['store_pass'])


class TestIPNHashValidation(unittest.TestCase):
    """Test the IPN hash validation logic."""

    def setUp(self):
        self.gateway = SSLCOMMERZ(SANDBOX_CONFIG)

        # Valid IPN payload from SSLCommerz sandbox
        self.valid_post_body = {
            'tran_id'                  : '5E121A0D01F92',
            'val_id'                   : '200105225826116qFnATY9sHIwo',
            'amount'                   : '10.00',
            'card_type'                : 'VISA-Dutch Bangla',
            'store_amount'             : '9.75',
            'card_no'                  : '418117XXXXXX6675',
            'bank_tran_id'             : '200105225825DBgSoRGLvczhFjj',
            'status'                   : 'VALID',
            'tran_date'                : '2020-01-05 22:58:21',
            'currency'                 : 'BDT',
            'card_issuer'              : 'TRUST BANK, LTD.',
            'card_brand'               : 'VISA',
            'card_issuer_country'      : 'Bangladesh',
            'card_issuer_country_code' : 'BD',
            'store_id'                 : 'test_testemi',
            'verify_sign'              : 'd42fab70ae0bcbda5280e7baffef60b0',
            'verify_key'               : (
                'amount,bank_tran_id,base_fair,card_brand,card_issuer,'
                'card_issuer_country,card_issuer_country_code,card_no,'
                'card_type,currency,currency_amount,currency_rate,'
                'currency_type,risk_level,risk_title,status,store_amount,'
                'store_id,tran_date,tran_id,val_id,value_a,value_b,'
                'value_c,value_d'
            ),
            'verify_sign_sha2'         : '02c0417ff467c109006382d56eedccecd68382e47245266e7b47abbb3d43976e',
            'currency_type'            : 'BDT',
            'currency_amount'          : '10.00',
            'currency_rate'            : '1.0000',
            'base_fair'                : '0.00',
            'value_a'                  : '',
            'value_b'                  : '',
            'value_c'                  : '',
            'value_d'                  : '',
            'risk_level'               : '0',
            'risk_title'               : 'Safe',
        }

    def test_valid_ipn_returns_true(self):
        """A properly signed IPN payload should validate successfully."""
        result = self.gateway.hash_validate_ipn(self.valid_post_body)
        self.assertTrue(result, "Valid IPN should return True")

    def test_tampered_amount_fails(self):
        """Tampering with any value should cause validation to fail."""
        tampered = dict(self.valid_post_body)
        tampered['amount'] = '999.00'   # tamper with amount
        result = self.gateway.hash_validate_ipn(tampered)
        self.assertFalse(result, "Tampered IPN should return False")

    def test_missing_verify_key_fails(self):
        """Missing verify_key should cause validation to fail."""
        payload = dict(self.valid_post_body)
        del payload['verify_key']
        result = self.gateway.hash_validate_ipn(payload)
        self.assertFalse(result)

    def test_missing_verify_sign_fails(self):
        """Missing verify_sign should cause validation to fail."""
        payload = dict(self.valid_post_body)
        del payload['verify_sign']
        result = self.gateway.hash_validate_ipn(payload)
        self.assertFalse(result)


class TestHelperMethods(unittest.TestCase):
    """Test internal utility methods."""

    def setUp(self):
        self.gateway = SSLCOMMERZ(SANDBOX_CONFIG)

    def test_checkKey_present(self):
        self.assertTrue(self.gateway.checkKey({'key': 'val'}, 'key'))

    def test_checkKey_absent(self):
        self.assertFalse(self.gateway.checkKey({'key': 'val'}, 'missing'))

    def test_ksort_returns_sorted(self):
        d = {'c': 3, 'a': 1, 'b': 2}
        result = self.gateway.ksort(d)
        keys = [k for k, _ in result]
        self.assertEqual(keys, ['a', 'b', 'c'])

    def test_ksort_returns_all_values(self):
        d = {'z': 'last', 'a': 'first'}
        result = dict(self.gateway.ksort(d))
        self.assertEqual(result['a'], 'first')
        self.assertEqual(result['z'], 'last')


class TestTransactionQueries(unittest.TestCase):
    """
    Live API tests — these require a real SSLCommerz sandbox connection.
    Skipped by default; remove the @unittest.skip decorator to run them.
    """

    def setUp(self):
        self.gateway = SSLCOMMERZ(SANDBOX_CONFIG)
        self.session_key = 'A8EF93B75B8107E4F36049E80B4F9149'
        self.tran_id     = '5E121A0D01F92'

    @unittest.skip("Requires live sandbox connection — run manually when needed.")
    def test_transaction_query_by_session(self):
        """Query transaction using session key."""
        response = self.gateway.transaction_query_session(self.session_key)
        self.assertIsInstance(response, dict)
        print("\n[session query]", response)

    @unittest.skip("Requires live sandbox connection — run manually when needed.")
    def test_transaction_query_by_tranid(self):
        """Query transaction using tran_id."""
        response = self.gateway.transaction_query_tranid(self.tran_id)
        self.assertIsInstance(response, dict)
        print("\n[tran_id query]", response)

    @unittest.skip("Requires live sandbox connection — run manually when needed.")
    def test_refund_status_query(self):
        """Query refund status using a refund reference ID."""
        response = self.gateway.query_refund_status('SAMPLE_REFUND_REF')
        self.assertIsInstance(response, dict)
        print("\n[refund status]", response)


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 60)
    print("  SSLCommerz Library Test Suite")
    print("=" * 60)
    unittest.main(verbosity=2)
