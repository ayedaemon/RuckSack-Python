from flask import Flask, request, render_template
import os
from PIL import Image
import folium
from PIL.ExifTags import TAGS, GPSTAGS


## Variables
app = Flask(__name__, template_folder="templates")
tempates_folder = "templates"
images_folder = "static"
images = [entry.path for entry in os.scandir(images_folder) if entry.is_file()]



## Metadata Extractor
def get_exif(filename):
    exif = Image.open(filename).getexif()
    if exif is not None:
        for key, value in exif.items():
            name = TAGS.get(key, key)
            exif[name] = exif.pop(key)
    return dict(exif)
	
def get_gps(exif):
    for key,value in exif.items():
        name = str(GPSTAGS.get(key,key))
        yield(name,value)
	
def get_decimal_coordinates(info):
    for key in ['Latitude', 'Longitude']:
        if 'GPS'+key in info and 'GPS'+key+'Ref' in info:
            e = info['GPS'+key]
            ref = info['GPS'+key+'Ref']
            info[key] = ( e[0][0]/e[0][1] +
                          e[1][0]/e[1][1] / 60 +
                          e[2][0]/e[2][1] / 3600
                        ) * (-1 if ref in ['S','W'] else 1)
    if 'Latitude' in info and 'Longitude' in info:
        return (info['Latitude'],info['Longitude'])
	
def extract(i):
    exif = get_exif(i)
    loc = []
    try:
        data = [j for i, j in exif.items() if i == 'GPSInfo'][0]
        loc = get_decimal_coordinates(dict(get_gps(data)))
    except:
        pass
    return (i,loc)
    

def updatedb():
    images = [entry.path for entry in os.scandir(images_folder) if entry.is_file()]
    with open("location.csv","w") as f:    
        for i in images:
            n, l = extract(i)
            l1 = 'None'
            l2 = 'None'
            try:
                l1 = str(l[0])
                l2 = str(l[1])
            except:
                pass
            print(n, l1, l2)
            f.write(f"{n},{l1},{l2}\n")    
    
    
def create_map():
    m = folium.Map(zoom_start=10) 
    data = open("location.csv","r").read().split("\n")[:-1]
    for i in data:
        n, l1, l2 = i.split(',')
        if len(n)<0 or l1 != "None" and l2 != "None":
            n = n.replace("\\","/")
            folium.Marker([l1, l2], tooltip=f"<img src='{n}' height=100 width=100> </img>").add_to(m)
    m.save(os.path.join(tempates_folder, "loc.html"))
    
           
## Routes
@app.route("/", methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        f = request.files['file']
        save_path = os.path.join(images_folder, f.filename)
        f.save(save_path)
        updatedb()
    return render_template("index.html", frame_src="/loc")


@app.route("/loc")
def loc():
    create_map()
    return render_template("loc.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port="80")