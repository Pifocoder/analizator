import './pages/index.css';

// import Swiper JS
import Swiper, { Navigation, Pagination, Mousewheel } from 'swiper';
// import Swiper styles
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';

const videos = [
    {
        title : "Велосипеды",
        url : "auqPIfVSUOM",
        statistics : [0.8, 0.5],
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
        title: "Новость",
        theme: "Тема",
        text: "Даже если вы новичок в дизайне в поисках идеальных цветов для своего сайта, эти палитры помогут создать по-настоящему профессиональный и модный проек",
        statistics : [0.8, 0.9],
        statisticsNames : ["Позитивность новости", "Реакция людей"]
    },
    {
        title: "Новость",
        theme: "Тема",
        text: "Даже если вы новичок в дизайне в поисках идеальных цветов для своего сайта, эти палитры помогут создать по-настоящему профессиональный и модный проек",
        statistics : [0.4, 0.5],
        statisticsNames : ["Позитивность новости", "Реакция людей"]
    },
    {
        title: "Новость",
        theme: "Тема",
        text: "Даже если вы новичок в дизайне в поисках идеальных цветов для своего сайта, эти палитры помогут создать по-настоящему профессиональный и модный проек",
        statistics : [0.4, 0.5],
        statisticsNames : ["Позитивность новости", "Реакция людей"]
    },
    {
        title: "Новость",
        theme: "Тема",
        text: "Даже если вы новичок в дизайне в поисках идеальных цветов для своего сайта, эти палитры помогут создать по-настоящему профессиональный и модный проек",
        statistics : [0.4, 0.5],
        statisticsNames : ["Позитивность новости", "Реакция людей"]
    },
    {
        title: "Новость",
        theme: "Тема",
        text: "Даже если вы новичок в дизайне в поисках идеальных цветов для своего сайта, эти палитры помогут создать по-настоящему профессиональный и модный проек",
        statistics : [0.4, 0.5],
        statisticsNames : ["Позитивность новости", "Реакция людей"]
    },
]

const header = document.querySelector('.header');
const headerSlideTemplate = header.querySelector('#swiper-slide').content;
const swiperWrapper = header.querySelector('.swiper-wrapper');
function initHeader() {
    videos.forEach(video => {
        const newSlide = headerSlideTemplate.querySelector('.swiper-slide').cloneNode(true);
        
        const newSlideImg = newSlide.querySelector('.swiper__news');
        newSlideImg.src = `//img.youtube.com/vi/${video["url"]}/maxresdefault.jpg`;
        
        newSlide.querySelector('.swiper__link').href = "#";
        newSlide.querySelector('.swiper__link').textContent = "Подробнее...";
        
        swiperWrapper.append(newSlide);
    });
}

const cardTemplate = document.querySelector('#card').content;
const cardStatTempalte = cardTemplate.querySelector('#card__stat').content;
const cardList = document.querySelector('.list');
function initNewsList() {
    posts.forEach(post => {
        const newPost = cardTemplate.querySelector('.card').cloneNode(true);
        
        newPost.querySelector('.card__preview').textContent = post["text"];
        newPost.querySelector('.card__theme').textContent = post["theme"];
        newPost.querySelector('.card__title').textContent = post["title"];

        const stats = newPost.querySelector('.card__stat-area');
        for (let i = 0; i < post["statistics"].length; ++i) {
            const newStat = cardStatTempalte.querySelector('.card__stat').cloneNode(true);
            newStat.querySelector('.card__stat-name').textContent = post["statisticsNames"][i];
            newStat.querySelector('.card__stat-line-limit').style.width = `calc(300px * 0.85 * ${post["statistics"][i]})`;
            
            stats.append(newStat);
        }
        cardList.append(newPost);
    });
}
initHeader();
initNewsList();

const swiper = new Swiper(document.querySelector(".mySwiper"), {
    modules: [Navigation, Pagination, Mousewheel],
    direction: "horizontal",
    slidesPerView: 1,
    spaceBetween: 30,
    mousewheel: true,
    pagination: {
    el: ".swiper-pagination",
    clickable: true,
    },
});