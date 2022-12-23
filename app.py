import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
import jwt
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
password = os.getenv("password")
dbconfig = {
    "host": "localhost",
    "user": "root",
    "password": password,
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

# 註冊會員
@app.route("/api/user", methods=["POST"])
def login_post():
    try:
        datas = request.get_json()
        name = datas["name"]
        email = datas["email"]
        password = datas["password"]

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
            connection_object.close()
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
            return jsonify({"data": member_data})
    except:
        return jsonify({"error": True, "message": "伺服器內部錯誤"}), 500


@app.route("/api/user/auth", methods=["PUT"])
def login_put():
    try:
        datas = request.get_json()
        email = datas["email"]
        password = datas["password"]
        
        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor(buffered=True)
        sql = ("select email,password from member where email=%s")
        val = (email,)
        cursor.execute(sql, val)

        account = cursor.fetchone()
        encrypted_password = account[1]
        connection_object.close()

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
                "select count(id) from attractions where category = %s or name like %s")
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
                "select * from attractions where category = %s or name like %s  limit %s,12")
            val = (keyword, "%"+keyword+"%", page*12)
            cursor.execute(sql, val)
            results = cursor.fetchall()
            # connection_object.close()
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
            connection_object.close()
            return jsonify(dataReturn), 200

        else:
            connection_object = connection_pool.get_connection()
            cursor = connection_object.cursor(buffered=True)
            cursor.execute("select count(id) from attractions ")
            count = cursor.fetchone()
            count = int(count[0])

            if count % 12 != 0:
                paging = count//12
                allpages = paging
            else:
                paging = count//12
                allpages = paging-1

            alldatas = []
            sql = ("select * from attractions  id  limit %s,12")
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
            connection_object.close()
            return jsonify(dataReturn), 200

    except Error as e:  # 500 伺服器內部錯誤
        errorReturn = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        connection_object.close()
        return jsonify(errorReturn), 500


@app.route("/api/attraction/<attractionId>", methods=["GET"])
def getApiId(attractionId):
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor(buffered=True)
    cursor.execute("select count(id) from attractions")
    count = cursor.fetchone()
    count = int(count[0])
    
    if attractionId.isdigit() is True:
        serchId = int(attractionId)

        if serchId > 0 and serchId <= count:  # id介於有效範圍

            connection_object = connection_pool.get_connection()
            cursor = connection_object.cursor()
            cursor.execute(
                "select * from attractions where id = %s ", (attractionId,))
            resultData = cursor.fetchone()
            connection_object.close()

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
            # connection_object.close()
            return jsonify(dataReturn), 200

        else:  # 400 id超過有效範圍
            errorReturn = {
                "error": True,
                "message": "超過有效範圍"
            }
            connection_object.close()
            return jsonify(errorReturn), 400
    else:
        errorReturn = {
            "error": True,
            "message": "請輸入有效數值"
        }
        connection_object.close()
        return jsonify(errorReturn), 400

    # except Error as e:  # 500 伺服器內部錯誤
    #     errorReturn = {
    #         "error": True,
    #         "message": "伺服器內部錯誤"
    #     }
    #     connection_object.close()
    #     return jsonify(errorReturn), 500


@app.route("/api/categories", methods=["GET"])
def getApiCategory():
    try:
        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor()
        cursor.execute("select category from attractions  ")
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
        connection_object.close()
        return jsonify(dataReturn), 200

    except Error as e:  # 500 伺服器內部錯誤
        errorReturn = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        # connection_object.close()
        return jsonify(errorReturn), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)
