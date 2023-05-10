const news = document.querySelectorAll(".card");
console.log(news);
news.forEach(function (item) {
    console.log(item);
    item.addEventListener('mouseover', function(event) {
        console.log(event.target.closest('.card__image'));
    })
});