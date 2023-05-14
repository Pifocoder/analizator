const news = document.querySelectorAll(".card");
console.log(news);
news.forEach(function (item) {
    console.log(item);
    item.addEventListener('mouseover', function(event) {
        console.log(event.target.closest('.card__image'));
    })
});

const videos = [
    {
        title : "Велосипеды",
        url : "auqPIfVSUOM",
        statistics : [0.4, 0.5],
        statisticsNames : ["Позитивность новости", "Реакция людей"]
    },
    {
        title : "Велосипеды",
        url : "auqPIfVSUOM",
        statistics : [0.4, 0.5],
        statisticsNames : ["Позитивность новости", "Реакция людей"]
    },    
    {
        title : "Велосипеды",
        url : "auqPIfVSUOM",
        statistics : [0.4, 0.5],
        statisticsNames : ["Позитивность новости", "Реакция людей"]
    },
    {
        title : "Велосипеды",
        url : "auqPIfVSUOM",
        statistics : [0.4, 0.5],
        statisticsNames : ["Позитивность новости", "Реакция людей"]
    }
]
const posts = [
    {
        title : "Новость",
        text : "Даже если вы новичок в дизайне в поисках идеальных цветов для своего сайта, эти палитры помогут создать по-настоящему профессиональный и модный проек",
        theme : "Спорт",
        statistics : [0.4, 0.5],
        statisticsNames : ["Позитивность новости", "Реакция людей"]
    },
    {
        title : "Новость",
        text : "Даже если вы новичок в дизайне в поисках идеальных цветов для своего сайта, эти палитры помогут создать по-настоящему профессиональный и модный проек",
        theme : "Спорт",
        statistics : [0.4, 0.5],
        statisticsNames : ["Позитивность новости", "Реакция людей"]
    },
    {
        title : "Новость",
        text : "Даже если вы новичок в дизайне в поисках идеальных цветов для своего сайта, эти палитры помогут создать по-настоящему профессиональный и модный проек",
        theme : "Спорт",
        statistics : [0.4, 0.5],
        statisticsNames : ["Позитивность новости", "Реакция людей"]
    },
    {
        title : "Новость",
        text : "Даже если вы новичок в дизайне в поисках идеальных цветов для своего сайта, эти палитры помогут создать по-настоящему профессиональный и модный проек",
        theme : "Спорт",
        statistics : [0.4, 0.5],
        statisticsNames : ["Позитивность новости", "Реакция людей"]
    },
]

function addNews() {
    
}

function initMainPage() {

}