from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib import messages
from django.template.loader import render_to_string
from .forms import LateNotificationForm
from .models import LateNotification
import json

@login_required
def send_late_email(delay_time, reason, custom_time=None, username=None):
    """Send late arrival email"""
    from django.conf import settings
    from django.core.mail import EmailMessage
    from django.template.loader import render_to_string
    
    actual_delay = custom_time if custom_time else delay_time
    
    # Use the username or fallback to email user
    user_display = username if username else "User"
    
    subject = f"Late Arrival Notification - {actual_delay} minutes"
    
    context = {
        'delay_time': actual_delay,
        'reason': reason or 'No reason provided',
        'user_email': user_display  # Simple fix - just use username
    }
    
    html_message = render_to_string('notification/email_template.html', context)
    
    email = EmailMessage(
        subject=subject,
        body=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.MANAGER_EMAIL],
        cc=settings.CC_EMAILS,
    )
    email.content_subtype = "html"
    
    return email.send()

@login_required
def index(request):
    if request.method == 'POST':
        delay_time = request.POST.get('delay_time')
        custom_time = request.POST.get('custom_time')
        reason = request.POST.get('reason', '')
        
        # Validate required fields
        if not delay_time:
            messages.error(request, 'Please select a delay time')
            return render(request, 'notification/index.html')
        
        if delay_time == '0' and not custom_time:
            messages.error(request, 'Please enter a custom delay time')
            return render(request, 'notification/index.html')
        
        try:
            # SIMPLE FIX: Just pass the username
            send_late_email(delay_time, reason, custom_time, request.user.username)
            messages.success(request, 'Late notification sent successfully!')
            return redirect('notification:success')
            
        except Exception as e:
            messages.error(request, f'Error sending email: {e}')
    
    return render(request, 'notification/index.html')
    
@login_required
def success(request):
    return render(request, 'notification/success.html')