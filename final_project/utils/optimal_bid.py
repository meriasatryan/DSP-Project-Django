import math


def calculate_optimal_bid(total_budget, num_impressions, click_prob, imp_prob, revenue_amount, frequency_capping,
                          conv_prob, auction_type):
    # Calculate expected click and conversion rates
    expected_click_rate = click_prob * imp_prob
    expected_conv_rate = expected_click_rate * conv_prob

    # Calculate expected revenue per impression
    expected_revenue = revenue_amount * expected_conv_rate

    # Calculate the maximum number of impressions per campaign based on the frequency capping
    max_impressions = math.ceil(num_impressions / frequency_capping)

    # Calculate the maximum bid price that can be spent per impression
    max_bid_price = total_budget / max_impressions

    # Calculate the expected revenue per bid
    expected_bid_revenue = expected_revenue * max_bid_price

    # Calculate the optimal bid price based on the auction type
    if auction_type == '1st_price':
        optimal_bid_price = max_bid_price
    elif auction_type == '2nd_price':
        optimal_bid_price = max_bid_price * expected_bid_revenue / expected_revenue

    return optimal_bid_price
