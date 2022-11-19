from flask import *
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["JSON_SORT_KEYS"] = False

from mysql.connector import pooling
from mysql.connector import Error
import mysql.connector 


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
    auth_plugin="mysql_native_password",
    **dbconfig
)

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

@app.route("/api/attractions", methods=["GET"])
def InquireAttraction():
	try:
		page = int(request.args.get("page",0))
		keyword = request.args.get("keyword")
		#print(page, type(page))
		#print(keyword, type(keyword))

		connection_object = connection_pool.get_connection()
		cursor = connection_object.cursor(buffered=True)
		cursor.execute("select count(id) from attractions")
		count=cursor.fetchone()
		connection_object.close()
		#print(count)
		
		count=int(count[0])
		if count%12 !=0:
			split_page=count//12
			pages=split_page
		else:
			pages=split_page-1
		#print(pages)

		if page<=pages :	
			if keyword :
				connection_object = connection_pool.get_connection()
				cursor = connection_object.cursor(buffered=True)
				sql=("select * from attractions where category = %s or name like %s ORDER BY id")
				val=(keyword,"%"+keyword+"%")
				cursor.execute(sql,val)
				result=cursor.fetchall()
				connection_object.close()
				#print(result)
				
				count=(len(result))
				print(count)

				if count%12 !=0:
					split_page=count//12
					pages=split_page
				else:
					pages=split_page-1
				print(pages)

				if page>pages:
					errorReturn = {
						"error": True,
						"message": "超過有效範圍"
					}
					return jsonify(errorReturn), 500
				
				endindex=0
				if ((page+1)*12>count):
					endindex=count
				else:
					endindex=(page+1)*12


				alldatas=[]
				for i in range(page*12,endindex):
					datas={
						"id":result[i][0],
						"name":result[i][1],
						"category":result[i][2],
						"description":result[i][3],		
						"address":result[i][4],
						"transport":result[i][5],
						"mrt":result[i][6],
						"lat":result[i][7],
						"lng":result[i]	[8],
						"images":result[i][9]
					}

					alldatas.append(datas)

					nextpage=0
					if page+1>pages:
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
				cursor.execute("select * from attractions order by id")
				result=cursor.fetchall()
				connection_object.close()
				
				endindex=0
				if ((page+1)*12>count):
					endindex=count
				else:
					endindex=(page+1)*12

				alldatas=[]
				for i in range(page*12,endindex):
					datas={
						"id":result[i][0],
						"name":result[i][1],
						"category":result[i][2],
						"description":result[i][3],
						"address":result[i][4],
						"transport":result[i][5],
						"mrt":result[i][6],
						"lat":result[i][7],
						"lng":result[i]	[8],
						"images":result[i][9]
					}
					alldatas.append(datas)

					nextpage=0
					if page+1>pages:
						nextpage=None
					else:
						nextpage=page+1

					dataReturn = {
					'nextPage': nextpage,
					'data': alldatas
				}
				return jsonify(dataReturn), 200

	except Error as e:#500 伺服器內部錯誤
		# print(e)
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
				print(resultData)

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
					"images":resultData[9]}
				print(data )

				dataReturn = {
					"data": data
				}

				# print('dataReturn: ', dataReturn)

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
		# print(e)
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
		print(resultData)

		catdatas=[]
		for datas in resultData:
			for element in datas:
				catdatas.append(element)
		print(catdatas)

		noRepeatData=[]
		for i in catdatas:
			if i not in noRepeatData:
				noRepeatData.append(i )
		return noRepeatData

	except Error as e:#500 伺服器內部錯誤
		# print(e)
		errorReturn = {
			"error": True,
			"message": "伺服器內部錯誤"
		}
		return jsonify(errorReturn), 500


				
			


app.run(port=3000,debug=True)