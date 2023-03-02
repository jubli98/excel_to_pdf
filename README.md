# excel_to_pdf
Merge all uploaded excel into pdf and add a string as a header

It is a project made in fastapi for aggregating multiple excel's data into one pdf file. 

Urls available: 
  
  "/" (POST):
      Input parameters:
        files, name
        
      Sample input- {"files": <excel_files>, "name": "Combined Docs"}

      Output- PDF with all excel's data combined
