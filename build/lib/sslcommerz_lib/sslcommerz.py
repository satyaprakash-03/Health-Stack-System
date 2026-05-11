import requests
import hashlib
import logging

logger = logging.getLogger(__name__)


class SSLCOMMERZ(object):
    """
    SSLCommerz Payment Gateway integration library.

    Supports:
      - Payment session creation
      - Transaction validation
      - Refund initiation & status query
      - Transaction query by session / tran_id
      - IPN hash validation
    """

    store_id       = None
    store_pass     = None
    issandbox      = None
    mode           = None
    createSessionUrl = None
    validation_url   = None
    transaction_url  = None

    def __init__(self, config):
        """
        Initialize the SSLCOMMERZ gateway client.

        Args:
            config (dict): Must contain:
                - 'store_id'   : Your SSLCommerz store ID
                - 'store_pass' : Your SSLCommerz store password
                - 'issandbox'  : True → sandbox mode | False → live mode
        """
        self.store_id  = config['store_id']
        self.store_pass = config['store_pass']
        self.mode = 'sandbox' if config['issandbox'] else 'securepay'

        self.createSessionUrl = (
            f"https://{self.mode}.sslcommerz.com/gwprocess/v4/api.php"
        )
        self.validation_url = (
            f"https://{self.mode}.sslcommerz.com/validator/api/validationserverAPI.php"
        )
        self.transaction_url = (
            f"https://{self.mode}.sslcommerz.com/validator/api/merchantTransIDvalidationAPI.php"
        )

    # ──────────────────────────────────────────────────────────────
    # SESSION
    # ──────────────────────────────────────────────────────────────
    def createSession(self, post_body):
        """
        Create a payment session with SSLCommerz.

        Args:
            post_body (dict): Payment parameters. Mandatory fields include:
                total_amount, currency, tran_id, success_url, fail_url,
                cancel_url, cus_name, cus_email, cus_phone, cus_add1,
                cus_city, cus_country.
                Refer: https://developer.sslcommerz.com/

        Returns:
            dict: SSLCommerz API JSON response.
        """
        post_body['store_id']     = self.store_id
        post_body['store_passwd'] = self.store_pass
        return self.call_api('POST', self.createSessionUrl, post_body)

    # ──────────────────────────────────────────────────────────────
    # VALIDATION
    # ──────────────────────────────────────────────────────────────
    def validationTransactionOrder(self, validation_id):
        """
        Validate a completed transaction.

        Args:
            validation_id (str): The val_id returned by SSLCommerz
                                 after a successful payment.

        Returns:
            dict: Validation result from SSLCommerz API.
        """
        params = {
            'val_id'      : validation_id,
            'store_id'    : self.store_id,
            'store_passwd': self.store_pass,
            'format'      : 'json',
        }
        return self.call_api('GET', self.validation_url, params)

    # ──────────────────────────────────────────────────────────────
    # REFUND
    # ──────────────────────────────────────────────────────────────
    def init_refund(self, bank_tran_id, refund_amount, refund_remarks):
        """
        Initiate a refund for a transaction.

        Args:
            bank_tran_id   (str): Bank-end transaction ID.
            refund_amount  (float): Amount to refund.
            refund_remarks (str): Reason for refund.

        Returns:
            dict: Refund initiation response.
        """
        params = {
            'bank_tran_id'  : bank_tran_id,
            'refund_amount' : refund_amount,
            'refund_remarks': refund_remarks,
            'store_id'      : self.store_id,
            'store_passwd'  : self.store_pass,
            'format'        : 'json',
        }
        return self.call_api('GET', self.transaction_url, params)

    def query_refund_status(self, refund_ref_id):
        """
        Query the status of an initiated refund.

        Args:
            refund_ref_id (str): Reference ID returned when refund was initiated.

        Returns:
            dict: Refund status response.
        """
        params = {
            'refund_ref_id': refund_ref_id,
            'store_id'     : self.store_id,
            'store_passwd' : self.store_pass,
            'format'       : 'json',
        }
        return self.call_api('GET', self.transaction_url, params)

    # ──────────────────────────────────────────────────────────────
    # TRANSACTION QUERIES
    # ──────────────────────────────────────────────────────────────
    def transaction_query_session(self, sessionkey):
        """
        Query a transaction by session key.

        Args:
            sessionkey (str): Session key generated during transaction initiation.

        Returns:
            dict: Transaction details.
        """
        params = {
            'sessionkey'  : sessionkey,
            'store_id'    : self.store_id,
            'store_passwd': self.store_pass,
            'format'      : 'json',
        }
        return self.call_api('GET', self.transaction_url, params)

    def transaction_query_tranid(self, tran_id):
        """
        Query a transaction by your custom Transaction ID.

        Args:
            tran_id (str): The tran_id you sent during session creation.

        Returns:
            dict: Transaction details.
        """
        params = {
            'tran_id'     : tran_id,
            'store_id'    : self.store_id,
            'store_passwd': self.store_pass,
            'format'      : 'json',
        }
        return self.call_api('GET', self.transaction_url, params)

    # ──────────────────────────────────────────────────────────────
    # IPN HASH VALIDATION
    # ──────────────────────────────────────────────────────────────
    def hash_validate_ipn(self, post_body):
        """
        Validate the IPN (Instant Payment Notification) from SSLCommerz
        using MD5 hash comparison to prevent tampering.

        Args:
            post_body (dict): The POST data received from SSLCommerz IPN.

        Returns:
            bool: True if the IPN is valid, False otherwise.
        """
        if not (self.checkKey(post_body, 'verify_key') and
                self.checkKey(post_body, 'verify_sign')):
            logger.warning("IPN validation failed: missing verify_key or verify_sign.")
            return False

        verify_keys = post_body['verify_key'].split(",")
        new_params = {key: post_body[key] for key in verify_keys}

        # Hash the store password
        hashed_pass = hashlib.md5(self.store_pass.encode()).hexdigest()
        new_params['store_passwd'] = hashed_pass

        # Sort and build hash string
        sorted_params = self.ksort(new_params)
        hash_string = '&'.join(f"{k}={v}" for k, v in sorted_params)
        computed_hash = hashlib.md5(hash_string.encode()).hexdigest()

        if computed_hash == post_body['verify_sign']:
            return True

        logger.warning("IPN hash mismatch. Possible tampering detected.")
        return False

    # ──────────────────────────────────────────────────────────────
    # HELPERS
    # ──────────────────────────────────────────────────────────────
    def checkKey(self, post_body, key):
        """Check if a key exists in the given dict."""
        return key in post_body

    def ksort(self, d):
        """Return dict items sorted by key (PHP ksort equivalent)."""
        return [(k, d[k]) for k in sorted(d.keys())]

    def call_api(self, method, url, payload):
        """
        Internal method to make HTTP calls to the SSLCommerz API.

        Args:
            method  (str): 'GET', 'POST', 'PUT', or 'DELETE'
            url     (str): Target URL
            payload (dict): Request parameters / body

        Returns:
            dict | None: Parsed JSON response, or None on failure.
        """
        try:
            method = method.upper()

            if method == 'POST':
                response = requests.post(url, data=payload, timeout=30)
            elif method == 'GET':
                response = requests.get(url, params=payload, timeout=30)
            elif method == 'PUT':
                response = requests.put(url, data=payload, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(url, timeout=30)
            else:
                logger.error(f"call_api: Invalid HTTP method '{method}'")
                return {'error': f"HTTP method '{method}' is not supported."}

            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout:
            logger.error(f"SSLCommerz API timed out: {url}")
            return {'error': 'Request timed out. Please try again.'}

        except requests.exceptions.ConnectionError:
            logger.error(f"SSLCommerz API connection error: {url}")
            return {'error': 'Connection failed. Check your internet or SSLCommerz status.'}

        except requests.exceptions.HTTPError as e:
            logger.error(f"SSLCommerz HTTP error: {e}")
            return {'error': str(e)}

        except Exception as e:
            logger.exception(f"Unexpected error in SSLCommerz call_api: {e}")
            return {'error': 'An unexpected error occurred.'}
