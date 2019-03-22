import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
# from django.contrib.auth.models import User
from accounts_app.models import CustomUser
from fundraiser_app.models import Fundraiser, FundraiserCategory, FundraiserMsgUpdate
from fundraiser_app.utilities import add_90_days, minus_10_second_buffer


class MyTests(TestCase):
    @classmethod
    def setUpTestData(self):
        # Set up data for the whole TestCase
        print("**********************setUpTestData: Run once to set up non-modified data for all class methods.**********************")
        self.user_1 = CustomUser.objects.create(username="aaa", email='aaa@aaa.com', password='django1234')
        self.user_2 = CustomUser.objects.create(username="bbb", email='bbb@bbb.com', password='django5678')
        self.category = FundraiserCategory.objects.create(category_name='Technology', slug='technology')
        self.fundraiser = Fundraiser.objects.create(
                                                user=self.user_1,
                                                category=self.category,
                                                title='Tesla Wardenclyffe Tower',
                                                slug='tesla-wardenclyffe-tower',
                                                body='Help us raise money to create a Tesla Wardenclyffe Tower for free energy, wireless energy transmission, etc.\
                                                        With this devlopment, we can be energy independent and flying in cars in no time.',
                                                created=timezone.now(),
                                                ends_on=add_90_days(),
                                                amount_needed=1000
                                                )
        self.old_fundraiser = Fundraiser.objects.create(
                                                user=self.user_1,
                                                category=self.category,
                                                title='Ye Olde Fart',
                                                slug='ye-olde-fart',
                                                body='Silent But Deadly Certification Approved (SBDCA) for 10 years from created date. Open can on people unaware. Hold your breath.',
                                                created=timezone.now(),
                                                ends_on=datetime.datetime(2017, 1, 12, 16, 29, 0),
                                                amount_needed=50000
                                                )
        self.msg_update = FundraiserMsgUpdate.objects.create(
                                                fundraiser=self.fundraiser,
                                                user=self.user_1,
                                                title='1st update for user_1',
                                                body='This is the body attribute for the first update on a Fundraiser object',
                                                created=timezone.now(),
                                                updated=minus_10_second_buffer()
                                                )

    def test_non_authorized_users_redirected_away_from_edit_fundraiser(self):
        response = self.client.get(reverse('fundraiser_app:edit_fundraiser_detail', args=[self.fundraiser.category.slug, self.fundraiser.id, self.fundraiser.created.year, self.fundraiser.created.month, self.fundraiser.created.day, self.fundraiser.slug]))
        self.assertRedirects(response, reverse('fundraiser_app:detail', args=[self.fundraiser.category.slug, self.fundraiser.id, self.fundraiser.created.year, self.fundraiser.created.month, self.fundraiser.created.day, self.fundraiser.slug]))

    def test_non_authorized_users_redirected_away_from_edit_fundraiser_msg_updates(self):
        response = self.client.get(reverse('fundraiser_app:edit_msg_update', args=[self.fundraiser.category.slug, self.msg_update.id, self.fundraiser.slug]))
        self.assertRedirects(response, reverse('fundraiser_app:detail', args=[self.fundraiser.category.slug, self.fundraiser.id, self.fundraiser.created.year, self.fundraiser.created.month, self.fundraiser.created.day, self.fundraiser.slug]))

    def test_non_authorized_users_redirected_away_from_delete_fundraiser_msg_updates(self):
        response = self.client.get(reverse('fundraiser_app:delete_msg_update', args=[self.fundraiser.category.slug, self.msg_update.id, self.fundraiser.slug]))
        self.assertRedirects(response, reverse('fundraiser_app:detail', args=[self.fundraiser.category.slug, self.fundraiser.id, self.fundraiser.created.year, self.fundraiser.created.month, self.fundraiser.created.day, self.fundraiser.slug]))

    def test_non_authorized_user_gets_donation_form_instead_of_edit_form(self):
        response = self.client.get(reverse('fundraiser_app:detail', args=[self.fundraiser.category.slug, self.fundraiser.id, self.fundraiser.created.year, self.fundraiser.created.month, self.fundraiser.created.day, self.fundraiser.slug]))
        # check donation form is rendered, NOT the form to change
        self.assertTrue(str(response.context['donation']))
        # Check for 200 "success"
        self.assertEqual(response.status_code, 200)
        # Check for  correct template
        self.assertTemplateUsed(response, 'fundraiser_app/fundraiser_detail.html')

    def test_fundraiser_list_gets_objects_less_than_90_days_old_from_create_date(self):
        fundraisers = Fundraiser.objects.filter(ends_on__gt=timezone.now())
        self.assertEqual(len(fundraisers), 1)

    def test_old_fundraiser_is_ended(self):
        fundraiser = Fundraiser.objects.get(id=self.old_fundraiser.id)
        self.assertTrue(fundraiser, True)

    def test_msg_update_returns_false_for__is_updated__within_first_10_seconds(self):
        msg_update = FundraiserMsgUpdate.objects.get(id=self.msg_update.id)
        self.assertIs(msg_update.is_updated(), False)
