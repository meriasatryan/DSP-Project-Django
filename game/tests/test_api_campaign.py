# import json

# from django.test import TestCase
# from rest_framework.test import APIClient
# from ..models import Campaign
# from django.urls import reverse


# class CampaignTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.url = reverse('campaign')
#         self.url_detailed = reverse('campaign_id', args=[0])
#         self.objects = [
#             {'name': 'campaign1', 'budget': 10},
#             {'name': 'campaign2', 'budget': 20},
#         ]
#         for obj in self.objects:
#             Campaign.objects.create(**obj)

    # def test_create_object(self):
    #     data = {'name': 'campaign3', 'budget': 30}
    #     response = self.client.post(self.url, data, format='json')
    #     self.assertEqual(response.status_code, 201)
    #     obj = Campaign.objects.filter(name=data['name']).first()
    #     self.assertIsNotNone(obj)
    #     self.assertEqual(obj.budget, data['budget'])

#     def test_list_objects(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 200)
#         response_json = response.json()
#         response_json = json.dumps(response_json)
#         response_json = json.loads(response_json)
#         self.assertEqual(len(response_json), len(self.objects))
#         for i, obj in enumerate(self.objects):
#             self.assertEqual(response_json[i]['name'], obj['name'])
#             self.assertEqual(response_json[i]['budget'], obj['budget'])

#     def test_get_object_by_id(self):
#         obj = Campaign.objects.first()
#         response = self.client.get(f'{self.url}{obj.id}/')
#         response_json = response.json()
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response_json['name'], obj.name)
#         self.assertEqual(response_json['budget'], obj.budget)

#     def test_update_object(self):
#         obj = Campaign.objects.first()
#         data = {'name': 'new name', 'budget': 5}
#         response = self.client.patch(f'{self.url}{obj.id}/', data, format='json')
#         self.assertEqual(response.status_code, 200)
#         obj.refresh_from_db()
#         print(obj.name)
#         self.assertEqual(obj.name, data['name'])
#         self.assertEqual(obj.budget, data['budget'])

#     def test_delete_object(self):
#         obj = Campaign.objects.first()
#         response = self.client.delete(f'{self.url}{obj.id}/')
#         self.assertEqual(response.status_code, 204)
#         self.assertIsNone(Campaign.objects.filter(id=obj.id).first())