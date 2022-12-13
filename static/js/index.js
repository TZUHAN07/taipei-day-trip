let attractionImg = " "
let attractionName = " "
let attractionCat = " "
let attractionMrt = " "
let attractionId =" "
let nextpage = 0
let catkeyword =" "

//選擇器設定
const content = document.getElementById("content")
const button = document.getElementById("button")
const search = document.getElementById("keyword")

//監聽btn,取得景點資料
button.addEventListener("click", function () {
    console.log("click")
    nextpage = 0;
    content.innerHTML = " "
    getKeywordData(true)
})
//監聽input，點擊時跳出視窗
search.addEventListener("click", function () {
    document.getElementById("searchlist").classList.add("show")

    const catkeyword=document.getElementsByClassName("searchlistItems")
    
    for (const elem of catkeyword) {
        elem.addEventListener("click", function () {
            inputValue()
        })

       const search=document.getElementById("keyword")
       let str=" "
        function inputValue(){
            search.innerHTML=" "
            str=elem.textContent 
            search.value=str 
        }
    }
})
//點擊其他地方，彈跳框收起來
document.addEventListener("click", (event) => {
    let list = document.getElementById("list")
    let search = document.getElementById("keyword")
    let anyplace = event.target
    if (list == anyplace|| list.contains(anyplace)||search == anyplace) {
        // ... 
      } else {
        document.getElementById("searchlist").classList.remove("show")
      }
  
})

getKeywordData(true)

//佈局景點的div
function newAttractions(urlId) {
    // let urlId=attractionId
    let attractionPicDiv = document.createElement("div")
    attractionPicDiv.classList.add("attraction-pic")
    
    attractionPicDiv.onclick = function(){
        location.href=`/attraction/${urlId}`
    }

    let attractionNameDiv = document.createElement("div")
    attractionNameDiv.classList.add("attraction-name")
    let attractionCatMrtDiv = document.createElement("div")
    attractionCatMrtDiv.classList.add("attraction-cat-mrt")
    let attractionCatDiv = document.createElement("div")
    attractionCatDiv.classList.add("cat")
    let attractionMrtDiv = document.createElement("div")
    attractionMrtDiv.classList.add("mrt")

    let attractionImgDiv = document.createElement("div")
    attractionImgDiv.classList.add("attraction-img")
    let viewpoint = document.createElement("img")
    viewpoint.setAttribute("src", attractionImg)
    viewpoint.setAttribute("alt", "attraction-img")


    content.appendChild(attractionPicDiv).appendChild(attractionImgDiv).appendChild(viewpoint)
    content.appendChild(attractionPicDiv).appendChild(attractionCatMrtDiv)
    let nametext = document.createTextNode(attractionName)
    attractionNameDiv.appendChild(nametext)
    attractionImgDiv.appendChild(attractionNameDiv)
 
    attractionCatMrtDiv.appendChild(attractionMrtDiv)
    let mrttext = document.createTextNode(attractionMrt)
    attractionCatMrtDiv.appendChild(mrttext)
    attractionCatMrtDiv.appendChild(attractionCatDiv)
    let cattext = document.createTextNode(attractionCat)
    attractionCatMrtDiv.appendChild(cattext)

}

// fetch 連線json資料 搜尋景點
function getKeywordData(searching) {
    let api = "";
    const keyword = document.getElementById("keyword").value
    console.log(keyword)
    if (searching) {
        api = `/api/attractions?page=${nextpage}&keyword=${keyword}`
    } else {
        api = `/api/attractions?page=${nextpage}`
    }
    console.log(api)
    fetch(api)
        .then(function (response) {
            return response.json()
        }).then(function (data) {
            console.log(data)
            let resultData = data.data
            nextpage = data.nextPage
            if (resultData.length !== 0 ) {
                console.log(resultData.length)
                for (let i = 0; i < resultData.length; i++) {
                    const firstUrl = resultData[i].images[0]
                    attractionImg = firstUrl
                    const nameTitle = resultData[i].name
                    attractionName = nameTitle
                    const catTitle = resultData[i].category
                    attractionCat = catTitle
                    const mrtTitle = resultData[i].mrt
                    attractionMrt = mrtTitle
                    const id =resultData[i].id
                    
                    newAttractions(id)
                }
            }else{
                let content = document.getElementById("content")
                let not_data = document.createElement("div")
                not_data.textContent = "找不到「 " + keyword + "」的相關資料"
                content.appendChild(not_data)
            }

        })
        .catch(function (err) {
            console.log("錯誤訊息", err)
        })
}

// 當視窗觸及觀察目標(footer)時，就載入下一頁景點；page==null結束觀察
let callback = (entries, observer) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            if (nextpage != null) {
                if (nextpage > 0) {
                    getKeywordData(true);
                }
            } else {
                observer.unobserve(footer)
            }
        }
    })
}

let options = {
    root: null,
    rootMargin: '10px',
    threshold: 0.25
}

let observer = new IntersectionObserver(callback, options);

const footer = document.getElementById("footer");
observer.observe(footer);


let ListItems = " ";
fetch(`/api/categories`
)
    .then(function (response) {
        return response.json()
    }).then(function (data) {
        let catData = data.data;
        for (let i = 0; i < catData.length; i++) {
            const searchListItem = data.data[i];
            ListItems = searchListItem
            newListItem(ListItems)
        }
    })

function newListItem() {
    let searchlistDiv = document.createElement("div")
    searchlistDiv.classList.add("searchlistItems")
    searchlistDiv.setAttribute("id", "searchlistItems")


    const searchlist = document.getElementById("searchlist")
    searchlist.appendChild(searchlistDiv)
    let itemsText = document.createTextNode(ListItems)
    searchlistDiv.appendChild(itemsText)

}


