import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os,jwt,requests
from datetime import datetime, timezone, timedelta
from flask import *
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["JSON_SORT_KEYS"] = False
app.config["SECRET_KEY"] = "secertonly"


# from api import *
# from user import *

app = Flask(__name__, static_folder="static", static_url_path="/")
bcrypt = Bcrypt(app)

load_dotenv()

dbconfig = {
    "host": "localhost",
    "user": "root",
    "password": os.getenv("password"),
    "database": "tpdaywebsite",
}

connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="pynative_pool",
    pool_size=15,
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

#建立新的訂單
@app.route("/api/orders", methods=["POST"])
def order_post():
    try:
        cookies = request.cookies.get("access_token")
        member_data = jwt.decode(
            cookies, "secertonly", algorithms=["HS256"]
        )
        # print(member_data)
        if cookies is None:
            dataReturn = {
                "error": True,
                "message": "未登入系統，拒絕存取"
            }
            return jsonify(dataReturn),403
        data = request.get_json()
        prime = data["prime"]
        price = data["order"]["price"]
        trip_id = data["order"]["trip"]["attraction"]["id"]
        trip_name = data["order"]["trip"]["attraction"]["name"]
        trip_address = data["order"]["trip"]["attraction"]["address"]
        trip_image = data["order"]["trip"]["attraction"]["image"]
        trip_date = data["order"]["trip"]["date"]
        trip_time = data["order"]["trip"]["time"]
        name = data["order"]["contact"]["name"]
        email = data["order"]["contact"]["email"]
        phone = data["order"]["contact"]["phone"]
        memberId=member_data["id"]
        status=1

        tz = timezone(timedelta(hours=+8))
        dt = datetime.now(tz)
        dt_string = dt.strftime("%Y%m%d%H%M%S")
        order_number = dt_string

        if name==""or email=="" or phone =="":
            return jsonify({"error": True, "message": "尚有資料未輸入"}), 400
        else:
            connection_object = connection_pool.get_connection()
            cursor = connection_object.cursor(buffered=True)
            insert_data = (
                "INSERT INTO  orderlist (number, price, attractionId, date,time,memberId, phone, codestatus)VALUES (%s,%s,%s,%s,%s,%s,%s,%s) "
            )

            val = (order_number,price,trip_id,trip_date,trip_time,memberId,phone,status)
            cursor.execute(insert_data , val)
            connection_object.commit()

            headers = {
	    		"Content-Type": "application/json",
	    		"x-api-key": "partner_vDU0LpYWT8sMGjL6DxiwEwM5pL9d8o467u4dghPzQpeeR9cuNnlDn0EY"
	    		}
            orderdata ={
                "prime": prime,
	    		"partner_key": "partner_vDU0LpYWT8sMGjL6DxiwEwM5pL9d8o467u4dghPzQpeeR9cuNnlDn0EY",
	    		"merchant_id": "tzuhan_CTBC",
	    		"details": trip_name +","+trip_date+","+trip_time+","+"的訂單",
	    		"amount": price,
	    		"cardholder": {
	    			"phone_number": phone,
	    			"name": name,
	    			"email": email,
	    		},
                "remember":True
            }
            # Pay by Prime to TapPay Server & get TapPay result
            response = requests.post("https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime", json = orderdata, headers = headers)
            response = response.json()

            if response["status"] == 0:
                dataReturn={
                "data":{
	    				"number": order_number,
	    				"payment": {
	    				"status": "0",
	    				"message": "付款成功"
	    				}
	    			}
                }
                return jsonify(dataReturn),200
            else:
                dataReturn = {
                "error": True,
                "message": "付款失敗,待付款"
                }
            return jsonify(dataReturn),400
    except:  # 500 伺服器內部錯誤
        return jsonify({"error": True, "message": "伺服器內部錯誤"}), 500
    finally:
        connection_object.close()

#取得訂單資訊
@app.route("/api/order/<number>")
def order_get(number):
    try:
        cookies = request.cookies.get("access_token")
        if number:
            if cookies is None:
                dataReturn = {
                    "error": True,
                    "message": "未登入系統，拒絕存取"
                }
                return jsonify(dataReturn),403
            else:
                connection_object = connection_pool.get_connection()
                cursor = connection_object.cursor(buffered=True)
                sql = (
                    "SELECT  number, price, attractionId, attractions.name, attractions.address, attractions.images, date, time, member.name, member.email, phone,codestatus  FROM orderlist INNER JOIN attractions ON orderlist.attractionId = attractions.id INNER JOIN member ON orderlist.memberId = member.id"
                )
                cursor.execute(sql)
                result = cursor.fetchone()  
                if result is None:
                    order_data = {"data": None}
                    return jsonify(order_data),400
                else:
                    order_data = {
                        "data": {
                            "number": result[0],
                            "price": result[1],
                            "trip": {
                              "attraction": {
                                "id": result[2],
                                "name": result[3],
                                "address": result[4],
                                "image": result[5].split(",")[0]
                              },
                              "date": result[6],
                              "time": result[7]
                            },
                            "contact": {
                              "name": result[8],
                              "email": result[9],
                              "phone": result[10]
                            },
                            "status":result[11]
                        }
                    }
                    # print(order_data)
                    return jsonify(order_data),200
    except:  # 500 伺服器內部錯誤
        return jsonify({"error": True, "message": "伺服器內部錯誤"}), 500
    finally:
        connection_object.close()
    

# 取得未確認訂單行程
@app.route("/api/booking", methods=["GET"])
def booking_get():
    try:
        cookies = request.cookies.get("access_token")
        if cookies is None:
            dataReturn = {
                "error": True,
                "message": "未登入系統，拒絕存取"
            }
            return jsonify(dataReturn),403
        else:
            connection_object = connection_pool.get_connection()
            cursor = connection_object.cursor(buffered=True)
            sql = (
                "SELECT attractionId,name,address,images,date,time,price from booking  INNER JOIN  attractions ON booking.attractionId=attractions.id")
            cursor.execute(sql)
            result = cursor.fetchone()  
            if result is None:
                booking_data = {"data": None}
                return jsonify(booking_data) 
            else:
                booking_data = {
                "data":{
	    				"attraction": {
	    					"id": result[0],
	    					"name": result[1],
	    					"address": result[2],
	    					"image": result[3].split(",")[0]
	    				},
	    				"date": result[4],
	    				"time": result[5],
	    				"price": result[6]
	    			}
                }
                # print(booking_data)
                return jsonify(booking_data),200
    except:  # 500 伺服器內部錯誤
        return jsonify({"error": True, "message": "伺服器內部錯誤"}), 500
    finally:
        connection_object.close()


# 建立新的預定行程
@app.route("/api/booking", methods=["POST"])
def booking_post():
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor(buffered=True)
    try:
        cookies = request.cookies.get("access_token")
        

        if cookies is None:
            dataReturn = {
                "error": True,
                "message": "未登入系統，拒絕存取"
            }
            return jsonify(dataReturn),403
        else:
            data = request.get_json()
            attractionId = data["attractionId"]
            date = data["date"]
            time = data["time"]
            price= data["price"]

            if date == "" or time == "":
                dataReturn = {
                "error": True,
                "message": "日期或時間尚未選擇"
                }
                return jsonify(dataReturn),400
            else:
                sql = "select * from booking"
                cursor.execute(sql)
                result = cursor.fetchone()
                if result:
                    update_data = ("UPDATE booking SET attractionId = %s, date = %s, time = %s, price = %s ")
                    val = (attractionId , date, time, price)
                    cursor.execute(update_data , val) 
                    connection_object.commit()
                    return jsonify({"ok": True}), 200
                else:
                    insert_data = ("INSERT INTO booking (attractionId, date, time, price) VALUES (%s,%s,%s,%s)")
                    val = (attractionId , date, time, price)
                    cursor.execute(insert_data , val)
                    connection_object.commit()
                    return jsonify({"ok": True}), 200
    except:  # 500 伺服器內部錯誤
        return jsonify({"error": True, "message": "伺服器內部錯誤"}), 500
    finally:
        connection_object.close()

        

# 刪除目前預定行程
@app.route("/api/booking", methods=["DELETE"])
def booking_delete():
    try:
        cookies = request.cookies.get("access_token")
        if cookies is None:
            dataReturn = {
                "error": True,
                "message": "未登入系統，拒絕存取"
            }
            return jsonify(dataReturn),403
        else:
            connection_object = connection_pool.get_connection()
            cursor = connection_object.cursor(buffered=True)
            sql=("DELETE FROM booking ")
            cursor.execute(sql)
            connection_object.commit()
            return jsonify({"ok": True}), 200
    except:  # 500 伺服器內部錯誤
        return jsonify({"error": True, "message": "伺服器內部錯誤"}), 500
    


# 註冊會員
@app.route("/api/user", methods=["POST"])
def login_post():
    try:
        data = request.get_json()
        name = data["name"]
        email = data["email"]
        password = data["password"]

        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor(buffered=True)
        sql = ("select * from member where email = %s")
        val = (email,)
        cursor.execute(sql, val)
        account = cursor.fetchone()

        if account is None:
            hashed_password = bcrypt.generate_password_hash(password)
            insert_data = (
                "INSERT INTO member (name, email,password) VALUES (%s,%s,%s)")
            val = (name, email, hashed_password)
            cursor.execute(insert_data, val)
            connection_object.commit()
            return jsonify({"ok": True}), 200
        elif account[2] == email:
            dataReturn = {
                "error": True,
                "message": "註冊失敗,Email已被使用過"
            }
            return (dataReturn), 400
        else:
            dataReturn = {
                "error": True,
                "message": "註冊失敗，重複的 Email 或其他原因"
            }
            return jsonify(dataReturn), 400
    except:  # 500 伺服器內部錯誤
        return jsonify({"error": True, "message": "伺服器內部錯誤"}), 500
    finally:
        connection_object.close()




@app.route("/api/user/auth", methods=["GET"])
def login_get():
    try:
        # 獲取 cookie 的字典
        cookies = request.cookies.get("access_token")
        if cookies is None:
            return jsonify({"data": None})
        else:
            member_data = jwt.decode(
                cookies, "secertonly", algorithms=["HS256"])
            return jsonify({"data": member_data}),200
    except:
        return jsonify({"error": True, "message": "伺服器內部錯誤"}), 500


@app.route("/api/user/auth", methods=["PUT"])
def login_put():
    try:
        data = request.get_json()
        email = data["email"]
        password = data["password"]
        
        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor(buffered=True)
        sql = ("SELECT * FROM member WHERE email=%s")
        val = (email,)
        cursor.execute(sql, val)

        account = cursor.fetchone()
        # print(account)
        encrypted_password = account[3]

        if account is None:
            dataReturn = {
                "error": True,
                "message": "登入失敗，帳號或密碼錯誤或其他原因"
            }
            return jsonify(dataReturn), 400
        else:
            if bcrypt.check_password_hash(encrypted_password, password):
                payload = {
                    "id": account[0],
                    "name": account[1],
                    "email": email,
                }
                
                access_token = jwt.encode(payload, "secertonly")
                response = make_response({"ok": True})
                # 設置 cookie，並指定 cookie 的名稱、值、有效期限等信息
                response.set_cookie("access_token", access_token,
                                    max_age=60*60*24*7, httponly=True)
                return response
            else:
                return {
                  "error": True,
                  "message": "帳號或密碼錯誤"
                },400
    except:
        return jsonify({"error": True, "message": "伺服器內部錯誤"}), 500
    finally:
        connection_object.close()


@app.route("/api/user/auth", methods=["DELETE"])
def login_delete():
    try:
        response = make_response({"ok": True})
        response.delete_cookie("access_token")
        return response
    except:
        return jsonify({"error": True, "message": "伺服器內部錯誤"}), 500

# attraction
@app.route("/api/attractions", methods=["GET"])
def InquireAttraction():
    try:
        page = int(request.args.get("page", 0))
        keyword = request.args.get("keyword", None)

        if keyword:
            connection_object = connection_pool.get_connection()
            cursor = connection_object.cursor(buffered=True)
            sql = (
                "SELECT count(id) FROM attractions WHERE category = %s or name like %s")
            val = (keyword, "%"+keyword+"%")
            cursor.execute(sql, val)
            count = cursor.fetchone()
            count = int(count[0])

            if count % 12 != 0:
                paging = count//12
                allpages = paging
            else:
                paging = count//12
                allpages = paging-1

            alldatas = []
            sql = (
                "SELECT * FROM attractions WHERE category = %s or name like %s  limit %s,12")
            val = (keyword, "%"+keyword+"%", page*12)
            cursor.execute(sql, val)
            results = cursor.fetchall()
            for result in results:
                datas = {
                    "id": result[0],
                    "name": result[1],
                    "category": result[2],
                    "description": result[3],
                    "address": result[4],
                    "transport": result[5],
                    "mrt": result[6],
                    "lat": result[7],
                        "lng": result[8],
                        "images": result[9].split(",")
                }
                alldatas.append(datas)

            nextpage = 0
            if page+1 > allpages:
                nextpage = None
            else:
                nextpage = page+1

            dataReturn = {
                'nextPage': nextpage,
                'data': alldatas
            }
            return jsonify(dataReturn), 200

        else:
            connection_object = connection_pool.get_connection()
            cursor = connection_object.cursor(buffered=True)
            cursor.execute("SELECT count(id) FROM attractions ")
            count = cursor.fetchone()
            count = int(count[0])

            if count % 12 != 0:
                paging = count//12
                allpages = paging
            else:
                paging = count//12
                allpages = paging-1

            alldatas = []
            sql = ("SELECT * FROM attractions  id  LIMIT %s,12")
            val = (page*12,)
            cursor.execute(sql, val)
            results = cursor.fetchall()
            for result in results:
                datas = {
                    "id": result[0],
                    "name": result[1],
                    "category": result[2],
                    "description": result[3],
                    "address": result[4],
                    "transport": result[5],
                    "mrt": result[6],
                    "lat": result[7],
                        "lng": result[8],
                        "images": result[9].split(",")
                }
                alldatas.append(datas)

            nextpage = 0
            if page+1 > allpages:
                nextpage = None
            else:
                nextpage = page+1

            dataReturn = {
                'nextPage': nextpage,
                'data': alldatas
            }
            return jsonify(dataReturn), 200
    except :  # 500 伺服器內部錯誤
        return jsonify({"error": True, "message": "伺服器內部錯誤"}), 500
    finally:
        connection_object.close()



@app.route("/api/attraction/<attractionId>", methods=["GET"])
def getApiId(attractionId):
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor(buffered=True)
    cursor.execute("SELECT count(id) FROM attractions")
    count = cursor.fetchone()
    count = int(count[0])
    try:
        if attractionId.isdigit() is True:
            serchId = int(attractionId)

            if serchId > 0 and serchId <= count:  # id介於有效範圍
                connection_object = connection_pool.get_connection()
                cursor = connection_object.cursor()
                cursor.execute(
                    "select * from attractions where id = %s ", (attractionId,))
                resultData = cursor.fetchone()

                data = {
                    "id": resultData[0],
                    "name": resultData[1],
                    "category": resultData[2],
                    "description": resultData[3],
                    "address": resultData[4],
                    "transport": resultData[5],
                    "mrt": resultData[6],
                    "lat": resultData[7],
                        "lng": resultData[8],
                        "images": resultData[9].split(",")}

                dataReturn = {
                    "data": data
                }
                return jsonify(dataReturn), 200

            else:  # 400 id超過有效範圍
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
    except:  # 500 伺服器內部錯誤
        return jsonify({"error": True, "message": "伺服器內部錯誤"}), 500
    finally:
        connection_object.close()



@app.route("/api/categories", methods=["GET"])
def getApiCategory():
    try:
        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor()
        cursor.execute("SELECT category FROM attractions  ")
        resultData = cursor.fetchall()

        catdatas = []
        for datas in resultData:
            for element in datas:
                catdatas.append(element)

        noRepeatData = []
        for i in catdatas:
            if i not in noRepeatData:
                noRepeatData.append(i)

        dataReturn = {
            "data": noRepeatData
        }
        return jsonify(dataReturn), 200
    except Error as e:  # 500 伺服器內部錯誤
        return jsonify({"error": True, "message": "伺服器內部錯誤"}), 500
    finally:
        connection_object.close()



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)
