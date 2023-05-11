from parsers.youtube_parser import getINFO
from parsers.vk_parser import parse_vk

channels = ['UCOiAwKQuFMdJuK7wwDIoKpA', 'UCdubelOloxR3wzwJG9x8YqQ', 'UCm6Ojkip8Py17C7pRhR66rA',
                'UCFzJjgVicCtFxJ5B0P_ei8A']
data = getINFO(channels)
groups = [-170206299, -211210115, -26323016, 453382669, -30266386, -52620949, 561960677, 565282958, -148321046, -98331381, -216321473]
parse_vk(groups)