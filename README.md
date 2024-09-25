# DigitalSEE (Digital South-Eastern Europe) data entry system

**Research Institution:** University of Sofia

**Research group name:**  Digital Humanities. ICT Applications for History and Language

**Main research area of the group:** Digital Humanities

**Leading researcher:**  Associate Professor Dr. Maria Baramova

This project is a Flask-based web application that allows users to generate, upload, and manage XML files containing metadata about historical or archaeological sites as part of the **DigitalSEE** initiative. Users can input data via a web form, which is saved as an XML file. The application also supports searching for uploaded files, and viewing them.


## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#run-the-flask-application)
- [Application Routes](#application-routes)
- [Usage](#usage)
- [Dataset](#dataset)
- [Form Fields](#form-fields)
- [Error Handling](#error-handling)
- [Troubleshooting](#troubleshooting)

## Features
- **XML File Generation**: Users can fill out forms, and the application generates XML files based on the input.
- **File Upload**: Upload and save XML files to a directory.
- **Search & View**: Search through uploaded XML files based on keywords and metadata.
- **File Download**: Download generated or uploaded XML files from the server.
- **File Management**: List and view all uploaded XML files.

## Requirements

- **Python 3.11.7 or higher**
- **Flask 2.x**
- **Flask-WTF 1.x**
- **Werkzeug**
- **WTForms**

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Bestroi150/DigitalSEE-DataEntrySystem.git
   cd DigitalSEE-DataEntrySystem

2. **Clone the repository:**
   ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
## Configuration

- **Upload Directory**: The default upload directory is **uploads**/. Ensure this folder exists in the root of the project.
- **Maximum Upload Size**: The maximum upload size for XML files is set to **16 MB** by default. This can be changed in the code.


## Run the Flask application

1. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate`
2. **Run the Flask application:**
`python app.py`
  
## Application Routes

-   **`/`** (`GET`): Homepage with a form to generate XML files.
-   **`/submit`** (`POST`): Submit form data, generates XML, and stores it in the `uploads/` directory. 
-   **`/view-uploads`** (`GET`, `POST`): View and search through uploaded XML files.
## Usage

1.  **Generate XML Files**
    
    -   Navigate to the homepage (`http://127.0.0.1:5000/`).
    -   Fill out the form with details about the historical or archaeological site.
    -   Submit the form. The XML file will be generated and stored in the `uploads/` folder.
2.  **View and Search Files**
    
    -   Go to `http://127.0.0.1:5000/view-uploads`.
    -   Search through the uploaded XML files by entering keywords in the search box.
  
## Dataset
The XML metadata generated using this system has been compiled into a dataset, which can be accessed through the following repository: [DigitalSEE](https://github.com/Bestroi150/DigitalSEE/tree/main). This dataset contains detailed records of historical and archaeological sites and is a key component of the DigitalSEE initiative. 

## Form Fields

The form requires input of the following metadata fields:

-   **Filename**: The name of the generated XML file.
-   **Author**: Name of the author.
-   **Name (Source/Contemporary)**: Names from source and contemporary context.
-   **Description**: Description of the site or object.
-   **Provenance**: Geographic coordinates, links to GeoNames, Pleiades, etc.
-   **Dating Criteria**: Criteria for dating the site or object.
-   **Date**: Time period based on source and contemporary records.
-   **Categories/Subcategories**: Select from a variety of categories like communication, religious sites, inscriptions, etc.
-   **Language**: The original and publication language.
-   **Keywords**: Keywords for the site or object.

## Error Handling

-   **404 Error**: If a route is not found, a custom 404 error page will be displayed.
-   **500 Error**: If there's a server error, an error message will be shown, and the exception will be logged.

## Troubleshooting

-   **File Not Saving**: Verify the `uploads` folder exists and has write permissions.

## License

 - Creative Commons Attribution-ShareAlike 4.0 International

## Funding statement
This study is financed by the European Union-NextGenerationEU, through the National Recovery and Resilience Plan of the Republic of Bulgaria, project No BG-RRP-2.004-0008
