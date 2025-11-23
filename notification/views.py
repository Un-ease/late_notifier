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
def send_late_email(delay_time, reason, custom_time=None):
    """Send late arrival email"""
    actual_delay = custom_time if custom_time else delay_time
    
    subject = f"Late Arrival Notification - {actual_delay} minutes"
    
    context = {
        'delay_time': actual_delay,
        'reason': reason or 'No reason provided',
    }
    
    html_message = render_to_string('notification/email_template.html', context)
    plain_message = f"""
    Late Arrival Notification
    
    I will be approximately {actual_delay} minutes late today.
    Reason: {reason or 'No reason provided'}
    
    I apologize for any inconvenience and will update you if the situation changes.
    """
    
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
        form = LateNotificationForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)
            
            # Send email
            try:
                send_late_email(
                    notification.delay_time,
                    notification.reason,
                    notification.custom_time
                )
                notification.email_sent = True
                notification.save()
                
                messages.success(request, 'Late notification sent successfully!')
                return redirect('success')
                
            except Exception as e:
                messages.error(request, f'Error sending email: {str(e)}')
    else:
        form = LateNotificationForm()
    
    return render(request, 'notification/index.html', {'form': form})

@login_required
def success(request):
    return render(request, 'notification/success.html')