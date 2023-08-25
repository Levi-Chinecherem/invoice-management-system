from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, JsonResponse 
from .models import Student, Payment, Invoice, PaymentCategory
from django.shortcuts import render, redirect, get_object_or_404
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import Spacer, SimpleDocTemplate, Paragraph, Image as PLImage
from PIL import Image as PILImage
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
import qrcode
from io import BytesIO
from weasyprint import HTML
from django.template.loader import render_to_string
import uuid
import os
from django.conf import settings
from django.utils import timezone
from django.core.files.base import ContentFile

def is_staff(user):
    return user.is_authenticated and user.is_staff

def home(request):
    return render(request, 'payments/home.html')

@login_required
def profile(request):
    user = request.user
    try:
        student = Student.objects.get(user=user)
        is_student = True
    except Student.DoesNotExist:
        student = None
        is_student = False

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        department = request.POST.get('department')
        level = request.POST.get('level')
        school = request.POST.get('school')
        sex = request.POST.get('sex')

        if is_student:
            # Update existing student details
            student.full_name = full_name
            student.department = department
            student.level = level
            student.school = school
            student.sex = sex
            student.save()

            messages.success(request, 'Profile updated successfully!')
        else:
            # Create a new Student record
            student = Student.objects.create(
                user=user,
                full_name=full_name,
                department=department,
                level=level,
                school=school,
                sex=sex
            )

            messages.success(request, 'Profile created successfully!')

        return redirect('profile')

    context = {'student': student, 'is_student': is_student}
    return render(request, 'payments/profile.html', context)

@login_required
def payment(request):
    if request.method == 'POST':
        payment_category_id = request.POST.get('payment_category')
        amount = request.POST.get('amount')

        payment_category = PaymentCategory.objects.get(id=payment_category_id)
        student = request.user.student

        payment = Payment.objects.create(
            student=student,
            payment_category=payment_category,
            amount=amount,
            approved=True  # Set default approval status
        )

        # Generate invoice as a PDF string
        invoice_pdf = generate_invoice_pdf(payment)
        # Save the invoice PDF string in the Invoice model
        invoice = Invoice(payment=payment, pdf=invoice_pdf)
        invoice.save()

        messages.success(request, 'Payment submitted successfully!')
        return redirect('payment')

    categories = PaymentCategory.objects.all()
    payments = Payment.objects.filter(student=request.user.student)

    context = {'categories': categories, 'payments': payments}
    return render(request, 'payments/payment.html', context)

def view_invoices(request):
    invoices = Invoice.objects.all()
    context = {'invoices': invoices}
    return render(request, 'payments/invoices.html', context)

# views.py
def view_invoice(request, payment_id):
    invoice = get_object_or_404(Invoice, payment__id=payment_id)
    context = {'invoice': invoice}
    return render(request, 'payments/view_invoice.html', context)

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    img_stream = BytesIO()
    img.save(img_stream, format='PNG')
    qr_code_bytes = img_stream.getvalue()

    return qr_code_bytes

def generate_invoice_pdf(payment):
    student = payment.student

    # Generate QR Code
    qr_code_data = f"Student: {student.full_name}\nDepartment: {student.department}\nLevel: {student.level}\nSchool: {student.school}\nDate: {timezone.now()}\nApproval: {'Approved' if payment.approved else 'Not Approved'}\nPayment ID: {payment.id}\nAmount: {payment.amount}"
    qr_code_img = generate_qr_code(qr_code_data)

    # Create the required folders if they don't exist
    media_root = settings.MEDIA_ROOT
    invoice_folder = os.path.join(media_root, 'invoice')
    qrcode_folder = os.path.join(media_root, 'qrcode')

    if not os.path.exists(invoice_folder):
        os.makedirs(invoice_folder)

    if not os.path.exists(qrcode_folder):
        os.makedirs(qrcode_folder)

    # Generate a unique payment_id for the Invoice
    invoice_payment_id = str(uuid.uuid4())

    # Generate a unique filename for the QRCode
    qrcode_filename = f'qrcode_{student.full_name}_{invoice_payment_id}.png'

    # Create a ContentFile from the image data
    qrcode_content = ContentFile(qr_code_img)

    # Set the created_at field manually
    created_at = timezone.now()

    # Generate a unique filename for the PDF
    pdf_filename = f'invoice_{student.full_name}_{invoice_payment_id}.pdf'
    pdf_path = os.path.join(invoice_folder, pdf_filename)

    # Generate PDF and append QR code image
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    elements = []


    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    elements = []

    # Title
    elements.append(Paragraph("KENULE BEESON SARO-WIWA POLYTECHNIC, BORI", getSampleStyleSheet()["Title"]))
    elements.append(Spacer(1, 12))

    # Payment Category
    elements.append(Paragraph("Payment Category: {}".format(payment.payment_category.title), getSampleStyleSheet()["Normal"]))
    elements.append(Spacer(1, 12))

    # Full Name Category
    elements.append(Paragraph("Full Name: {}".format(student.full_name), getSampleStyleSheet()["Normal"]))
    elements.append(Spacer(1, 12))

    # Department Category
    elements.append(Paragraph("Department: {}".format(student.department), getSampleStyleSheet()["Normal"]))
    elements.append(Spacer(1, 12))

    # Level Category
    elements.append(Paragraph("Level: {}".format(student.level), getSampleStyleSheet()["Normal"]))
    elements.append(Spacer(1, 12))

    # School Category
    elements.append(Paragraph("School: {}".format(student.school), getSampleStyleSheet()["Normal"]))
    elements.append(Spacer(1, 12))

    # Sex Category
    elements.append(Paragraph("Sex: {}".format(student.sex), getSampleStyleSheet()["Normal"]))
    elements.append(Spacer(1, 12))

    # Payment Details
    payment_info = "Payment Details:\nAmount: {}".format(payment.amount)
    elements.append(Paragraph(payment_info, getSampleStyleSheet()["Normal"]))
    elements.append(Spacer(1, 12))

    # Additional Payment Information
    additional_info = "Date of Payment: {}\nApproval Status: {}".format(
        timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
        "Approved" if payment.approved else "Not Approved"
    )
    elements.append(Paragraph(additional_info, getSampleStyleSheet()["Normal"]))

     # Append the QRCode image to the elements list
    elements.append(PLImage(qrcode_content, width=100, height=100))

    # Save the PDF
    doc.build(elements)
    buffer.seek(0)
    with open(pdf_path, 'wb') as pdf_file:
        pdf_file.write(buffer.read())

    # Create and save the Invoice instance
    invoice = Invoice(payment=payment)
    invoice.pdf.name = pdf_filename
    invoice.qrcode.save(qrcode_filename, qrcode_content)  # Save image data directly to the field
    invoice.created_at = created_at
    invoice.save()

    return pdf_path




from django.shortcuts import render
from django.http import JsonResponse
from PIL import Image
import pyzbar.pyzbar as pyzbar
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt

def scan_qr_code(request):
    return render(request, 'payments/scan_qr_code.html')

def decode_qrcode(image):
    decoded_data = ''
    try:
        decoded_objects = pyzbar.decode(image)
        for obj in decoded_objects:
            decoded_data = obj.data.decode('utf-8')
    except Exception as e:
        decoded_data = f'Error decoding QR code: {str(e)}'
    return decoded_data

def process_uploaded_image(image):
    image = Image.open(image)
    decoded_data = decode_qrcode(image)
    return decoded_data

@csrf_exempt
def scan_qrcode_camera(request):
    try:
        image_data = request.FILES['image'].read()
        image = Image.open(BytesIO(image_data))
        decoded_data = decode_qrcode(image)
        return JsonResponse({'message': decoded_data})
    except Exception as e:
        return JsonResponse({'message': f'Error: {str(e)}'}, status=400)
