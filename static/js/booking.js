const booking_membername =document.getElementById("booking_membername")

const allbooking_data =document.getElementsByClassName("allbooking_data")[0]
const no_booking =document.getElementById("no_booking")
const text_title =document.getElementById("text_title")
const booking_src =document.getElementById("booking_src")
const text_date_var =document.getElementById("text_date_var")
const text_time_var =document.getElementById("text_time_var")
const text_price_var =document.getElementById("text_price_var")
const text_place_var =document.getElementById("text_place_var")
const delete_icon =document.getElementById("delete_icon")


const contact_name_var =document.getElementById("contact_name_var")
const contact_email_var =document.getElementById("contact_email_var")
const contact_phone_var =document.getElementById("contact_phone_var")

const credit_number_var =document.getElementById("credit_number_var")
const overtime_email_var =document.getElementById("overtime_email_var")
const verify_password_var =document.getElementById("verify_password_var")

const total_pay =document.getElementById("total_pay")
const check_button =document.getElementById("check_button")

const footer =document.getElementById("footer")

//點擊台北一日遊,回首頁
const taipeibtn = document.getElementById("taipeibtn")
    taipeibtn.onclick = function(){
        location.href=`/`
    }
//檢查使用者是否登入
function checkLogin() {
    return fetch(`/api/user/auth`)
    .then(function (response) {
        return response.json()
    }).then(function (data) {
        if (data["data"]==null){
            location.href=`/`
        }else{
            bookingName()
        }
    }).catch(function (err) {
        console.log("錯誤訊息", err)
    })
}
checkLogin()
//顯示預定人名
function bookingName(){
    fetch(`/api/user/auth`)
        .then(function (response) {
            return response.json()
        }).then(function (data) {
            resultData=data.data
            console.log(resultData)
            if (resultData !=null){
                booking_membername.textContent=`您好，${resultData["name"]}，待預訂的行程如下：` 
                bookingData()
            }
        }).catch(function (err) {
            console.log("錯誤訊息", err) 
        })
}

//顯示預定行程
function bookingData(){
    fetch(`/api/booking`)
    .then(function (response) {
        return response.json()
    }).then(function (data) {
        resultData=data.data
        console.log(resultData)
        if (resultData !=null){
            text_title.textContent=`台北一日遊：${resultData["attraction"]["name"]}`
            booking_src.style.backgroundImage=`url(${resultData["attraction"]["image"]})`
            text_date_var.textContent=resultData["date"]
            if (resultData["time"] ==="moring"){
                text_time_var.textContent="早上9點到下午4點"
            }else{
                text_time_var.textContent="下午2點到下午9點"

            }
            text_price_var.textContent=`新台幣${resultData["price"]}元`
            text_place_var.textContent=resultData["attraction"]["address"]
            total_pay.textContent=`總價：新台幣${resultData["price"]}元`
        }else{
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
        fetch(`/api/booking`,{method: "DELETE"})
            .then(function (response) {
                return response.json()
            }).then(function (data) {
                console.log(data)
                if (data["ok"]){
                    document.location.pathname = '/booking'
                    footer.classList.add("nodata")
                }

            }).catch(function (err) {
                console.log("錯誤訊息", err) 
            })
})

// taypay
// TPDirect.setupSDK(127074, 'app_cwyzUpdHPbotnc3buGyVRNHMFG8sG6FQu2vJ5ygPPcWzhPNgXYDRSuBNPwyl', 'sandbox')
// TPDirect.card.setup(config)
// TPDirect.card.setup({
//     // Display ccv field
//     let fields = {
//         number: {
//             // css selector
//             element: '#card-number',
//             placeholder: '**** **** **** ****'
//         },
//         expirationDate: {
//             // DOM object
//             element: document.getElementById('card-expiration-date'),
//             placeholder: 'MM / YY'
//         },
//         ccv: {
//             element: '#card-ccv',
//             placeholder: 'ccv'
//         }
//     }

//     fields: fields,
//     styles: {
//         // Style all elements
//         'input': {
//             'color': 'gray'
//         },
//         // Styling ccv field
//         'input.ccv': {
//             // 'font-size': '16px'
//         },
//         // Styling expiration-date field
//         'input.expiration-date': {
//             // 'font-size': '16px'
//         },
//         // Styling card-number field
//         'input.card-number': {
//             // 'font-size': '16px'
//         },
//         // style focus state
//         ':focus': {
//             // 'color': 'black'
//         },
//         // style valid state
//         '.valid': {
//             'color': 'green'
//         },
//         // style invalid state
//         '.invalid': {
//             'color': 'red'
//         },
//         // Media queries
//         // Note that these apply to the iframe, not the root window.
//         '@media screen and (max-width: 400px)': {
//             'input': {
//                 'color': 'orange'
//             }
//         }
//     },
//     // 此設定會顯示卡號輸入正確後，會顯示前六後四碼信用卡卡號
//     isMaskCreditCardNumber: true,
//     maskCreditCardNumberRange: {
//         beginIndex: 6,
//         endIndex: 11
//     }
// })