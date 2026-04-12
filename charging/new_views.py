
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
    upi_id = "naveenceo637@okicici"  # Replace with your UPI ID
    upi_name = "EV Charge Hub"
    amount = booking.amount
    note = f"EV Booking {booking.id}"
    upi_string = f"upi://pay?pa={upi_id}&pn={urllib.parse.quote(upi_name)}&am={amount}&cu=INR&tn={urllib.parse.quote(note)}"

    qr_base64 = ""
    if QRCODE_AVAILABLE:
        qr = qrcode.QRCode(version=1, box_size=8, border=4)
        qr.add_data(upi_string)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#0072ff", back_color="white")
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        qr_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    if request.method == 'POST':
        # Mark as paid after user confirms
        booking.paymode = 'UPI'
        booking.payst = 1
        booking.save(update_fields=['paymode', 'payst'])
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
