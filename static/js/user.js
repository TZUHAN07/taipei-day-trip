const body=document.body
const login_signin = document.getElementById("login-signin")
const logout = document.getElementById("logout")

const login = document.getElementById("login")
const register = document.getElementById("register")
const black_background = document.getElementsByClassName("black_background")[0]

const login_email = document.getElementById("login_email")
const login_password = document.getElementById("login_password")
const login_button = document.getElementById("login_button")
const login_change = document.getElementsByClassName("login_change")[0]
const login_msg = document.getElementById("login_msg")

const register_name = document.getElementById("register_name")
const register_email= document.getElementById("register_email")
const register_password= document.getElementById("register_password")
const register_button= document.getElementById("register_button")
const register_change = document.getElementsByClassName("register_change")[0]
const register_msg = document.getElementById("register_msg")


//點擊登入/註冊 顯示登入表單
login_signin.addEventListener("click", function () {
    login.classList.add("show_block")
    black_background.classList.add("show_block")
})

// 關閉登入表單
login_button.addEventListener("click", function () {  
    logSystem()
})
// 切換至註冊表單
login_change.onclick=function(){
    login_change.classList.add("text_color")
    register.classList.add("show_block")
    login.classList.remove("show_block")
    login_email.value=""
    login_password.value=""
    login_msg.textContent=""

}
// 切換至登入表單
register_change.onclick=function(){
    register_change.classList.add("text_color")
    login.classList.add("show_block")
    register.classList.remove("show_block")
}

//點擊其他地方，表單收起來
black_background.addEventListener("click", function (event) {
    let anyplace = event.target
    if (login == anyplace|| login.contains(anyplace)||register == anyplace|| register.contains(anyplace)) {
        // ... 
      } else {
        clear_all()
        register.classList.remove("show_block")
        login.classList.remove("show_block")
        black_background.classList.remove("show_block")
      }
})
function clear_all(){
    login_email.value=""
    login_password.value=""
    login_msg.textContent=""
    register_name.value=""
    register_email.value=""
    register_password.value=""
    register_msg.textContent=""
}

// 判斷登入狀態：有登入->顯示"登出系統"；沒登入->顯示"登入/註冊"
function checkLogin() {
    fetch(`/api/user/auth`)
    .then(function (response) {
        return response.json()
    }).then(function (data) {
        if (data["data"]!=null){
            logout.classList.add("show_block")
            login_signin.classList.add("hide")
        }else{
            login_signin.classList.add("show_block")
        }
    }).catch(function (err) {
        console.log("錯誤訊息", err)
    })
}
checkLogin()

//登入系統驗證
function logSystem() {
    if (login_email.value===""|| login_password.value===""){
        login_msg.textContent= "尚有欄位未輸入"
        login_msg.style.color = "#ff2244"
    }else{
        fetch(`/api/user/auth`, {
            method: "PUT",
            headers:{"Content-Type":"application/json"},
            body: JSON.stringify({
                email: login_email.value,
                password: login_password.value,
            })
        }).then(function (response) {
            return response.json()
        }).then(function (data) {
            if(data["ok"]){
                location.reload()
            }else{
                login_msg.textContent = data["message"]
                login_msg.style.color = "#ff2244"
            }

        }).catch(function (err) {
            console.log("錯誤訊息", err)
        })
    }
}

// 點擊登出網頁會導回首頁
logout.addEventListener("click", function () {
    fetch(`/api/user/auth`, {method: 'DELETE'})
    .then((res)=>{
        return res.json()
    })
    .then((data)=>{
        if(data["ok"]){
            location.href='/'
        }
    })
    .catch((err)=>{
    console.log("錯誤訊息",err)
    })
})

// 註冊帳戶，關閉註冊表單
register_button.addEventListener("click", function () {  
    registerSystem()
})

// 註冊系統驗證
function registerSystem() {
    register_msg.style.color = "#ff2244"
    //  姓名:輸入2-10位中文或英文
    const register_name_verify=/^[\u4e00-\u9fa5a-zA-Z]{2,12}$/.test(register_name.value)
    //  信箱:符合信箱的格式
    const register_email_verify = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9-]+\.[a-zA-Z.]{2,5}$/.test(register_email.value)
    //  密碼:5-8位英數字(至少包含一個字母)
    const register_password_verify = /^(?=.*[A-Za-z])\w{8,12}$/.test(register_password.value)
    if (register_name.value === ""|| register_email.value === ""|| register_password.value === ""){
        register_msg.textContent= "尚有欄位未輸入"
    }else if(register_name_verify === false){
        register_msg.textContent= "姓名需為2-12字元的中文或英文"
    }else if(register_email_verify === false){
        register_msg.textContent= "信箱格式錯誤"
    }else if(register_password_verify === false){
        register_msg.textContent= "密碼需為8-12字元的英文或數字,至少有一個英文字母"
    }else{
        fetch(`/api/user`, {
            method: "POST",
            headers:{"Content-Type":"application/json"},
            body: JSON.stringify({
                name: register_name.value,
                email: register_email.value,
                password: register_password.value,
            })
        }).then(function (response) {
            return response.json()
        }).then(function (data) {
            if(data["ok"]){
                registerSuccess()
            }else{
                register_msg.textContent = data["message"]
            }

        }).catch(function (err) {
            console.log("錯誤訊息", err)
        })
    }
}
// 註冊成功：導向登入視窗
function registerSuccess(){
    register_msg.textContent = "註冊成功！請登入帳號"
    register_msg.style.color = "#448899"
    setTimeout(() => {
        login_msg.textContent= "歡迎登入台北一日遊"
        login_msg.style.color = "#448899"
        register.classList.remove("show_block")
        login.classList.add("show_block")
    }, 2000);
}
//預定行程
const tourbook=document.getElementById("tourbook")
tourbook.addEventListener("click", function () { 
    checkLogin()
    if(logout){
        location.href=`/api/booking`
    }
    
})