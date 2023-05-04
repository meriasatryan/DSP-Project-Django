import logging
import os
import random

from django.db.models import Q
from django.views.generic import View

from final_project.utils.ads_txt import is_authorized
from game.models import Bid, Config, Creative, ViewFrequency
from final_project.utils.http_responses import *
from final_project.utils.optimize_f import optimize
# from .optimize import betting_limit_cpc
from final_project.utils.optimize2 import betting_limit_revenue, betting_limit_cpc
from final_project.utils.resize import resize


class BidView(View):

    def get(self, request):
        bids = Bid.objects.all()
        data = []
        for bid in bids:
            data.append({'id': bid.external_id,
                         'click_prob': bid.click_prob,
                         'conv_prob': bid.conv_prob,
                         'site_domain': bid.site_domain,
                         'user_id': bid.user_id if bid.user_id else '',
                         'price': float(bid.price)
                         })
        return data_status(data)

    @staticmethod
    def find_allowed_creatives(creatives_without_blocked_categories, user_id, frequency_capping):
        users = ViewFrequency.objects.filter(user_id=user_id)
        allowed_creatives = list(creatives_without_blocked_categories)
        if len(users) != 0:
            for user in users:
                for cr in allowed_creatives:
                    if user.campaign == cr.campaign and user.times_viewed == frequency_capping:
                        del cr
        return allowed_creatives

    @staticmethod
    def chosen_creative_and_price(error_happened, id, allowed_creatives):
        bid = Bid.objects.get(external_id=id)
        creative = None
        if not error_happened:
            print("current round is ------------- ", bid.current_round)
            for cr in allowed_creatives:
                print(cr.campaign.budget, "_________________________________________hhjhjhhjsdjhdfkjgjmhdn")
                if cr.campaign.budget >= bid.price:
                    print("found corresponding creative", cr.name)
                    creative = cr
                    break
            if not creative:
                print("choosing the last creative with the highest budget")
                creative = allowed_creatives[-1]
                bid.price = creative.campaign.budget
        else:
            creative = random.choice(allowed_creatives)
            bid.price = creative.campaign.bid_floor

        return {'bid_price': bid.price, 'creative': creative}

    @staticmethod
    def get_current_round():
        if Bid.objects.count() > 1:
            print("round__________", Bid.objects.order_by('id')[Bid.objects.count() - 2].current_round)
        return (Bid.objects.order_by('id')[Bid.objects.count() - 2].current_round + 1) if Bid.objects.count() > 1 else 1

    def post(self, request):
        data = json.loads(request.body.decode())
        bid = None
        try:
            float(data['click']['prob'])
            float(data['conv']['prob'])

            creative = None
            if 'bcat' in data:
                print("bcat exists in data")
                creatives_without_blocked_categories = Creative.objects.filter(~Q(categories__code__in=data['bcat']),
                                                                               campaign__enabled=True)
                for bcat in data['bcat']:
                    if len(bcat) <= 5:
                        creatives_without_blocked_categories = creatives_without_blocked_categories.filter(
                            ~Q(categories__code__startswith=bcat + '-'))
                # deleted from here

            else:
                print("there is no bcat in data")
                creatives_without_blocked_categories = Creative.objects.filter(campaign__enabled=True)
            # moved here
            if len(creatives_without_blocked_categories) == 0:
                print("length of creatives_without_blocked_categories is 0")
                bid = Bid.objects.create(
                    external_id=data['id']
                )
                # NOTE/CHECK: it was calculated in history
                bid.current_round = BidView.get_current_round()
                bid.save()
                return no_bid_status()

            try:
                frequency_capping = Config.get_solo().frequency_capping
                if not frequency_capping:
                    raise AttributeError
                print("frequency_capping exists")
                user_id = data['user']['id']
                print("user_id exists")
                allowed_creatives = BidView.find_allowed_creatives(creatives_without_blocked_categories, user_id,
                                                                   frequency_capping)
                if len(allowed_creatives) == 0:
                    print('there is no allowed creative for this user')
                    bid = Bid.objects.create(
                        external_id=data['id']
                    )
                    bid.current_round = BidView.get_current_round()
                    bid.save()
                    return no_bid_status()
                allowed_creatives = sorted(allowed_creatives, key=lambda x: x.campaign.budget)

            except Exception as e:
                print("frequency capping or user_id doesn't exist", e)
                logging.exception(e)
                allowed_creatives = sorted(list(creatives_without_blocked_categories), key=lambda x: x.campaign.budget)

            print('allowed_creatives___',allowed_creatives)

            print("creating bid")
            bid = Bid.objects.create(
                external_id=data['id'],
                click_prob=float(data['click']['prob']),
                conv_prob=float(data['conv']['prob']),
                site_domain=data['site']['domain'],
                price=0
            )
            bid.current_round = BidView.get_current_round()
            print("current round is ------------- ", bid.current_round)
            bid.save()

            error_happened = False
            try:
                auth_error_happened = False
                try:
                    is_auth_ssp = is_authorized(data['site']['domain'], data['ssp']['id'])
                    print("AUTHSSP    :", is_auth_ssp)
                except Exception as e:
                    auth_error_happened = True
                    print(e)

                print(Config.get_solo().game_goal, "game goal")
                # bid = Bid.objects.get(id=data['id'])
                current_total_budget = Config.get_solo().current_total_budget

                if Config.get_solo().game_goal == "revenue":
                    # bid = Bid.objects.get(id=data['id'])
                    op1 = optimize(current_total_budget, bid.click_prob, bid.external_id)
                    op2 = betting_limit_revenue(current_total_budget, bid.click_prob, bid.external_id)
                    bid.price = max(op1, op2)
                    print("______op1==", op1)
                    print("______op2==", op2)

                    print(bid.price, "after optimize")
                    bid.save()
                    if not auth_error_happened and not is_auth_ssp:
                        if bid.click_prob < 70:
                            bid.price = bid.price * 5 / 10
                            bid.save()
                if Config.get_solo().game_goal == "cpc":
                    op1 = optimize(current_total_budget, bid.click_prob, bid.external_id)
                    # op2 = betting_limit_cpc(current_total_budget, bid.click_prob, bid.external_id)
                    op2 = betting_limit_cpc(current_total_budget, bid.click_prob, bid.external_id)

                    bid.price = max(op1, op2)
                    print("______op1==", op1)
                    print("______op2==", op2)

                    bid.price = max(optimize(current_total_budget, bid.click_prob, bid.id),
                                    betting_limit_cpc(current_total_budget, bid.click_prob, bid.id))
                    print(bid.price, "after optimize")
                    bid.save()
                    if not auth_error_happened and not is_auth_ssp:
                        print("authorized agnesik")
                        if bid.click_prob < 70:
                            raise ValueError
                print(bid.current_round)
            except Exception as e:
                print("error occurred", e)
                logging.exception(e)
                error_happened = True

            chosen_creative_and_price = BidView.chosen_creative_and_price(error_happened, data['id'], allowed_creatives)
            bid.price = chosen_creative_and_price['bid_price']
            creative = chosen_creative_and_price['creative']
            if 'user' in data and 'id' in data['user']:
                user = ViewFrequency.objects.get_or_create(user_id=data['user']['id'], campaign=creative.campaign)[0]
                print(user, "user$$$$$$$$$$$$$$44")
                bid.user_id = user.user_id

            bid.creative = creative
            bid.save()

        except Exception as e:
            print('error occurred', e)
            logging.exception(e)
            if bid:
                bid.delete()
            return ok_status()
        if bid.price <= 0:
            print("bid.price is less or equal to 0", bid.price)
            return no_bid_status()

        category = creative.categories.all()
        cats = []
        for c in category:
            cats.append(c.code)
        img_parameters = resize(creative, data['imp']['banner']['h'], data['imp']['banner']['w'])
        ip_address = os.environ.get("DSP_IP")
        response = {"external_id": bid.creative.external_id, "price": float(bid.price),
                    "image_url": f"https://{ip_address}{img_parameters[2]}?width={img_parameters[0]}&height={img_parameters[1]}",
                    "cat": cats}
        bid.save()
        print(bid.price, "bid.price")
        return data_status(response)
