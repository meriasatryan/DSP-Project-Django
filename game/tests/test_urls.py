# from django.test import SimpleTestCase, TestCase
# from django.urls import reverse, resolve
# from final_project.api.campaign import CampaignView
#
#
# class TestUrls(TestCase):
#
#     # def test_campaign_url(self):
#     #     url = reverse('campaign')
#     #     self.assertEquals(resolve(url).func.view_class, CampaignView)
#
#     # def test_campaign_id_url(self):
#     #     url = reverse('campaign_id', args=[2])
#     #     self.assertEquals(resolve(url).func.view_class, CampaignView)
#     #     # response = self.client.get(url)
#     #     # self.assertEqual(response.status_code, 200)
#     #     # self.assertContains(response, "Campaign details for ID 42")
#
#     def test_my_view(self):
#         url = reverse('campaign_id', args=[1])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
