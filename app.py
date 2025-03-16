from flask import Flask, request, render_template, send_file
from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
import tensorflow as tf
import os
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.units import inch
from datetime import datetime
import geocoder
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'D:/HACKATHON/static/uploads'

# Load the trained model
model = tf.keras.models.load_model('D:/HACKATHON/my_improved_model99.keras')

# Disease labels and cures
disease_labels = [
    "Goat Pox", "Healthy Jersey+Red Sindhi cow(NO DISEASE DETECTED)", "Healthy Jersey+Tharparkar cow(NO DISEASE DETECTED)", 
    "Jersey+Red Sindhi cow lump skin disease(causes skin damage and decrease milk production)", "Magot", "Scabies black bengal goat", 
    "Jersey+Tharparkar cow lump skin disease(causes skin damage and decrease milk production)", "Not Found"
]

cure_recommendations = {
    "Goat Pox": """1) preventive measures 
a) segregation of the affected animal from the normal herd
b) vaccination : goat pox vaccine (uttar kashi stain) should be given at the dose of  1 ml s/c. Immunity lasts for 8-9 months. So vaccine may be repeated every 6 months interval.
c) Cleanliness of the cattle shed with bleaching or phenyl 
d) Quarantine of new animal

2) Chemical control 
a) Broad spectrum antibiotic may be given intramuscularly or intravenously for 5-7 days.
b) Antihistaminic injection may be given.
c) Antipyretic injection should be continued for 5-7 days
d) Dressing of the affected place regularly to prevent any maggot infection.



3) Biological control 
a) Use of Fly- repellent inside or outside the shed.
b) Entry of other animals must be prevented inside the shed

4) Biological control 
A) Cattle shed must be properly cleaned and hygiene should be maintained regularly
B) Fly repellent or Fly killer maybe used inside or outside the cattle shed.
C) Food and drinking water container must be cleaned
D) Use of mosquito net (if possible)""",
    "Healthy Jersey+Red Sindhi cow(NO DISEASE DETECTED)": "NO need of cure already Healthy",
   "Healthy Jersey+Tharparkar cow(NO DISEASE DETECTED)": "NO need of cure already Healthy",
   #jersey cow
    "Jersey+Red Sindhi cow lump skin disease(causes skin damage and decrease milk production)": """
Viral Disease. Infectious and Air-borne Disease.
Damage Caused – Skin Damaged. Decreased Milk Production
    1)Preventive Measure
a)Vaccination must be done. (Goat Pox Vaccine may be used to prevent this disease)
2)Chemical Method
a)Temp rise to nearly 104o C and body pain is observed, it is recommended to apply an Analgesic 
a)i) (for e.g. Meloxicum)and a paracetamol injection to reduce fever and pain
b)Apply Antistaminic Medicine to reduce the swelling.
c)To heal the wound local dressing must be done with Iodine solution
d)An ointment (for e.g. Charmeal, Himax, etc) maybe used to heal the wound.
e)Livogen injection, Belamyl injection, Beekon L injection maybe used for healing purpose

3)Biological Measure
a)Cattle shed must be properly cleaned and hygiene should be maintained regularly
b)Fly repellent or Fly killer maybe used inside or outside the cattle shed.
c)Food and drinking water container must be cleaned
d)Use of mosquito net (if possible)

4)Indigenous Method
a)Mixture of neem and Haldi Powder in Lukewarm Water maybe used to wash the whole body 
b)Alum(KMnO4 solution) – 1:1000 proportion maybe used for body wash.
Alternative for lumpy skin disease

1) preventive measures 
a) segregation of the affected animal from the normal herd
b) vaccination : goat pox vaccine (uttar kashi stain) should be given at the dose of 3 ml s/c.
c Immunity lasts for 8-9 months. So vaccine may be repeated every 6 months interval.
d) Cleanliness of the cattle shed with bleaching or phenyl 
e) Quarantine of new animal

2) Chemical control 
a) Broad spectrum antibiotic may be given intramuscularly or intravenously for 5-7 days.
b) Antihistaminic injection may be given.
c) Antipyretic injection should be continued for 5-7 days
d) Dressing of the affected place regularly to prevent any maggot infection.

3) Biological control 
a) Use of Fly- repellent inside or outside the shed.
b) Entry of other animals must be prevented inside the shed.


Reference/Resources person(for cure) :
Dr. Somnath Dutta (Veterinary Surgeon)
ICAR - NDRI
Kalyani, Nadia, West Bengal, India
Dr. Amar Das,
Assistant Director, ARD
I/C South Bengal Broiler Integration 
WBLDCL (Feed Section)

""",
 #magot
    "Magot": """
    Causal Organism – Larvae of fly. Parasitic Disease. (Destroys that portion of a poultry where the fly lay egg.
Damages the meat quality of the poultry
    1) Preventive Measures:
       a) Firstly cure the intestinal problem of the bird.
       b) Litter should be dry inside the poultry and moisture percentage should not exceed 16%.
       c) Clean the outside area of the farm properly.
       d) Separate dead birds from live birds.
       e) Change fit formulation seasonally.
       f) Apply Cyromazine 2% in the field.

    2) Chemical Control:
       a) Wash the infected area with Betadine solution.
       b) Apply Eucalyptus Oil locally.

    3) Biological Control:
       a) Control flies outside the farm using repellents or fly-killers.

    4) Indian Method:
       a) Traditionally, turmeric powder is used to cure this disease.




       Reference/Resources person(for cure) :
Dr. Somnath Dutta (Veterinary Surgeon)
ICAR - NDRI
Kalyani, Nadia, West Bengal, India
Dr. Amar Das,
Assistant Director, ARD
I/C South Bengal Broiler Integration 
WBLDCL (Feed Section)
    """

,#scabies
    "Scabies black bengal goat": """Mixed disease caused by virus, bacteria, protozoa, etc

1. Preventive measure 
a)Segregation of affected animal from healthy animals
b)Cleanliness of the goat-shed must be maintained. Food and water container must be cleaned properly.
c)Quarantine measures should be taken for new animals.
d)Entry of the other animals must be prevented inside the goat-shed

2.Chemical Measure 
a) Butox or Escaboil maybe applied locally
b) Himax or Lorexane ointment maybe applied locally
c) Ivermectin injection at the dose of 1 ml/50kg body weight maybe applied.

3. Biological Control
Fly should be controlled inside or outside the shed with some fly repellent

4.Indegenous Method
a) Wash the body with neem and turmeric(Haldi) and extract with lukewarm water
b) Wash the affected part of the goat with Glycerine + KMnO4 solution




Reference/Resources person(for cure) :
Dr. Somnath Dutta (Veterinary Surgeon)
ICAR - NDRI
Kalyani, Nadia, West Bengal, India
Dr. Amar Das,
Assistant Director, ARD
I/C South Bengal Broiler Integration 
WBLDCL (Feed Section)""",
  #jersey cow
    "Jersey+Tharparkar cow lump skin disease(causes skin damage and decrease milk production)": """
Viral Disease. Infectious and Air-borne Disease.
Damage Caused – Skin Damaged. Decreased Milk Production
    1)Preventive Measure
a)Vaccination must be done. (Goat Pox Vaccine may be used to prevent this disease)
2)Chemical Method
a)Temp rise to nearly 104o C and body pain is observed, it is recommended to apply an Analgesic 
a)i)(for e.g. Meloxicum) and a paracetamol injection to reduce fever and pain
b)Apply Antistaminic Medicine to reduce the swelling.
c)To heal the wound local dressing must be done with Iodine solution
d)An ointment (for e.g. Charmeal, Himax, etc) maybe used to heal the wound.
e)Livogen injection, Belamyl injection, Beekon L injection maybe used for healing purpose

3)Biological Measure
a)Cattle shed must be properly cleaned and hygiene should be maintained regularly
b)Fly repellent or Fly killer maybe used inside or outside the cattle shed.
c)Food and drinking water container must be cleaned
d)Use of mosquito net (if possible)

4)Indigenous Method
a)Mixture of neem and Haldi Powder in Lukewarm Water maybe used to wash the whole body 
b)Alum(KMnO4 solution) – 1:1000 proportion maybe used for body wash.
Alternative for lumpy skin disease

1) preventive measures 
a) segregation of the affected animal from the normal herd
b) vaccination : goat pox vaccine (uttar kashi stain) should be given at the dose of 3 ml s/c. 
c)Immunity lasts for 8-9 months. So vaccine may be repeated every 6 months interval.
d) Cleanliness of the cattle shed with bleaching or phenyl 
e) Quarantine of new animal

2) Chemical control 
a) Broad spectrum antibiotic may be given intramuscularly or intravenously for 5-7 days.
b) Antihistaminic injection may be given.
c) Antipyretic injection should be continued for 5-7 days
d) Dressing of the affected place regularly to prevent any maggot infection.

3) Biological control 
a) Use of Fly- repellent inside or outside the shed.
b) Entry of other animals must be prevented inside the shed


Reference/Resources person(for cure) :
Dr. Somnath Dutta (Veterinary Surgeon)
ICAR - NDRI
Kalyani, Nadia, West Bengal, India
Dr. Amar Das,
Assistant Director, ARD
I/C South Bengal Broiler Integration 
WBLDCL (Feed Section)
""",
 
    "Not Found": "No disease detected. Ensure regular monitoring."
}



@app.route('/')
def krishi():
    return render_template('krishi.html')



@app.route('/<page_name>')
def render_page(page_name):
    try:
        return render_template(f"{page_name}.html")
    except:
        return "<h1>404 - Page Not Found</h1>", 404



@app.route('/predict', methods=['POST'])
def predict():
    files = request.files.getlist('images')
    # if len(files) != 4:
    #     return "Error: Please upload exactly 4 images.", 400

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    predictions = []
    filenames = []

    for file in files:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        filenames.append(file.filename)

        # Preprocess the image
        image = Image.open(filepath)
        image = image.resize((224, 224))
        image = np.array(image) / 255.0
        image = np.expand_dims(image, axis=0)

        prediction = model.predict(image)
        predictions.append(prediction[0])

    # Aggregate predictions
    avg_prediction = np.mean(predictions, axis=0)
    predicted_class_index = np.argmax(avg_prediction)
    disease = disease_labels[predicted_class_index] if predicted_class_index < len(disease_labels) else "Not Found"
    cure = cure_recommendations.get(disease, "No cure information available.")
    
    # Format cure for HTML
    cure_html = cure.replace("\n", "<br>")

    # Get user location
    location = geocoder.ip('me').latlng if geocoder.ip('me') else "Unknown Location"

    return render_template(
        'result.html',
        disease=disease,
        cure=cure_html,  # Use formatted HTML
        images=filenames,
        location=location
    )
@app.route('/login_form')
def login_form():
    return render_template('login_form.html')

def get_user_location():
    g = geocoder.ip('me')  # Get the location of the user based on their IP
    return g.city, g.state, g.country


@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    # Extract form data
    disease = request.form['disease']
    cure = request.form['cure']
    images = request.form.getlist('images')  # List of image filenames
    location = request.form.get('location', 'Unknown')  # Default 'Unknown' if not provided
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # PDF buffer for in-memory PDF
    pdf_buffer = io.BytesIO()
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter  # Page size

    # Set padding for the content
    padding = 50  # Padding for text and images to prevent overflow

    # Get user location (dummy function - replace with actual implementation)
    
    city, state, country = get_user_location()

    # Set font for text
    pdf.setFont("Helvetica", 12)

    # Add logo to the center of the title (centered logo)
    logo_path = 'static/logo.png'
    logo_width = 60  # Logo width
    logo_height = 60  # Logo height
    logo_x_position = (width - logo_width) / 2  # Center the logo horizontally
    pdf.drawImage(logo_path, logo_x_position, height - 100, width=logo_width, height=logo_height)

    # Title as "KrishiSahayak" with subtitle below (centered)
    title = "KrishiSahayak"
    subtitle = "Livestock Disease Detection"
    
    # Title and subtitle centered
    pdf.setFont("Helvetica-Bold", 24)
    title_width = pdf.stringWidth(title, "Helvetica-Bold", 24)
    pdf.drawString((width - title_width) / 2, height - 150, title)

    # Subtitle centered
    pdf.setFont("Helvetica", 14)
    subtitle_width = pdf.stringWidth(subtitle, "Helvetica", 14)
    pdf.drawString((width - subtitle_width) / 2, height - 180, subtitle)

    # Location, Time, Disease, Cure
    pdf.setFont("Helvetica-Bold", 10)  # Bold for key labels
    pdf.drawString(padding, height - 220, f"Location: ")

    # Reset font for content
    pdf.setFont("Helvetica", 10)
    pdf.drawString(padding + 80, height - 220, f"{city}, {state}, {country}")

    pdf.setFont("Helvetica-Bold", 10)  # Bold for key labels
    pdf.drawString(padding, height - 240, f"Time: ")

    # Reset font for content
    pdf.setFont("Helvetica", 10)
    pdf.drawString(padding + 80, height - 240, time)

    pdf.setFont("Helvetica-Bold", 10)  # Bold for key labels
    pdf.drawString(padding, height - 260, f"Disease: ")

    # Reset font for content
    pdf.setFont("Helvetica", 10)
    pdf.drawString(padding + 80, height - 260, disease)

    pdf.setFont("Helvetica-Bold", 10)  # Bold for key labels
    pdf.drawString(padding, height - 280, f"Cure: ")

    # Adjust Cure size (this is where you can change the font size)
    cure_font_size = 8  # Change this value to adjust the size of the cure text
    pdf.setFont("Helvetica", cure_font_size)
    formatted_cure = cure.replace('<br>', '\n')
    # Create text object for cure (this allows wrapping of the text)
    text_object = pdf.beginText(padding , height - 300)
    text_object.setFont("Helvetica", cure_font_size)
    text_object.setTextOrigin(padding , height - 300)
    text_object.setFillColor(colors.black)
    # text_object.textLines(cure)
    text_object.textLines(formatted_cure)
    pdf.drawText(text_object)


# Title and subtitle centered

    # Adjust y_position for next content
    y_position = height - 350
    if y_position < padding:
        pdf.showPage()
        y_position = height - 100  # Reset position for new page

    # Check if there are images
    if images:
        # End of first page, start second page for images
        pdf.showPage()

        # Title on the second page for images
        pdf.setFont("Helvetica-Bold", 18)
        title_width = pdf.stringWidth("Uploaded Images", "Helvetica-Bold", 18)
        pdf.drawString((width - title_width) / 2, height - 40, "Uploaded Images by user:")

        # Resize images to fit on one page (4 images on one page)
        image_width = 200  # Two images per row
        image_height = 200 # Maintain aspect ratio (height = 3/4 of width)
        y_position = height - 200-100  # Start drawing images after title

        # Loop through uploaded images and add them to PDF
        for idx, img in enumerate(images):
            # Adjust img_path to use the correct 'uploads' folder
            img_path = os.path.join('static', 'uploads', img)  # Updated path with 'uploads' folder
            x_position = padding + (idx % 2) * (image_width + padding)  # Place images in two columns

            # Check if image exists before drawing
            if os.path.exists(img_path):
                # Draw image
                pdf.drawImage(img_path, x_position, y_position, width=image_width, height=image_height)

                # Adjust y-position for next image
                if idx % 2 == 1:  # After placing two images, move to the next row
                    y_position -= (image_height + padding)
            else:
                print(f"Image not found: {img_path}")

            # If images exceed the page, add a new page
            if y_position < padding:
                pdf.showPage()
                y_position = height - 100  # Reset position for new page

    # Save the PDF to the buffer
    pdf.save()
    pdf_buffer.seek(0)

    # Generate the filename with the current date and time
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Livestock_Report_{current_time}.pdf"

    # Send the PDF as a downloadable file
    return send_file(pdf_buffer, as_attachment=True, download_name=filename)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)



