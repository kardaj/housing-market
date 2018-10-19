import requests
import shapefile
from zipfile import ZipFile
import StringIO
from pyproj import Proj, transform
import shapely.geometry
from app.model import db, Amenity
from app.common import flask_app_context

inProj = Proj(init='epsg:2154', preserve_units=True)
outProj = Proj(init='epsg:4326')
amenity_type = 'bike_stop'

with flask_app_context:
    there_s_change = False
    r = requests.get('https://data.bordeaux-metropole.fr/files.php?gid=105&format=2')
    with ZipFile(StringIO.StringIO(r.content), 'r') as zipshape:
        dbfname, _, shpname, shxname = zipshape.namelist()
        r = shapefile.Reader(shp=StringIO.StringIO(zipshape.read(shpname)),
                             shx=StringIO.StringIO(zipshape.read(shxname)),
                             dbf=StringIO.StringIO(zipshape.read(dbfname)))
        for feature in r.shapeRecords():
            x, y = feature.shape.__geo_interface__['coordinates']
            lng, lat = transform(inProj, outProj, x, y)
            shp = shapely.geometry.point.Point(lng, lat)
            geometry = shp.wkt
            name = str(hash(feature.record[3]))
            row = db.session.query(Amenity).filter_by(name=name, amenity_type=amenity_type).one_or_none()
            if row is None:
                amenity = Amenity(name=name, geometry=geometry, amenity_type=amenity_type)
                db.session.add(amenity)
                there_s_change = True
    if there_s_change:
        db.session.commit()
