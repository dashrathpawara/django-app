from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    
    peoples = [
        {'name' : 'Ram Padvi' , 'age' : 28},
        {'name' : 'Rohan Valvi' , 'age' : 27},
        {'name' : 'Himmat Pawara' , 'age' : 25},
        {'name' : 'Digesh Pawara' , 'age' : 1},
        {'name' : 'Lovely Pawara' , 'age' : 17},
    ]

    return render(request , "home/index.html" , context= {'peoples' : peoples})

def contact(request):
    return render(request , "home/contact.html") 

def about(request):
    return render(request , "home/about.html") 

def success_page(request):
    print("*" * 10)
    return HttpResponse(""" <h1> This is my KhapakhapDB </h1>
    <p> must say that this is my second link to god
    """)