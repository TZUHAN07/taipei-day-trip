const booking_membername = document.getElementById("booking_membername")

const allbooking_data = document.getElementsByClassName("allbooking_data")[0]
const no_booking = document.getElementById("no_booking")
const text_title = document.getElementById("text_title")
const booking_src = document.getElementById("booking_src")
const text_date_var = document.getElementById("text_date_var")
const text_time_var = document.getElementById("text_time_var")
const text_price_var = document.getElementById("text_price_var")
const text_place_var = document.getElementById("text_place_var")
const delete_icon = document.getElementById("delete_icon")


const footer = document.getElementById("footer")

//點擊台北一日遊,回首頁
const taipeibtn = document.getElementById("taipeibtn")
taipeibtn.onclick = function () {
    location.href = `/`
}
//檢查使用者是否登入
function checkLogin() {
    return fetch(`/api/user/auth`)
        .then(function (response) {
            return response.json()
        }).then(function (data) {
            if (data["data"] == null) {
                location.href = `/`
            } else {
                bookingName()
            }
        }).catch(function (err) {
            console.log("錯誤訊息", err)
        })
}
checkLogin()
//顯示預定人名
function bookingName() {
    fetch(`/api/user/auth`)
        .then(function (response) {
            return response.json()
        }).then(function (data) {
            resultData = data.data
            console.log(resultData)
            if (resultData != null) {
                booking_membername.textContent = `您好，${resultData["name"]}，待預訂的行程如下：`
                bookingData()
            }
        }).catch(function (err) {
            console.log("錯誤訊息", err)
        })
}

//顯示預定行程
function bookingData() {
    fetch(`/api/booking`)
        .then(function (response) {
            return response.json()
        }).then(function (data) {
            resultData = data.data
            console.log(resultData)
            if (resultData != null) {
                text_title.textContent = `台北一日遊：${resultData["attraction"]["name"]}`
                booking_src.style.backgroundImage = `url(${resultData["attraction"]["image"]})`
                text_date_var.textContent = resultData["date"]
                if (resultData["time"] == "morning") {
                    text_time_var.textContent = "早上9點到下午4點"
                } else {
                    text_time_var.textContent = "下午2點到下午9點"

                }
                text_price_var.textContent = `新台幣${resultData["price"]}元`
                text_place_var.textContent = resultData["attraction"]["address"]
                total_pay.textContent = `總價：新台幣${resultData["price"]}元`
            } else {
                no_booking.classList.add("show_block")
                allbooking_data.classList.add("hide")
                footer.classList.add("nodata")
            }
        }).catch(function (err) {
            console.log("錯誤訊息", err)
        })
}

//  刪除預定行程
delete_icon.addEventListener("click", function () {
    fetch(`/api/booking`, { method: "DELETE" })
        .then(function (response) {
            return response.json()
        }).then(function (data) {
            console.log(data)
            if (data["ok"]) {
                document.location.pathname = '/booking'
                footer.classList.add("nodata")
            }

        }).catch(function (err) {
            console.log("錯誤訊息", err)
        })
})

// taypay
TPDirect.setupSDK(
    127074,
    "app_cwyzUpdHPbotnc3buGyVRNHMFG8sG6FQu2vJ5ygPPcWzhPNgXYDRSuBNPwyl",
    "sandbox"
)
let fields = {
    number: {
        // css selector
        element: "#card-number",
        placeholder: "**** **** **** ****"
    },
    expirationDate: {
        // DOM object
        element: document.getElementById("card-expiration-date"),
        placeholder: "MM / YY"
    },
    ccv: {
        element: "#card-ccv",
        placeholder: "ccv"
    }
}
TPDirect.card.setup({
    fields: fields,
    styles: {
        // Style all elements
        // "input": {
        //     "color": "gray"
        // },
        // Styling ccv field
        "input.ccv": {
            "font-size": "16px"
        },
        // Styling expiration-date field
        "input.expiration-date": {
            "font-size": "16px"
        },
        // Styling card-number field
        "input.card-number": {
            "font-size": "16px"
        },
        // style focus state
        ":focus": {
            "color": "black"
        },
        // style valid state
        ".valid": {
            "color": "green"
        },
        // style invalid state
        ".invalid": {
            "color": "red"
        },
        // Media queries
        // Note that these apply to the iframe, not the root window.
        '@media screen and (max-width: 400px)': {
            'input': {
                'color': 'orange'
            }
        }
    }
})

const error_msg = document.getElementsByClassName("error_msg")[0]
const credit_error_msg = document.getElementsByClassName("credit_error_msg")[0]

const contact_name_var = document.getElementById("contact_name_var")
const contact_email_var = document.getElementById("contact_email_var")
const contact_phone_var = document.getElementById("contact_phone_var")

const credit_number_var = document.getElementById("credit_number_var")
const overtime_email_var = document.getElementById("overtime_email_var")
const verify_password_var = document.getElementById("verify_password_var")

const total_pay = document.getElementById("total_pay")
const check_button = document.getElementById("check_button")

let orderdata;
check_button.addEventListener("click", function () {
    error_msg.style.color = "#ff2244"
    credit_error_msg.style.color = "#ff2244"
    const contact_name = /^[\u4e00-\u9fa5]{2,12}$|^[a-zA-Z\s]{0,10}$/.test(contact_name_var.value)
    const contact_email = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9-]+\.[a-zA-Z.]{2,5}$/.test(contact_email_var.value)
    const contact_phone = /^[0-9]{10}$/.test(contact_phone_var.value)

    if (contact_name_var.value == "" || contact_email_var.value == "" || contact_phone_var.value == "") {
        error_msg.textContent = "尚有聯絡資訊未輸入"
    } else if (contact_name == false) {
        error_msg.textContent = "姓名格式錯誤，無特殊字元"
    } else if (contact_email == false) {
        error_msg.textContent = "信箱格式錯誤"
    } else if (contact_phone == false) {
        error_msg.textContent = "手機號碼格式錯誤"
    } else {
        // 取得 TapPay Fields 的 status,Get prime
        TPDirect.card.getPrime(function (result) {
            if (result.status !== 0) {
                console.log("get prime error" + result.msg)
                credit_error_msg.textContent = "信用卡資訊錯誤或欄位尚未填寫"
                return
            }
            // alert('get prime 成功，pri  me: ' + result.card.prime)
            let prime = result.card.prime
            orderdata = {
                "prime": prime,
                "order": {
                    "price": resultData["price"],
                    "trip": resultData,
                    "contact": {
                        "name": contact_name_var.value,
                        "email": contact_email_var.value,
                        "phone": contact_phone_var.value
                    }
                }
            }
            console.log(orderdata)
            order()
        })
    }
})


function order() {
    fetch(`/api/orders`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(orderdata)
    }).then(function (response) {
        if (response.status == 403) {
            login.classList.add("show_block")
            black_background.classList.add("show_block")
        }
        console.log(response)
        return response.json()
    }).then(function (data) {
        if (data != null) {
            const num = data["data"]["number"]
            const url = "/thankyou?number=" + num
            location.href = url
            removeOrderData()
        }
    }).catch(function (err) {
        console.log("錯誤訊息", err)
    })
}

function removeOrderData(){
    fetch(`/api/booking`, { method: "DELETE" })
        .then(function (response) {
            return response.json()
        }).then(function (data) {
            console.log(data)
            if (data["ok"]) {
                document.location.pathname = "/thankyou"
            }

        }).catch(function (err) {
            console.log("錯誤訊息", err)
        })
}