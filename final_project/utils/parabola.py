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

    previous_bid_price = max_bid * Decimal(click_prob)
    bid_price = max_bid * Decimal(click_prob)
    learning_rate = 0.005
    gradient = -click_prob * 2 * (previous_bid_price - max_bid / 2)

    # learning_rate += 0.01

    for i in range(num_requests):
        gradient = -click_prob * 2 * previous_bid_price
        if bid_price - Decimal(learning_rate * gradient) < max_bid:
            bid_price -= Decimal(learning_rate * gradient)
            previous_bid_price = bid_price
        else:
            break
        # print(bid_price)
    #

    bid.save()
    return Decimal(bid_price)
