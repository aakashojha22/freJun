from datetime import datetime, timedelta

from django.http import HttpResponse
from django.shortcuts import render
import json
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from django.core.cache import cache

from api.models import PhoneNumber


@csrf_exempt
def inbound_sms(request):
    content = {'message': '', 'error': ''}
    if request.method == "POST":
        if request.POST.get('from'):
            from_ = request.POST.get('from')
            if len(from_) > 17 or len(from_) < 6 or from_.isnumeric() == False:
                content['error'] = 'from is invalid '
        else:
            content['error'] = 'from is missing'

        if request.POST.get('to'):
            to = request.POST.get('to')
            if len(to) > 17 or len(to) < 6 or to.isnumeric() == False:
                content['error'] = 'to is invalid'
        else:
            content['error'] = 'to is missing'

        if request.POST.get('text'):
            text = request.POST.get('text')
            if len(text) > 120 or len(text) < 1:
                content['error'] = 'text is invalid'
        else:
            content['error'] = 'text is missing'
        try:
            if from_ and to and text:
                if text[:4] == 'STOP':
                    if to != cache.get(from_):
                        cache.set(from_ + 'stop', to, timeout=14400)
                        content['message'] = 'inbound_sms'
                    else:
                        content['message'] = 'inbound_sms already exist. '
                else:
                    content['message'] = 'Invalid Request Raised'
        except:
            content['error'] = 'unknown failure'
    return HttpResponse(json.dumps(content), content_type="application/json")


@csrf_exempt
def outbound_sms(request):
    content = {'message': '', 'error': ''}
    if request.method == "POST":
        if request.POST.get('from'):
            from_ = request.POST.get('from')
            if len(from_) > 17 or len(from_) < 6 or from_.isnumeric() == False:
                content['error'] = 'from is invalid '
        else:
            content['error'] = 'from is missing'

        if request.POST.get('to'):
            to = request.POST.get('to')
            if len(to) > 17 or len(to) < 6 or to.isnumeric() == False:
                content['error'] = 'to is invalid'
        else:
            content['error'] = 'to is missing'

        if request.POST.get('text'):
            text = request.POST.get('text')
            if len(text) > 120 or len(text) < 1:
                content['error'] = 'text is  invalid'
        else:
            content['error'] = 'text is missing'
        try:
            if from_ and to and text:
                if PhoneNumber.objects.filter(number=from_):
                    if to == cache.get(from_ + 'stop'):
                        content['error'] = 'sms from {from_} to {to} blocked by STOP request'.format(from_=from_, to=to)
                    else:
                        if cache.get(from_):
                            data = cache.get(from_)

                            if data['count'] < 50:
                                count = data['count'] + 1
                                cache.set(from_, {'count': count, 'time': datetime.now()}, timeout=86400)

                                content['message'] = 'outbound sms ok'
                            else:
                                content['error'] = 'requested more than 50 times.'

                        else:
                            cache.set(from_, {'count': 1, 'time': datetime.now()}, timeout=86400)
                            print(cache.get(from_))
                            content['message'] = 'outbound sms ok'


                else:
                    content['error'] = 'from parameter not found'
        except:
            content['error'] = 'unknown failure'

    return HttpResponse(json.dumps(content), content_type="application/json")


@csrf_exempt
def get_cache(request):
    if request.method == "POST":
        from_ = request.POST.get('from')
        try:
            qs = PhoneNumber.objects.get(number=from_)
            print(qs)
        except:
            print('None')

        user_data = cache.get(from_)
        return HttpResponse(json.dumps(user_data), content_type="application/json")
    else:
        return HttpResponse("None/json")
