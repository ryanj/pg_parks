from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort
from pg import pg

app = Flask(__name__)
app.config.from_pyfile('map.cfg')
table_name = os.environ['OPENSHIFT_APP_NAME']

db = pg.connect(table_name, \
     os.environ['OPENSHIFT_POSTGRESQL_DB_HOST'], \
     int(os.environ['OPENSHIFT_POSTGRESQL_DB_PORT']), \
     None, None, \
     os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME'], \
     os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD'] )

@app.route('/')
def index():
    #return render_template('index.html',
    #    parks=Map.query.order_by(Map.pub_date.desc()).all()
    #)
    return render_template('index.html')

#return all parks:
@app.route("/parks")
def parks():
    #query the DB for all the parkpoints
    result = db.query('SELECT * FROM '+ table_name+";")

    #Now turn the results into valid JSON
    return str(json.dumps({'results':list(result)},default=json_util.default))

#bounding box (within?lat1=45.5&lon1=-82&lat2=46.5&lon2=-81)
@app.route("/parks/within")
def within():
    #get the request parameters
    lat1 = float(request.args.get('lat1'))
    lon1 = float(request.args.get('lon1'))
    lat2 = float(request.args.get('lat2'))
    lon2 = float(request.args.get('lon2'))
    print "lat1 = " + lat1
    print "lon1 = " + lon1
    print "lat2 = " + lat2
    print "lon2 = " + lon2

    #use the request parameters in the query
    result = db.query("SELECT * FROM "+table_name+" t WHERE ST_Intersects( \
        ST_MakeEnvelope("+lat1+", "+lon1+", "+lat2+", "+lon2+", 4326) \
        t.the_geom)")

    #turn the results into valid JSON
    return str(json.dumps({'results' : list(result)},default=json_util.default))

@app.route("/test")
def test():
    return "<strong>It's Alive!</strong>"

if __name__ == '__main__':
    app.run()
