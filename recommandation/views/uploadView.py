from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def uploadTemplate(request):
        return render(request, 'upload.html')

@csrf_exempt
def upload_api(request):
        file_obj = request.FILES['file']
        print(file_obj)
        return HttpResponse(status=204)
