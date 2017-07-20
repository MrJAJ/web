from django.shortcuts import render

# Create your views here.
def temp(request):
    return render(request, 'website/temp.html')
def tips(request):
    return render(request, 'website/tips.html')
def h404(request):
    return render(request, 'website/404.html')

def index(request):
    return render(request, 'website/index.html')
def full(request):
    return render(request, 'website/full.html')
def jieindex(request):
    return render(request, 'website/jie/index.html')
def jiedetail(request):
    return render(request, 'website/jie/detail.html')
def jieadd(request):
    return render(request, 'website/jie/add.html')
def userindex(request):
    return render(request, 'website/user/index.html')
def userhome(request):
    return render(request, 'website/user/home.html')
def userset(request):
    return render(request, 'website/user/set.html')
def usermessage(request):
    return render(request, 'website/user/message.html')
def useractivate(request):
    return render(request, 'website/user/activate.html')
def userforget(request):
    return render(request, 'website/user/forget.html')
def userlogin(request):
    return render(request, 'website/user/login.html')
def userreg(request):
    return render(request, 'website/user/reg.html')
