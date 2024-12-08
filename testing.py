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

    def test_invalid_initial_deposit(self):
        result = self.bank.create_account("Bob", 50, "Savings")
        self.assertIsInstance(result, str)
        self.assertIn("Initial deposit", result)

    def test_deposit(self):
        account = self.bank.create_account("Charlie", 300, "Checking")
        result_1 = self.bank.deposit_to_account(account.account_number, 200)
        result_2 = self.bank.deposit_to_account(account.account_number, -50)
        self.assertIn("Deposited", result_1)
        self.assertEqual(account.balance, 500)
        self.assertEqual(len(account.view_transactions('Deposit')), 1)
        self.assertIn("positive", result_2)  # Handle error message for negative deposit

    def test_withdrawal(self):
        account = self.bank.create_account("David", 1000, "Business")
        result_1 = self.bank.withdraw_from_account(account.account_number, 200)
        result_2 = self.bank.withdraw_from_account(account.account_number, 2000)  # Overdraw test
        self.assertIn("Withdrew", result_1)
        self.assertEqual(account.balance, 800)
        self.assertIn("denied", result_2)

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

    def test_transfer_failure_insufficient_balance(self):
        account1 = self.bank.create_account("Ivan", 200, "Business")
        account2 = self.bank.create_account("Judy", 300, "Savings")
        result = self.bank.transfer(account1.account_number, account2.account_number, 1500)
        self.assertIn("Withdrawal denied", result)

    def test_transfer_between_nonexistent_accounts(self):
        result = self.bank.transfer(999, 1000, 100)
        self.assertIn("One or both accounts not found", result)

    def test_apply_interest(self):
        account = self.bank.create_account("Kelly", 1000, "Savings")
        initial_balance = account.balance
        account.apply_interest()
        self.assertGreater(account.balance, initial_balance)
        self.assertEqual(len(account.view_transactions('Interest')), 1)

    def test_view_transactions_with_filter(self):
        account = self.bank.create_account("Morgan", 1000, "Savings")
        self.bank.deposit_to_account(account.account_number, 500)
        self.bank.withdraw_from_account(account.account_number, 300)
        deposits = account.view_transactions('Deposit')
        withdrawals = account.view_transactions('Withdraw')
        self.assertEqual(len(deposits), 1)
        self.assertEqual(len(withdrawals), 1)

if __name__ == '__main__':
    unittest.main()