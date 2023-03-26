from basket import Basket
from model import Model
import math
import numpy


class Strategy:
    def __init__(self, data, capital=100000, commodities=['gold', 'silver', 'oil']):
        self.data = data
        self.capital = capital
        self.commodities = commodities
        self.basket = Basket(capital/10, commodities)

    def next_week(self, current_values, alpha=0.2):
        percentile_preds = {}
        for commodity in self.commodities:
            current_value = current_values[commodity]
            percentile_preds[commodity] = (
                predict(commodity, commodity) - current_value)/current_value

        percentile_preds = dict(
            sorted(percentile_preds.items(), key=lambda x: x[1]))

        self._selling_strategy(percentile_preds, alpha)
        self._buying_strategy(percentile_preds, alpha)

    def _selling_strategy(self, percentile_preds, alpha, current_values={'gold': 15, 'silver': 10, 'oil': 20}):
        percentile_preds_down = {key: value for key,
                                 value in percentile_preds.items()
                                 if value < 0}

        for commodity, perc in percentile_preds_down.items():
            current_value = current_values[commodity]
            self.basket._sell(commodity, math.ceil(
                alpha*abs(perc)*getattr(self.basket, commodity)), current_value)

    def _buying_strategy(self, percentile_preds, alpha, current_values={'gold': 15, 'silver': 10, 'oil': 20}):
        percentile_preds_up = {key: value for key,
                               value in percentile_preds.items() if value > 0}
        percentile_preds_up = dict(sorted(percentile_preds_up.items(
        ), key=lambda x: x[1], reverse=True))
        for commodity, perc in percentile_preds_up.items():
            current_value = current_values[commodity]
            self.basket._buy(commodity, alpha *
                             self.basket.money*perc, current_value)

    def portfolio(self, current_values={'gold': 15, 'silver': 10, 'oil': 20}):
        portfolio = self.basket.money
        for commodity, value in current_values.items():
            portfolio += getattr(self.basket, commodity)*value
        return portfolio
