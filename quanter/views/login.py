from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
import json

def index(request):
    return render_to_response("index.html")

def logininfo(request):
    try:
        email = request.user.email
    except:
        return HttpResponse(json.dumps("unexist"),content_type="application/json")
    jsonResult = json.dumps(email)
    return HttpResponse(jsonResult,content_type="application/json")
