import unittest
from banking import Bank, Account

class TestBankSystem(unittest.TestCase):
    def setUp(self):
        self.bank = Bank()

    def test_create_account(self):
        account = self.bank.create_account("Alice", 500, "Savings")
        self.assertIsNotNone(account)
        self.assertEqual(account.name, "Alice")
        self.assertEqual(account.balance, 500)
        self.assertEqual(account.account_type, "Savings")

    def test_invalid_account_type(self):
        result = self.bank.create_account("Bob", 500, "InvalidType")
        self.assertIsInstance(result, str)
        self.assertIn("Invalid account type", result)

    def test_initial_deposit_limit(self):
        result = self.bank.create_account("Bob", 50, "Savings")
        self.assertIsInstance(result, str)
        self.assertIn("Initial deposit", result)

    def test_deposit(self):
        account = self.bank.create_account("Charlie", 300, "Checking")
        result = self.bank.deposit_to_account(account.account_number, 200)
        self.assertIn("Deposited", result)
        self.assertEqual(account.balance, 500)
        self.assertEqual(len(account.view_transactions('Deposit')), 1)

    def test_withdrawal(self):
        account = self.bank.create_account("David", 1000, "Business")
        result = self.bank.withdraw_from_account(account.account_number, 200)
        self.assertIn("Withdrew", result)
        self.assertEqual(account.balance, 800)
        self.assertEqual(len(account.view_transactions('Withdraw')), 1)

    def test_withdrawal_limit(self):
        account = self.bank.create_account("Eve", 10000, "Savings")
        result = self.bank.withdraw_from_account(account.account_number, 6000)
        self.assertIn("Daily withdrawal limit", result)

    def test_minimum_balance(self):
        account = self.bank.create_account("Frank", 100, "Savings")
        result = self.bank.withdraw_from_account(account.account_number, 50)
        self.assertIn("Minimum balance", result)

    def test_transfer(self):
        account1 = self.bank.create_account("Grace", 500, "Checking")
        account2 = self.bank.create_account("Heidi", 500, "Savings")
        result = self.bank.transfer(account1.account_number, account2.account_number, 200)
        self.assertIn("Transferred", result)
        self.assertEqual(account1.balance, 300)
        self.assertEqual(account2.balance, 700)

    def test_transfer_failure(self):
        account1 = self.bank.create_account("Ivan", 200, "Business")
        account2 = self.bank.create_account("Judy", 300, "Savings")
        result = self.bank.transfer(account1.account_number, account2.account_number, 1500)
        self.assertIn("Withdrawal denied", result)

    def test_apply_interest(self):
        account = self.bank.create_account("Kelly", 1000, "Savings")
        initial_balance = account.balance
        account.apply_interest()
        self.assertGreater(account.balance, initial_balance)
        self.assertEqual(len(account.view_transactions('Interest')), 1)

    def test_account_summary(self):
        account = self.bank.create_account("Leo", 800, "Business")
        self.bank.deposit_to_account(account.account_number, 200)
        self.bank.withdraw_from_account(account.account_number, 100)
        with self.assertLogs(level='INFO') as log:
            self.bank.get_account_summary(account.account_number)
        self.assertTrue(any("Total Transactions" in message for message in log.output))

if __name__ == '__main__':
    unittest.main()