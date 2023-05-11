from parsers.youtube_parser import getINFO
from parsers.vk_parser import parse_vk

ntv_url = "https://www.youtube.com/watch?v=Diz-6gO6wrY&t=14s&ab_channel=%D0%9D%D0%A2%D0%92%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D0%B8"
getINFO(ntv_url)
groups = [-170206299, -211210115, -26323016, 453382669, -30266386, -52620949, 561960677, 565282958, -148321046, -98331381, -216321473]
parse_vk(groups)