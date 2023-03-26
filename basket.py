import math


class Basket:
    def __init__(self, commodities):
        for com in commodities:
            setattr(self, com, 0)

    def _buy(self, commodity, investment_money, stock_value):
        money_diff = 0
        if investment_money > stock_value:
            shares = math.floor(investment_money/stock_value)
            money_diff = -shares*stock_value
            setattr(self, commodity, getattr(self, commodity)+shares)
        return money_diff

    def _sell(self, commodity, shares, value):
        money_diff = shares*value
        setattr(self, commodity, getattr(self, commodity)-shares)
        return money_diff
