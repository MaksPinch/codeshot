from django.shortcuts import render
def home_view(request):
    context = {
        "title": "CodeShot",
        "subtitle": "Create syntax-highlighted code previews.",
    }
    return render(request, 'codeshot/home.html', context)

