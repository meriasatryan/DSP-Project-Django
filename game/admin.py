from django.contrib import admin
from game.models import *


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('id', 'impressions_total', 'auction_type', 'mode', 'budget', 'impression_revenue', 'click_revenue',
                    'conversion_revenue', 'frequency_capping', 'current_total_budget')


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('id', 'name', 'budget')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('id', 'code', 'name')


@admin.register(Creative)
class CreativeAdmin(admin.ModelAdmin):
    ordering = ['id']
    # 'categories'
    list_display = ('id', 'external_id', 'name', 'file', 'campaign', 'url', 'width', 'height')


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = (
        'id', 'click_prob', 'conv_prob', 'site_domain', 'user_id', 'price', 'creative', 'win', 'revenue',
        'current_round')

