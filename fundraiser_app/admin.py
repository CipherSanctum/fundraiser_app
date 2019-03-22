from django.contrib import admin
from .models import Fundraiser, FundraiserCategory, FundraiserDonation, FundraiserMsgUpdate


@admin.register(FundraiserCategory)
class FundraiserCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    prepopulated_fields = {'slug': ('category_name',)}


class FundraiserMsgUpdateInline(admin.TabularInline):
    model = FundraiserMsgUpdate


@admin.register(Fundraiser)
class FundraiserAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'user', 'created', 'ends_on', 'amount_raised', 'amount_needed', 'my_est_cut')
    list_editable = ('ends_on',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'body', 'slug', 'user__username')
    list_filter = ('created', 'ends_on')
    inlines = [FundraiserMsgUpdateInline]


@admin.register(FundraiserDonation)
class FundraiserDonationAdmin(admin.ModelAdmin):
    list_display = ('fundraiser', 'amount', 'trans_id', 'paid')
    search_fields = ('first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'trans_id')
    list_filter = ('paid',)
