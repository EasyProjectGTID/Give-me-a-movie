from django.shortcuts import render


def uploadTemplate(request):
        return render(request, 'upload.html')
