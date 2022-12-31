const attrId = location.pathname.split('/')[2]
console.log(attrId)

//選擇器設定
const morning = document.getElementById("morning")
const afternoon = document.getElementById("afternoon")
const price = document.getElementById("price")

//點擊台北一日遊,回首頁
const taipeibtn = document.getElementById("taipeibtn")
    taipeibtn.onclick = function(){
        location.href=`/`
    }

const viewimg = document.getElementsByClassName("viewimg")[0]
const viewtext_name = document.getElementsByClassName("viewtext_name")[0]
const viewtext_cat_mrt = document.getElementsByClassName("viewtext_cat_mrt")[0]
const veiw_describe = document.getElementsByClassName("veiw_describe")[0]
const veiw_address_text = document.getElementsByClassName("veiw_address_text")[0]
const veiw_traffic_text = document.getElementsByClassName("veiw_traffic_text")[0]
let images = []
//取得頁面初始資料
const getallData = function () {
    let attractionId = attrId
    return fetch(`/api/attraction/${attractionId}`)
        .then(function (response) {
            return response.json()
        }).then(function (data) {
            let resultData = data.data
            console.log(resultData)
            images = resultData.images
            getViewData(resultData)

        }).catch(function (err) {
            console.log("錯誤訊息", err)
        })
}

//創建初始頁面資料內容
const getViewData = function (resultData) {
    const name = resultData.name
    const cat = resultData.category
    const mrt = resultData.mrt
    const describe = resultData.description
    const address = resultData.address
    const transport = resultData.transport

    viewtext_name.textContent = name
    viewtext_cat_mrt.textContent = cat + " at " + mrt
    veiw_describe.textContent = describe
    veiw_address_text.textContent = address
    veiw_traffic_text.textContent = transport

}

// 監聽morining,afternoon
function handler(e){
    const time=document.querySelector('input[name="time"]:checked').value
    if (time== "morning"){
        price.textContent = "新台幣 2000 元"
    }else{
        price.textContent = "新台幣 2500 元"
    }
    console.log(time)
  }

// 開始預預約行程按鈕
const checktour_button=document.getElementById("checktour_button")
checktour_button.addEventListener("click", function () { 
    const date=document.getElementsByClassName("date")[0].value
    const time=document.querySelector('input[name="time"]:checked').value
    let basic_price=0
    if (time== "morning"){
        basic_price=2000
    }else{
        basic_price=2500
    }

    fetch(`/api/booking`,{
        method: "POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({
            attractionId: attrId,
            date: date,
            time: time,
            price: basic_price
        })
    }).then(function (response) {
        if (response.status==403 ){
            login.classList.add("show_block")
            black_background.classList.add("show_block")
        }
        console.log(response)
        return response.json()
    }).then(function (data) {
        console.log(data)
        if (data["ok"]){
            location.href=`/booking`
        }
    }).catch(function (err) {
        console.log("錯誤訊息", err)
    })
    
})

//連播圖片
function allsrc(index) {
    let mySlidesDiv = document.createElement("div")
    mySlidesDiv.classList.add("mySlides")
    let mySlides_img = document.createElement("img")
    mySlides_img.classList.add("mySlides_img")
    mySlides_img.setAttribute("src", images[index])
    mySlides_img.setAttribute("alt", "mySlides_img")

    const slideshow_container = document.getElementById("slideshow_container")
    slideshow_container.appendChild(mySlidesDiv).appendChild(mySlides_img)

    let dotSpan = document.createElement("span")
    dotSpan.classList.add("dot")

    const dotBar = document.getElementById("dotBar")
    dotBar.appendChild(dotSpan)

    dotSpan.onclick = function () {
        currentSlide(index+1)
    }
}

async function slideshow_create() {
    await getallData()
    for (let index = 0; index < images.length; index++) {
        allsrc(index)
    }
    showSlides(slideIndex);
}



/* Slideshow JavaScript */
let slideIndex = 1;

function plusSlides(n) {
    showSlides(slideIndex += n);
}

function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    let dots = document.getElementsByClassName("dot");
    if (n > slides.length) { slideIndex = 1 }
    if (n < 1) { slideIndex = slides.length };
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].classList.remove("active");
    }
    slides[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].classList.add("active");
}

slideshow_create()