import uvicorn
import shutil
import os.path 
from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from serve_model_yolov5 import predict, read_imagefile


app_desc = """<h2>Try this app by uploading any image with `predict/image`</h2>
"""


app = FastAPI(title='Yolov5 FastAPI Starter Pack', description=app_desc)


app.mount("/static", StaticFiles(directory="static"), name="static")



templates = Jinja2Templates(directory='webTemplates/')


@app.get("/", include_in_schema=False)
async def index(request: Request):
    
    return templates.TemplateResponse('form_yolov5.html', context={'request': request})


@app.post("/")
async def predict_api(request: Request, email: str = Form(...), model: str = Form(...), threshold: str = Form(...), file: UploadFile = File(...)):

    email = email
    model = model
    threshold = threshold
    filename = file.filename
    filename_basename = os.path.splitext(filename)[0]

    mycmd='python detect.py \
    --source "static/' + filename + '"  \
    --weights ' + model + ' \
    --conf-thres '+ threshold + ' \
    --project static --name output --exist-ok --save-txt --save-conf'    


    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")

    if not extension:
        predictionMessage = "Image must be jpg or png format!"
    else:
        #
        #with open("/tmp/destination.png", "wb") as buffer:
        #    shutil.copyfileobj(file.file, buffer)
  
        image = read_imagefile(await file.read())
        image.save("static/" + filename)

        # predictionMessage = predict(image)
        predictionMessage = predict(mycmd)
    return templates.TemplateResponse('form_yolov5.html', context={'request': request, 'email': email, 'model': model, 'threshold': threshold, 'filename': filename, 'filename_basename': filename_basename, 'prediction': predictionMessage, 'mycmd': mycmd})

    
# Python  python main.py
#  uvicorn main:app  --host 0.0.0.0 --port 9999
if __name__ == "__main__":
    #uvicorn.run(app, debug=True)
    uvicorn.run(app, port=8080, host='0.0.0.0')
