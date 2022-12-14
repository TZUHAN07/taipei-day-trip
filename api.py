from flask import *
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["JSON_SORT_KEYS"] = False

import os
from dotenv import load_dotenv

from mysql.connector import pooling
from mysql.connector import Error
import mysql.connector 

# 建立Application 物件，可以設定靜態檔案的路徑處理
app = Flask(__name__, static_folder="static", static_url_path="/")

load_dotenv()
password = os.getenv("password")
dbconfig = {
        "host": "localhost",
        "user":"root",
        "password": password,
        "database":"tpdaywebsite",
}

connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="pynative_pool",
    pool_size=5,
    pool_reset_session=True,
    auth_plugin="mysql_native_password",
    **dbconfig
)

#attraction
@app.route("/api/attractions", methods=["GET"])
def InquireAttraction():
	try:
		page = int(request.args.get("page",0))
		keyword = request.args.get("keyword",None)

		if keyword :
			connection_object = connection_pool.get_connection()
			cursor = connection_object.cursor(buffered=True)
			sql=("select count(id) from attractions where category = %s or name like %s")
			val=(keyword,"%"+keyword+"%")
			cursor.execute(sql,val)
			count=cursor.fetchone()
			connection_object.close()

			count=int(count[0])
			
			if count%12 !=0:
				paging=count//12
				allpages=paging
			else:
				paging=count//12
				allpages=paging-1
			
			alldatas=[]
			sql=("select * from attractions where category = %s or name like %s  limit %s,12")
			val=(keyword,"%"+keyword+"%",page*12)
			cursor.execute(sql,val)
			results=cursor.fetchall()
			# connection_object.close()
			for result in results:
				datas={
					"id":result[0],
					"name":result[1],
					"category":result[2],
					"description":result[3],		
					"address":result[4],
					"transport":result[5],
					"mrt":result[6],
					"lat":result[7],
					"lng":result[8],
					"images":result[9].split(",")
				}
				alldatas.append(datas)

			nextpage=0
			if page+1>allpages:
				nextpage=None
			else:
				nextpage=page+1

			dataReturn = {
			'nextPage': nextpage,
			'data': alldatas
			}
			return jsonify(dataReturn), 200

			
		else:
			connection_object = connection_pool.get_connection()
			cursor = connection_object.cursor(buffered=True)
			cursor.execute("select count(id) from attractions ")
			count=cursor.fetchone()
			connection_object.close()

			count=int(count[0])

			if count%12 !=0:
				paging=count//12
				allpages=paging
			else:
				paging=count//12
				allpages=paging-1

			alldatas=[]
			sql=("select * from attractions  id  limit %s,12")
			val=(page*12,)
			cursor.execute(sql,val)
			results=cursor.fetchall()
			for result in results:
				datas={
					"id":result[0],
					"name":result[1],
					"category":result[2],
					"description":result[3],
					"address":result[4],
					"transport":result[5],
					"mrt":result[6],
					"lat":result[7],
					"lng":result[8],
					"images":result[9].split(",")
				}
				alldatas.append(datas)

			nextpage=0
			if page+1>allpages:
				nextpage=None
			else:
				nextpage=page+1

			dataReturn = {
				'nextPage': nextpage,
				'data': alldatas
			}
			return jsonify(dataReturn), 200		

	except Error as e:#500 伺服器內部錯誤
		errorReturn = {
			"error": True,
			"message": "伺服器內部錯誤"
		}
		return jsonify(errorReturn), 500
			
@app.route("/api/attraction/<attractionId>", methods=["GET"])
def getApiId(attractionId):	
	connection_object = connection_pool.get_connection()
	cursor = connection_object.cursor(buffered=True)
	cursor.execute("select count(id) from attractions")
	count=cursor.fetchone()
	connection_object.close()
		
	count=int(count[0])
	try:
		if attractionId.isdigit() is True:
			serchId = int(attractionId)

			if serchId>0 and serchId<=count: # id介於有效範圍	
			
				connection_object = connection_pool.get_connection()
				cursor = connection_object.cursor()
				cursor.execute("select * from attractions where id = %s ", (attractionId,) )
				resultData=cursor.fetchone()
				connection_object.close()

				data ={
					"id":resultData[0],
					"name":resultData[1],
					"category":resultData[2],
					"description":resultData[3],
					"address":resultData[4],
					"transport":resultData[5],
					"mrt":resultData[6],
					"lat":resultData[7],
					"lng":resultData[8],
					"images":resultData[9].split(",")}

				dataReturn = {
					"data": data
				}
				return jsonify(dataReturn), 200


			else: #400 id超過有效範圍
				errorReturn = {
					"error": True,
					"message": "超過有效範圍"
				}
				return jsonify(errorReturn), 400
		else:
			errorReturn = {
					"error": True,
					"message": "請輸入有效數值"
			}
			return jsonify(errorReturn), 400

	except Error as e:#500 伺服器內部錯誤
		errorReturn = {
			"error": True,
			"message": "伺服器內部錯誤"
		}
		return jsonify(errorReturn), 500

@app.route("/api/categories", methods=["GET"])
def getApiCategory():
	try:
		connection_object = connection_pool.get_connection()
		cursor = connection_object.cursor()
		cursor.execute("select category from attractions  " )
		resultData=cursor.fetchall()
		connection_object.close()

		catdatas=[]
		for datas in resultData:
			for element in datas:
				catdatas.append(element)

		noRepeatData=[]
		for i in catdatas:
			if i not in noRepeatData:
				noRepeatData.append(i )

		dataReturn = {
					"data": noRepeatData
				}
		return jsonify(dataReturn), 200	


	except Error as e:#500 伺服器內部錯誤
		errorReturn = {
			"error": True,
			"message": "伺服器內部錯誤"
		}
		return jsonify(errorReturn), 500

if __name__ == '__main__':
    app.run( host="0.0.0.0",port=3000, debug=True)