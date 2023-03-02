from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse
from typing import List
import pandas as pd
import pdfkit, os
import fitz, re

app = FastAPI()

@app.post('/')
async def excel_pdf(files: List[UploadFile]=None, name: str = Form(None)):
    """
        Function to merge all uploaded excel into pdf and add a string as a header
    """
    
    #Creating a directory if it doesn't exist and cleaning the files inside the directory if it exists 
    if not os.path.exists("static"):
        os.makedirs("static")
    else:
        for temp in os.listdir("static"):
            os.remove(os.path.join("static", temp))

    flag = 0
    result = fitz.open()
    for file in files:
        filename = os.path.join("static", file.filename)
        
        #excel files are filtered out of  the uploaded files
        if file.filename.endswith('.xlsx'):
            
            #saving the file
            with open(filename, "wb") as f:
                f.write(file.file.read())

            #file is converted to html
            df = pd.read_excel(filename, dtype=object)
            df.to_html(filename.replace(".xlsx", ".html"))
            
            #header tag is added to the first excel for the string passed
            if flag == 0:
                with open(filename.replace(".xlsx", ".html")) as fp:
                    html = str(fp.read())
                    with open(filename.replace(".xlsx", ".html"), "w+") as fps:
                        fps.write(f"<h1 style=\"text-align: center;\"> {name} </h1>\n"+html)
                flag+=1
            
            #file is saved as pdf
            pdfkit.from_file(filename.replace(".xlsx", ".html"), filename.replace(".xlsx", ".pdf"))
            
            #generated pdf is appended to the overall result
            result.insert_pdf(fitz.open(filename.replace(".xlsx", ".pdf")))

            #all intermediate generated files are removed for better space complexity
            os.remove(filename.replace(".xlsx", ".pdf"))
            os.remove(filename.replace(".xlsx", ".html"))
            os.remove(filename.replace(".xlsx", ".xlsx"))
    
    # final result is saved for returning
    result.save(f'static/{name}.pdf')

    return FileResponse(f'static/{name}.pdf', content_disposition_type='application/pdf')
