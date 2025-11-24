import threading
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib import messages
from django.template.loader import render_to_string
from .models import LateNotification

def send_late_email_async(delay_time, reason, custom_time=None):
    """Send email in background thread"""
    def send():
        try:
            actual_delay = custom_time if custom_time else delay_time
            
            subject = f"Late Arrival Notification - {actual_delay} minutes"
            
            context = {
                'delay_time': actual_delay,
                'reason': reason or 'No reason provided',
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
            email.send()
        except Exception as e:
            print(f"Email sending failed: {e}")
    
    # Run in background thread
    thread = threading.Thread(target=send)
    thread.start()

@login_required
def index(request):
    if request.method == 'POST':
        delay_time = request.POST.get('delay_time')
        custom_time = request.POST.get('custom_time')
        reason = request.POST.get('reason', '')
        
        if not delay_time:
            messages.error(request, 'Please select a delay time')
            return render(request, 'notification/index.html')
        
        delay_time = int(delay_time)
        custom_time = int(custom_time) if custom_time else None
        
        if delay_time == 0 and not custom_time:
            messages.error(request, 'Please enter a custom delay time')
            return render(request, 'notification/index.html')
        
        try:
            # Save to database first
            notification = LateNotification.objects.create(
                delay_time=delay_time,
                custom_time=custom_time,
                reason=reason,
                email_sent=False
            )
            
            # Send email in background (non-blocking)
            send_late_email_async(delay_time, reason, custom_time)
            
            # Mark as sent immediately (you could update this later with a callback)
            notification.email_sent = True
            notification.save()
            
            messages.success(request, 'Late notification is being sent!')
            return redirect('notification:success')
            
        except Exception as e:
            messages.error(request, f'Error: {e}')
    
    return render(request, 'notification/index.html')