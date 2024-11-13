from django.shortcuts import render
from fpdf import FPDF
from django.http import HttpResponse
from .forms import ResumeForm  # Import your form here

def home_view(request):
    return render(request, 'home.html')  

def resume_view(request):
    if request.method == "POST":
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            # Extract form data
            name = form.cleaned_data['name']
            # You can also extract other fields here if needed
            # photo = form.cleaned_data['photo'] (if you want to use the photo)

            # Create PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Resume", ln=True, align='C')
            pdf.cell(200, 10, txt=f"Name: {name}", ln=True, align='L')
            # Add other information to the PDF as needed

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
            response.write(pdf.output(dest='S').encode('latin1'))
            return response
    else:
        form = ResumeForm()  # Instantiate the form for GET requests

    return render(request, 'input.html', {'form': form})  # Pass the form to the template

def sample_view(request):
    return render(request, 'sample.html')
