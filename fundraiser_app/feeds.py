from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from .models import Fundraiser, FundraiserMsgUpdate


class RSSFundraiserMsgUpdateFeed(Feed):
    description_template = 'fundraiser_app/feed_description.xml'       #  Gets items(), and gives <description> for each <item>... See files for details
    # title_template = 'fundraiser_app/feed_title.xml'                 #  Gets items(), and gives <title> for each <item>

    # METHODS FOR Fundraiser
    def get_object(self, request, category_slug, fundr_id, slug):       # general/5/well-x-area/rss2/
        return Fundraiser.objects.get(pk=fundr_id)                      # http://127.0.0.1:8000/fundraiser_app/general/5/well-x-area/rss2/

    def title(self, obj):
        return 'Fundraiser message updates for: "{}"'.format(obj.title) # Fundraiser.title

    def link(self, obj):
        return obj.get_absolute_url()   # linked Fundraiser.title

    def description(self, obj):
        return '{}'.format(obj.body)    # Fundraiser.body


    # METHODS FOR FundraiserMsgUpdate
    def items(self, obj):
        return FundraiserMsgUpdate.objects.filter(fundraiser=obj)   # obj=FundraiserMsgUpdate

    def item_title(self, item):     # for each item returned by items(), return its title as a string
        return item.title

    def item_description(self, item):   # Takes an item returned from items(), and returns whatever attribute you want as a normal Python string.
        return '{}'.format(item.body)   # Some feed readers don't show markdown syntax properly... So it might show up as normal string.


class AtomFundraiserMsgUpdateFeed(RSSFundraiserMsgUpdateFeed):
    feed_type = Atom1Feed
    subtitle = RSSFundraiserMsgUpdateFeed.description   # RSSFundraiserMsgUpdateFeed.description(self, obj)... because it checks 2 optional methods, and attribute last
                                                        # <summary> tag comes from RSSFundraiserMsgUpdateFeed.item_description(self, item)
