const urlParams = new URLSearchParams(window.location.search)
const number = urlParams.get('number');
console.log(number)
const order_number=document.getElementById("order_number")

//點擊台北一日遊,回首頁
const taipeibtn = document.getElementById("taipeibtn")
    taipeibtn.onclick = function(){
        location.href=`/`
    }

function orderdata(){
    fetch(`/api/order/${number}`)
    .then(function (response) {
        return response.json()
    }).then(function (data) {
        let  resultData = data.data
        console.log(resultData)
        if (resultData != null) {
            order_number.textContent=number
        }
    }).catch(function (err) {
        console.log("錯誤訊息", err)
    })
}
orderdata()