from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone
import math, io, base64, secrets, threading
from datetime import datetime, date, timedelta
from random import randint
import urllib.parse
from django.utils.timezone import localtime
import requests
from django.urls import reverse
from django.template.loader import render_to_string

try:
    import qrcode
    from PIL import Image
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False

# PDF generation imports
try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError):
    WEASYPRINT_AVAILABLE = False
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        REPORTLAB_AVAILABLE = True
    except ImportError:
        REPORTLAB_AVAILABLE = False

# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
from .models import (
    EVAdmin,
    EVRegister,
    EVStation,
    EVBooking
)



def index(request):
    stations = EVStation.objects.filter(status=1)
    messages.success(request, """<h3>Welcome to EV Charge Hub!</h3><span>&nbsp;&nbsp;&nbsp;</span>
                     Your trusted partner for EV charging solutions.""")
    return render(request, 'index.html', {'stations': stations})


# --- Admin Views --- #

def admin_login(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pwd = request.POST.get('password')
        admin = EVAdmin.objects.filter(username=uname, password=pwd).first()
        if admin:
            request.session['admin'] = uname
            messages.success(request, "Login successful!")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid admin credentials.")
    return render(request, 'login_admin.html')


def admin_dashboard(request):
    if not request.session.get('admin'):
        messages.error(request, "Invalid admin credentials. please login")
        return redirect('admin_login')

    approve_station = request.GET.get('approve')
    if approve_station:
        station = EVStation.objects.filter(uname=approve_station).first()
        if station:
            station.status = 1
            station.save()
            messages.success(request, f'Station "{approve_station}" approved successfully.')
            # Send approval email to station
            try:
                def send_approval_email(st):
                    try:
                        html = f"""<html><body style="background:#0a0e1a;font-family:Arial,sans-serif;padding:30px;">
<div style="max-width:600px;margin:auto;background:#0d1117;border-radius:16px;overflow:hidden;">
<div style="background:linear-gradient(90deg,#00c6ff,#0072ff,#7b2ff7);height:5px;"></div>
<div style="padding:30px;text-align:center;">
<h1 style="color:#00c6ff;">&#9889; EV CHARGE HUB</h1>
<h2 style="color:#34d399;">&#10003; Station Approved!</h2>
<p style="color:#8892a4;">Your station <strong style="color:#fff;">{st.name}</strong> has been approved by admin!</p>
<div style="background:#131920;border-radius:12px;padding:16px;text-align:left;margin:16px 0;">
<table style="width:100%;color:#fff;font-size:14px;">
<tr><td style="color:#8892a4;padding:5px 0;">Station</td><td>{st.name}</td></tr>
<tr><td style="color:#8892a4;padding:5px 0;">Username</td><td style="color:#00c6ff;">{st.uname}</td></tr>
<tr><td style="color:#8892a4;padding:5px 0;">Location</td><td>{st.area}, {st.city}</td></tr>
</table></div>
<p style="color:#8892a4;font-size:13px;">You can now login and start accepting bookings!</p>
</div>
<div style="background:linear-gradient(90deg,#00c6ff,#0072ff,#7b2ff7);height:4px;"></div>
</div></body></html>"""
                        mail = EmailMultiAlternatives(
                            subject='✅ Station Approved – EV Charge Hub',
                            body=f'Your station {st.name} has been approved!',
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            to=[st.email],
                        )
                        mail.attach_alternative(html, "text/html")
                        mail.send(fail_silently=True)
                    except Exception:
                        pass
                threading.Thread(target=send_approval_email, args=(station,)).start()
            except Exception:
                pass

    stations = EVStation.objects.all()
    users = EVRegister.objects.all()
    bookings = EVBooking.objects.all()

    # Stats for dashboard
    total_stations = stations.count()
    active_stations = stations.filter(is_active=True).count()
    total_users = users.count()
    total_bookings = bookings.count()
    completed_bookings = bookings.filter(chargest=3).count()
    paid_bookings = bookings.filter(payst__gt=0).count()
    total_revenue = sum(b.amount for b in bookings.filter(payst__gt=0))

    return render(request, 'admin.html', {
        'stations': stations,
        'users': users,
        'bookings': bookings,
        'total_stations': total_stations,
        'active_stations': active_stations,
        'total_users': total_users,
        'total_bookings': total_bookings,
        'completed_bookings': completed_bookings,
        'paid_bookings': paid_bookings,
        'total_revenue': total_revenue,
    })



def admin_logout(request):
    request.session.flush()
    messages.success(request, "You have been logged out.")
    return redirect('admin_login')


# --- Station Owner Views --- #

def station_login(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pwd = request.POST.get('pass')
        owner = EVStation.objects.filter(uname=uname, passw=pwd).first()
        if owner and owner.status == 1:
            request.session['station_owner'] = uname
            owner.is_active = True
            owner.last_seen = timezone.now()
            owner.save(update_fields=['is_active', 'last_seen'])
            messages.success(request, "Login successful!")
            return redirect('station_home')
        else:
            messages.error(request, "Invalid station credentials or not approved yet.")
    return render(request, 'login2.html')


import random
def station_forgot_password(request):
    if request.method == 'POST':
        step = request.POST.get('step', 'email')

        if step == 'email':
            identifier = request.POST.get('identifier')
            station = EVStation.objects.filter(uname=identifier).first() or EVStation.objects.filter(email=identifier).first()
            if station:
                otp = str(random.randint(100000, 999999))
                request.session['station_reset_otp'] = otp
                request.session['station_reset_uname'] = station.uname
                # Send OTP email
                try:
                    import threading
                    from django.core.mail import send_mail
                    def send_otp():
                        send_mail(
                            'EV Charge Hub - Password Reset OTP',
                            f'Your OTP for password reset is: {otp}\nValid for 10 minutes.',
                            settings.DEFAULT_FROM_EMAIL,
                            [station.email],
                            fail_silently=True,
                        )
                    threading.Thread(target=send_otp).start()
                except:
                    pass
                messages.success(request, f"OTP sent to your registered email!")
                return render(request, 'station_forgot_password.html', {'step': 'otp', 'identifier': station.uname})
            else:
                messages.error(request, "No station found with this username/email.")
                return render(request, 'station_forgot_password.html', {'step': 'email'})

        elif step == 'otp':
            identifier = request.POST.get('identifier')
            otp = request.POST.get('otp')
            saved_otp = request.session.get('station_reset_otp')
            if otp == saved_otp:
                messages.success(request, "OTP verified! Set your new password.")
                return render(request, 'station_forgot_password.html', {'step': 'reset', 'identifier': identifier})
            else:
                messages.error(request, "Invalid OTP. Try again.")
                return render(request, 'station_forgot_password.html', {'step': 'otp', 'identifier': identifier})

        elif step == 'reset':
            identifier = request.POST.get('identifier')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password != confirm_password:
                messages.error(request, "Passwords do not match!")
                return render(request, 'station_forgot_password.html', {'step': 'reset', 'identifier': identifier})
            station = EVStation.objects.filter(uname=identifier).first()
            if station:
                station.passw = new_password
                station.save()
                request.session.pop('station_reset_otp', None)
                request.session.pop('station_reset_uname', None)
                messages.success(request, "Password reset successful! Please login.")
                return redirect('station_login')
            else:
                messages.error(request, "Something went wrong. Try again.")

    return render(request, 'station_forgot_password.html', {'step': 'email'})


def station_register(request):
    if request.method == 'POST':
        sname = request.POST.get('sname')
        stype = request.POST.get('stype')
        numcharger = request.POST.get('num_charger')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        area = request.POST.get('area')
        city = request.POST.get('city')
        landmark = request.POST.get('landmark')
        lat = request.POST.get('lat')
        lon = request.POST.get('lon')
        uname = request.POST.get('uname')
        passw = request.POST.get('pass')
        if EVStation.objects.filter(uname=uname).exists():
            messages.error(request, "Username already exists")
            return redirect('station_register')

        station = EVStation(
            name=sname,
            stype = stype,
            numcharger=numcharger,
            mobile = mobile,
            email = email,
            area = area,
            city = city,
            landmark = landmark,
            lat = lat,
            lon = lon,
            uname=uname,
            passw=passw,
            status=0,  # Not approved yet
            # add other required fields here from request.POST
        )
        station.save()
        messages.success(request, "Station registered! Waiting for admin approval.")
        return redirect('station_login')
    return render(request, 'reg_station.html')


def station_home(request):
    if not request.session.get('station_owner'):
        messages.error(request, "Invalid station credentials. please login")
        return redirect('station_login')
    
    uname = request.session['station_owner']
    station = get_object_or_404(EVStation, uname=uname)
    station.is_active = True
    station.last_seen = timezone.now()
    station.save(update_fields=['is_active', 'last_seen'])
    bookings = EVBooking.objects.filter(station=station, status=1)
    return render(request, 'home.html', {'station': station, 'bookings': bookings})

def get_slot_data(station):
    now = localtime()
    rdate = now.strftime("%Y-%m-%d")

    sdata = []
    num = station.numcharger

    for i in range(1, num + 1):
        # NOTE: station field is FK now, so use station=station NOT station=station.name
        booking = EVBooking.objects.filter(
            slot=i,
            station=station,
            status=1,
            rdate=rdate,
        ).first()

        if booking:
            sdata.append({
                'slot_flag': 'yes',
                'slot_num': i,
                'booking': booking,
            })
        else:
            sdata.append({
                'slot_flag': 'no',
                'slot_num': i,
                'booking': None,
            })

    return sdata

def station_view_slots(request, sid):
    if not request.session.get('station_owner'):
        messages.error(request, "Invalid station credentials. please login")
        return redirect('station_login')
    
    # Handle payment action
    if request.GET.get('act') == 'pay':
        rid = request.GET.get('rid')
        if rid:
            try:
                booking = EVBooking.objects.get(id=rid)
                booking.payst = 1  # Mark as paid
                booking.status = 3   # Mark as completed/paid status
                booking.save()
                messages.success(request, f"Payment for Slot.no : {booking.slot} booking ID {rid} has been marked as received.")
            except EVBooking.DoesNotExist:
                messages.error(request, f"Booking with Slot.no : {booking.slot} booking ID {rid} not found.")
            # Redirect to the same page without query parameters to avoid re-execution
            return redirect('station_view', sid=sid)

    station = get_object_or_404(EVStation, uname=sid)

    # ADDED LOGIC: If the logged-in owner is viewing their own station, ensure it's marked active.
    if request.session.get('station_owner') == station.uname:
        if not station.is_active:
            station.is_active = True
            station.save(update_fields=['is_active'])

    slots = get_slot_data(station)

    return render(request, 'view.html', {'station': station, 'slots': slots})


def start_charge(request, rid, sid):
    if not request.session.get('station_owner'):
        messages.error(request, "Invalid station credentials. please login")
        return redirect('station_login')

    booking = get_object_or_404(EVBooking, id=rid)
    station = get_object_or_404(EVStation, uname=sid)

    if booking.station != station:
        messages.error(request, "Booking does not belong to this station.")
        return redirect('station_view', sid=sid)

    if request.method in ['GET', 'POST']:
        # Start charging state, initialise timer
        booking.chargest = 2  # charging

        # default duration if not set
        if booking.mins <= 0:
            booking.mins = 30

        # total duration in seconds for this charge
        booking.duration_seconds = booking.mins * 60

        # set a fixed end time based on server time
        booking.end_time = timezone.now() + timedelta(seconds=booking.duration_seconds)

        # # keep old fields if you still use them anywhere else (optional)
        # booking.chargemin = booking.mins
        # booking.chargesec = 0

        booking.save(update_fields=[
            'chargest',
            'mins',
            'duration_seconds',
            'end_time',
            # 'chargemin',
            # 'chargesec',
        ])

    # Redirect back to booking detail or slots
    return redirect('station_view', sid=sid)

@require_POST
def finish_charge(request, rid):
    booking = get_object_or_404(EVBooking, id=rid)
    booking.chargest = 3
    booking.save(update_fields=['chargest'])
    return HttpResponse("ok")

def station_report(request):
    if not request.session.get('station_owner'):
        messages.error(request, "Invalid station credentials. please login")
        return redirect('station_login')
    
    uname = request.session['station_owner']
    station = get_object_or_404(EVStation, uname=uname)

    # Ensure the station is marked active when the owner views the report.
    if not station.is_active:
        station.is_active = True
        station.save(update_fields=['is_active'])

    # Get all bookings for this station
    bookings = EVBooking.objects.filter(station=station).order_by('-rdate', '-rtime')

    # Prepare data for the template
    history = []
    for b in bookings:
        history.append({
            'user': b.uname.name,  # Get the user's name from the related EVRegister object
            'slot_no': b.slot,
            'in_time': b.btime1,
            'out_time': b.btime2,
            'start_date': b.rdate,
            # 'end_date': b.end_time.date() if b.end_time else '',
            'end_date': b.rdate,
            'status': b.chargest,
            'pay_status': b.payst,
            'amount': b.amount,
        })

    return render(request, 'report.html', {'history': history, 'station': station})


def station_logout(request):
    if 'station_owner' in request.session:
        uname = request.session['station_owner']
        try:
            station = EVStation.objects.get(uname=uname)
            station.is_active = False
            station.save()
            del request.session['station_owner']
        except EVStation.DoesNotExist:
            pass
    messages.success(request, "You have been logged out.")
    return redirect('station_login')


@csrf_exempt
@require_http_methods(["POST"])
def update_station_status(request):
    if 'station_owner' in request.session:
        uname = request.session['station_owner']
        try:
            station = EVStation.objects.get(uname=uname)
            station.is_active = False
            station.save(update_fields=['is_active'])
        except EVStation.DoesNotExist:
            # This could happen if the station was deleted but the session persists.
            pass
    # Return a 204 No Content response as is standard for beacon requests.
    return HttpResponse(status=204)



def user_login(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pwd = request.POST.get('pass')
        user = EVRegister.objects.filter(uname=uname, passw=pwd).first()
        if user:
            request.session['user'] = uname
            messages.success(request, "Login successful!")
            # Send welcome back email in background
            try:
                def send_login_mail(u):
                    try:
                        html = f"""<html><body style="background:#0a0e1a;font-family:Arial,sans-serif;padding:30px;">
<div style="max-width:500px;margin:auto;background:#0d1117;border-radius:16px;overflow:hidden;">
<div style="background:linear-gradient(90deg,#00c6ff,#0072ff,#7b2ff7);height:5px;"></div>
<div style="padding:30px;text-align:center;">
<h1 style="color:#00c6ff;margin:0;">&#9889; EV CHARGE HUB</h1>
<h3 style="color:#fff;margin:12px 0 4px;">Welcome back, {u.name}! 👋</h3>
<p style="color:#8892a4;font-size:13px;">You just logged in to EV Charge Hub</p>
<div style="background:#131920;border-radius:10px;padding:12px;margin:16px 0;text-align:left;">
<p style="color:#8892a4;font-size:12px;margin:0 0 4px;">Username</p>
<p style="color:#00c6ff;font-weight:700;font-size:16px;margin:0;">{u.uname}</p>
</div>
<p style="color:#8892a4;font-size:12px;">If this wasn't you, please change your password immediately.</p>
</div>
<div style="background:linear-gradient(90deg,#00c6ff,#0072ff,#7b2ff7);height:4px;"></div>
</div></body></html>"""
                        mail = EmailMultiAlternatives(
                            subject='👋 Welcome back to EV Charge Hub!',
                            body=f'Welcome back {u.name}! You just logged in.',
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            to=[u.email],
                        )
                        mail.attach_alternative(html, "text/html")
                        mail.send(fail_silently=True)
                    except Exception:
                        pass
                threading.Thread(target=send_login_mail, args=(user,)).start()
            except Exception:
                pass
            return redirect('user_home')
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'login.html')


def user_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        bank = request.POST.get('bank', '')
        account = request.POST.get('account', '')
        card = request.POST.get('card', '')
        uname = request.POST.get('uname')
        passw = request.POST.get('pass')
        latitude = request.POST.get('latitude', '')
        longitude = request.POST.get('longitude', '')

        # Check for any fields left empty (optional, but helps avoid errors)
        if not all([name, address, mobile, email, uname, passw]):
            messages.error(request, "All fields are required!")
            return render(request, 'register.html')

        # Username unique check
        if EVRegister.objects.filter(uname=uname).exists():
            messages.error(request, "Username already exists. Try another.")
            return render(request, 'register.html')

        # Save user
        user = EVRegister(
            uname=uname,
            passw=passw,
            name=name,
            address=address,
            mobile=mobile,
            email=email,
            bank=bank,
            account=account,
            card=card,
            latitude=latitude,
            longitude=longitude,
        )
        user.save()

        # Send confirmation email in background thread
        try:
            import threading
            html_message = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Welcome to EV Charge Hub</title>
</head>
<body style="margin:0;padding:0;background-color:#0a0e1a;font-family:'Segoe UI',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#0a0e1a;padding:40px 0;">
    <tr>
      <td align="center">
        <table width="620" cellpadding="0" cellspacing="0" style="background-color:#0d1117;border-radius:20px;overflow:hidden;">
          <tr><td style="background:linear-gradient(90deg,#00c6ff,#0072ff,#7b2ff7);height:5px;"></td></tr>
          <tr>
            <td style="padding:40px;text-align:center;">
              <h1 style="color:#00c6ff;">⚡ EV CHARGE HUB</h1>
              <h2 style="color:#ffffff;">Welcome, {name}! 🎉</h2>
              <p style="color:#8892a4;">Registration successful! Username: <strong style="color:#00c6ff;">{uname}</strong></p>
            </td>
          </tr>
          <tr><td style="background:linear-gradient(90deg,#00c6ff,#0072ff,#7b2ff7);height:4px;"></td></tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""
            from django.core.mail import EmailMultiAlternatives
            def send_email():
                try:
                    mail = EmailMultiAlternatives(
                        subject='⚡ Welcome to EV Charge Hub – Registration Successful!',
                        body=f'Hi {name}, your registration at EV Charge Hub was successful! Username: {uname}',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[email],
                    )
                    mail.attach_alternative(html_message, "text/html")
                    mail.send(fail_silently=True)
                except Exception:
                    pass
            threading.Thread(target=send_email).start()
        except Exception:
            pass

        messages.success(request, "Registration successful, please login.")
        return redirect('user_login')

    return render(request, 'register.html')


def user_home(request):
    if 'user' not in request.session:
        messages.error(request, "Invalid user credentials. please login")
        return redirect('user_login')
    uname = request.session['user']
    user = EVRegister.objects.get(uname=uname)
    bookings = EVBooking.objects.filter(uname=uname)
    context = {
        'data': user,
        'bookings': bookings,
        'uname': user.uname
    }
    return render(request, 'userhome.html', context)


def user_station_selection(request):
    if 'user' not in request.session:
        messages.error(request, "Invalid user credentials. please login")
        return redirect('user_login')

    now = datetime.now()
    rdate2 = now.strftime("%Y-%m-%d")

    # Get user coordinates, convert to float
    lat2 = float(request.GET.get('lat', 0))
    lon2 = float(request.GET.get('lon', 0))
    has_location = lat2 != 0 and lon2 != 0
    R = 6373.0  # Earth radius in km

    uname = ""
    if 'user' in request.session:
        uname = request.session['user']

    search_query = ""
    if request.method == "POST":
        search_query = request.POST.get('getval', '').strip()

    stations = EVStation.objects.all()

    if search_query:
        stations = stations.filter(
            city__icontains=search_query
        ) | stations.filter(
            area__icontains=search_query
        ) | stations.filter(
            name__icontains=search_query
        ) | stations.filter(
            landmark__icontains=search_query
        )

    data = []
    for st in stations:
        try:
            lat1 = float(st.lat)
            lon1 = float(st.lon)
        except (TypeError, ValueError):
            continue


        # convert degrees to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
        if a > 1:
            a = 1
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = round(R * c, 2)

        bookings = EVBooking.objects.filter(station=st, rdate=rdate2, status=1)
        booking_status = "yes" if bookings.exists() else "no"
        booking_info = [
            [bk.uname, bk.carno, bk.reserve, bk.slot, bk.rdate, bk.btime1, bk.btime2]
            for bk in bookings
        ]

        dt = [
            st.uname, st.name, st.area, st.city, st.landmark,
            st.numcharger, st.lat, st.lon,
            booking_info, booking_status, distance if has_location else 'N/A', st.is_active
        ]
        data.append(dt)

    return render(request, 'station.html', {
        'data': data,
        'uname': uname,
        'st' : "1",
        'rdate2': rdate2,
        'search_query': search_query,
    })



def user_view_station_slots(request, sid):
    if 'user' not in request.session:
        messages.error(request, "Invalid user credentials. please login")
        return redirect('user_login')

    station = get_object_or_404(EVStation, uname=sid)
    uname = request.session.get('user', '')


    now = timezone.localtime()
    rdate = now.strftime("%Y-%m-%d")
    now_str = now.strftime("%H:%M")

    slots = []
    for i in range(1, station.numcharger + 1):

        booking = EVBooking.objects.filter(
            station__uname=sid,
            slot=i,
            status=1,
            rdate=rdate
        ).first()
        if booking and booking.chargest == 2:
            # If now >= end time, mark complete
            try:
                if now_str >= booking.btime2:
                    booking.chargest = 3
                    booking.chargemin = 0
                    booking.chargesec = 0
                    booking.save(update_fields=['chargest', 'chargemin', 'chargesec'])
            except Exception:
                pass
        slots.append({'slot': i, 'booked': booking is not None, 'booking': booking})


    return render(
        request,
        'slot.html',
        {
            'station': station,
            'slots': slots,
            'uname': uname,
            'sid': sid,
        }
    )


def book_slot(request):
    if 'user' not in request.session:
        messages.error(request, "Invalid user credentials. please login")
        return redirect('user_login')

    msg = ""
    uname = request.session['user']
    sid = request.GET.get('sid') or request.POST.get('sid')
    slot = request.GET.get('slot') or request.POST.get('slot')

    now = timezone.localtime()
    rdate = now.strftime("%Y-%m-%d")
    cdate = now.strftime("%Y-%m-%d") # Use YYYY-MM-DD format for current date
    cd1 = cdate.split("-")

    # Get the station object
    station = EVStation.objects.filter(uname=sid).first()
    tarr = [str(i) for i in range(24)]

    # Check existing bookings for this slot for today
    existing_bookings = EVBooking.objects.filter(station__uname=sid, status=1, slot=slot, rdate=cdate)
    arr_time = []
    for eb in existing_bookings:
        if eb.rtime:
            arr_time.append(eb.rtime.split(":"))

    if request.method == "POST":
        carno = request.POST['carno']
        reserve = request.POST['reserve']
        sid = request.POST['sid']
        slot = request.POST['slot']
        bdate = request.POST['bdate'] # This is YYYY-MM-DD from the form

        t1 = request.POST['t1']
        t2 = request.POST['t2']
        t3 = request.POST['t3']
        t4 = request.POST['t4']

        sh = int(t1)
        btime1 = f"{t1}:{t2}"
        btime2 = f"{t3}:{t4}"

        now = timezone.localtime()
        booking_datetime_str = f"{bdate} {btime1}"
        booking_datetime = datetime.strptime(booking_datetime_str, "%Y-%m-%d %H:%M")
        # Make booking_datetime timezone-aware
        booking_datetime = timezone.make_aware(booking_datetime, timezone.get_current_timezone())


        if booking_datetime < now:
            messages.error(request, "Booking for a past date or time is not allowed.")
            return redirect('slot', sid=sid)

        start = datetime.strptime(btime1, "%H:%M")
        end = datetime.strptime(btime2, "%H:%M")
        delta_minutes = int((end - start).total_seconds() // 60)
        if delta_minutes <= 0:
            delta_minutes = 30  # fallback

        bd1 = bdate.split("-")

        # d0 is today, d1 is booking day
        d0 = date(int(cd1[0]), int(cd1[1]), int(cd1[2]))
        d1 = date(int(bd1[0]), int(bd1[1]), int(bd1[2]))
        delta = d1 - d0
        dy = delta.days

        x = 0
        # STRONG double booking check - same slot, overlapping time
        slot_conflict = EVBooking.objects.filter(
            station__uname=sid, slot=slot, rdate=bdate, status=1
        ).exclude(chargest=3).exclude(btime2__lte=btime1).exclude(btime1__gte=btime2).exists()
        
        if slot_conflict:
            messages.error(request, f"⚠️ Slot {slot} is already booked during {btime1} - {btime2}. Please choose a different time or slot.")
            return redirect('slot', sid=sid)

        # Check station capacity - max 1 booking per slot at same time
        concurrent_bookings = EVBooking.objects.filter(
            station__uname=sid, rdate=bdate, status=1, slot=slot
        ).exclude(chargest=3).exclude(btime2__lte=btime1).exclude(btime1__gte=btime2).count()
        
        if concurrent_bookings >= 1:
            x = 99

        if x < 2 and dy >= 0:
            cimage = "evch.jpg"
            # Book new slot
            user = EVRegister.objects.get(uname=uname)
            station = EVStation.objects.get(uname=sid)
            new_booking = EVBooking.objects.create(
                uname=user,
                station=station,
                carno=carno,
                reserve=reserve,
                slot=slot,
                cimage=cimage,
                rtime=f"{t1}:{t2}",
                rdate=bdate,
                etime=f"{t3}:{t4}",
                edate=bdate,
                status=1,
                btime1=btime1,
                btime2=btime2,
                mins=delta_minutes,
                chargest=0,
                chargemin=delta_minutes,
                chargesec=0,
            )
            messages.success(request, f"Slot.no : {new_booking.slot} Booked successfully.")

            # Send booking confirmation email with QR
            try:
                def send_booking_email(booking, user_obj):
                    qr_data = (f"EV Charge Hub Booking\nBooking ID: {booking.id}\n"
                               f"Station: {booking.station.name}\nSlot: {booking.slot}\n"
                               f"Date: {booking.rdate}\nTime: {booking.btime1} - {booking.btime2}\n"
                               f"Vehicle: {booking.carno}")
                    qr_base64 = ""
                    if QRCODE_AVAILABLE:
                        import qrcode as qrc
                        qr = qrc.QRCode(version=1, box_size=6, border=3)
                        qr.add_data(qr_data)
                        qr.make(fit=True)
                        img = qr.make_image(fill_color="#0072ff", back_color="white")
                        buf = io.BytesIO()
                        img.save(buf, format='PNG')
                        qr_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                    qr_img_tag = f'<img src="data:image/png;base64,{qr_base64}" style="width:180px;height:180px;border-radius:12px;margin:16px 0;border:4px solid #0072ff;">' if qr_base64 else ''
                    html_msg = f"""<html><body style="background:#0a0e1a;font-family:Arial,sans-serif;padding:30px;">
<div style="max-width:600px;margin:auto;background:#0d1117;border-radius:16px;overflow:hidden;">
  <div style="background:linear-gradient(90deg,#00c6ff,#0072ff,#7b2ff7);height:5px;"></div>
  <div style="padding:30px;text-align:center;">
    <h1 style="color:#00c6ff;margin:0;">&#9889; EV CHARGE HUB</h1>
    <p style="color:#4a9eff;letter-spacing:3px;font-size:12px;">BOOKING CONFIRMED</p>
    <h2 style="color:#34d399;">&#10003; Slot Booked Successfully!</h2>
    <p style="color:#8892a4;">Hi <strong style="color:#fff;">{user_obj.name}</strong>, your slot is confirmed!</p>
    {qr_img_tag}
    <div style="background:#131920;border-radius:12px;padding:16px;text-align:left;margin:16px 0;">
      <table style="width:100%;color:#fff;font-size:14px;">
        <tr><td style="color:#8892a4;padding:5px 0;">Booking ID</td><td style="color:#00c6ff;font-weight:700;">#{booking.id}</td></tr>
        <tr><td style="color:#8892a4;padding:5px 0;">Station</td><td>{booking.station.name}</td></tr>
        <tr><td style="color:#8892a4;padding:5px 0;">Slot No.</td><td>{booking.slot}</td></tr>
        <tr><td style="color:#8892a4;padding:5px 0;">Date</td><td>{booking.rdate}</td></tr>
        <tr><td style="color:#8892a4;padding:5px 0;">Time</td><td>{booking.btime1} - {booking.btime2}</td></tr>
        <tr><td style="color:#8892a4;padding:5px 0;">Vehicle</td><td>{booking.carno}</td></tr>
      </table>
    </div>
    <p style="color:#8892a4;font-size:12px;">Show this QR code at the charging station</p>
  </div>
  <div style="background:linear-gradient(90deg,#00c6ff,#0072ff,#7b2ff7);height:4px;"></div>
</div></body></html>"""
                    try:
                        mail = EmailMultiAlternatives(
                            subject=f'⚡ Booking Confirmed – Slot {booking.slot} | EV Charge Hub',
                            body=f'Booking confirmed! Slot {booking.slot} at {booking.station.name} on {booking.rdate}',
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            to=[user_obj.email],
                        )
                        mail.attach_alternative(html_msg, "text/html")
                        mail.send(fail_silently=True)
                    except Exception:
                        pass
                user_obj = EVRegister.objects.get(uname=uname)
                threading.Thread(target=send_booking_email, args=(new_booking, user_obj)).start()
            except Exception:
                pass
        else:
            messages.error(request, f"Booking failed. Slot.no : {slot} may be unavailable or invalid time.")

        return redirect('booking_qr', rid=new_booking.id) if x < 2 and dy >= 0 else redirect('slot', sid=sid)

    context = {
        'msg': msg,
        'uname': uname,
        'sid': sid,
        'slot': slot,
        'rdate': rdate,
        'tarr': tarr
    }
    return render(request, 'book.html', context)


def rebook(request, rid):
    if 'user' not in request.session:
        messages.error(request, "Invalid user credentials. please login")
        return redirect('user_login')

    booking = get_object_or_404(EVBooking, id=rid)

    # Only owner can reschedule
    if booking.uname.uname != request.session['user']:
        messages.error(request, "You are not allowed to reschedule this booking.")
        return redirect('slot', sid=booking.station.uname)

    now = timezone.localtime()
    rdate = now.strftime('%Y-%m-%d')  # for <input type="date">
    tarr = [str(i) for i in range(24)]

    if request.method == 'POST':
        bdate = request.POST.get('bdate')      # 'YYYY-MM-DD'
        t1 = request.POST.get('t1')           # start hour
        t2 = request.POST.get('t2')           # start minute
        t3 = request.POST.get('t3')           # end hour
        t4 = request.POST.get('t4')           # end minute

        btime1 = f"{t1}:{t2}"
        btime2 = f"{t3}:{t4}"

        # basic validation: date not in past
        cd = date.fromisoformat(rdate)
        bd = date.fromisoformat(bdate)
        if bd < cd:
            messages.error(request, "Cannot reschedule to a past date.")
            return render(request, 'rebook.html', {
                'booking': booking,
                'rdate': rdate,
                'tarr': tarr,
            })

        # Todo: add your collision rules (max 2 per hour, etc.)

        # Update existing booking
        booking.btime1 = btime1
        booking.btime2 = btime2
        booking.rdate = bd.strftime('%Y-%m-%d')  # or '%Y-%m-%d' – match what you use elsewhere
        booking.save()

        messages.success(request, f"Slot.no : {booking.slot} Booking rescheduled successfully.")
        return redirect('slot', sid=booking.station.uname)

    return render(request, 'rebook.html', {
        'booking': booking,
        'rdate': rdate,
        'tarr': tarr,
    })


def booking_out(request, rid):
    if 'user' not in request.session:
        messages.error(request, "Invalid user credentials. please login")
        return redirect('user_login')

    booking = get_object_or_404(EVBooking, id=rid)

    # Only the owner can act
    if hasattr(booking.uname, 'uname'):
        booking_uname = booking.uname.uname
    else:
        booking_uname = booking.uname

    if booking_uname != request.session['user']:
        messages.error(request, "You cannot cancel this booking.")
        return redirect('slot', sid=booking.station.uname)

    # Allow cancel only before charging
    if booking.chargest != 0:
        messages.error(request, "Charging already started. Cannot cancel now.")
        return redirect('slot', sid=booking.station.uname)

    booking.status = 0  # cancelled
    booking.save(update_fields=['status'])
    messages.success(request, f"Slot.no : {booking.slot} Booking cancelled successfully.")
    return redirect('slot', sid=booking.station.uname)


def select_plan(request):
    if 'user' not in request.session:
        messages.error(request, "Invalid user credentials. please login")
        return redirect('user_login')

    sid = request.GET.get('sid') or request.POST.get('sid')
    rid = request.GET.get('rid') or request.POST.get('rid')

    if not rid:
        if sid:
            return redirect('slot', sid=sid)
        return redirect('user_home')

    booking = get_object_or_404(EVBooking, id=rid)

    # If charging complete, mark old booking as done (status=3) before allowing re-charge
    if booking.chargest == 3 and booking.status == 1:
        booking.status = 3
        booking.save(update_fields=['status'])

    # Check if next person already booked this slot at overlapping time
    now = timezone.localtime()
    now_str = now.strftime("%H:%M")
    next_booking = EVBooking.objects.filter(
        station=booking.station,
        slot=booking.slot,
        rdate=booking.rdate,
        status=1,
    ).exclude(id=booking.id).first()

    if next_booking:
        messages.error(request, f"⚠️ Slot {booking.slot} is already booked by another user from {next_booking.btime1} to {next_booking.btime2}. Please vacate the slot.")
        return redirect('slot', sid=booking.station.uname)

    if request.method == 'POST':
        plan = request.POST.get('plan')
        if not plan:
            messages.error(request, 'Please select a plan')
            return render(request, 'select.html', {'sid': sid, 'rid': rid, 'booking': booking})

        plan_int = int(plan)
        booking.plan = plan_int

        # map each plan number to mins and amount
        if plan_int == 1:
            booking.amount = 100
        elif plan_int == 2:
            booking.amount = 200
        elif plan_int == 3:
            booking.amount = 300

        booking.chargest = 1
        booking.status = 1
        booking.save(update_fields=['plan', 'amount', 'chargest', 'status'])

        request.session['booking_id'] = booking.id
        return redirect('slot', sid=sid)

    return render(request, 'select.html', {'sid': sid, 'rid': rid, 'booking': booking})


def tariff_view(request):
    return render(request, 'tariff.html')


def user_history(request):
    if 'user' not in request.session:
        messages.error(request, "Invalid user credentials. please login")
        return redirect('user_login')
    
    uname = request.session['user']

    # Get all bookings for this user, with related station data
    bookings = EVBooking.objects.filter(uname=uname).select_related('station').order_by('-rdate', '-rtime')

    history_data = []
    for b in bookings:
        rtime_obj = None
        if b.rtime:
            try:
                # Attempt to parse time in HH:MM:SS or HH:MM format
                rtime_obj = datetime.strptime(b.rtime, '%H:%M:%S').time()
            except ValueError:
                try:
                    rtime_obj = datetime.strptime(b.rtime, '%H:%M').time()
                except ValueError:
                    # Handle cases where rtime is not in expected format
                    rtime_obj = None # Or set a default time, or pass the raw string

        history_data.append({
            'station_name': b.station.name if b.station else '',
            'station_city': b.station.city if b.station else '',
            'station_lat': b.station.lat if b.station else '',
            'station_lon': b.station.lon if b.station else '',
            'slot': b.slot,
            'amount': b.amount,
            'rtime': rtime_obj,
            'etime': b.btime2,
            'rdate': b.rdate,
            # 'edate': b.end_time.date() if b.end_time else '',
            'edate': b.rdate,
            'chargest': b.chargest,
            'payst': b.payst,
        })

    return render(request, 'history.html', {'data': history_data, 'uname': uname})


def payment(request, rid=None):
    if 'user' not in request.session:
        messages.error(request, "Invalid user credentials. please login")
        return redirect('user_login')

    # 1) Get booking either from URL (OUT after charge) or from session (old flow)
    if rid is not None:
        booking = get_object_or_404(EVBooking, id=rid)
    else:
        booking_id = request.session.get('booking_id')
        if not booking_id:
            messages.error(request, "No active booking to pay for.")
            return redirect('user_home')
        booking = get_object_or_404(EVBooking, id=booking_id)

    # 2) Optional: ensure only owner can pay
    if hasattr(booking.uname, 'uname'):
        booking_uname = booking.uname.uname
    else:
        booking_uname = booking.uname

    if booking_uname != request.session['user']:
        messages.error(request, "You cannot pay for this booking.")
        return redirect('slot', sid=booking.station.uname)

    # 3) Optional: ensure charging is completed before payment
    if booking.chargest != 3:
        messages.error(request, "Charging not completed yet.")
        return redirect('slot', sid=booking.station.uname)

    # 4) Set end time / amount like Flask (optional, if not already done elsewhere)
    # booking.amount should already be set from select_plan; if you still need min 20:
    if booking.amount <= 0:
        booking.amount = 20
        booking.save(update_fields=['amount'])

    # 5) Handle payment submit
    if request.method == 'POST':
        pay_mode = request.POST.get('pay_mode')
        if not pay_mode:
            messages.error(request, "Please select a payment mode.")
            return render(request, 'payment.html', {'booking': booking})

        # Bank mode → generate OTP and go to verify_otp
        if pay_mode == 'Bank':
            otp = str(randint(100000, 999999))
            booking.paymode = pay_mode
            booking.otp = otp
            booking.save(update_fields=['paymode', 'otp'])

            # --- Send SMS ---
            try:
                user = EVRegister.objects.get(uname=request.session['user'])
                mobile = user.mobile

                # The message must match the pre-approved template associated with the templateid
                sms_message = f"Dear {user.uname} Emergency Alert Message in the link:Key:{otp} By SMSWAY IOTCLD"
                # URL-encode the message
                encoded_message = urllib.parse.quote(sms_message)

                url = (
                    "http://pay4sms.in/sendsms/"
                    f"?token=b81edee36bcef4ddbaa6ef535f8db03e&credit=2&sender=IOTCLD"
                    f"&message={encoded_message}&number={mobile}&templateid=1207162443838625724"
                )

                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
                }
                r = requests.get(url, timeout=10, headers=headers)

                if r.status_code == 200 and "sent" in r.text.lower(): # Check for "sent" in response text
                    messages.success(request, "OTP has been sent to your mobile.")
                else:
                    messages.error(request, f"Failed to send OTP. SMS gateway returned status {r.status_code}.")
            except Exception as e:

                messages.error(request, "Failed to send OTP. Please try again.")
                # We might want to stay on the payment page if OTP sending fails
                return render(request, 'payment.html', {'booking': booking})

            return redirect('verify_otp', rid=booking.id)

        # Other modes → mark paid directly
        else:
            booking.paymode = pay_mode
            booking.payst = 1
            booking.save(update_fields=['paymode', 'payst'])
            messages.success(request, f"Payment successful for Slot.no : {booking.slot}, Paid Amount INR {booking.amount}.")
            # Send payment confirmation email
            try:
                user_obj = EVRegister.objects.get(uname=request.session['user'])
                def send_pay_email(b, u):
                    try:
                        html = f"""<html><body style="background:#0a0e1a;font-family:Arial,sans-serif;padding:30px;">
<div style="max-width:600px;margin:auto;background:#0d1117;border-radius:16px;overflow:hidden;">
<div style="background:linear-gradient(90deg,#00c6ff,#0072ff,#7b2ff7);height:5px;"></div>
<div style="padding:30px;text-align:center;">
<h1 style="color:#00c6ff;">&#9889; EV CHARGE HUB</h1>
<h2 style="color:#34d399;">&#10003; Payment Successful!</h2>
<p style="color:#8892a4;">Hi <strong style="color:#fff;">{u.name}</strong>, your payment is confirmed!</p>
<div style="background:#131920;border-radius:12px;padding:16px;text-align:left;margin:16px 0;">
<table style="width:100%;color:#fff;font-size:14px;">
<tr><td style="color:#8892a4;padding:5px 0;">Booking ID</td><td style="color:#00c6ff;font-weight:700;">#{b.id}</td></tr>
<tr><td style="color:#8892a4;padding:5px 0;">Station</td><td>{b.station.name}</td></tr>
<tr><td style="color:#8892a4;padding:5px 0;">Slot</td><td>{b.slot}</td></tr>
<tr><td style="color:#8892a4;padding:5px 0;">Amount Paid</td><td style="color:#34d399;font-weight:700;">&#8377;{b.amount}</td></tr>
<tr><td style="color:#8892a4;padding:5px 0;">Payment Mode</td><td>{b.paymode}</td></tr>
</table></div>
<img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=EV+Booking+{b.id}+Payment+Confirmed+Amount+{b.amount}" style="width:150px;height:150px;border-radius:8px;margin:10px 0;border:3px solid #34d399;">
<p style="color:#8892a4;font-size:12px;">Thank you for using EV Charge Hub!</p>
</div>
<div style="background:linear-gradient(90deg,#00c6ff,#0072ff,#7b2ff7);height:4px;"></div>
</div></body></html>"""
                        mail = EmailMultiAlternatives(
                            subject=f'✅ Payment Confirmed – ₹{b.amount} | EV Charge Hub',
                            body=f'Payment confirmed! Booking #{b.id}, Amount: ₹{b.amount}',
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            to=[u.email],
                        )
                        mail.attach_alternative(html, "text/html")
                        mail.send(fail_silently=True)
                    except Exception:
                        pass
                threading.Thread(target=send_pay_email, args=(booking, user_obj)).start()
            except Exception:
                pass
            return redirect('slot', sid=booking.station.uname)

    return render(request, 'payment.html', {'booking': booking})


def verify_otp(request, rid):
    if 'user' not in request.session:
        messages.error(request, "Invalid user credentials. please login")
        return redirect('user_login')
    
    booking = get_object_or_404(EVBooking, id=rid)

    key = booking.otp
    msg = ""

    if request.method == 'POST':
        otp_entered = request.POST.get('otp', '').strip()
        if otp_entered and otp_entered == key:
            booking.payst = 2    # pay_st=2
            booking.status = 3   # status=3
            booking.save(update_fields=['payst', 'status'])
            messages.success(request, f"Payment successful for Slot.no : {booking.slot}, Paid Amount INR {booking.amount}.")
            return redirect('slot', sid=booking.station.uname)
        else:
            msg = "Invalid OTP"
            messages.error(request, msg)

    return render(request, 'verify_otp.html', {'booking': booking, 'msg': msg})


def resend_otp(request, rid):
    if 'user' not in request.session:
        messages.error(request, "Invalid user credentials. please login")
        return redirect('user_login')

    booking = get_object_or_404(EVBooking, id=rid)

    # Generate a new OTP
    otp = str(randint(100000, 999999))
    booking.otp = otp
    booking.save(update_fields=['otp'])

    # --- Send SMS ---
    try:
        user = EVRegister.objects.get(uname=request.session['user'])
        mobile = user.mobile

        # The message must match the pre-approved template associated with the templateid
        sms_message = f"Dear {user.uname} Emergency Alert Message in the link:Key:{otp} By SMSWAY IOTCLD"
        # URL-encode the message
        encoded_message = urllib.parse.quote(sms_message)

        url = (
            "http://pay4sms.in/sendsms/"
            f"?token=b81edee36bcef4ddbaa6ef535f8db03e&credit=2&sender=IOTCLD"
            f"&message={encoded_message}&number={mobile}&templateid=1207162443838625724"
        )

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        r = requests.get(url, timeout=10, headers=headers)

        if r.status_code == 200 and "sent" in r.text.lower(): # Check for "sent" in response text
            messages.success(request, "OTP has been resent to your mobile.")
        else:
            messages.error(request, f"Failed to resend OTP. SMS gateway returned status {r.status_code}.")
    except Exception as e:
        messages.error(request, "Failed to resend OTP. Please try again.")

    return redirect('verify_otp', rid=booking.id)


def user_logout(request):
    if 'user' in request.session:
        request.session.flush()
    messages.success(request, "You have been logged out.")
    return redirect('user_login')


@csrf_exempt
@require_POST
def station_heartbeat(request):
    if 'station_owner' in request.session:
        uname = request.session['station_owner']
        try:
            station = EVStation.objects.get(uname=uname)
            station.last_seen = timezone.now()
            station.save(update_fields=['last_seen'])
            return HttpResponse(status=200)
        except EVStation.DoesNotExist:
            pass
    return HttpResponse(status=401) # Unauthorized


def booking_status_api(request):
    now = datetime.now()
    rdate2 = now.strftime("%Y-%m-%d")

    stations = EVStation.objects.all()
    data = {}
    for st in stations:
        bookings = EVBooking.objects.filter(station=st, rdate=rdate2, status=1)
        booking_status = "yes" if bookings.exists() else "no"
        booking_info = [
            {
                'slot': bk.slot,
                'btime1': bk.btime1,
                'btime2': bk.btime2,
            }
            for bk in bookings
        ]
        data[st.uname] = {
            'booking_status': booking_status,
            'booking_info': booking_info,
        }

    return JsonResponse(data)


def station_status_api(request):
    # Update inactive stations based on last_seen timestamp
    # A station is considered inactive if its last_seen is older than 30 seconds
    thirty_seconds_ago = timezone.now() - timedelta(seconds=120)
    EVStation.objects.filter(is_active=True, last_seen__lt=thirty_seconds_ago).update(is_active=False)

    stations = EVStation.objects.all()
    data = {station.uname: {'is_active': station.is_active, 'status': station.status} for station in stations}
    return JsonResponse(data)


def station_slots_api(request, sid):
    # Allow both station owners and regular users to hit this endpoint
    if not (request.session.get('station_owner') or request.session.get('user')):
         return JsonResponse({'error': 'Authentication required'}, status=403)

    station = get_object_or_404(EVStation, uname=sid)
    slots_data = get_slot_data(station)

    # Serialize the data to make it safe for JSON conversion
    serializable_slots = []
    for slot in slots_data:
        booking_info = None
        if slot['booking']:
            b = slot['booking']
            
            # Format end_time to ISO 8601 string if it exists
            end_time_iso = b.end_time.isoformat() if b.end_time else None

            booking_info = {
                'id': b.id,
                'carno': b.carno,
                'chargest': b.chargest,
                'payst': b.payst,
                'paymode': b.paymode,
                'end_time': end_time_iso,
                'uname': b.uname.uname, # Add this line
            }
        serializable_slots.append({
            'slot_flag': slot['slot_flag'],
            'slot_num': slot['slot_num'],
            'booking': booking_info
        })

    return JsonResponse({'slots': serializable_slots, 'current_user_uname': request.session.get('user', '')})



# PDF Generation Functions

def history_pdf(request):
    """Generate PDF for user charging history"""
    if 'user' not in request.session:
        messages.error(request, "Invalid user credentials. please login")
        return redirect('user_login')
    
    uname = request.session['user']
    
    # Get all bookings for this user, with related station data
    bookings = EVBooking.objects.filter(uname=uname).select_related('station').order_by('-rdate', '-rtime')

    history_data = []
    for b in bookings:
        rtime_obj = None
        if b.rtime:
            try:
                # Attempt to parse time in HH:MM:SS or HH:MM format
                rtime_obj = datetime.strptime(b.rtime, '%H:%M:%S').time()
            except ValueError:
                try:
                    rtime_obj = datetime.strptime(b.rtime, '%H:%M').time()
                except ValueError:
                    # Handle cases where rtime is not in expected format
                    rtime_obj = None

        history_data.append({
            'station_name': b.station.name if b.station else '',
            'station_city': b.station.city if b.station else '',
            'slot': b.slot,
            'amount': b.amount,
            'rtime': rtime_obj,
            'etime': b.btime2,
            'rdate': b.rdate,
            'chargest': b.chargest,
            'payst': b.payst,
        })

    if WEASYPRINT_AVAILABLE:
        # Use WeasyPrint for better PDF quality
        html_string = render_to_string('history_pdf.html', {'data': history_data, 'uname': uname})
        html = HTML(string=html_string)
        pdf = html.write_pdf()
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="charging_history_{uname}.pdf"'
        return response
        
    elif REPORTLAB_AVAILABLE:
        # Fallback to ReportLab
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="charging_history_{uname}.pdf"'
        
        doc = SimpleDocTemplate(response, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title = Paragraph(f"Charging History for {uname}", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Table data
        data = [['S.No', 'Station', 'Slot', 'Date', 'Time', 'Amount', 'Status']]
        for i, row in enumerate(history_data, 1):
            status = 'Completed' if row['chargest'] == 3 else 'Charging' if row['chargest'] == 2 else 'Waiting' if row['chargest'] == 1 else 'Cancelled'
            data.append([
                str(i),
                f"{row['station_name']}, {row['station_city']}",
                str(row['slot']),
                row['rdate'],
                row['rtime'].strftime('%H:%M') if row['rtime'] else '--',
                f"₹{row['amount']}",
                status
            ])
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        doc.build(elements)
        return response
    else:
        # No PDF library available
        messages.error(request, "PDF generation is not available. Please install WeasyPrint or ReportLab.")
        return redirect('history')


def report_pdf(request):
    """Generate PDF for station reports"""
    if not request.session.get('station_owner'):
        messages.error(request, "Invalid station credentials. please login")
        return redirect('station_login')
    
    uname = request.session['station_owner']
    station = get_object_or_404(EVStation, uname=uname)

    # Get all bookings for this station
    bookings = EVBooking.objects.filter(station=station).order_by('-rdate', '-rtime')

    # Prepare data for the template
    history = []
    for b in bookings:
        history.append({
            'user': b.uname.name,  # Get the user's name from the related EVRegister object
            'slot_no': b.slot,
            'in_time': b.btime1,
            'out_time': b.btime2,
            'start_date': b.rdate,
            'end_date': b.rdate,
            'status': b.chargest,
            'pay_status': b.payst,
            'amount': b.amount,
        })

    if WEASYPRINT_AVAILABLE:
        # Use WeasyPrint for better PDF quality
        html_string = render_to_string('report_pdf.html', {'history': history, 'station': station})
        html = HTML(string=html_string)
        pdf = html.write_pdf()
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="station_report_{station.name}.pdf"'
        return response
        
    elif REPORTLAB_AVAILABLE:
        # Fallback to ReportLab
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="station_report_{station.name}.pdf"'
        
        doc = SimpleDocTemplate(response, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title = Paragraph(f"Station Report - {station.name}", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Station info
        info = Paragraph(f"Location: {station.area}, {station.city}<br/>Chargers: {station.numcharger}", styles['Normal'])
        elements.append(info)
        elements.append(Spacer(1, 12))
        
        # Table data
        data = [['S.No', 'User', 'Slot', 'Date', 'In Time', 'Out Time', 'Amount', 'Status']]
        for i, row in enumerate(history, 1):
            status = 'Completed' if row['status'] == 3 else 'Charging' if row['status'] == 2 else 'Waiting' if row['status'] == 1 else 'Cancelled'
            data.append([
                str(i),
                row['user'],
                str(row['slot_no']),
                row['start_date'],
                row['in_time'],
                row['out_time'],
                f"₹{row['amount']}",
                status
            ])
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        doc.build(elements)
        return response
    else:
        # No PDF library available
        messages.error(request, "PDF generation is not available. Please install WeasyPrint or ReportLab.")
        return redirect('station_report')
# ─── Forgot Password ─────────────────────────────────────────────────────────

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        user = EVRegister.objects.filter(email=email).first()
        if not user:
            messages.error(request, "No account found with that email.")
            return render(request, 'forgot_password.html')

        token = secrets.token_urlsafe(32)
        request.session[f'reset_{token}'] = user.uname
        reset_link = request.build_absolute_uri(reverse('reset_password', args=[token]))

        html_msg = f"""<html><body style="background:#0a0e1a;font-family:Arial,sans-serif;padding:40px;">
<div style="max-width:600px;margin:auto;background:#0d1117;border-radius:16px;overflow:hidden;">
  <div style="background:linear-gradient(90deg,#00c6ff,#0072ff,#7b2ff7);height:5px;"></div>
  <div style="padding:40px;text-align:center;">
    <h1 style="color:#00c6ff;">⚡ EV Charge Hub</h1>
    <h2 style="color:#fff;">Password Reset</h2>
    <p style="color:#8892a4;">Hi <strong style="color:#00c6ff;">{user.name}</strong>, click below to reset your password.</p>
    <a href="{reset_link}" style="display:inline-block;margin-top:20px;padding:14px 32px;background:linear-gradient(90deg,#00c6ff,#0072ff);color:#fff;border-radius:8px;text-decoration:none;font-weight:600;">Reset Password</a>
    <p style="color:#555;margin-top:20px;font-size:12px;">Link expires when you close the browser.</p>
  </div>
  <div style="background:linear-gradient(90deg,#00c6ff,#0072ff,#7b2ff7);height:4px;"></div>
</div></body></html>"""

        def send_reset():
            try:
                mail = EmailMultiAlternatives(
                    subject='⚡ EV Charge Hub – Password Reset',
                    body=f'Reset your password: {reset_link}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                )
                mail.attach_alternative(html_msg, "text/html")
                mail.send(fail_silently=True)
            except Exception:
                pass
        threading.Thread(target=send_reset).start()

        messages.success(request, "Password reset link sent to your email!")
        return redirect('user_login')

    return render(request, 'forgot_password.html')


def reset_password(request, token):
    uname = request.session.get(f'reset_{token}')
    if not uname:
        messages.error(request, "Invalid or expired reset link.")
        return redirect('forgot_password')

    if request.method == 'POST':
        new_pass = request.POST.get('password', '')
        confirm = request.POST.get('confirm', '')
        if not new_pass or new_pass != confirm:
            messages.error(request, "Passwords do not match.")
            return render(request, 'reset_password.html', {'token': token})

        user = EVRegister.objects.filter(uname=uname).first()
        if user:
            user.passw = new_pass
            user.save(update_fields=['passw'])
            del request.session[f'reset_{token}']
            messages.success(request, "Password reset successful! Please login.")
            return redirect('user_login')

    return render(request, 'reset_password.html', {'token': token})


# ─── Booking QR Code ─────────────────────────────────────────────────────────

def booking_qr(request, rid):
    if 'user' not in request.session:
        return redirect('user_login')

    booking = get_object_or_404(EVBooking, id=rid)

    qr_data = (
        f"EV Charge Hub Booking\n"
        f"Booking ID: {booking.id}\n"
        f"Station: {booking.station.name}\n"
        f"Slot: {booking.slot}\n"
        f"Date: {booking.rdate}\n"
        f"Time: {booking.btime1} - {booking.btime2}\n"
        f"Vehicle: {booking.carno}\n"
        f"Amount: Rs.{booking.amount}"
    )

    qr_base64 = ""
    if QRCODE_AVAILABLE:
        qr = qrcode.QRCode(version=1, box_size=8, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#0072ff", back_color="white")
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        qr_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    return render(request, 'booking_qr.html', {
        'booking': booking,
        'qr_base64': qr_base64,
    })


# ─── UPI Payment ─────────────────────────────────────────────────────────────

def upi_payment(request, rid):
    if 'user' not in request.session:
        return redirect('user_login')

    booking = get_object_or_404(EVBooking, id=rid)

    if booking.chargest != 3:
        messages.error(request, "Charging not completed yet.")
        return redirect('slot', sid=booking.station.uname)

    # UPI payment string (works with PhonePe, GPay, Paytm)
    upi_id = "naveenarul637-3@okicici"
    upi_name = "EV Charge Hub"
    amount = booking.amount
    note = f"EV Booking {booking.id}"
    upi_string = f"upi://pay?pa={upi_id}&pn={urllib.parse.quote(upi_name)}&am={amount}&cu=INR&tn={urllib.parse.quote(note)}"

    qr_base64 = ""
    try:
        import qrcode as qrc
        qr = qrc.QRCode(version=1, box_size=8, border=4)
        qr.add_data(upi_string)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#0072ff", back_color="white")
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        qr_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    except Exception:
        pass

    if request.method == 'POST':
        # Mark as paid after user confirms
        booking.paymode = 'UPI'
        booking.payst = 1
        booking.status = 0  # Reset slot to free
        booking.save(update_fields=['paymode', 'payst', 'status'])
        messages.success(request, f"UPI Payment confirmed for Slot {booking.slot}! Amount: Rs.{booking.amount}")
        return redirect('slot', sid=booking.station.uname)

    return render(request, 'upi_payment.html', {
        'booking': booking,
        'qr_base64': qr_base64,
        'upi_id': upi_id,
        'upi_string': upi_string,
    })


# ─── Google Maps View ─────────────────────────────────────────────────────────

def maps_view(request):
    if 'user' not in request.session:
        return redirect('user_login')

    stations = EVStation.objects.filter(status=1)
    stations_data = []
    for st in stations:
        stations_data.append({
            'name': st.name,
            'lat': st.lat,
            'lon': st.lon,
            'area': st.area,
            'city': st.city,
            'landmark': st.landmark,
            'uname': st.uname,
            'is_active': st.is_active,
            'numcharger': st.numcharger,
        })

    return render(request, 'maps.html', {
        'stations': stations_data,
        'uname': request.session['user'],
    })


# ─── Razorpay Payment ────────────────────────────────────────────────────────

def razorpay_payment(request, rid):
    if 'user' not in request.session:
        return redirect('user_login')

    booking = get_object_or_404(EVBooking, id=rid)

    if booking.chargest != 3:
        messages.error(request, "Charging not completed yet.")
        return redirect('slot', sid=booking.station.uname)

    try:
        import razorpay
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        amount_paise = int(float(booking.amount) * 100)
        order = client.order.create({
            'amount': amount_paise,
            'currency': 'INR',
            'payment_capture': 1,
            'notes': {'booking_id': str(booking.id)}
        })
        return render(request, 'razorpay_payment.html', {
            'booking': booking,
            'order': order,
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'amount_paise': amount_paise,
        })
    except Exception as e:
        messages.error(request, f"Payment gateway error: {str(e)}")
        return redirect('slot', sid=booking.station.uname)


@csrf_exempt
def razorpay_callback(request):
    if request.method == 'POST':
        try:
            import razorpay
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            params = {
                'razorpay_order_id': request.POST.get('razorpay_order_id'),
                'razorpay_payment_id': request.POST.get('razorpay_payment_id'),
                'razorpay_signature': request.POST.get('razorpay_signature'),
            }
            client.utility.verify_payment_signature(params)
            booking_id = request.POST.get('booking_id')
            booking = get_object_or_404(EVBooking, id=booking_id)
            booking.paymode = 'Razorpay'
            booking.payst = 2
            booking.save(update_fields=['paymode', 'payst'])
            messages.success(request, f"Payment successful! Amount: ₹{booking.amount}")
            return redirect('slot', sid=booking.station.uname)
        except Exception:
            messages.error(request, "Payment verification failed.")
            return redirect('user_home')
    return redirect('user_home')


def charging_wait(request, rid):
    if 'user' not in request.session:
        return redirect('user_login')
    booking = get_object_or_404(EVBooking, id=rid)
    # Block access if charging already completed
    if booking.chargest == 3:
        messages.success(request, "Charging completed! Please proceed to payment.")
        return redirect('payment', rid=booking.id)
    return render(request, 'charging_wait.html', {'booking': booking})
