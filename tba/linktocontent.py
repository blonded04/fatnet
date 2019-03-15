def link_ym(text):
    link = text.split('/album/')
    link = '/track/'.join(link)
    link = link.split('/track/')
    if "music.yandex.ru" in link[0]:
        link[0] = "https://music.yandex.ru"
    else:
        raise Exception
    if len(link[1]) != 7 or not link[1].isdigit():
        raise Exception
    link[2] = link[2][:9]
    if not link[2].isdigit():
        raise Exception
    full_link_src = link[0] + '/iframe/#track/' + link[1] + '/' + link[2] + '/'
    return '''<iframe frameborder="0" style="border:none;width:450px;height:100px;" width="450" height="100" src="{}">Слушайте <a>Track Name</a> — <a>Artist</a> на Яндекс.Музыке</iframe>'''.format(
        full_link_src)


def link_yt(text):
    link = text.split('/watch?v=')
    if "www.youtube.com" in link[0]:
        link[0] = "https://www.youtube.com"
    else:
        raise Exception
    link[1] = link[1][:11]
    if len(link[1]) != 11:
        raise Exception
    full_link_src = link[0] + '/embed/' + link[1]
    return '''<iframe width="560" height="315" src="{}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'''.format(
        full_link_src)


def linkify(text):
    if 'youtube.com' in text:
        try:
            return link_yt(text)
        except Exception:
            return text
    elif 'music.yandex.ru' in text:
        try:
            return link_ym(text)
        except Exception:
            return text
    return text
