from typing import List


def best_profit(history: List[float]) -> float:
    totalProfit = 1
    for i in range(1, len(history)):
        profit = history[i] / history[i - 1]
        if profit > 1:
            totalProfit *= profit
    return totalProfit

        