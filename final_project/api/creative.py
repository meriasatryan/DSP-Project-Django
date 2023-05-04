import os
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from game.models import Creative, Campaign, Category
from final_project.utils.http_responses import *
from final_project.utils.convert_blob import convert_blob


class CreativeView(View):
    """
    View for creating, reading, updating and deleting creative objects.
    """

    def get(self, request):
        """
        Returns a list of all creatives.
        """
        creatives = Creative.objects.all()
        data = []
        for creative in creatives:
            data.append({
                'id': creative.id,
                'url': creative.url,
                'external_id': creative.external_id,
                'name': creative.name,
                'campaign': {
                    'name': creative.campaign.name,
                    'budget': str(creative.campaign.budget),

                },
                'categories': [cat.code for cat in creative.categories.all()]
            })
        return data_status(data)

    def post(self, request):
        """
        API endpoint that creates a new creative object.

        Args:
            request: HTTP request object containing data for the new creative object.

        Returns:
            A JSON response indicating the status of the request and the created creative object if successful.
        """
        data = json.loads(request.body)
        creative = None
        try:
            creative = Creative.objects.create(
                external_id=data['external_id'],
                name=data['name'],
                campaign=Campaign.objects.get(id=data['campaign']['id']),
            )
            for cat in data['categories']:
                try:
                    creative.categories.add(Category.objects.get(code=cat['code']))
                except ObjectDoesNotExist:
                    creative.delete()
                    print("CREATIVE: no category with such id")
                    return ok_status()

            converted_blob = convert_blob(data['file'])
            creative.file = converted_blob['file']
            creative.url = converted_blob['url']
            creative.width = converted_blob['width']
            creative.height = converted_blob['height']

            ip_address = os.environ.get("DSP_IP")
            print(ip_address, "CREATIVE")
            response = {
                'id': creative.id,
                'external_id': creative.external_id,
                'name': creative.name,
                'categories': [{"id": c.id, "code": c.code} for c in creative.categories.all()],
                'campaign': {
                    'id': creative.campaign.id,
                    'name': creative.campaign.name
                },
                'url': f"http://{ip_address}{creative.url}"
            }
        except KeyError as k:
            if creative:
                creative.delete()
            print("key error", k)
            return ok_status()
        except TypeError as t:
            if creative:
                creative.delete()
            print("wrong type", t)
            return ok_status()
        except ObjectDoesNotExist:
            if creative:
                creative.delete()
            print("object doesnt exist")
            return ok_status()
        creative.save()
        return data_status_creative_campaign(response)

    @staticmethod
    def check_view(request, id):
        """
        Checks the HTTP request method and calls the appropriate method.
        """
        if request.method == "GET":
            return CreativeView.get_by_id(request, id)
        if request.method == "DELETE":
            return CreativeView.delete(request, id)
        if request.method == "PATCH":
            return CreativeView.edit(request, id)

    @staticmethod
    def get_by_id(request, id):
        """
        Returns the creative with the specified ID.
        """
        try:
            creative = Creative.objects.get(id=id)
        except ObjectDoesNotExist:
            return failed_status("obj_not_found")
        ip_address = os.environ.get("DSP_IP")
        return data_status({
            'url': f"https://{ip_address}{creative.url}",
            'external_id': creative.external_id,
            'name': creative.name,
            'campaign': {
                'id': creative.campaign.id,
                'name': creative.campaign.name,
                'budget': float(creative.campaign.budget),
            },
            'categories': [cat.code for cat in creative.categories.all()]
        })

    @staticmethod
    def delete(request, id):
        """
        Deletes a Creative object with the given ID.

        Args:
            request (HttpRequest): The HTTP request object.
            id (int): The ID of the Creative object to delete.

        Returns:
            HttpResponse: A JSON response indicating whether the operation was successful.
        """
        try:
            creative = Creative.objects.get(id=id)
        except ObjectDoesNotExist:
            return failed_status("obj_not_found")
        creative.delete()
        return success_status_delete()

    @staticmethod
    def edit(request, id):
        """
        Edits a Creative object with the given ID.

        Args:
            request (HttpRequest): The HTTP request object.
            id (int): The ID of the Creative object to edit.

        Returns:
            HttpResponse: A JSON response indicating whether the operation was successful.
        """
        data = json.loads(request.body)
        try:
            creative = Creative.objects.get(id=id)
        except ObjectDoesNotExist:
            return failed_status("obj_not_found")
        if 'name' in data:
            creative.name = data['name']
        if 'campaign_id' in data:
            creative.campaign = Campaign.objects.get(id=data['campaign_id'])
        if 'categories' in data:
            for cat in data['categories']:
                try:
                    creative.categories.add(Category.objects.get(code=cat['code']))
                except ObjectDoesNotExist:
                    print("CREATIVE: no category with such id")
                    return ok_status()
        if 'file' in data:
            converted_blob = convert_blob(data['file'])
            creative.file = converted_blob['file']
            creative.url = converted_blob['url']
            creative.width = converted_blob['width']
            creative.height = converted_blob['height']
        creative.save()
        return ok_status()
