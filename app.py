from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    redirect
)
import xml.etree.ElementTree as ET
import os
import codecs
import xml.dom.minidom
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import InputRequired

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = os.urandom(24)

app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

ALLOWED_EXTENSIONS = {'xml'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class MyForm(FlaskForm):
    # Common Fields
    required_string_field = lambda label: StringField(label, validators=[InputRequired()])
    optional_string_field = lambda label: StringField(label)
    select_field = lambda label, choices: SelectField(label, choices=choices)
    
    # Reusable Choice Lists
    dating_criteria_choices = [
        ('', '--Please select from the list--'),
        ('lettering', 'Paleography of the document'),
        ('nomenclature', 'Personal names and naming conventions for a specific period'),
        ('prosopography', 'Mention of historically attested individuals'),
        ('reign', 'Mention of officials with known periods of rule'),
        ('titulature', 'Mention of imperial or other titles with known dates'),
        ('internal-date', 'Explicit dating in the document'),
        ('context', 'Archaeological or architectural context'),
    ]
    
    age_choices = [
        ('', '--Please select from the list--'),
        ('prehistory', 'Prehistory'),
        ('iron_age', 'Iron Age'),
        ('roman_age', 'Roman Age'),
        ('late_antiquity', 'Late Antiquity'),
        ('middle_ages', 'Middle Ages'),
        ('ottoman_period', 'Ottoman Period'),
    ]
    
    certainty_choices = [
        ('', '--Please select from the list--'),
        ('high', 'High certainty'),
        ('medium', 'Relative certainty'),
        ('low', 'Low certainty'),
    ]
    
    language_choices = [
        ('', '--Please select from the list--'),
        ('eng', 'English'), ('ara', 'Arabic'), ('bos', 'Bosnian'), ('bul', 'Bulgarian'), 
        ('ell', 'Modern Greek'), ('spa', 'Spanish'), ('ita', 'Italian'), ('lat', 'Latin'), 
        ('deu', 'German'), ('ota', 'Ottoman Turkish'), ('fas', 'Persian'), ('pol', 'Polish'), 
        ('ron', 'Romanian'), ('rus', 'Russian'), ('srp', 'Serbian'), ('grc', 'Ancient Greek'), 
        ('tur', 'Turkish'), ('hun', 'Hungarian'), ('fre', 'French'), ('hrv', 'Croatian'), 
        ('chu', 'Church Slavonic')
    ]

    # Main Form Fields
    filename = required_string_field('Filename')
    author = required_string_field('Author')
    name_source = required_string_field('Name (according to source)')
    name_contemporary = required_string_field('Name (contemporary)')
    description = TextAreaField('Description')
    provenance_origin = optional_string_field('Provenance Origin')
    latitude = required_string_field('Latitude')
    longitude = required_string_field('Longitude')
    geonamesLink = optional_string_field('Geonames Link')
    pleiadesLink = optional_string_field('Pleiades Link')
    date = required_string_field('Date')
    datingCriteria = select_field('Dating Criteria', dating_criteria_choices)
    localizationSource = optional_string_field('Localization Certainty')
    localizationCertainty = select_field('Localization Certainty', certainty_choices)
    age = select_field('Age (according to source)', age_choices)
    
    # Observed Data
    provenanceObservedIn = required_string_field('Provenance Observed In')
    latitudeObserved = optional_string_field('Latitude Observed')
    longitudeObserved = optional_string_field('Longitude Observed')
    geonamesLinkObserved = optional_string_field('Geonames Link Observed')
    pleiadesLinkObserved = optional_string_field('Pleiades Link Observed')
    dateObserved = optional_string_field('Date Observed')
    datingCriteriaObserved = select_field('Dating Criteria Observed', dating_criteria_choices)
    
    # Other Locations
    provenanceOtherLocations = optional_string_field('Provenance Other Locations')
    latitudeOther = optional_string_field('Latitude Other')
    longitudeOther = optional_string_field('Longitude Other')
    geonamesLinkOtherLocations = optional_string_field('Geonames Link Other Locations')
    dateOtherLocations = optional_string_field('Date Other Locations')
    datingCriteriaOtherLocations = select_field('Dating Criteria Other Locations', dating_criteria_choices)
    
    # Current Location
    currentLocation = optional_string_field('Current Location')
    latitudeCurrent = optional_string_field('Latitude Current')
    longitudeCurrent = optional_string_field('Longitude Current')
    geonamesLinkCurrent = optional_string_field('Geonames Link Current')
    pleiadesLinkCurrent = optional_string_field('Pleiades Link Current')

    # Categories and Subcategories
    categories = SelectMultipleField('Category', choices=[
        ('communication', 'Communication'), ('religious', 'Religious sites & objects'), ('inscriptions', 'Inscriptions'),
        ('fortifications', 'Fortifications'), ('settlements', 'Settlements'), ('linear_structures', 'Linear structures'),
        ('manuscripts', 'Manuscripts'), ('water', 'Water'), ('economy', 'Economy'), ('other', 'Other'), ('burials', 'Burials')
    ], validators=[InputRequired()])
    
    subcategories = {
        'communication': SelectMultipleField('Communication Subcategories', choices=[
            ('inn', 'Inn'), ('bridge', 'Bridge'), ('viaduct', 'Viaduct'), ('imaret', 'Imaret'),
            ('ford', 'Ford'), ('quarantine', 'Quarantine'), ('postStation', 'Post Station'), 
            ('roadsideFountain', 'Roadside fountain'), ('oldRoadRemains', 'Old Road Remains')
        ]),
        'religious': SelectMultipleField('Religious Subcategories', choices=[
            ('church', 'Church'), ('paganTemple', 'Pagan Temple'), ('chapel', 'Chapel'), 
            ('mosque', 'Mosque'), ('tekke', 'Tekke'), ('madrasah', 'Madrasah'), ('turbe', 'Türbe'),
            ('ancientMausoleum', 'Ancient Mausoleum'), ('monastery', 'Monastery'), ('caveMonastery', 'Cave Monastery'),
            ('votiveTablet', 'Votive Tablet'), ('votiveStone', 'Votive Stone'), ('megaliths', 'Megaliths'), ('synagogue', 'Synagogue')
        ]),
        'inscriptions': SelectMultipleField('Inscriptions Subcategories', choices=[
            ('funerary_inscription', 'Funerary Inscription'), ('boundary_inscription', 'Boundary Inscription'),
            ('milestone', 'Milestone'), ('building_inscription', 'Building Inscription'), 
            ('dedicatory_inscription', 'Dedicatory Inscription'), ('honorary_inscription', 'Honorary Inscription'), 
            ('votive_inscription', 'Votive Inscription'), ('list', 'List'), ('legal_inscription', 'Legal Inscription')
        ]),
        # Similar structure for other categories...
    }

    # Publication and Language Details
    authorPublication = optional_string_field('Author of Publications (as in Bibliography)')
    startDate = optional_string_field('Start Date')
    endDate = optional_string_field('End Date')
    ageContemporary = select_field('Age (contemporary)', age_choices)
    originalLanguage = select_field('Original Language', language_choices)
    publicationLanguage = select_field('Publication Language', language_choices)

    # Additional Information
    sourceInformation = required_string_field('Source Information/Bibliography')
    annotation = TextAreaField('Annotations')
    keywords = required_string_field('Keywords')
    sourceContent = TextAreaField('Source Content')
    copyrightStoragePlace = optional_string_field('Copyright Storage Place')
    viaf = optional_string_field('VIAF')
    iiif = optional_string_field('IIIF')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():   
    try:
        author = request.form.get('author')
        name_source = request.form.get('name_source')
        name_contemporary = request.form.get('name_contemporary')
        description = request.form.get('description')
        provenance_origin = request.form.get('provenance_origin')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        geonamesLink = request.form.get('geonamesLink')
        pleiadesLink = request.form.get('pleiadesLink')
        date = request.form.get('date')
        datingCriteria = request.form.get('datingCriteria')
        localizationSource = request.form.get('localizationSource')
        localizationCertainity = request.form.get('localizationCertainity')
        age = request.form.get('age')
        provenanceObservedIn = request.form.get('provenanceObservedIn')
        latitudeObserved = request.form.get('latitudeObserved')
        longitudeObserved = request.form.get('longitudeObserved')
        geonamesLinkObserved = request.form.get('geonamesLinkObserved')
        pleiadesLinkObserved = request.form.get('pleiadesLinkObserved')
        dateObserved = request.form.get('dateObserved')
        datingCriteriaObserved = request.form.get('datingCriteriaObserved')
        provenanceOtherLocations = request.form.get('provenanceOtherLocations')
        latitudeOther = request.form.get('latitudeOther')
        longitudeOther = request.form.get('longitudeOther')
        geonamesLinkOtherLocations = request.form.get('geonamesLinkOtherLocations')
        dateOtherLocations = request.form.get('dateOtherLocations')
        datingCriteriaOtherLocations = request.form.get('datingCriteriaOtherLocations')
        currentLocation = request.form.get('currentLocation')
        latitudeCurrent = request.form.get('latitudeCurrent')
        longitudeCurrent = request.form.get('longitudeCurrent')
        geonamesLinkCurrent = request.form.get('geonamesLinkCurrent')
        pleiadesLinkCurrent = request.form.get('pleiadesLinkCurrent')  
        selected_categories = request.form.getlist('category')
        selected_lists = request.form.getlist('list')
        selected_items = request.form.getlist('item')
        authorPublication = request.form.get('authorPublication')
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        ageContemporary = request.form.get('ageContemporary')
        originalLanguage = request.form.get('originalLanguage')
        publicationLanguage = request.form.get('publicationLanguage')
        sourceInformation = request.form.get('sourceInformation')
        annotation = request.form.get('annotation')
        keywords = request.form.get('keywords')
        sourceContent = request.form.get('sourceContent')
        copyrightStoragePlace = request.form.get('copyrightStoragePlace')
        viaf = request.form.get('viaf')
        iiif = request.form.get('iiif')

        # Create the XML structure
        root = ET.Element("siteObject")

        author_element = ET.SubElement(root, "author")
        author_element.text = author
        
        name_source_element = ET.SubElement(root, "nameSource")
        name_source_element.text = name_source
        
        name_contemporary_element = ET.SubElement(root, "nameContemporary")
        name_contemporary_element.text = name_contemporary
        
        description_element = ET.SubElement(root, "description")
        description_element.text = description
        
        provenance_origin_element = ET.SubElement(root, "provenanceOrigin")
        provenance_origin_element.text = provenance_origin
        
        geographic_coordinates_element = ET.SubElement(root, "geographicCoordinates")
        
        latitude_element = ET.SubElement(geographic_coordinates_element, "latitude")
        latitude_element.text = latitude
        
        longitude_element = ET.SubElement(geographic_coordinates_element, "longitude")
        longitude_element.text = longitude

        geonamesLink_element = ET.SubElement(root, 'geonamesLink')
        geonamesLink_element.text = geonamesLink

        pleiadesLink_element = ET.SubElement(root, 'pleiadesLink')
        pleiadesLink_element.text = pleiadesLink

        date_element = ET.SubElement(root, 'date')
        date_element.text = date
        
        datingCriteria_element = ET.SubElement(root, 'datingCriteria')
        datingCriteria_element.text = datingCriteria
        
        localizationSource_element = ET.SubElement(root, 'localizationSource')
        localizationSource_element.text = localizationSource
        

        localizationCertainity_element = ET.SubElement(root, 'localizationCertainity')
        localizationCertainity_element.text = localizationCertainity

        age_element=ET.SubElement(root, 'age')
        age_element.text = age

        provenanceObservedIn_element = ET.SubElement(root, 'provenanceObservedIn')
        provenanceObservedIn_element.text = provenanceObservedIn
                
        geographic_coordinatesObserved_element = ET.SubElement(root, "geographicCoordinatesObserved")
        
        latitudeObserved_element = ET.SubElement(geographic_coordinatesObserved_element, "latitudeObserved")
        latitudeObserved_element.text = latitudeObserved
        
        longitudeObserved_element = ET.SubElement(geographic_coordinatesObserved_element, "longitudeObserved")
        longitudeObserved_element.text = longitudeObserved
              
                
        geonamesLinkObserved_element = ET.SubElement(root, 'geonamesLinkObserved')
        geonamesLinkObserved_element.text = geonamesLinkObserved
        
        pleiadesLinkObserved_element = ET.SubElement(root, 'pleiadesLinkObserved')
        pleiadesLinkObserved_element.text = pleiadesLinkObserved

        dateObserved_element = ET.SubElement(root, 'dateObserved')
        dateObserved_element.text = dateObserved
        
        datingCriteriaObserved_element = ET.SubElement(root, 'datingCriteriaObserved')
        datingCriteriaObserved_element.text = datingCriteriaObserved

        provenanceOtherLocations_element = ET.SubElement(root, 'provenanceOtherLocations')
        provenanceOtherLocations_element.text = provenanceOtherLocations

        geographic_coordinatesOther_element = ET.SubElement(root, "geographicCoordinatesOther")
        
        latitudeOther_element = ET.SubElement(geographic_coordinatesOther_element, "latitudeOther")
        latitudeOther_element.text = latitudeOther
        
        longitudeOther_element = ET.SubElement(geographic_coordinatesOther_element, "longitudeOther")
        longitudeOther_element.text = longitudeOther

        geonamesLinkOtherLocations_element = ET.SubElement(root, 'geonamesLinkOtherLocations')
        geonamesLinkOtherLocations_element.text = geonamesLinkOtherLocations

        dateOtherLocations_element = ET.SubElement(root, 'dateOtherLocations')
        dateOtherLocations_element.text = dateOtherLocations
        
        datingCriteriaOtherLocations_element = ET.SubElement(root, 'datingCriteriaOtherLocations')
        datingCriteriaOtherLocations_element.text = datingCriteriaOtherLocations

        currentLocationElem = ET.SubElement(root, 'currentLocation')
        currentLocationElem.text = currentLocation

        geographicCoordinatesCurrent_element = ET.SubElement(root, 'geographicCoordinatesCurrent')
        
        latitudeCurrent_element = ET.SubElement(geographicCoordinatesCurrent_element, 'latitudeCurrent')
        latitudeCurrent_element.text = latitudeCurrent
        
        longitudeCurrent_element = ET.SubElement(geographicCoordinatesCurrent_element, 'longitudeCurrent')
        longitudeCurrent_element.text = longitudeCurrent

        geonamesLinkCurrent_element = ET.SubElement(root, 'geonamesLinkCurrent')
        geonamesLinkCurrent_element.text = geonamesLinkCurrent

        pleiadesLinkCurrent_element = ET.SubElement(root, 'pleiadesLinkCurrent')
        pleiadesLinkCurrent_element.text = pleiadesLinkCurrent

         # Extract the selected categories and their subcategories
        selected_categories = request.form.getlist('categories[]')

        # Create a dictionary to map category names to their respective subcategories
        category_subcategory_mapping = {
            "communication":request.form.getlist('communication_subcategories[]'),
            "religious": request.form.getlist('religious_subcategories[]'),
            "inscriptions": request.form.getlist('inscriptions_subcategories[]'),
            "fortifications": request.form.getlist('fortifications_subcategories[]'),
            "settlements": request.form.getlist('settlements_subcategories[]'),
            "linear":request.form.getlist('linear_subcategories[]'),
            "manuscripts": request.form.getlist('manuscript_subcategories[]'),
            "water": request.form.getlist('water_subcategories[]'),
            "economy": request.form.getlist('economy_subcategories[]'),
            "other": request.form.getlist('other_subcategories[]'),
            "burials": request.form.getlist('burials_subcategories[]'),
            # Add more category-subcategory mappings as needed
        }

        # Iterate through selected categories and generate XML elements for subcategories
        for category_name in selected_categories:
            if category_name in category_subcategory_mapping:
                subcategories = category_subcategory_mapping[category_name]

                # Wrap the subcategories in <desc type="category"> and <list type="subcategory">
                category_element = ET.Element("desc", type="category")
                list_element = ET.Element("list", type=category_name)

                for subcategory in subcategories:
                    item_element = ET.Element("item")
                    item_element.text = subcategory
                    list_element.append(item_element)

                category_element.append(list_element)
                root.append(category_element)
            else:
                # This is a category with no subcategories, wrap it in <desc type="category">
                category_element = ET.Element("desc", type="category")
                category_element.text = category_name
                root.append(category_element)

        authorPublication_element = ET.SubElement(root,'authorPublication')
        authorPublication_element.text = authorPublication

        informationDates_element = ET.SubElement(root, 'informationDates')
        
        startDate_element = ET.SubElement(informationDates_element, 'startDate')
        startDate_element.text = startDate
        endDate_element = ET.SubElement(informationDates_element, 'endDate')
        endDate_element.text = endDate

        age_contemporary_element=ET.SubElement(root, 'ageContemporary')
        age_contemporary_element.text = ageContemporary

        originalLanguage_element= ET.SubElement(root, 'originalLanguage', {'xml:lang': originalLanguage})        
        originalLanguage_element.text = originalLanguage

        publicationLanguage_element = ET.SubElement(root, 'publicationLanguage', {'xml:lang': publicationLanguage})
        publicationLanguage_element.text = publicationLanguage
               
        sourceInformation_element = ET.SubElement(root, 'sourceInformation')
        sourceInformation_element.text = sourceInformation
        
        annotation_element= ET.SubElement(root, 'annotation')
        annotation_element.text = annotation
        
        keywords_element = ET.SubElement(root, 'keywords')
        keywords_element.text = keywords
        
        sourceContent_element = ET.SubElement(root, 'sourceContent')
        sourceContent_element.text = sourceContent
        
        copyrightStoragePlace_element = ET.SubElement(root, 'copyrightStoragePlace')
        copyrightStoragePlace_element.text = copyrightStoragePlace
        
        viaf_element = ET.SubElement(root, 'viaf')
        viaf_element.text = viaf
        
        iiif_element = ET.SubElement(root, 'iiif')
        iiif_element.text = iiif

        # Write XML to file
        filename = request.form['filename']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}.xml")
        xml_string = ET.tostring(root, encoding='utf-8')
        xml_pretty = xml.dom.minidom.parseString(xml_string).toprettyxml(indent='    ')
        with codecs.open(filepath, "w", "utf-8") as xml_file:
            xml_file.write(xml_pretty)

        return render_template('success.html')

    except Exception as e:
        print(e)
        return "An error occurred", 500

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload', methods=['POST'])
def upload():
    if 'xml_file' not in request.files:
        return 'No file part'
    xml_file = request.files['xml_file']
    if xml_file.filename == '':
        return 'No selected file'
    if xml_file and allowed_file(xml_file.filename):
        filename = secure_filename(xml_file.filename)
        xml_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect('/')
    return 'Invalid file uploaded.'

@app.route('/view-uploads', methods=['GET', 'POST'])
def view_uploads():
    search_query = request.args.get('search', '').lower()
    
    try:
        files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.xml')]
        
        xml_contents = {}
        for filename in files:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            with open(filepath, 'r', encoding='utf-8') as xml_file:
                content = xml_file.read()
                root = ET.fromstring(content)
                site_object = {child.tag: child.text for child in root}
                xml_contents[filename] = site_object

        if search_query:
            xml_contents = {k: v for k, v in xml_contents.items() if any(search_query in str(value).lower() for value in v.values())}

        return render_template('view_uploads.html', xml_contents=xml_contents, search_query=search_query)
    
    except Exception as e:
        print(e)
        return "An error occurred", 500



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
