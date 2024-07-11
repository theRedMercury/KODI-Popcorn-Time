#!/usr/bin/env python

__license__ = "GPLv3"
__version__ = "3.0.0"
__author__ = "theRedMercury"

import json
import re
from urllib.request import Request, urlopen


URL_API_SERVER = [
        "https://fusme.link",
        "https://jfper.link",
        "https://uxert.link",
        "https://yrkde.link",
        "https://movies-api.ga",
        "https://movies-api.tk",
        "https://popcorn-time.ga",
        "https://shows.cf",
    ]

def get_torrest_plugin_url(magnet_link, with_run=False) -> str:
    if with_run:
        return f"runplugin(plugin://plugin.video.torrest/play_magnet?magnet={magnet_link})"

    return f"plugin://plugin.video.torrest/play_magnet?magnet={magnet_link}"


def get_youtube_plugin_url(trailer_url) -> str:
    trailer = ""
    try:
        trailer_regex = re.match('^[^v]+v=(.{11}).*', trailer_url)
        trailer = f"plugin://plugin.video.youtube/?action=play_video&videoid={trailer_regex.group(1)}"
    except:
        pass
    return trailer


def get_stream_info_video(quality):
    if quality == "2160p":
        return {"width": 3840, "height": 2160}
    if quality == "1080p":
        return {"width": 1920, "height": 1080}
    if quality == "720p":
        return {"width": 1280, "height": 720}
    if quality == "480p":
        return {"width": 720, "height": 480}

    return {"width": 3840, "height": 2160}


class API:
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.66 Safari/537.36",
        "Accept-Encoding": "none",
    }

    genres = {
        30400: "action",
        30401: "adventure",
        30402: "animation",
        30403: "comedy",
        30404: "crime",
        30405: "disaster",
        30406: "documentary",
        30407: "drama",
        30408: "eastern",
        30409: "family",
        30410: "fan-film",
        30411: "fantasy",
        30412: "film-noir",
        30413: "history",
        30414: "horror",
        30415: "indie",
        30416: "music",
        30417: "mystery",
        30418: "road",
        30419: "romance",
        30420: "science-fiction",
        30421: "short",
        30422: "sports",
        30423: "sporting-event",
        30424: "suspense",
        30425: "thriller",
        30427: "war",
        30428: "western"
    }

    def __init__(self):
        pass

    """
    Search :    {domain}/{types}/1?keywords={keywords}
    List :      {domain}/{types}/{page}?genre={genre}&sort={sort}
    Season :    {domain}/{types}/{imdb_id}
    """

    @staticmethod
    def get_list(utils, dom_link, types, page, genre, sort_request):
        req = Request(
            f"{dom_link}/{types}/{page}?genre={genre}&sort={sort_request}",
            headers=API.header,
        )
        return API.get_request(utils, req)

    @staticmethod
    def get_list_show_all(utils, dom_link, types, id_show):
        req = Request(
            f"{dom_link}/{types}/{id_show}",
            headers=API.header,
        )
        return API.get_request(utils, req)

    @staticmethod
    def get_search(utils, dom_link, types, keywords):
        req = Request(
            f"{dom_link}/{types}/1?keywords={keywords.replace(' ', '+')}",
            headers=API.header,
        )
        return API.get_request(utils, req)

    @staticmethod
    def get_request(utils, request):
        try:
            response = urlopen(request)
            results = json.loads(response.read())
            utils.log.debug(f"API : {request.get_full_url()} > {results}")
            if len(results) == 0:
                return None
            return results

        except Exception as e:
            utils.log.warning(f"API request fail : {request.get_full_url()}")
            utils.log.warning(e)
            return None
