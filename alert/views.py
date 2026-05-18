from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Profile, Contact, Alert, News


# ---------------- HOME ----------------
def home(request):
    news = News.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'news': news})


# ---------------- POLICY PAGE ----------------
def policy(request):
    return render(request, 'policy.html')


# ---------------- REGISTER ----------------
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        terms = request.POST.get('terms')   # ✅ NEW

        # validation
        if not username or not password or not role:
            messages.error(request, "All fields required ❌")
            return redirect('register')

        if not terms:
            messages.error(request, "Please accept Terms & Conditions ❌")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists ❌")
            return redirect('register')

        # create user
        user = User.objects.create_user(username=username, password=password)

        # update profile
        try:
            profile = user.profile
            profile.role = role
            profile.save()
        except:
            messages.error(request, "Profile creation failed ❌")
            return redirect('register')

        messages.success(request, "Registration successful ✅")
        return redirect('login')

    return render(request, 'register.html')


# ---------------- LOGIN ----------------
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Login successful ✅")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password ❌")

    return render(request, 'login.html')


# ---------------- LOGOUT ----------------
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')


# ---------------- DASHBOARD ----------------
@login_required
def dashboard(request):
    try:
        role = request.user.profile.role
    except Profile.DoesNotExist:
        messages.error(request, "Profile not found ❌")
        return redirect('login')

    # 🔔 Notification count (pending alerts)
    notification_count = Alert.objects.filter(status='pending').count()

    # USER
    if role == 'user':
        return render(request, 'user_dashboard.html', {
            'contacts': Contact.objects.filter(user=request.user),
            'alerts': Alert.objects.filter(user=request.user).order_by('-created_at'),
            'notification_count': notification_count
        })

    # POLICE
    elif role == 'police':
        return render(request, 'police_dashboard.html', {
            'alerts': Alert.objects.all().order_by('-created_at'),
            'notification_count': notification_count
        })

    # ADMIN
    else:
        return render(request, 'admin_dashboard.html', {
            'alerts': Alert.objects.all().order_by('-created_at'),
            'notification_count': notification_count
        })


# ---------------- SOS ----------------
@login_required
def send_sos(request):
    if request.method == 'POST':
        lat = request.POST.get('latitude')
        lon = request.POST.get('longitude')

        if not lat or not lon:
            messages.error(request, "Location not found ❌")
            return redirect('dashboard')

        location = f"{lat}, {lon}"

        Alert.objects.create(
            user=request.user,
            location=location,
            status='pending'   # ✅ important for notification
        )

        messages.success(request, "SOS sent successfully 🚨")

    return redirect('dashboard')


# ---------------- ADD CONTACT ----------------
@login_required
def add_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        if not name or not phone:
            messages.error(request, "Name & Phone required ❌")
            return redirect('add_contact')

        Contact.objects.create(
            user=request.user,
            name=name,
            phone=phone,
            email=email
        )

        messages.success(request, "Contact added successfully ✅")
        return redirect('dashboard')

    return render(request, 'add_contact.html')


# ---------------- UPDATE ALERT ----------------
@login_required
def update_alert_status(request, alert_id, action):
    alert = get_object_or_404(Alert, id=alert_id)

    if action == 'accept':
        alert.status = 'accepted'
        messages.success(request, "Alert Accepted ✅")

    elif action == 'reject':
        alert.status = 'rejected'
        messages.error(request, "Alert Rejected ❌")

    alert.save()
    return redirect('dashboard')