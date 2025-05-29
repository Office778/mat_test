
import bcrypt
import datetime
import random
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customers
from .validators import is_valid_password
import json
from django.http import JsonResponse
import json
import datetime
import bcrypt
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Customers
from .models import Options



def generate_unique_customer_id():
    while True:
        new_id = str(random.randint(100000, 999999))
        if not Customers.objects.filter(cus_id=new_id).exists():
            return new_id


def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile').strip()
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        terms = request.POST.get('terms')

        if not terms:
            messages.error(request, "You must accept the terms.")
            return redirect('signup')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        if not is_valid_password(password):
            messages.error(request, "Weak password.")
            return render(request, 'signup.html')

        if not mobile.startswith('+91') or len(mobile) != 13:
            messages.error(request, "Please enter a valid mobile number starting with +91.")
            return render(request, 'signup.html')

        mobile_error = None
        email_error = None

        if Customers.objects.filter(cus_mobile=mobile).exists():
            mobile_error = "Mobile already registered."

        if Customers.objects.filter(cus_email=email).exists():
            email_error = "Email already registered."

        if mobile_error or email_error:
            return render(request, 'signup.html', {
                'mobile_error': mobile_error,
                'email_error': email_error,
                'name': name,
                'mobile': mobile,
                'email': email
            })


        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

        request.session['signup_data'] = {
            'name': name,
            'mobile': mobile,
            'email': email,
            'password': hashed_password,
        }
        return redirect('verify_otp')

    return render(request, 'signup.html')


from django.http import JsonResponse
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import Customers
import os, json
from django.utils import timezone
import datetime
from django.core.mail import send_mail
from django.templatetags.static import static
from email.mime.image import MIMEImage

def verify_otp_view(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            otp_verified = body.get('verified')

            if otp_verified:
                session_data = request.session.get('signup_data')
                if not session_data:
                    return JsonResponse({'error': 'Session expired.'}, status=400)

                customer_id = generate_unique_customer_id()

                customer = Customers(
                    cus_id=customer_id,
                    cus_name=session_data['name'],
                    cus_mobile=session_data['mobile'],
                    cus_email=session_data['email'],
                    cus_password=session_data['password'],
                    image_name='',
                    image_type='',
                    image_path='',
                    haroscope_file_path='',
                    profile_for='',
                    name_for='',
                    gender='',
                    religion='',
                    mothertongue='',
                    caste='',
                    city='',
                    marital_status='',
                    diet='',
                    height='',
                    qualification='',
                    work='',
                    discription='',
                    cus_credits=0,
                    trust_mark=0,
                    switch_1=0,
                    switch_2=0,
                    t_c='Yes',
                    last_login=timezone.now(),  # 🔥 fixed
                    trn_date=timezone.now(),    # 🔥 fixed
                )
                customer.save()

                # ✅ Send Welcome Email (HTML with PDFs)
                subject = "Welcome to Achudha Matrimony!"
                from_email = "no-reply@achudhamatrimony.in"
                to_email = session_data['email']

                text_content = f"""
Dear {session_data['name']},

Thank you for registering with Achudha Matrimony.
We are happy to have you on board and hope you find your perfect match soon!

ID: {customer_id}
Name: {session_data['name']}
Mobile: {session_data['mobile']}
Email: {session_data['email']}

Regards,
Achudha Matrimony Team
"""

                html_content = render_to_string('signup_success.html', {
                    'name': session_data['name'],
                    'customer_id': customer_id,
                    'mobile': session_data['mobile'],
                    'email': session_data['email'],
                })

                email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
                email.attach_alternative(html_content, "text/html")


                

                # Attach PDFs
                terms_pdf = r'C:\Users\achud\Desktop\mysql\mydata\dataapp\static\pdfs\Terms_and_conditions.pdf'
                privacy_pdf = r'C:\Users\achud\Desktop\mysql\mydata\dataapp\static\pdfs\Privacy_policy.pdf'

                if os.path.exists(terms_pdf):
                    email.attach_file(terms_pdf)

                if os.path.exists(privacy_pdf):
                    email.attach_file(privacy_pdf)


                email.send(fail_silently=False)
               

             # ✅ Notify Admin
                subject = "New Customer Signup - Achudha Matrimony!"
                text_content = (
                    f"A new customer has just signed up:\n\n"
                    f"Name: {session_data['name']}\n"
                    f"Mobile: {session_data['mobile']}\n"
                    f"Email: {session_data['email']}"
                )

                # Build the HTML content
                html_content = render_to_string('signup_success.html', {
                    'name': session_data['name'],
                    'mobile': session_data['mobile'],
                    'email': session_data['email'],
                })

                # Send the email
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=from_email,
                    to=["help@achudhamatrimony.in"]
                )
                email.attach_alternative(html_content, "text/html")

                terms_pdf = r'C:\Users\achud\Desktop\mysql\mydata\dataapp\static\pdfs\Terms_and_conditions.pdf'
                privacy_pdf = r'C:\Users\achud\Desktop\mysql\mydata\dataapp\static\pdfs\Privacy_policy.pdf'

                if os.path.exists(terms_pdf):
                    email.attach_file(terms_pdf)

                if os.path.exists(privacy_pdf):
                    email.attach_file(privacy_pdf)

                email.send(fail_silently=False)



                del request.session['signup_data']
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'OTP not verified.'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'GET':
        mobile = request.session.get('signup_data', {}).get('mobile', '')
        return render(request, 'verify_otp.html', {'mobile': mobile})

    return JsonResponse({'error': 'Invalid request method.'}, status=405)





from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
import bcrypt
from .models import Customers

def login_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        try:
            # Fetch the customer by their name
            customer = Customers.objects.get(cus_email=name)
        except Customers.DoesNotExist:
            messages.error(request, "Customer Email not found.")
            return redirect('login')

        # Check if the password matches using bcrypt
        if bcrypt.checkpw(password.encode('utf-8'), customer.cus_password.encode('utf-8')):
            # Save the customer_id in the session to persist login state
            request.session['customer_id'] = customer.id
            
            # Check if the user's profile is complete
            if not customer.profile_for:  # Assuming profile_for is a required field for a complete profile
                # If profile is incomplete, redirect to the profile update page
                messages.success(request, "Login successful! Please complete your profile.")
                return redirect('user_update_profile')
            else:
                # If profile is complete, redirect to the dashboard
                return redirect('user_dashboard')  # Redirect to the dashboard page

        else:
            messages.error(request, "Incorrect password.")
            return redirect('login')

    return render(request, 'login.html')



import random
import string
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Customers

def generate_captcha():
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    print(f"[DEBUG] Generated CAPTCHA: {code}")
    return code

def home(request):
    if 'customer_id' not in request.session:
        return redirect('login')

    customers = Customers.objects.all().order_by('-trn_date')
    name = customers.first().cus_name if customers else 'No Customers'

    if request.method == 'POST':
        # Check if enquiry form is submitted (no CAPTCHA required)
        if request.POST.get('mobile') and request.POST.get('enquiry'):
            user_name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            enquiry = request.POST.get('enquiry')
            user_email = request.POST.get('email')

            if not all([user_name, mobile, enquiry, user_email]):
                return render(request, 'home.html', {
                    'customers': customers,
                    'name': name,
                    'error': "Please fill all required fields.",
                    'captcha_code': request.session.get('captcha_code')
                })

            subject_customer = "Thank you for contacting Achudha Matrimony!"
            message_customer = f"""Hi {user_name},

Thank you for reaching out regarding '{enquiry}'.
We have received your enquiry and will contact you shortly.

Best Regards,
Achudha Matrimony Team
"""

            subject_company = "New Customer Enquiry Received"
            message_company = f"""New enquiry received:

Name: {user_name}
Mobile: {mobile}
Email: {user_email}
Enquiry Type: {enquiry}
"""

            try:
                EmailMessage(
                    subject=subject_customer,
                    body=message_customer,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[user_email]
                ).send()

                EmailMessage(
                    subject=subject_company,
                    body=message_company,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.EMAIL_HOST_USER],
                ).send()

                return redirect('success')

            except Exception as e:
                return render(request, 'home.html', {
                    'customers': customers,
                    'name': name,
                    'error': f"Email sending failed: {str(e)}",
                    'captcha_code': request.session.get('captcha_code')
                })

        # === Main form with CAPTCHA and optional file upload ===
        entered_captcha = request.POST.get('captcha_input')
        stored_captcha = request.session.get('captcha_code')

        if entered_captcha != stored_captcha:
            return render(request, 'home.html', {
                'customers': customers,
                'name': name,
                'error': 'Invalid captcha entered.',
                'captcha_code': stored_captcha
            })

        # Process main form
        user_name = request.POST.get('name')
        user_email = request.POST.get('email')
        category = request.POST.get('category')
        message = request.POST.get('message')
        uploaded_file = request.FILES.get('file')

        allowed_types = ['image/jpeg', 'image/png', 'application/pdf']
        max_size = 5 * 1024 * 1024

        if uploaded_file:
            if uploaded_file.content_type not in allowed_types:
                return render(request, 'home.html', {
                    'customers': customers,
                    'name': name,
                    'error': 'Invalid file type. Only JPEG, PNG, and PDF allowed.',
                    'captcha_code': stored_captcha
                })
            if uploaded_file.size > max_size:
                return render(request, 'home.html', {
                    'customers': customers,
                    'name': name,
                    'error': 'File size exceeds 5MB limit.',
                    'captcha_code': stored_captcha
                })

        subject = f"New {category} from {user_name}"
        body = f"Name: {user_name}\nEmail: {user_email}\nCategory: {category}\n\nMessage:\n{message}"

        email = EmailMessage(
            subject=subject,
            body=body,
            from_email='help@achudhamatrimony.in',
            to=['help@achudhamatrimony.in'],
            reply_to=[user_email]
        )

        if uploaded_file:
            uploaded_file.seek(0)  # 🔴 Add this line
            email.attach(uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)

        try:
            email.send()

            confirmation_email = EmailMessage(
                subject="Thank you for your message",
                body="We received your message and will respond shortly.",
                from_email='no-reply@achudhamatrimony.in',
                to=[user_email]
            )
            confirmation_email.send()

            request.session['captcha_code'] = generate_captcha()
            return redirect('success')

        except Exception as e:
            return render(request, 'home.html', {
                'customers': customers,
                'name': name,
                'error': f"An error occurred while sending the email: {str(e)}",
                'captcha_code': stored_captcha
            })

    # GET request – refresh CAPTCHA
    request.session['captcha_code'] = generate_captcha()

    return render(request, 'home.html', {
        'customers': customers,
        'name': name,
        'captcha_code': request.session['captcha_code']
    })

def logout_view(request):
    request.session.flush()
    return redirect('login')

import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from .models import Customers, Options

# Function to generate the desired file path for profile photos
def user_profile_photo(instance, filename):
    ext = filename.split('.')[-1]
    return f"user_profile_photos/{instance.cus_id}/{instance.cus_id}.{ext}"

def upload_profile_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        image_name = default_storage.save('profile_images/' + image_file.name, ContentFile(image_file.read()))
        image_url = default_storage.url(image_name)
        # Save the image URL to the user's profile or database
        return JsonResponse({'image_url': image_url})
    return JsonResponse({'error': 'No image uploaded'}, status=400)


from django.shortcuts import render, redirect
from django.conf import settings
import os
from .models import Customers, Options

import os
from django.conf import settings

def user_update_profile(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('login')

    try:
        customer = Customers.objects.get(id=customer_id)
    except Customers.DoesNotExist:
        return redirect('login')

    if request.method == "POST":
        # Update fields
        customer.name_for = request.POST.get('name_for', '')
        customer.profile_for = request.POST.get('profile_for', '')
        customer.gender = request.POST.get('gender', '')
        customer.religion = request.POST.get('religion', '')
        customer.caste = request.POST.get('caste', '')
        customer.qualification = request.POST.get('qualification', '')
        customer.mothertongue = request.POST.get('mothertongue', '')
        customer.height = request.POST.get('height', '')
        customer.city = request.POST.get('city', '')
        customer.dob = request.POST.get('dob', '')
        customer.work = request.POST.get('work', '')
        customer.discription = request.POST.get('discription', '')
        customer.marital_status = request.POST.get('marital_status', '')
        customer.diet = request.POST.get('diet', '')

        # Delete image logic
        if request.POST.get('delete_photo'):
            if customer.image_path:
                image_full_path = os.path.join(settings.MEDIA_ROOT, str(customer.image_path))
                if os.path.exists(image_full_path):
                    os.remove(image_full_path)
            customer.image_path = 'img/default-m.jpg'  # Set default image
            customer.image_name = ''
            customer.image_type = ''  # Adjust according to default image type

        # New image upload logic
        elif 'profile_image' in request.FILES:
            uploaded_file = request.FILES['profile_image']

            if uploaded_file.size > 5 * 1024 * 1024:
                messages.error(request, "Image size should not exceed 5MB.")
                return redirect('user_update_profile')

            ext = uploaded_file.name.split('.')[-1]
            image_filename = f"{customer.cus_id}.{ext}"
            folder_path = os.path.join('user_profile_photos', str(customer.cus_id))
            image_path = os.path.join(folder_path, image_filename)

            full_folder_path = os.path.join(settings.MEDIA_ROOT, folder_path)
            os.makedirs(full_folder_path, exist_ok=True)

            full_image_path = os.path.join(settings.MEDIA_ROOT, image_path)
            with open(full_image_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # ✅ Assign only if file uploaded
            customer.image_path = image_path
            customer.image_name = customer.cus_id
            customer.image_type = image_filename

        # If no image uploaded and no delete request, set default image
        if not request.FILES and not request.POST.get('delete_photo'):
            if not customer.image_path:  # Ensure no image path is set
                customer.image_path = 'img/default-m.jpg'
                customer.image_name = ''
                customer.image_type = ''  # Adjust according to default image type

        customer.save()
        return redirect('user_dashboard')

    religions = Options.objects.filter(category__iexact='Religion').values_list('name', flat=True)
    castes = Options.objects.filter(category__iexact='Inter-Religion').values_list('name', flat=True)
    qualifications = Options.objects.filter(category__iexact='Qualification').values_list('name', flat=True)
    mothertongue = Options.objects.filter(category__iexact='Mother Tongue').values_list('name', flat=True)
    heights = Options.objects.filter(category='Height').order_by('name').values_list('name', flat=True)
    print(customer.marital_status)

    return render(request, 'user_update_profile.html', {
        'religions': religions,
        'castes': castes,
        'qualifications': qualifications,
        'mothertongue': mothertongue,
        'heights': heights,
        'customer': customer,
        'profile_for': customer.profile_for,
        'dob': customer.dob,
        'marital_status':customer.marital_status,
       
        
    })



def user_dashboard(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('login')

    try:
        customer = Customers.objects.get(id=customer_id)
    except Customers.DoesNotExist:
        return redirect('login')
    
    # Get latest credit info
    latest_tran = HistoryTran.objects.filter(cus_id=customer.cus_id).order_by('-date').first()
    current_credits = latest_tran.credit if latest_tran else 0   

    # Profile completion analysis
    fields = [
        customer.image_name,
        customer.profile_for,
        customer.dob,
        customer.religion,
        customer.caste,
        customer.qualification,
        customer.height,
        customer.city,
        customer.mothertongue,
    ]

    filled = sum(1 for field in fields if field not in [None, '', 'null'])
    total = len(fields)
    profile_progress = int((filled / total) * 100) if total > 0 else 0

    # 🔍 Watchlist count (profiles I unlocked)
    watchlist_count = HistoryUnlock.objects.filter(cus_id=customer.cus_id).count()

    # 👁️‍🗨️ People who unlocked me
    unlocked_by_others_count = HistoryUnlock.objects.filter(cus_unlock_ids=customer.cus_id).count()

    return render(request, 'user_dashboard.html', {
        'customer': customer,
        'profile_progress': profile_progress,
        'current_credits': current_credits,
        'watchlist_count': watchlist_count,
        'unlocked_by_others_count': unlocked_by_others_count,
    })



from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Customers, Options, HistoryUnlock
from .utils import encode_id

def customer_list(request):
    # Filters
    location_filter = request.GET.get('city', '')
    gender_filter = request.GET.get('gender', '')
    religion_filter = request.GET.get('religion', '')
    mothertongue_filter = request.GET.get('mothertongue', '')

    # Dropdown options
    genders = Options.objects.filter(category__iexact='gender').values_list('name', flat=True)
    religions = Options.objects.filter(category__iexact='religion').values_list('name', flat=True)
    mothertongues = Options.objects.filter(category__iexact='mother tongue').values_list('name', flat=True)

    # Get current customer from session
    customer_id = request.session.get('customer_id')
    current_customer = None
    unlocked_ids = set()
    unlocked_me_ids = set()

    if customer_id:
        try:
            current_customer = Customers.objects.get(id=customer_id)
            # Get only unlocked profile cus_ids
            unlocked_ids = set(
                HistoryUnlock.objects.filter(cus_id=current_customer.cus_id)
                .values_list('cus_unlock_ids', flat=True)
            )

            unlocked_me_ids = set(
            HistoryUnlock.objects.filter(cus_unlock_ids=current_customer.cus_id)
            .values_list('cus_id', flat=True)
        )
            
        except Customers.DoesNotExist:
            pass

    # Base queryset
    customers = Customers.objects.all()

    # Apply filters
    if location_filter:
        customers = customers.filter(city=location_filter)
    if gender_filter:
        customers = customers.filter(gender=gender_filter)
    if religion_filter:
        customers = customers.filter(religion=religion_filter)
    if mothertongue_filter:
        customers = customers.filter(mothertongue=mothertongue_filter)

    # Annotate each customer with logic: show image only if unlocked or switch_2 == 0
    for customer in customers:
        customer.encoded_id = encode_id(customer.id)
        customer.show_image_to_viewer = (customer.switch_2 == 0) or (str(customer.cus_id) in unlocked_ids)
        customer.is_watchlisted = str(customer.cus_id) in unlocked_ids  # ✅ New
        customer.unlocked_me = str(customer.cus_id) in unlocked_me_ids

    # Pagination
    paginator = Paginator(customers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'customer_list.html', {
        'customers': page_obj,
        'page_obj': page_obj,
        'gender_filter': gender_filter,
        'religion_filter': religion_filter,
        'mothertongue_filter': mothertongue_filter,
        'genders': genders,
        'religions': religions,
        'mothertongues': mothertongues,
        'current_customer': current_customer,
        'no_profiles_message': "No profiles found matching your criteria." if not customers.exists() else ""
    })

from django.shortcuts import redirect
from .models import Customers

def toggle_switch_2(request):
    if request.method == "POST":
        customer_id = request.session.get('customer_id')
        if not customer_id:
            return redirect('login')

        try:
            customer = Customers.objects.get(id=customer_id)
            customer.switch_2 = 1 if 'switch_2' in request.POST else 0
            customer.save(update_fields=['switch_2'])
        except Customers.DoesNotExist:
            pass

    return redirect('user_dashboard')  # Adjust to your dashboard URL name

import os, base64, uuid
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.conf import settings
from .models import Customers

def upload_cropped_image(request):
    if request.method == "POST":
        customer_id = request.session.get('customer_id')
        if not customer_id:
            return JsonResponse({'error': 'Not authenticated'})

        try:
            customer = Customers.objects.get(id=customer_id)
        except Customers.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'})

        base64_image = request.POST.get('image')
        if not base64_image:
            return JsonResponse({'error': 'No image data'})

        try:
            format, imgstr = base64_image.split(';base64,')
            ext = format.split('/')[-1]
            filename = f"{customer.cus_id}.{ext}"  # Use customer ID as filename
            folder_path = os.path.join('user_profile_photos', str(customer.cus_id))
            image_path = os.path.join(folder_path, filename).replace('\\', '/')

            full_folder_path = os.path.join(settings.MEDIA_ROOT, folder_path)
            os.makedirs(full_folder_path, exist_ok=True)

            full_image_path = os.path.join(settings.MEDIA_ROOT, image_path)
            with open(full_image_path, 'wb') as f:
                f.write(base64.b64decode(imgstr))

            # Save path info to database
            customer.image_name = customer.cus_id
            customer.image_type = filename
            customer.image_path = image_path
            customer.save()

            return JsonResponse({'message': 'Image uploaded successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Invalid request method'})


# plan_views
from .models import Plan

def plans_view(request):
    plans = Plan.objects.all()
    return render(request, 'plans.html', {'plans': plans})

# individual-customer-page view
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .models import Customers, HistoryTran, HistoryUnlock
from .utils import decode_id


def mask_mobile(mobile):
    if mobile and len(mobile) > 4:
        return mobile[:4] + "xxxxxx"
    return mobile


def mask_email(email):
    if email and "@" in email:
        local, domain = email.split("@", 1)
        return "xxxxx@" + domain
    return email


def customer_detail(request, encoded_id):
    # Get logged-in user (Customer B)
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('login')

    try:
        session_customer = Customers.objects.get(id=customer_id)
    except Customers.DoesNotExist:
        return redirect('login')

    # Decode the profile being viewed (Customer A)
    try:
        decoded_id = decode_id(encoded_id)
    except ValueError:
        return render(request, '404.html', {'error': 'Invalid profile ID.'}, status=404)

    viewed_customer = get_object_or_404(Customers, id=decoded_id)

    # Check if profile is already unlocked or is own profile
    unlocked = session_customer.id == viewed_customer.id or HistoryUnlock.objects.filter(
        cus_id=str(session_customer.cus_id),
        cus_unlock_ids=str(viewed_customer.cus_id)
    ).exists()

    # Handle unlock POST request
    if request.method == 'POST' and not unlocked:
        # Fetch latest credit transaction
        latest_tran = HistoryTran.objects.filter(cus_id=session_customer.cus_id).order_by('-date').first()
        current_credits = latest_tran.credit if latest_tran else 0

        if current_credits > 0:
            # Deduct 1 credit
            latest_tran.credit = current_credits - 1
            latest_tran.save()

            # Record unlock action
            HistoryUnlock.objects.create(
                date=timezone.now(),
                cus_id=str(session_customer.cus_id),
                cus_unlock_ids=str(viewed_customer.cus_id)
            )
            unlocked = True
        else:
            # No credits - show insufficient credits page
            return render(request, 'insufficient_credits.html')

    # Refresh latest credits after any deduction
    latest_tran = HistoryTran.objects.filter(cus_id=session_customer.cus_id).order_by('-date').first()
    current_credits = latest_tran.credit if latest_tran else 0

    # Show image only if profile is public (switch_2 == 0) or unlocked
    show_image_to_viewer = viewed_customer.switch_2 == 0 or unlocked

    # Show full contact info only if unlocked, else masked
    if unlocked:
        mobile_to_show = viewed_customer.cus_mobile
        email_to_show = viewed_customer.cus_email
    else:
        mobile_to_show = mask_mobile(viewed_customer.cus_mobile)
        email_to_show = mask_email(viewed_customer.cus_email)

    return render(request, 'customer_detail.html', {
        'customer': viewed_customer,
        'encoded_id': encoded_id,
        'current_credits': current_credits,
        'is_unlocked': unlocked,
        'show_image_to_viewer': show_image_to_viewer,
        'mobile_to_show': mobile_to_show,
        'email_to_show': email_to_show,
    })

from django.shortcuts import render

def insufficient_credits_view(request):
    return render(request, 'insufficient_credits.html')

def near_me_profiles(request):
    if 'customer_id' not in request.session:
        return redirect('login')
    
    customer_id = request.session['customer_id']
    
    try:
        customer = Customers.objects.get(id=customer_id)
        user_city = customer.city
    except Customers.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('login')
    
    nearby_profiles = Customers.objects.filter(city__startswith=user_city[:5]).exclude(id=customer_id)[:4]

    # Add encoded ID
    for profile in nearby_profiles:
        profile.encoded_id = encode_id(profile.id)

    return render(request, 'near_me_profiles.html', {'profiles': nearby_profiles})


from .utils import decode_id  
def profile_detail(request, cus_id):# or import it from wherever you placed it

    decoded_id = decode_id(cus_id)
    if not decoded_id:
        return render(request, 'profile_detail.html', {'error': 'Invalid profile ID'})
    
    try:
        profile = Customers.objects.get(id=decoded_id)
    except Customers.DoesNotExist:
        profile = None

    return render(request, 'profile_detail.html', {'profile': profile})



from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings

def email_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        enquiry = request.POST.get('enquiry')
        customer_email = request.POST.get('email')

        if not all([name, mobile, enquiry, customer_email]):
            return render(request, 'home.html', {'error': "Please fill all fields."})

        customer_email = customer_email.strip()

        # Email to Customer
        subject_customer = "Thank you for contacting Achudha Matrimony!"
        message_customer = f"""Hi {name},

Thank you for reaching out regarding '{enquiry}'.
We have received your enquiry and will contact you shortly.

Best Regards,
Achudha Matrimony Team
"""

        # Email to Company (yourself)
        subject_company = "New Customer Enquiry Received"
        message_company = f"""New enquiry received:

Name: {name}
Mobile: {mobile}
Email: {customer_email}
Enquiry Type: {enquiry}
"""

        try:
            # 1. Send thank you email to customer
            customer_email_message = EmailMessage(
                subject=subject_customer,
                body=message_customer,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[customer_email],
            )
            customer_email_message.send(fail_silently=False)

            # 2. Send enquiry details to your company email
            company_email_message = EmailMessage(
                subject=subject_company,
                body=message_company,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.EMAIL_HOST_USER],
            )
            company_email_message.send(fail_silently=False)

            return redirect('success')
        except Exception as e:
            return render(request, 'home.html', {'error': f"Email sending failed: {str(e)}"})

    return render(request, 'home.html')

def success(request):
    return render(request, 'success.html')

# login_with_otp section

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import Customers
from urllib.parse import unquote
import json


def login_with_otp(request):
    """
    Render the OTP login form.
    """
    return render(request, 'login_with_otp.html')


def verify_otp_login(request):
    """
    Verifies the OTP-based login.
    Checks if the mobile number exists and logs the user in.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mobile = data.get('mobile', '').strip()

            # Normalize mobile number to start with +91
            if not mobile.startswith('+91'):
                mobile = '+91' + mobile

            print("Incoming verified mobile:", mobile)

            # Check if mobile exists in the Customers table
            customer = Customers.objects.filter(cus_mobile=mobile).first()

            if customer:
                # Use mobile number as username
                user, created = User.objects.get_or_create(username=customer.cus_mobile)

                # Ensure user can't login with a password
                if created:
                    user.set_unusable_password()
                    user.save()

                # Perform login
                login(request, user)

                # Store customer ID in session
                request.session['customer_id'] = customer.id

                # Redirect to dashboard or next URL
                next_url = request.GET.get('next', '/dashboard/')
                return JsonResponse({
                    'success': True,
                    'redirect': unquote(next_url)
                })

            return JsonResponse({
                'success': False,
                'message': 'Mobile number not registered!'
            })

        except Exception as e:
            print("Error in verify_otp_login:", e)
            return JsonResponse({'success': False, 'message': 'Server error'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})



from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def check_mobile_existence(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mobile = data.get('mobile', '').strip()
            if Customers.objects.filter(cus_mobile=mobile).exists():
                return JsonResponse({'exists': True})
            return JsonResponse({'exists': False})
        except Exception as e:
            print("Error in check_mobile_existence:", e)
            return JsonResponse({'exists': False})
    return JsonResponse({'exists': False})


# // password-reset




# views.py

from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import Customers
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def reset_verify_otp_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        mobile = data.get('mobile', '').strip()

        if not mobile:
            return JsonResponse({'success': False, 'message': 'Mobile number is required.'})

        if not mobile.startswith('+91'):
            mobile = '+91' + mobile  # Ensure the mobile number has the country code

        customer = Customers.objects.filter(cus_mobile=mobile).first()

        if customer:
            request.session['password_reset_allowed'] = True
            request.session['reset_mobile'] = customer.cus_mobile  # Store mobile in session
            return JsonResponse({'success': True, 'redirect_url': '/password_reset/'})
        else:
            return JsonResponse({'success': False, 'message': 'Mobile number not registered!'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})



import bcrypt
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Customers

def custom_password_reset(request):
    # Ensure the user has verified OTP and the mobile is in session
    if not request.session.get('password_reset_allowed') or not request.session.get('reset_mobile'):
        messages.error(request, "Please verify OTP before resetting password.")
        return redirect('reset_verify_otp_login')  # Redirect to OTP verification if not allowed

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        
        if not new_password:
            messages.error(request, "Please enter the new password.")
            return redirect('password_reset')  # Redirect back to password reset page if no password

        mobile = request.session.get('reset_mobile')  # Retrieve mobile number from session
        customer = Customers.objects.filter(cus_mobile=mobile).first()

        if customer:
            # Hash and save the new password
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            customer.cus_password = hashed_password
            customer.save()

            # Clear session values
            request.session.pop('password_reset_allowed', None)
            request.session.pop('reset_mobile', None)

            messages.success(request, "Your password has been updated successfully.")
            return redirect('login')  # Redirect to login page after successful reset

    return render(request, 'password_reset.html')  # Render password reset page template



def reset_password_otp(request):
    return render(request, 'password_reset_otp.html')  # Template where the user inputs their mobile number



from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
from .models import Plan, Customers
import pytz
from django.utils import timezone

def payment_page(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)

    plan_name = plan.plan.lower()
    qr_image = None
    if "basic" in plan_name:
        qr_image = "images/payments/basic.jpg"
    elif "advanced" in plan_name:
        qr_image = "images/payments/advanced1.jpg"
    elif "ultra" in plan_name:
        qr_image = "images/payments/ultra1.jpg"

    if request.method == "POST":
        utr = request.POST.get('utr')

        if not utr:
            return HttpResponse("UTR number is required.", status=400)

        customer_id = request.session.get('customer_id')
        if not customer_id:
            return HttpResponse("Customer not found. Please log in.", status=404)

        try:
            customer = Customers.objects.get(id=customer_id)
        except Customers.DoesNotExist:
            return HttpResponse("Customer not found for the current session.", status=404)

        # ✅ Correct Token ID format (YYYYMMDD + customerID)
        india_timezone = pytz.timezone('Asia/Kolkata')
        now_in_ist = timezone.now().astimezone(india_timezone)

# Generate token ID with date, 12-hour format time, milliseconds, and customer ID
        token_id = now_in_ist.strftime("%Y%m%d%I%M%S%f")[:-3] + str(customer.cus_id)

        context = {
            'customer_name': customer.cus_name,
            'customer_email': customer.cus_email,
            'token_id': token_id,
            'plan_name': plan.plan,
            'credits': plan.credit,
            'amount': plan.amt,
            'utr': utr,
        }

        html_message = render_to_string('customer_payment_email.html', context)

        # ✅ Send confirmation email to customer (ONCE, no reply)
        customer_email = EmailMessage(
            subject="Test - Payment Confirmation - Achudha Matrimony - {token_id}",
            body=html_message,
            from_email='no-reply@achudhamatrimony.in',
            to=[customer.cus_email],
            headers={
                'Message-ID': f"<{token_id}@achudhamatrimony.in>",  # Prevent threading
                'In-Reply-To': '',
                'References': '',
            }
        )
        customer_email.content_subtype = "html"
        customer_email.send()

        # ✅ Send company notification (ONCE)
        company_email = EmailMessage(
            subject=f"Test - New Plan Purchase - {customer.cus_email}",
            body=html_message,
            from_email='no-reply@achudhamatrimony.in',
            to=['help@achudhamatrimony.in']
        )
        company_email.content_subtype = "html"
        company_email.send()

        messages.success(request, "Payment submitted successfully. Confirmation email sent.")
        return redirect('payment-success')

    context = {
        'plan': plan,
        'qr_image': qr_image,
    }
    return render(request, 'paymentpage.html', context)


def payment_success(request):
    return render(request, 'payment_success.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import HistoryTran, Customers

def my_plan(request):
    customer_id = request.session.get('customer_id')
    print("Session customer_id:", customer_id)

    if not customer_id:
        messages.warning(request, "Please log in to view your plan.")
        return redirect('login')

    try:
        # Get the customer instance
        customer = Customers.objects.get(id=customer_id)

        # Now use the real cus_id to filter transactions
        transactions = HistoryTran.objects.filter(cus_id=customer.cus_id).order_by('-date')
        print(f"Found {transactions.count()} transactions for customer.cus_id: {customer.cus_id}")

        context = {
            'transactions': transactions,
        }
        return render(request, 'myplan.html', context)

    except Customers.DoesNotExist:
        messages.error(request, "Customer not found.")
        return redirect('login')
    

from django.shortcuts import render
from .models import Customers, HistoryUnlock
from .utils import encode_id  # ✅ Make sure this is correctly imported

def people_unlock(request):
    cus_id = request.session.get('customer_id')
    print(f"Customer ID from session: {cus_id}")

    if not cus_id:
        print("Customer not logged in.")
        return render(request, 'people_unlock.html', {
            'unlocked_data': [],
            'error': 'Please log in to view your people-unlock.'
        })

    try:
        session_customer = Customers.objects.get(id=cus_id)
        print(f"Session customer found: {session_customer.cus_name}")
    except Customers.DoesNotExist:
        print(f"Customer with ID {cus_id} not found.")
        return render(request, 'people_unlock.html', {
            'unlocked_data': [],
            'error': 'Customer not found.'
        })

    # 🔄 Find who unlocked ME
    unlock_entries = HistoryUnlock.objects.filter(cus_unlock_ids=session_customer.cus_id)
    print(f"Total entries where my profile was unlocked: {unlock_entries.count()}")

    unlocked_data = []
    for entry in unlock_entries:
        try:
            unlocker = Customers.objects.get(cus_id=entry.cus_id)
            unlocked_data.append({
                'unlocker': unlocker,
                'unlock_date': entry.date,
                'encoded_id': encode_id(unlocker.id),  # ✅ Add encoded ID
            })
            print(f"{unlocker.cus_name} unlocked your profile on {entry.date}")
        except Customers.DoesNotExist:
            print(f"Unlocking customer with ID {entry.cus_id} not found.")
            continue

    return render(request, 'people_unlock.html', {
        'unlocked_data': unlocked_data,
        'customer_name': session_customer.cus_name,
        'error': None if unlocked_data else 'No one has unlocked your profile yet.'
    })


from django.shortcuts import render
from .models import Customers, HistoryUnlock
from .utils import encode_id  # ✅ Import your encoder

def watchlist_view(request):
    cus_id = request.session.get('customer_id')
    print(f"Customer ID from session: {cus_id}")

    if not cus_id:
        print("Customer not logged in.")
        return render(request, 'watchlist.html', {
            'unlocked_data': [],
            'error': 'Please log in to view your watchlist.'
        })

    try:
        session_customer = Customers.objects.get(id=cus_id)
        print(f"Session customer found: {session_customer.cus_name}")
    except Customers.DoesNotExist:
        print(f"Customer with ID {cus_id} not found.")
        return render(request, 'watchlist.html', {
            'unlocked_data': [],
            'error': 'Customer not found.'
        })

    unlock_entries = HistoryUnlock.objects.filter(cus_id=session_customer.cus_id)
    print(f"Total unlock entries found: {unlock_entries.count()}")

    unlocked_data = []
    for entry in unlock_entries:
        print(f"Processing unlock entry: {entry.cus_unlock_ids}")
        try:
            unlocked_profile = Customers.objects.get(cus_id=entry.cus_unlock_ids)
            unlock_cus = Customers.objects.get(cus_id=entry.cus_id)

            unlocked_data.append({
                'unlocked_profile': unlocked_profile,
                'unlock_date': entry.date,
                'unlock_cus': unlock_cus,
                'encoded_id': encode_id(unlocked_profile.id),  # ✅ Add encoded ID
            })
            print(f"Unlocked profile: {unlocked_profile.cus_name}")
        except Customers.DoesNotExist:
            print(f"Profile with ID {entry.cus_unlock_ids} does not exist.")
            continue

    print(f"Unlocked data to display: {len(unlocked_data)} profiles.")
    return render(request, 'watchlist.html', {
        'unlocked_data': unlocked_data,
        'customer_name': session_customer.cus_name,
        'error': None if unlocked_data else 'No profiles unlocked yet.'
    })


from django.shortcuts import render
from .models import Blog

def blog_list(request):
    blogs = Blog.objects.all().order_by('-date')
    return render(request, 'blog_list.html', {'blogs': blogs})


# views.py
from django.shortcuts import render, get_object_or_404
from .models import Blog

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'blog_detail.html', {'blog': blog})


import os
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.timezone import now
from .models import Customers

def user_horoscope_path(cus_id):
    return f"user_profile_photos/{cus_id}/Horoscope.pdf"

def upload_horoscope(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        messages.error(request, "Customer not identified. Please log in again.")
        return redirect('login')

    try:
        customer = Customers.objects.get(pk=customer_id)
    except Customers.DoesNotExist:
        messages.error(request, "Customer record not found.")
        return redirect('login')
    
    existing_horoscope = customer.haroscope_file_path if customer.haroscope_file_path else None

    if request.method == 'POST':
        file = request.FILES.get('horoscope_file')

        if not file:
            messages.error(request, "Please select a file to upload.")
            return redirect('upload_horoscope')

        if file.size > 5 * 1024 * 1024:
            messages.error(request, "File size must be under 5MB.")
            return redirect('upload_horoscope')

        # Save file
        relative_path = user_horoscope_path(customer.cus_id)
        full_path = os.path.join(settings.MEDIA_ROOT, relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        customer.haroscope_file_path = relative_path
        customer.save()

        # Render email HTML template
        email_body = render_to_string('horoscope_email.html', {
            'customer_id': customer.cus_id,
            'customer_name': customer.cus_name,
            'customer_mobile': customer.cus_mobile,
            'customer_email': customer.cus_email,
            'current_year': now().year,
        })

        # Send HTML email (without file attachment)
        email = EmailMessage(
            subject=f"Horoscope Uploaded - {customer.cus_name}",
            body=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=['help@achudhamatrimony.in']
        )
        email.content_subtype = 'html'
        email.send()

        return redirect('upload_success')

    return render(request, 'upload_horoscope.html',{
        'existing_horoscope': existing_horoscope,
        'MEDIA_URL': settings.MEDIA_URL,

    })


def upload_success(request):
    return render(request, 'upload_success.html')


import os
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.timezone import now
from .models import Customers

def user_trust_path(cus_id):
    return f"user_profile_photos/{cus_id}/Trustmark.pdf"

def upload_trustmark(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        messages.error(request, "Customer not identified. Please log in again.")
        return redirect('login')

    try:
        customer = Customers.objects.get(pk=customer_id)
    except Customers.DoesNotExist:
        messages.error(request, "Customer record not found.")
        return redirect('login')

    existing_trustmark = customer.trust_file_path

    if request.method == 'POST':
        file = request.FILES.get('trust_file')

        if not file:
            messages.error(request, "Please select a file to upload.")
            return redirect('upload_trustmark')

        if file.size > 5 * 1024 * 1024:
            messages.error(request, "File size must be under 5MB.")
            return redirect('upload_trustmark')

        # Save file
        relative_path = user_trust_path(customer.cus_id)
        full_path = os.path.join(settings.MEDIA_ROOT, relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Update DB
        customer.trust_file_path = relative_path
        customer.save()

        # Send email
        email_body = render_to_string('Trustmark_email.html', {
            'customer_id': customer.cus_id,
            'customer_name': customer.cus_name,
            'customer_mobile': customer.cus_mobile,
            'customer_email': customer.cus_email,
            'current_year': now().year,
        })

        email = EmailMessage(
            subject=f"Trustmark Uploaded - {customer.cus_name}",
            body=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=['help@achudhamatrimony.in']
        )
        email.content_subtype = 'html'
        email.send()

        return redirect('upload_trust_success')

    return render(request, 'upload_trustmark.html', {
        'existing_trustmark': existing_trustmark,
        'MEDIA_URL': settings.MEDIA_URL,
    })

def upload_trust_success(request):
    return render(request, 'upload_trust_success.html')
