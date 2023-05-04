from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View

from game.models import Campaign, Config
from final_project.utils.http_responses import *


class CampaignView(View):
    """
    A View for handling Campaign related requests.
    """

    def get(self, request):
        """
        Returns all Campaign objects.

        Returns:
            A HTTP response with a list of Campaign objects.
        """
        campaigns = Campaign.objects.all()
        data = []
        for campaign in campaigns:
            data.append({'id': campaign.id, 'name': campaign.name, 'budget': float(campaign.budget),
                         'reserved_budget': float(campaign.reserved_budget), 'enabled': campaign.enabled,
                         'bid_floor': float(campaign.bid_floor)})
        return data_status(data)

    def post(self, request):
        """
        Creates a new Campaign object.

        Returns:
            A HTTP response with the new Campaign object.
        """
        data = json.loads(request.body)
        campaign = None
        if 'name' in data and 'budget' in data:
            used_budget = 0
            for c in Campaign.objects.all():
                used_budget += c.reserved_budget
            max_buget = Config.get_solo().budget - used_budget
            if Decimal(data['budget']) <= max_buget:
                campaign = Campaign.objects.create(
                    name=data['name'],
                    budget=Decimal(data['budget']),
                    reserved_budget=Decimal(data['budget'])
                )
        else:
            return ok_status()
        if campaign:
            campaign.bid_floor = campaign.budget / Config.get_solo().impressions_total
            campaign.save()
        else:
            print("There is no that much budget to create campaign")
            return ok_status()
        response = {'id': campaign.id, 'name': campaign.name, 'budget': float(campaign.budget)}
        return data_status_creative_campaign(response)

    @staticmethod
    def check_view(request, id):
        """
        Checks the HTTP request method and calls the appropriate method.
        """
        if request.method == "GET":
            return CampaignView.get_by_id(request, id)
        if request.method == "DELETE":
            return CampaignView.delete(request, id)
        if request.method == "PATCH":
            return CampaignView.edit(request, id)

    @staticmethod
    def get_by_id(request, id):
        """
        Returns the campaign with the specified ID.
        """
        try:
            campaign = Campaign.objects.get(id=id)
        except ObjectDoesNotExist:
            return failed_status("obj_not_found")
        return data_status({'id': campaign.id, 'name': campaign.name, 'budget': float(campaign.budget),
                            'reserved_budget': float(campaign.reserved_budget), 'enabled': campaign.enabled,
                            'bid_floor': float(campaign.bid_floor)})

    @staticmethod
    def delete(request, id):
        """
        Delete a campaign by its ID and add its budget to the campaign with the highest budget.

        Args:
            request (HttpRequest): The HTTP request object.
            id (int): The ID of the Campaign object to delete.

        Returns:
            HttpResponse: A JSON response indicating whether the operation was successful.
        """
        try:
            campaign = Campaign.objects.get(id=id)
        except ObjectDoesNotExist:
            return failed_status("obj_not_found")
        other_campaigns = Campaign.objects.exclude(id=id)
        print(other_campaigns)
        max_budget = 0
        campaign_with_max_budget = None
        for c in other_campaigns:
            if c.budget > max_budget:
                max_budget = c.budget
                campaign_with_max_budget = c
        if campaign_with_max_budget:
            campaign_with_max_budget.budget += campaign.budget
            campaign_with_max_budget.reserved_budget += campaign.reserved_budget
            campaign_with_max_budget.save()
            campaign.delete()
        else:
            print("CAMPAIGN: Cannot delete single campaign")
            return failed_status("camt delete single campaign")
        return success_status_delete()

    @staticmethod
    def edit(request, id):
        """
        Edit a campaign by its ID.

        Args:
            request (HttpRequest): The HTTP request object.
            id (int): The ID of the Campaign object to edit.

        Returns:
            HttpResponse: A JSON response indicating whether the operation was successful.
        """
        data = json.loads(request.body)
        try:
            campaign = Campaign.objects.get(id=id)
        except ObjectDoesNotExist:
            return failed_status("obj_not_found")
        if 'name' in data:
            campaign.name = data['name']
        if 'enabled' in data:
            campaign.enabled = data['enabled']
        if 'bid_floor' in data:
            campaign.bid_floor = data['bid_floor']
        campaign.save()
        return ok_status()
