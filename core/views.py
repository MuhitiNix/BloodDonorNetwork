from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from .models import DonorProfile
from django.contrib.gis.measure import D

def register_page(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone_number')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        blood_group = request.POST.get('blood_group')
        occupation = request.POST.get('occupation')
        last_donation = request.POST.get('last_donation_date')
        
        lat = request.POST.get('latitude')
        lng = request.POST.get('longitude')

       
        if not User.objects.filter(username=phone).exists():
            user = User.objects.create_user(username=phone, first_name=full_name)
        else:
            user = User.objects.get(username=phone)

        donor_location = Point(float(lng), float(lat), srid=4326)

        if last_donation == "":
            last_donation = None

      
        DonorProfile.objects.update_or_create(
            user=user,
            defaults={
                'phone_number': phone,
                'date_of_birth': dob,
                'gender': gender,
                'blood_group': blood_group,
                'occupation': occupation,
                'last_donation_date': last_donation,
                'location': donor_location
            }
        )
        return redirect('register')

    return render(request, 'core/register.html')


def search_donors(request):
    donors = DonorProfile.objects.filter(is_available=True)

    blood_group = request.GET.get('blood_group')
    if blood_group:
        donors = donors.filter(blood_group=blood_group)

    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    radius = request.GET.get('radius', 5)

    if lat and lng:
        searcher_location = Point(float(lng), float(lat), srid=4326)
        donors = donors.filter(location__distance_lte=(searcher_location, D(km=float(radius))))

    return render(request, 'core/search.html', {'donors': donors})