from django.shortcuts import render

def ad_generator_frame(request):
    return render(request, 'ad_generator_frame.html')

def ad_generator_payment_frame(request):
    return render(request, 'ad_generator_payment_frame.html')