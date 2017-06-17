import parse_tomtom
import psycopg2 as pg

conn = pg.connect("dbname=traveltimes user=gis host=localhost")
cur = conn.cursor()

SQL = "DROP TABLE IF EXISTS observations"
cur.execute(SQL)
conn.commit()

SQL = "CREATE TABLE observations( \
        local_time timestamp, \
        id text, \
        flrp_lat double precision, \
        flrp_lon double precision, \
        flrp_frc integer, \
        flrp_fow integer, \
        flrp_dnp double precision, \
        llrp_lat double precision, \
        llrp_lon double precision, \
        llrp_frc integer, \
        llrp_fow integer, \
        llrp_dnp double precision, \
        quality double precision, \
        free_flow_speed double precision, \
        free_flow_traveltime double precision, \
        poffs double precision, \
        noffs double precision )"

cur.execute(SQL)
conn.commit()

observations = parse_tomtom.parse_tomtom("data/traffictomtom_2016-03-03_1600.xml")
for obs in observations:
    cur.execute("INSERT INTO observations VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", obs)
conn.commit()

# We need to have run CREATE EXTENSION postgis first

SQL = "SELECT AddGeometryColumn ('public','observations','geom',4326,'LINESTRING',2);"
cur.execute(SQL)
conn.commit()


SQL = "UPDATE observations set geom =ST_SetSRID(ST_MakeLine(ST_MakePoint(flrp_lon,flrp_lat),ST_MakePoint(llrp_lon,llrp_lat)),4326)"
cur.execute(SQL)
conn.commit()
