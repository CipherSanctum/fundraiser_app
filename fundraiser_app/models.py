from django.db import models
from accounts_app.models import CustomUser
from django.urls import reverse
from django.utils import timezone
from .utilities import add_90_days


class FundraiserCategory(models.Model):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150)

    class Meta:
        ordering = ('category_name',)
        verbose_name = 'Fundraiser Category'
        verbose_name_plural = 'Fundraiser Categories'

    def __str__(self):
        return self.category_name


class Fundraiser(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(FundraiserCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    body = models.TextField()  # markdown support
    created = models.DateTimeField(auto_now_add=True)
    ends_on = models.DateTimeField(default=add_90_days)
    amount_needed = models.DecimalField(max_digits=12, decimal_places=2, default=1)
    amount_raised = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    my_est_cut = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Fundraiser'
        verbose_name_plural = 'Fundraisers'

    def get_absolute_url(self):
        return reverse('fundraiser_app:detail', args=[self.category.slug, self.id, self.created.year, self.created.month, self.created.day, self.slug])

    def get_percentage_raised(self):
        if self.amount_raised == 0:
            return 0
        return round((self.amount_raised / self.amount_needed) * 100, 4)

    def is_ended(self):
        if self.ends_on < timezone.now():
            return True
        return False

    def __str__(self):
        return self.title


class FundraiserMsgUpdate(models.Model):
    fundraiser = models.ForeignKey(Fundraiser, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField()

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Fundraiser Update'
        verbose_name_plural = 'Fundraiser Updates'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('fundraiser_app:msg_update', args=[self.fundraiser.category.slug, self.id, self.fundraiser.slug])

    def is_updated(self):
        if self.updated > self.created:
            return True
        return False


class FundraiserDonation(models.Model):
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default='Anonymous')  # able to be anonymous??
    fundraiser = models.ForeignKey(Fundraiser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=False)
    paid = models.BooleanField(default=False)
    trans_id = models.CharField(max_length=150, blank=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Fundraiser Donation'
        verbose_name_plural = 'Fundraiser Donations'

    def __str__(self):
        return 'Payment {}'.format(self.id)


# class FundraiserImage(models.Model):    # add multiple images to own DB, to be displayed at top of fundraiser.
#     # image = models.URLField(max_length=200, blank=True)
#     image = models.ImageField(upload_to='fundraiser_images/%Y/%m/%d', blank=True)
#     fundraiser = models.ForeignKey(Fundraiser, on_delete=models.CASCADE)
