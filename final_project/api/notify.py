from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View

from game.models import Bid, ViewFrequency, Config
from final_project.utils.http_responses import *


class NotifyView(View):
    """
    A view for handling notification requests from the Ad Exchange.

    Upon receiving a notification, this view updates the corresponding Bid
    object with information about the outcome of the auction. If the bid was
    successful, the view also updates the campaign budget and revenue.

    Returns:
        HttpResponse: A response indicating that the notification was received
        and processed.
    """

    def post(self, request):
        print("NOTIFY: received")
        data = json.loads(request.body.decode())
        bid = None
        try:
            id = data['id']
            win = data['win']
            if win:
                price = Decimal(data['price'])
                click = data['click']
                conversion = data['conversion']
                revenue = data['revenue']

        except KeyError:
            print("missed parameter")
            return ok_status()
        try:
            bid = Bid.objects.get(external_id=data['id'])
            bid.win = win
            if win:
                bid.creative.campaign.budget -= price
                config = Config.get_solo()
                config.current_total_budget -= price
                config.save()
                bid.revenue += data['revenue']
                bid.creative.campaign.save()
                bid.click_happened = click
                bid.conversion_happened = conversion
                print('check if there is a user_id in bid')
                if bid.user_id:
                    user = ViewFrequency.objects.get(user_id=bid.user_id, campaign=bid.creative.campaign)
                    user.times_viewed += 1
                    user.save()
            bid.save()
        except ObjectDoesNotExist:
            return ok_status()
        return notify_status()
