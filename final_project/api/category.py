import json

from django.views.generic import View
from game.models import Category
from final_project.utils.http_responses import data_status, failed_status


class CategoryView(View):
    """
    View for creating and reading Category objects.
    """

    def get(self, request):
        """
        Retrieve a list of all categories.
        """
        categories = Category.objects.all()
        data = []
        for category in categories:
            data.append(
                {"code": category.code, "name": category.name}
            )
        return data_status(data)

    def post(self, request):
        """
        Create a new Category object.
        """
        data = json.loads(request.body)
        response = []
        if "code" in data and "name" in data:
            category = Category.objects.create(
                code=data["code"],
                name=data["name"]
            )
        else:
            return failed_status("invalid_post_data")
        category.save()
        response.append({"code": category.code, "name": category.name})
        return data_status(response)
