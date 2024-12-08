import datetime

# Constants for transaction limits
DAILY_WITHDRAWAL_LIMIT = 5000.0
MINIMUM_BALANCE = 100.0
ACCOUNT_TYPES = {
    'Savings': 0.01,  # Interest rate of 1%
    'Checking': 0.00,  # No interest
    'Business': 0.02   # Interest rate of 2%
}

# Account class to handle individual account data
class Account:
    def __init__(self, account_number, name, initial_deposit, account_type='Savings'):
        self.account_number = account_number
        self.name = name
        self.balance = initial_deposit
        self.account_type = account_type
        self.transactions = []  # Record of transactions
        self.daily_withdrawal_total = 0.0
        self.last_withdrawal_date = None
        self.account_open_date = datetime.datetime.now()

    def deposit(self, amount):
        if amount <= 0:
            return "Deposit amount must be positive."
        try:
            self.balance += amount
            self.log_transaction('Deposit', amount)
            return f"Deposited {amount}. New balance is {self.balance}."
        except Exception as e:
            return f"Error during deposit: {str(e)}"

    def withdraw(self, amount):
        if amount <= 0:
            return "Withdrawal amount must be positive."
        
        today = datetime.date.today()
        
        if self.last_withdrawal_date != today:
            self.daily_withdrawal_total = 0
        
        if (self.daily_withdrawal_total + amount > DAILY_WITHDRAWAL_LIMIT):
            return "Daily withdrawal limit exceeded."
        
        if self.balance - amount < MINIMUM_BALANCE:
            return f"Withdrawal denied. Minimum balance should be {MINIMUM_BALANCE}."
        
        try:
            self.balance -= amount
            self.daily_withdrawal_total += amount
            self.last_withdrawal_date = today
            self.log_transaction('Withdraw', amount)
            return f"Withdrew {amount}. New balance is {self.balance}."
        except Exception as e:
            return f"Error during withdrawal: {str(e)}"

    def apply_interest(self):
        try:
            interest_rate = ACCOUNT_TYPES.get(self.account_type, 0)
            interest_amount = self.balance * interest_rate
            self.balance += interest_amount
            self.log_transaction('Interest', interest_amount)
            print(f"Interest of {interest_amount} applied. New balance is {self.balance}.")
        except Exception as e:
            print(f"Error applying interest: {str(e)}")

    def log_transaction(self, transaction_type, amount):
        transaction_record = {
            'type': transaction_type,
            'amount': amount,
            'date': datetime.datetime.now()
        }
        self.transactions.append(transaction_record)

    def view_details(self):
        details = (
            f"Account Number: {self.account_number}, Name: {self.name}, "
            f"Balance: {self.balance}, Account Type: {self.account_type}, "
            f"Opened On: {self.account_open_date.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        return details

    def view_transactions(self, filter_type=None):
        filtered_transactions = [
            transaction for transaction in self.transactions
            if filter_type is None or transaction['type'] == filter_type
        ]
        return filtered_transactions

# Bank class to manage multiple accounts
class Bank:
    def __init__(self):
        self.accounts = {}
    
    def create_account(self, name, initial_deposit, account_type='Savings'):
        account_number = len(self.accounts) + 1
        if initial_deposit < MINIMUM_BALANCE:
            return f"Error: Initial deposit must be at least {MINIMUM_BALANCE}."
        
        if account_type not in ACCOUNT_TYPES:
            return f"Error: Invalid account type. Available types: {', '.join(ACCOUNT_TYPES.keys())}."

        account = Account(account_number, name, initial_deposit, account_type)
        self.accounts[account_number] = account
        return account

    def get_account(self, account_number):
        return self.accounts.get(account_number, None)

    def deposit_to_account(self, account_number, amount):
        account = self.get_account(account_number)
        if not account:
            return "Account not found."
        return account.deposit(amount)

    def withdraw_from_account(self, account_number, amount):
        account = self.get_account(account_number)
        if not account:
            return "Account not found."
        return account.withdraw(amount)

    def transfer(self, from_account_number, to_account_number, amount):
        from_account = self.get_account(from_account_number)
        to_account = self.get_account(to_account_number)
        if not from_account or not to_account:
            return "One or both accounts not found."
        
        withdraw_message = from_account.withdraw(amount)
        if "Withdrew" in withdraw_message:
            to_account.deposit(amount)
            return f"Transferred {amount} from {from_account_number} to {to_account_number}."
        else:
            return withdraw_message

    def apply_monthly_interest(self):
        for account in self.accounts.values():
            account.apply_interest()

    def get_account_summary(self, account_number):
        account = self.get_account(account_number)
        if account:
            details = account.view_details()
            transaction_count = len(account.transactions)
            total_deposits = sum(
                trans['amount'] for trans in account.transactions if trans['type'] == 'Deposit'
            )
            total_withdrawals = sum(
                trans['amount'] for trans in account.transactions if trans['type'] == 'Withdraw'
            )
            summary = (
                f"{details}\nTotal Transactions: {transaction_count}\n"
                f"Total Deposits: {total_deposits}, Total Withdrawals: {total_withdrawals}"
            )
            print(summary)
        else:
            print("Account not found.")

def main():
    bank = Bank()
    while True:
        print("\n=== Bank Management System ===")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. View Account Details")
        print("6. View Transactions")
        print("7. Apply Monthly Interest")
        print("8. View Account Summary")
        print("9. Exit")
        
        choice = input("Enter your choice: ")
        
        try:
            if choice == "1":
                name = input("Enter account holder's name: ")
                initial_deposit = float(input("Enter initial deposit: "))
                account_type = input(f"Enter account type ({', '.join(ACCOUNT_TYPES.keys())}): ")
                account = bank.create_account(name, initial_deposit, account_type)
                if isinstance(account, str):
                    print(account)
                else:
                    print(f"Account created successfully. Account Number: {account.account_number}") 
                 
            elif choice == "2":
                account_number = int(input("Enter account number: "))
                amount = float(input("Enter deposit amount: "))
                print(bank.deposit_to_account(account_number, amount))
            
            elif choice == "3":
                account_number = int(input("Enter account number: "))
                amount = float(input("Enter withdrawal amount: "))
                print(bank.withdraw_from_account(account_number, amount))
            
            elif choice == "4":
                from_account_number = int(input("Enter from account number: "))
                to_account_number = int(input("Enter to account number: "))
                amount = float(input("Enter transfer amount: "))
                print(bank.transfer(from_account_number, to_account_number, amount))

            elif choice == "5":
                account_number = int(input("Enter account number: "))
                account = bank.get_account(account_number)
                if account:
                    print(account.view_details())
                else:
                    print("Account not found.")

            elif choice == "6":
                account_number = int(input("Enter account number: "))
                account = bank.get_account(account_number)
                if account:
                    filter_type = input("Enter transaction type to filter (Deposit, Withdraw, or leave blank for all): ")
                    transactions = account.view_transactions(filter_type if filter_type else None)
                    if transactions:
                        for transaction in transactions:
                            print(f"Type: {transaction['type']}, Amount: {transaction['amount']}, Date: {transaction['date']}")
                    else:
                        print("No transactions found.")
                else:
                    print("Account not found.")

            elif choice == "7":
                bank.apply_monthly_interest()
                print("Monthly interest applied to all accounts.")

            elif choice == "8":
                account_number = int(input("Enter account number: "))
                bank.get_account_summary(account_number)

            elif choice == "9":
                print("Exiting the system.")
                break
            else:
                print("Invalid choice, please try again.")
        except ValueError as e:
            print(f"Invalid input: {str(e)}")

if __name__ == "__main__":
    main()