from django.shortcuts import render
from fpdf import FPDF
from django.http import HttpResponse
import os
from django.conf import settings

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 24)
        self.cell(0, 10, 'Resume', 0, 1, 'C')
        self.ln(10)  # Line break

    def footer(self):
        self.set_y(-15)  # Position at 1.5 cm from bottom
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font("Arial", 'B', 14)
        self.cell(0, 10, title, 0, 1, 'L')
        self.set_line_width(0.5)
        self.set_draw_color(173, 216, 230)  # Grey color for the line
        self.line(10, self.get_y(), 200, self.get_y())  # Draw a line below the title
        self.ln(2)  # Line break

    def chapter_body(self, body):
        self.set_font("Arial", '', 12)
        self.multi_cell(0, 10, body)
        self.ln(5)  # Line break

    def add_section(self, title, body):
        self.chapter_title(title)
        self.chapter_body(body)

def home_view(request):
    return render(request, 'home.html')

def sample_view(request):
    return render(request, 'sample.html')

def resume_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        education = request.POST.get('education')
        experience = request.POST.get('experience')
        skills = request.POST.get('skills')
        photo = request.FILES.get('photo')  # Get the uploaded photo

        # Create PDF
        pdf = PDF()
        pdf.add_page()

        # Draw a border around the content
        pdf.set_line_width(1)
        pdf.set_draw_color(173, 216, 230)  # Grey color for the border
        pdf.rect(5, 5, 200, 287)  # Adjust these values based on your layout

        # User Information - Photo on top left
        pdf.set_xy(10, 15)  # Move the photo position higher (top left)
        if photo:
            if not os.path.exists(settings.MEDIA_ROOT):
                os.makedirs(settings.MEDIA_ROOT)

            photo_path = os.path.join(settings.MEDIA_ROOT, photo.name)
            try:
                with open(photo_path, 'wb+') as destination:
                    for chunk in photo.chunks():
                        destination.write(chunk)

                if os.path.isfile(photo_path):
                    pdf.image(photo_path, x=10, y=15, w=30)  # Decreased width of the photo
                else:
                    print("Error: Photo not saved.")
            except Exception as e:
                print(f"Error saving photo: {e}")

        # Center Email and Phone with Name in between
        pdf.set_xy(10, 20)  # Move to the right of the photo
        pdf.set_font("Arial", 'B', size=20)
        pdf.cell(0, 10, name, ln=True, align='C')  # Center aligned name

        pdf.set_font("Arial", 'I', size=12)
        pdf.cell(0, 10, f"Email: {email}", ln=True, align='C')  # Center aligned email
        pdf.cell(0, 10, f"Phone: {phone}", ln=True, align='C')  # Center aligned phone
        pdf.ln(10)  # Line break

        # Add sections with headers
        pdf.add_section("Education", education)
        pdf.add_section("Experience", experience)
        pdf.add_section("Skills", skills)

        # Final touches and generate PDF
        try:
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
            response.write(pdf.output(dest='S').encode('latin1'))

            # Optionally delete the photo after creating the PDF
            if photo and os.path.isfile(photo_path):
                os.remove(photo_path)  # Clean up the saved photo after generating the PDF

            return response
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return HttpResponse("An error occurred while generating the PDF.")

    return render(request, 'input.html')
