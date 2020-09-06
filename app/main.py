from flask import Flask, render_template, jsonify, request, url_for
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.ext.automap import automap_base
#from sqlalchemy.orm import Session
#from sqlalchemy import create_engine, MetaData, Table, Integer, Column
from app import config as cfg
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = cfg.DATABASE_URL
db = SQLAlchemy(app)



class houses_loc(db.Model):
#    __table_args__ = {'schema' : 'public'}
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.NUMERIC, unique=False, nullable=False)
    lon = db.Column(db.NUMERIC, unique=False, nullable=False)
    url = db.Column(db.VARCHAR(100), unique=False, nullable=False)
    precio = db.Column(db.NUMERIC(15,3), unique=False, nullable=False)


class map_tbl(db.Model):
#    __table_args__ = {'schema' : 'public'}
    id = db.Column(db.Integer, primary_key=True)
    cod_estado = db.Column(db.VARCHAR(25), unique=False, nullable=False)
    estado = db.Column(db.VARCHAR(25), unique=False, nullable=False)
    cod_municipio = db.Column(db.NUMERIC(4), unique=False, nullable=False)
    municipio = db.Column(db.VARCHAR(50), unique=False, nullable=False)   
    ctype = db.Column(db.VARCHAR(105), unique=False, nullable=False)
    coords = db.Column(db.TEXT, unique=False, nullable=False)
    prom_idh = db.Column(db.Numeric, unique=False, nullable=False)
    prom_precio = db.Column(db.Numeric, unique=False, nullable=False)
    prom_ingreso = db.Column(db.Numeric, unique=False, nullable=False)
    prom_precio_m2 = db.Column(db.Numeric, unique=False, nullable=False)
    numero_propiedades = db.Column(db.Numeric, unique=False, nullable=False)

class vw_records(db.Model):
#    __table_args__ = {'schema' : 'public'}
    id = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.VARCHAR(25), unique=False, nullable=False)
    municipio = db.Column(db.VARCHAR(50), unique=False, nullable=False)
    colonia = db.Column(db.VARCHAR(105), unique=False, nullable=False)
    calle = db.Column(db.VARCHAR(240), unique=False, nullable=False)
    descripcion = db.Column(db.VARCHAR(110), unique=False, nullable=False)
    precio = db.Column(db.NUMERIC(15,3), unique=False, nullable=False)
    url = db.Column(db.VARCHAR(120), unique=False, nullable=False)
    cod_estado = db.Column(db.NUMERIC(3), unique=False, nullable=False)
    cod_municipio = db.Column(db.NUMERIC(4), unique=False, nullable=False)

class estados(db.Model):

    cod_estado = db.Column(db.Numeric(3), primary_key=True)
    estado = db.Column(db.VARCHAR(150), unique=False, nullable=False)


class municipios(db.Model):
#    __table_args__ = {'schema' : 'dbo'}
    cod_edo_mun = db.Column(db.VARCHAR(10), primary_key=True)
    cod_estado = db.Column(db.Numeric(3), unique=False, nullable=False)
    cod_municipio = db.Column(db.Numeric(4), unique=False, nullable=False)
    municipio = db.Column(db.VARCHAR(255), unique=False, nullable=False)

class rep_municipios(db.Model):
#    __table_args__ = {'schema' : 'dbo'}
    id_edo_mun = db.Column(db.VARCHAR(10), primary_key=True)
    cod_estado = db.Column(db.Numeric(3), unique=False, nullable=False)
    cod_municipio = db.Column(db.Numeric(4), unique=False, nullable=False)
    estado = db.Column(db.VARCHAR(255), unique=False, nullable=False)
    municipio = db.Column(db.VARCHAR(255), unique=False, nullable=False)
    avg_precio = db.Column(db.Numeric, unique=False, nullable=False)
    count_inmuebles = db.Column(db.Numeric, unique=False, nullable=False)
    avg_superficie = db.Column(db.Numeric, unique=False, nullable=False)
    avg_precio_m2 = db.Column(db.Numeric, unique=False, nullable=False)
    avg_idh = db.Column(db.Numeric, unique=False, nullable=False)
    avg_income = db.Column(db.Numeric, unique=False, nullable=False)
    avg_health = db.Column(db.Numeric, unique=False, nullable=False)
    avg_education = db.Column(db.Numeric, unique=False, nullable=False)
    avg_recamaras = db.Column(db.Numeric, unique=False, nullable=False)
    avg_banos = db.Column(db.Numeric, unique=False, nullable=False)
    avg_estacionamientos = db.Column(db.Numeric, unique=False, nullable=False)

class rep_estados(db.Model):
#    __table_args__ = {'schema' : 'dbo'}
    cod_estado = db.Column(db.Numeric(3), primary_key=True)
    estado = db.Column(db.VARCHAR(255), unique=False, nullable=False)
    avg_precio = db.Column(db.Numeric, unique=False, nullable=False)
    count_inmuebles = db.Column(db.Numeric, unique=False, nullable=False)
    avg_superficie = db.Column(db.Numeric, unique=False, nullable=False)
    avg_precio_m2 = db.Column(db.Numeric, unique=False, nullable=False)
    avg_idh = db.Column(db.Numeric, unique=False, nullable=False)
    avg_income = db.Column(db.Numeric, unique=False, nullable=False)
    avg_health = db.Column(db.Numeric, unique=False, nullable=False)
    avg_education = db.Column(db.Numeric, unique=False, nullable=False)
    avg_recamaras = db.Column(db.Numeric, unique=False, nullable=False)
    avg_banos = db.Column(db.Numeric, unique=False, nullable=False)
    avg_estacionamientos = db.Column(db.Numeric, unique=False, nullable=False)



def getJsonResponse(qryResult):
    resultList = []
    for ele in qryResult:
        tmpdict = {k: v for k, v in ele.__dict__.items() if not k.startswith('_')}
        resultList.append(tmpdict)
    response = jsonify(resultList)  
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response



@app.route("/raw_data")
def get_source_ds():
    state = request.args.get('state', default = 0, type = int)
    mun = request.args.get('mun', default = 0, type = int)
    page = request.args.get('page', default = 1, type = int)
    result = vw_records.query

    if state != 0:
        result = result.filter(vw_records.c_estado == state)
    if mun != 0:
        result = result.filter(vw_records.c_mnpio == mun)
    
    result = result.paginate(page, 20, False).items
    return getJsonResponse(result)

# JSONS
@app.route("/states")
def get_estados():
    result = estados.query.all()
    return getJsonResponse(result)


@app.route("/municipalities")
def get_municipios():
    result = municipios.query.all()
    return getJsonResponse(result)


@app.route("/datos_estado")
def get_vw_datos_estado():
    state_1 = request.args.get('state1', default = 0, type = int)
    state_2 = request.args.get('state2', default = 0, type = int)
    result = rep_estados.query.filter(rep_estados.cod_estado.in_((state_1, state_2))).all()

    return getJsonResponse(result)


@app.route("/datos_municipio")
def get_vw_datos_municipio():
    
    edomun1 = request.args.get('edomun1', default = '0', type = str)
    edomun2 = request.args.get('edomun2', default = '0', type = str)

    result = rep_municipios.query.filter(rep_municipios.id_edo_mun.in_((edomun1, edomun2))).all()

    return getJsonResponse(result)
#---------------------------------------------------------------------
@app.route("/datos_municipio_estado")
def get_vw_datos_municipio_estado():
    
    state_1 = request.args.get('state1', default = 0, type = int)
    state_2 = request.args.get('state2', default = 0, type = int)

    result = rep_municipios.query.filter(rep_municipios.cod_estado.in_((state_1, state_2))).all()

    return getJsonResponse(result)




#*************************************************************************************************************************************

@app.route("/vw_map")
def get_vw_map():
    result = map_tbl.query.all()
    recordlist = []
    geoJson = {}
    geoJson["type"] = "FeatureCollection"
    geoJson["crs"] = { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } }
    geoJson["features"] = []

    for ele in result:
        tmpdict = {}
        tmpdict["type"] = "Feature"
        tmpdict["properties"] = {}
        tmpdict["properties"]["COD_ESTADO"] = ele.cod_estado
        tmpdict["properties"]["ESTADO"] = ele.estado
        tmpdict["properties"]["COD_MUNICIPIO"] = ele.cod_municipio
        tmpdict["properties"]["MUNICIPIO"] = ele.municipio
        tmpdict["properties"]["IDH"] = ele.prom_idh
        tmpdict["properties"]["PIB"] = ele.prom_ingreso
        tmpdict["properties"]["PRECIO"] = ele.prom_precio
        tmpdict["properties"]["PRECIO_M2"] = ele.prom_precio_m2
        tmpdict["properties"]["NUMERO"] = ele.numero_propiedades
        tmpdict["geometry"] = {}
        tmpdict["geometry"]["type"] = ele.ctype
        tmpdict["geometry"]["coordinates"] = json.loads(ele.coords)
        geoJson["features"].append(tmpdict)

    return(geoJson)
    #pprint.pprint(result)

@app.route("/datos_alt")
def datos_alt():
    result = houses_loc.query.all()
    recordlist = []
    #print(result[0].__dict__.keys())
    for ele in result:
        tmpdict = {}
        tmpdict["Location"] = [ele.lat, ele.lon]
        tmpdict["URL"] = ele.url
        tmpdict["PRECIO"] = ele.precio
 
        recordlist.append(tmpdict)
        response = jsonify(recordlist)
        response.headers.add("Access-Control-Allow-Origin", "*")
    return response





@app.route("/")
def index():
    #pagetitle = "Analysis: Housing prices in Mexico"
    #pagecontent = "Please select an option to explore our dataset"

    return render_template("index.html")

@app.route("/map")
def map():

    return render_template("map.html")

@app.route("/compare")
def graph():


    return render_template("compare.html")

@app.route("/about")
def about():


    return render_template("about.html")


@app.route("/data")
def data():
    state = request.args.get('state', default = 0, type = int)
    mun = request.args.get('mun', default = 0, type = int)
    page = request.args.get('page', default = 1, type = int)
    result = vw_records.query

    if state != 0:
        result = result.filter(vw_records.c_estado == state)
    if mun != 0:
        result = result.filter(vw_records.c_mnpio == mun)
    
    result = result.paginate(page, 20, False)

    next_url = url_for('data', page=result.next_num) \
        if result.has_next else None
    prev_url = url_for('data', page=result.prev_num) \
        if result.has_prev else None

    return render_template("data.html", houses=result.items, next_url=next_url, prev_url=prev_url)

    