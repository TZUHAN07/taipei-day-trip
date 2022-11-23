import json
#from json import load
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData,Float,TEXT,ForeignKey
from mysql.connector import pooling
from mysql.connector import Error
import mysql.connector 


engine = create_engine("mysql+pymysql://root:j610114*@localhost/tpdaywebsite")

with engine.connect() as connection:
    execute = connection.execute

    metadata = MetaData()
    attraction = Table("attractions", metadata,
        Column("id",Integer, primary_key=True,  nullable=False),
        Column("name",String(255), nullable=False),
        Column("category",String(255), nullable=False),
        Column("description",String(4095), nullable=False),  
        Column("address",String(255), nullable=False),
        Column("transport",String(4095), nullable=False), 
        Column("mrt",String(255), nullable=False),  
        Column("lat",Float, nullable=False),
        Column("lng",Float, nullable=False),
        Column("images",TEXT, nullable=False) 
    )
  

    metadata.create_all(engine)

dbconfig = {
        "host": "localhost",
        "user":"root",
        "password": "j610114*",
        "database":"tpdaywebsite",
}
connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="pynative_pool",
    pool_size=5,
    pool_reset_session=True,
    auth_plugin="mysql_native_password",#預設caching_sha2_password加密，必須加上一行把預設加密改為mysql_native_password
    **dbconfig
)

with open("/Users/chaotzuhan/Desktop/taipei-day-trip/data/taipei-attractions.json", mode='r') as file:
    datas = json.load(file)["result"]["results"]
id=0   
for data in datas:
    id+=1
    print(id)
    name=data["name"]
    category=data["CAT"]
    description=data["description"]
    address=data["address"]
    transport=data["direction"]
    mrt=data["MRT"]
    lat=data["latitude"]
    lng=data["longitude"]

    images=data["file"].lower()
    allimages = images.split(".jpg")[0:-1]
    path=[]
    for image in allimages:
        image = image+".jpg"
        path.append(image)

    allpaths=json.dumps(path)
    print(allpaths)
    #allpaths=",".join(path)
    #print(allpaths)

    try:
        connection_object = connection_pool.get_connection() 
        cursor = connection_object.cursor()
        insert_data = ("INSERT INTO attractions (id,name,category,description,address,transport,mrt,lat,lng,images) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        val=(id,name,category,description,address,transport,mrt,lat,lng,allpaths)
        print(val)
        cursor.execute(insert_data,val)

        connection_object.commit()
      
    except Error as e:
        print("Error while connecting to MySQL using Connection pool ", e)


    finally:
        # closing database connection.
        if connection_object.is_connected():
            cursor.close()
            connection_object.close()
            print("MySQL connection is closed")