# import json
# from django.test import TestCase
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient
# from ..models import Config


# class ConfigTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.url = reverse('config')
#         self.url_delete = ('config_delete')
#         self.my_object = Config.objects.create(impressions_total=5, auction_type=2, mode="free", budget=60,
#                                                impression_revenue=20,
#                                                click_revenue=25, conversion_revenue=30, frequency_capping=3)

#     def test_get_api(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         expected_content = json.loads(json.dumps(
#             '{"data": [{"id": 1, "impressions_total": 5, "auction_type": 2, '
#             '"mode": "free", "budget": 60, "impression_revenue": 20, "click_revenue": 25, '
#             '"conversion_revenue": 30, "frequency_capping": 3}], "status": "ok"}'))

#         self.assertJSONEqual(response.json(), expected_content)

#     def test_post_api(self):
#         data = {"id": 1, "impressions_total": 5, "auction_type": 2,
#                 "mode": "free", "budget": 60, "impression_revenue": 20, "click_revenue": 25,
#                 "conversion_revenue": 30, "frequency_capping": 3}

#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, 200)
