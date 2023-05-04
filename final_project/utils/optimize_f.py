import numpy as np
from django.db.models import Q

from game.models import Bid, Config
from decimal import Decimal


def cost_gradient(click_prob, max_bid, bid_price):
    return -click_prob


def cost_function(click_prob, max_bid, bid_price):
    return Decimal(-click_prob) * Decimal(bid_price - max_bid)


def optimize(budget, click_prob, id):
    num_requests = Bid.objects.count()
    bid = Bid.objects.get(external_id=id)
    rest_rounds = Config.get_solo().impressions_total - bid.current_round + 1
    max_bid = Config.get_solo().coefficient * (Decimal(budget) / Decimal(rest_rounds))

    learning_rate = 0.01

    bid_price = max_bid * Decimal(click_prob)
    cost = 0
    gradient = 0
    for j in range(num_requests):
        c = cost_function(click_prob, max_bid, bid_price)
        g = cost_gradient(click_prob, max_bid, bid_price)
        cost += c
        gradient += g
    cost /= num_requests
    gradient /= num_requests

    learning_rate += 0.01

    # Update the bid price
    if bid_price - Decimal(learning_rate * gradient) > 0:

        bid_price -= Decimal(learning_rate * gradient)

    # Print the current cost and bid price
    print(f"cost={cost}, bid_price={bid_price}")

    # Check for convergence
    if np.abs(gradient) < 1e-6:
        print("Converged!")

        # print("________________________________", f"cost={cost}, bid_price={bid_price}")
    # bid.price = Decimal(bid_price)
    bid.save()
    return Decimal(bid_price)
