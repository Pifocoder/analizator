import './pages/index.css';

// import Swiper JS
import Swiper, { Navigation, Pagination, Autoplay, Mousewheel } from 'swiper';
// import Swiper styles
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import 'swiper/css/bundle';

const swiper = new Swiper(document.querySelector(".mySwiper"), {
    modules: [Navigation, Pagination, Autoplay, Mousewheel],
    direction: "horizontal",
    slidesPerView: 1,
    spaceBetween: 30,
    mousewheel: true,
    pagination: {
    el: ".swiper-pagination",
    clickable: true,
    },
    autoplay: {
        delay: 4000,
        disableOnInteraction: false,
      },
});