import unittest
import threading
from DigitalWallet import DigitalWallet


class WalletSecurityQA(unittest.TestCase):

    # 1. Normal transaction
    def test_normal_transaction(self):
        wallet = DigitalWallet("1234")

        wallet.deposit(5000)
        result = wallet.withdraw(1000)

        self.assertEqual(result, "Withdrawn 1000")
        self.assertEqual(wallet.get_balance(), 4000)

    # 2. Insufficient balance
    def test_insufficient_balance(self):
        wallet = DigitalWallet("1234")

        wallet.deposit(1000)
        result = wallet.withdraw(2000)

        self.assertEqual(result, "Insufficient balance")
        self.assertEqual(wallet.get_balance(), 1000)

    # 3. Daily transfer limit
    def test_daily_limit(self):
        wallet = DigitalWallet("1234")

        wallet.deposit(20000)
        result = wallet.transfer(15000)

        self.assertEqual(result, "Daily transfer limit exceeded")
        self.assertEqual(wallet.get_balance(), 20000)

    # 4. Failed PIN attempts
    def test_failed_pin_attempts(self):
        wallet = DigitalWallet("1234")

        wallet.verify_pin("0000")
        wallet.verify_pin("1111")
        wallet.verify_pin("2222")

        self.assertEqual(wallet.failed_attempts, 3)

    # 5. Suspicious transaction
    def test_suspicious_transaction(self):
        wallet = DigitalWallet("1234")

        wallet.deposit(5000)

        alerts = wallet.fraud_detection()

        self.assertIn("Suspicious large transaction", alerts)

    # 6. Duplicate transactions
    def test_duplicate_transactions(self):
        wallet = DigitalWallet("1234")

        wallet.deposit(1000)
        wallet.deposit(1000)

        history = wallet.transaction_history()

        self.assertEqual(len(history), 2)

        self.assertEqual(history[0], history[1])

    # 7. Negative amount
    def test_negative_amount(self):
        wallet = DigitalWallet("1234")

        result = wallet.deposit(-500)

        self.assertEqual(result, "Invalid amount")
        self.assertEqual(wallet.get_balance(), 0)

    # 8. Concurrent transactions
    def test_concurrent_transactions(self):
        wallet = DigitalWallet("1234")
        wallet.deposit(10000)

        def withdraw_money():
            wallet.withdraw(1000)

        threads = []

        for _ in range(5):
            thread = threading.Thread(target=withdraw_money)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        self.assertEqual(wallet.get_balance(), 5000)


if __name__ == "__main__":
    unittest.main(verbosity=2)