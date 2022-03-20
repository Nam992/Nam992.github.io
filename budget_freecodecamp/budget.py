class Category:

    def __init__(self, name):
      self.name = name
      self.ledger = []

    #deposit method
    def get_balance(self):
      total = 0
      for item in self.ledger:
        total += item['amount']
      return total

    def check_funds(self, amount):
        balance=self.get_balance()
        if amount>balance:
            fund=False
        else:
            fund=True
        return fund

    def deposit(self, amount, description=""):

        self.ledger.append({"amount": amount, "description": description})


    def withdraw(self, amount, description = ""):
        fund=self.check_funds(amount)
        if fund==True:
            self.ledger.append({"amount": -amount, "description": description})
            withd=True
        else:
            withd=False
        return withd

    def transfer(self, amount, budget_category):
        fund=self.check_funds(amount)
        if fund==True:
            self.withdraw(amount, f"Transfer to {budget_category.name}")
            budget_category.deposit(amount, f"Transfer from {self.name}")
            trans=True
        else:
            trans=False
        return trans

    def __repr__(self):
        part1=int((30-len(self.name))/2)
        #line1=("*"*(part1) + str(self.name) + "*"*(part1))
        #for item in self.ledger:
          #print( item["description"], item["amount"])
        footer = ("*"*(part1) + str(self.name) + "*"*(part1)) + "\n"
        for item in self.ledger:
            desc=item["description"]
            desc1=desc[0:23]
            am=float(item["amount"])
            am = "{:.2f}".format(am)
            am=str(am)
            am1=am[0:7]
            footer=footer +desc1 +am1.rjust(30-len(desc1))+ "\n"
        tot=self.get_balance()
        footer=footer+"Total: "+str(tot)
        return footer

def create_spend_chart(categories):
    spent_amounts = []
    # Get total spent in each category
    for category in categories:
        spent = 0
        for item in category.ledger:
            if item["amount"] < 0:
                spent += abs(item["amount"])
        spent_amounts.append(round(spent, 2))

    # Calculate percentage rounded down to the nearest 10
    total = round(sum(spent_amounts), 2)
    spent_percentage = list(map(lambda amount: int((((amount / total) * 10) // 1) * 10), spent_amounts))

    # Create the bar chart substrings
    header = "Percentage spent by category\n"

    chart = ""
    for value in reversed(range(0, 101, 10)):
        chart += str(value).rjust(3) + '|'
        for percent in spent_percentage:
            if percent >= value:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"

    footer = "    " + "-" * ((3 * len(categories)) + 1) + "\n"
    names = list(map(lambda category: category.name, categories))
    max_length = max(map(lambda name: len(name), names))
    names = list(map(lambda name: name.ljust(max_length), names))
    for x in zip(*names):
        footer += "    " + "".join(map(lambda s: s.center(3), x)) + " \n"

    return (header + chart + footer).rstrip("\n")
