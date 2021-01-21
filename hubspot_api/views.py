from django.shortcuts import render
from django.conf import settings

from hubspot3 import Hubspot3
from hubspot3.deals import DealsClient

def hubspot_api(request):
    context = {}

    API_KEY = settings.HUBSPOT_API

    client = Hubspot3(api_key=API_KEY)

    # all of the clients are accessible as attributes of the main Hubspot3 Client
    contact = client.contacts.get_contact_by_email('stamg21@yopmail.com')
    contact_id = contact['vid']

    all_companies = client.companies.get_all()

    # new usage limit functionality - keep track of your API calls
    try:
        usage_limits = client.usage_limits
        # <Hubspot3UsageLimits: 28937/1000000 (0.028937%) [reset in 22157s, cached for 299s]>
    except Exception as e:
        print(f"No usage limits. ERROR: {e}")
        usage_limits = None

    try:
        calls_remaining = client.usage_limits.calls_remaining
        # 971063
    except Exception as e:
        print(f"No calls remaining result. ERROR: {e}")
        calls_remaining = None

    print(f'HUBS: all_companies={all_companies}, usage_limits={usage_limits}, calls_remaining={calls_remaining}')
    print(f'HUBS: contact={contact}, contact_id={contact_id}')

    return render(request, 'hubspot_api/hubspot-api.html', context)