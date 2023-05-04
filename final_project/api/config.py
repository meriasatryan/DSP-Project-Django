import json
from decimal import Decimal

from django.views.generic import View
from django.contrib.auth.models import Permission

from final_project.utils.load_categories import load_categories
from game.models import Config, Campaign, Bid, Category
from final_project.utils.http_responses import ok_status, failed_status, data_status


class ConfigView(View):
    """
    View for retrieving and updating the global configuration of the game.
    """

    def get(self, request):
        """
        Returns the current global configuration of the game.

        Returns:
            HTTP response with the current configuration data.
        """
        try:
            config = Config.get_solo()
            data = {"id": config.id, "impressions_total": config.impressions_total, "auction_type": config.auction_type,
                    "mode": config.mode, "budget": float(config.budget),
                    "impression_revenue": config.impression_revenue, "click_revenue": config.click_revenue,
                    "conversion_revenue": config.conversion_revenue, "frequency_capping": config.frequency_capping}
            return data_status(data)
        except IndexError:
            return failed_status("no_config")

    def post(self, request):
        """
        Updates the global configuration of the game.

        Args:
            request: HTTP request containing the updated configuration data.

        Returns:
            HTTP response indicating the success or failure of the update.
        """

        data = json.loads(request.body)
        if 'coefficient' in data:
            config = Config.get_solo()
            config.coefficient = data['coefficient']
            config.save()
        else:

            try:
                if data['auction_type'] not in [1, 2]:
                    print("auction type 1 or 2")
                    return ok_status()
                if data['mode'] not in ['script', 'free']:
                    print("mode is script or free")
                    return ok_status()
                if data['game_goal'] not in ['revenue', 'cpc']:
                    print("game goal is cpc or revenue")
                    return ok_status()
                Campaign.objects.all().delete()
                config = Config.get_solo()
                config.impressions_total = data['impressions_total']
                config.auction_type = data['auction_type']
                config.mode = data['mode']
                config.budget = Decimal(data['budget'])
                config.current_total_budget = config.budget
                config.impression_revenue = data['impression_revenue']
                config.click_revenue = data['click_revenue']
                config.conversion_revenue = data['conversion_revenue']
                config.game_goal = data['game_goal']
                if 'frequency_capping' in data:
                    config.frequency_capping = data['frequency_capping']
                else:
                    config.frequency_capping = None
                if not Category.objects.all().first():
                    load_categories('static/Content-Taxonomy-1.0.xlsx')
                if not Permission.objects.filter(codename='adops_permission').exists():
                    Permission.objects.create(
                        codename='adops_permission',
                        name='AdOps Permission',
                        content_type_id=1
                    )
                Bid.objects.all().delete()
                config.save()
            except KeyError:
                print("invalid post date")
                return ok_status()
            except TypeError:
                print("type error")
                return ok_status()
        return ok_status()
