from game.models import Bid, Config
from final_project.utils.http_responses import *
from decimal import Decimal


def betting_limit_revenue(budget, prob, bid_id):
    bid = Bid.objects.get(external_id=bid_id)
    rest_rounds = Config.get_solo().impressions_total - bid.current_round + 1
    budget_per_round = Decimal(budget) / Decimal(rest_rounds)
    percentage = prob * 100
    if 0 <= percentage < 40:
        if Config.get_solo().impression_revenue < budget_per_round:
            answer = Config.get_solo().impression_revenue
        else:
            answer = budget_per_round * 20 / 100
    elif 40 <= percentage < 50:
        if 1.1 * Config.get_solo().impression_revenue < budget_per_round:
            answer = 1.1 * Config.get_solo().impression_revenue
        else:
            answer = budget_per_round * 50 / 100
    elif 50 <= percentage < 70:
        answer = Decimal(prob) * Decimal(budget_per_round)
    elif 70 <= percentage <= 100:
        answer = budget_per_round
    else:
        return failed_status("percentage is either negative or greater than 100")

    if Bid.objects.count() > 1:
        penultimate_history = Bid.objects.order_by('id')[Bid.objects.count() - 2]
        # print(penultimate_history)
        if 60 > percentage > penultimate_history.click_prob * 100:
            print("increased _________________-")
            will_be_increased = Decimal((percentage - penultimate_history.click_prob * 100) // 10)
            answer = Decimal(answer)
            answer += Decimal(budget_per_round * will_be_increased) / 100
            return answer
        elif not penultimate_history.win and penultimate_history.click_prob == prob:
            print("same prob _____________________________")
            answer = Decimal(answer)
            if Decimal(answer) + budget_per_round * 10 / 100 <= budget_per_round:
                answer += Decimal(budget_per_round) * 10 / 100
            return answer
    return answer


def betting_limit_cpc(budget, prob, bid_id):
    bid = Bid.objects.get(external_id=bid_id)
    rest_rounds = Config.get_solo().impressions_total - bid.current_round + 1
    budget_per_round = Decimal(budget) / Decimal(rest_rounds)
    # print(budget_for_round)
    percentage = prob * 100
    if 0 <= percentage < 40:
        answer = budget_per_round * 25 / 100
    elif 40 <= percentage < 50:
        answer = budget_per_round * 40 / 100
    elif 50 <= percentage < 70:
        answer = budget_per_round * 60 / 100
    elif 70 <= percentage <= 80:
        answer = budget_per_round * 80 / 100
    elif 80 < percentage <= 100:
        answer = budget_per_round
    else:
        return failed_status("percentage is either negative or greater than 100")

    if Bid.objects.count() > 1:
        penultimate_history = Bid.objects.order_by('id')[Bid.objects.count() - 2]
        # print(penultimate_history)
        if 60 > percentage > penultimate_history.click_prob * 100:
            print("increased _________________-")
            will_be_increased = Decimal((percentage - penultimate_history.click_prob * 100) // 10)
            answer = Decimal(answer)
            answer += Decimal(budget_per_round * will_be_increased) / 100
            return answer
        elif not penultimate_history.win and penultimate_history.click_prob == prob:
            print("same prob _____________________________")
            answer = Decimal(answer)
            if Decimal(answer) + budget_per_round * 10 / 100 <= budget_per_round:
                answer += Decimal(budget_per_round) * 10 / 100
            return answer

    return answer
