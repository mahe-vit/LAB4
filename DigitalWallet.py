class DigitalWallet:
    DAILY_LIMIT = 10000

    def __init__(self, pin):
        self.pin = pin
        self.balance = 0
        self.failed_attempts = 0
        self.transactions = []

    def verify_pin(self, entered_pin):
        if entered_pin == self.pin:
            self.failed_attempts = 0
            return True

        self.failed_attempts += 1
        return False

    def deposit(self, amount):
        if amount <= 0:
            return "Invalid amount"

        self.balance += amount
        self.transactions.append(("Deposit", amount))
        return f"Deposited {amount}"

    def withdraw(self, amount):
        if amount <= 0:
            return "Invalid amount"

        if amount > self.balance:
            return "Insufficient balance"

        self.balance -= amount
        self.transactions.append(("Withdrawal", amount))
        return f"Withdrawn {amount}"

    def transfer(self, amount):
        if amount <= 0:
            return "Invalid amount"

        if amount > self.DAILY_LIMIT:
            return "Daily transfer limit exceeded"

        if amount > self.balance:
            return "Insufficient balance"

        self.balance -= amount
        self.transactions.append(("Transfer", amount))
        return "Transfer successful"

    def get_balance(self):
        return self.balance

    def transaction_history(self):
        return self.transactions

    def fraud_detection(self):
        flags = []

        if self.failed_attempts >= 3:
            flags.append("Multiple failed PIN attempts")

        if any(amount >= 5000 for _, amount in self.transactions):
            flags.append("Suspicious large transaction")

        if len(self.transactions) > 10:
            flags.append("Unusually high transaction count")

        return flags


if __name__ == "__main__":
    wallet = DigitalWallet("1234")

    print("Digital Wallet System")
    print("---------------------")

    print(wallet.deposit(5000))
    print(wallet.withdraw(1000))
    print(wallet.transfer(2000))

    print("Current Balance:", wallet.get_balance())
    print("Transaction History:", wallet.transaction_history())
    print("Fraud Alerts:", wallet.fraud_detection())