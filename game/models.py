"""
Module containing Django models for a programmatic advertising platform (DSP).

This module defines the following models:
- Config: Stores the configuration settings for the advertising platform.
- Campaign: Represents a campaign for a specific advertising effort.
- Category: Stores information about the categories of ads that can be displayed.
- Creative: Represents the creatives that can be used in ads for a campaign.
- Bid: Stores information about a bid for an ad.
- ViewFrequency: Tracks the number of times an ad has been viewed by a user.

Each model is defined as a subclass of Django's `models.Model` class.

"""

from django.core.validators import MinValueValidator
from django.db import models
from solo.models import SingletonModel


class Config(SingletonModel):
    """
    Model representing the configuration settings for the advertising platform.

    Attributes:
    - impressions_total: The total number of impressions for the platform.
    - auction_type: The type of auction to use for bidding.
    - mode: The mode of the platform.
    - budget: The total budget for the platform.
    - impression_revenue: The revenue generated from impressions.
    - click_revenue: The revenue generated from clicks.
    - conversion_revenue: The revenue generated from conversions.
    - frequency_capping: The frequency cap for ads.
    - current_total_budget: The current total budget for the platform.
    - game_goal: The goal of the game.
    """

    impressions_total = models.PositiveIntegerField(null=True)
    auction_type = models.PositiveIntegerField(null=True)
    mode = models.CharField(max_length=10, null=True)
    budget = models.DecimalField(validators=[MinValueValidator(0)], null=True, max_digits=6, decimal_places=2)
    impression_revenue = models.PositiveIntegerField(null=True)
    click_revenue = models.PositiveIntegerField(null=True)
    conversion_revenue = models.PositiveIntegerField(null=True)
    frequency_capping = models.IntegerField(validators=[MinValueValidator(1)], null=True)
    current_total_budget = models.DecimalField(validators=[MinValueValidator(0)], null=True, max_digits=6,
                                               decimal_places=2)
    game_goal = models.CharField(max_length=20, null=True)
    coefficient = models.PositiveIntegerField(null=True, default=3)


class Campaign(models.Model):
    """
    Model representing a campaign for a specific advertising effort.

    Attributes:
    - name: The name of the campaign.
    - budget: The total budget for the campaign.
    - reserved_budget: The reserved budget for the campaign.
    - enabled: Whether the campaign is enabled or not.
    - bid_floor: The minimum bid for the campaign.
    """

    name = models.CharField(max_length=100)
    budget = models.DecimalField(validators=[MinValueValidator(0)], null=True, max_digits=6, decimal_places=2)
    reserved_budget = models.DecimalField(validators=[MinValueValidator(0)], null=True, max_digits=6, decimal_places=2)
    enabled = models.BooleanField(default=True)
    bid_floor = models.DecimalField(validators=[MinValueValidator(0)], null=True, max_digits=6, decimal_places=2)


class Category(models.Model):
    """
    Model representing the categories of ads that can be displayed.

    Attributes:
    - code: The code for the category.
    - name: The name of the category.
    """

    code = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=100)


class Creative(models.Model):
    """
    Represents a creative object, which is an ad that can be displayed to users.

    Attributes:
        id (int): The ID of the creative.
        external_id (str): The external ID of the creative.
        name (str): The name of the creative.
        file (ImageField): The file of the creative.
        campaign (ForeignKey): The campaign that the creative belongs to.
        categories (ManyToManyField): The categories that the creative belongs to.
        url (URLField): The URL associated with the creative.
        width (int): The width of the creative.
        height (int): The height of the creative.
    """

    id = models.AutoField(primary_key=True)
    external_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    file = models.ImageField()
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    url = models.URLField()
    width = models.PositiveIntegerField(default=0)
    height = models.PositiveIntegerField(default=0)


class Bid(models.Model):
    """
    Represents a bid object, which is an offer to pay for an ad impression.

    Attributes:
        external_id (str): The external ID of the bid.
        click_prob (float): The probability that the bid will result in a click.
        conv_prob (float): The probability that the bid will result in a conversion.
        site_domain (str): The domain of the site that the bid is for.
        user_id (str): The ID of the user that the bid is for.
        price (DecimalField): The price of the bid.
        creative (ForeignKey): The creative of the bid response.
        win (bool): Whether or not the bid won the auction.
        revenue (int): The revenue generated by the bid.
        current_round (int): The current round of bidding.
    """

    external_id = models.CharField(max_length=30, unique=True)
    click_prob = models.FloatField(null=True)
    conv_prob = models.FloatField(null=True)
    site_domain = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    price = models.DecimalField(validators=[MinValueValidator(0)], max_digits=6, decimal_places=2, null=True)
    creative = models.ForeignKey(Creative, on_delete=models.CASCADE, null=True)
    win = models.BooleanField(default=False)
    revenue = models.PositiveIntegerField(default=0)
    current_round = models.PositiveIntegerField(default=0)
    click_happened = models.BooleanField(default=False)
    conversion_happened = models.BooleanField(default=False)


class ViewFrequency(models.Model):
    """
    Represents the number of times a user has viewed a campaign.

    Attributes:
        user_id (str): The ID of the user.
        campaign (ForeignKey): The campaign that the view frequency is associated with.
        times_viewed (int): The number of times the user has viewed the campaign.
    """

    user_id = models.CharField(max_length=100)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    times_viewed = models.PositiveIntegerField(default=0)
