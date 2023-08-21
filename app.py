from flask import Flask, request, jsonify
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image as ReportLabImage, Spacer
from reportlab.lib.units import inch
from PIL import Image as PILImage
from pathlib import Path


app = Flask(__name__)

@app.route('/create_doc', methods=['POST'])
def create_doc():
    data = request.json

    filename = data['filename']
    fileformat = data['fileformat']
    filepath_input = data['filepath_input']

    doc = SimpleDocTemplate(filename + fileformat, pagesize=letter)

    elements = []

    image_paths = filepath_input.split('"')
    image_paths = [i for i in image_paths if i != '']

    for image_path in image_paths:
        image_path = image_path.replace('/', '//')
        image_path = Path(image_path)

        with open(image_path, "rb") as img_file:
            pil_image = PILImage.open(img_file)
            desired_width = 5.0 * inch
            desired_height = 7.0 * inch
            pil_image = pil_image.resize((int(desired_width), int(desired_height)))

            image_reportlab = ReportLabImage(image_path, width=desired_width, height=desired_height)
            elements.append(image_reportlab)
            elements.append(Spacer(1, 0.5 * inch))

    doc.build(elements)
    
    return jsonify({'message': 'Document created successfully'})

if __name__ == '__main__':
    app.run(debug=True)



# This is function for create Doc.

# def createDoc(filename, fileformat, filepath_input):
#     '''
#     Give filename, fileformat, filepaths
#     filepaths should be given without spaces just paste it in the filepath_input attribute.
#     '''
#     doc = SimpleDocTemplate(filename + fileformat, pagesize=letter)

#     elements = []



#     image_paths = filepath_input.split('"')

#     image_paths = [i for i in image_paths if i!='']
#     print(image_paths)

#     for image_path in image_paths: 
#         image_path = image_path.replace('/', '//')  
#         image_path = Path(image_path)
#         print(image_path)

#         with open(image_path, "rb") as img_file:
#                 pil_image = PILImage.open(img_file)
#                 desired_width = 5.0 * inch
#                 desired_height = 7.0 * inch
#                 pil_image = pil_image.resize((int(desired_width), int(desired_height)))

#                 image_reportlab = ReportLabImage(image_path, width=desired_width, height=desired_height)
#                 elements.append(image_reportlab)
#                 elements.append(Spacer(1, 0.5 * inch))
#     doc.build(elements)



# createDoc('dmeo2', '.xlxs', r'"C:\Users\16244\OneDrive - Compunnel Software Group, Inc\Pictures\ROMS-high-level.jpg""C:\Users\16244\OneDrive - Compunnel Software Group, Inc\Pictures\ROMS-high-level.jpg"')



