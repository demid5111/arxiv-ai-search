"""googlesearch is a Python library for searching Google, easily."""
from time import sleep
from bs4 import BeautifulSoup
from requests import get
from .user_agents import get_useragent


def _req(term, results, lang, start, proxies, timeout):
    resp = get(
        url="https://www.google.com/search",
        headers={
            "User-Agent": get_useragent(),
            "Cookie": "HSID=A8HqGE-pHe01b3Dho; SSID=A3KgZtj1jG6MAZj5c; APISID=mFcbFI-R4dyDbE1C/AwId3DDQTxb6FKmnL; SAPISID=IDynE2s36jXDreF1/AjNf_VpxDw7sa8EIr; __Secure-1PAPISID=IDynE2s36jXDreF1/AjNf_VpxDw7sa8EIr; __Secure-3PAPISID=IDynE2s36jXDreF1/AjNf_VpxDw7sa8EIr; SEARCH_SAMESITE=CgQItJkB; SID=dQh18U8F8MwH5brbR5vn6fLSsuFgSLnKxFQI0v8M9Y4rM-8HvNbIZYp6kx88kqtBVHxDow.; __Secure-1PSID=dQh18U8F8MwH5brbR5vn6fLSsuFgSLnKxFQI0v8M9Y4rM-8HlywrMV_3hHwJAxHh7nzgQg.; __Secure-3PSID=dQh18U8F8MwH5brbR5vn6fLSsuFgSLnKxFQI0v8M9Y4rM-8H9jPWiNvffqOqZ-UFhGbRjg.; AEC=Ackid1RNCvk-ogso5VQAs_ruP6DXLd-6fEbj4nXK9i4AmvS3NCYJHIYKKg; 1P_JAR=2023-11-28-16; __Secure-1PSIDTS=sidts-CjEBNiGH7uGWFVtJW1AljZkDROA6VrKkMvOmCvTVA34n6G5l0oLAG-sTOT6guw2IxsY6EAA; __Secure-3PSIDTS=sidts-CjEBNiGH7uGWFVtJW1AljZkDROA6VrKkMvOmCvTVA34n6G5l0oLAG-sTOT6guw2IxsY6EAA; NID=511=UJSVdKYlyz6djF-bSQBTAJ12di7Xrh0drZQ_utamY3OrkstLHwhAdGfOCF2AW4iVwM-hBacR5TCnIil931h8uU6S78gQgdFzROR-n6gAHEaK4ag3IR9qgc07W4zIHeAsoY-m-0ZgkvWTd04z_lABq2pZCjlGlRbJyj9EoMEZBtKaa16ec5BXD5rqqdblq2eMKew8z7GS6YUoKNnATjqGITq4FwXfyd-1qkt5Jv9wlPBpizkS2-zols1cj05D34gDdP4bvmsV16bUNVSyngzM6OHKA2lMmLvbuhIoPllKJ2Q0mveZTRhE0n_8PdkYGG6L7Nna2VEe1fRtAG2hZBhnIy8qVvQPJtLmNY49h12-UEG4W_LOgPAGZs-qieY; DV=YxwnN4hdpX1SUOdSY-cMjB_aDL5qwRjWSxWyBWS9eAEAALDvYO7I265HmgAAABBCjJMXcI0dMAAAAI3rylNz9FMWEgAAAA; SIDCC=ACA-OxPszN3ITvLndAceYc9OlnuLoyO6URcbeM-qQy7-fC6HIx7LbLPFEa-ZotMdBgWYVCAGebGk; __Secure-1PSIDCC=ACA-OxPix79BElvO-yiGbSYXOIQ3TqagmCK-qcUM7OH0Tc7-uH7HiobgTRB4BqJHXRzfajt1yjUg; __Secure-3PSIDCC=ACA-OxODi8tJO2UJ7Hn75hY2yU_04jlY87mz2bmhdH-2mwJ60bwYD7BdR7C0aBxdAAqt26KL8_9A"
        },
        params={
            "q": term,
            "num": results + 2,  # Prevents multiple requests
            "hl": lang,
            "start": start,
        },
        proxies=proxies,
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp


class SearchResult:
    def __init__(self, url, title, description):
        self.url = url
        self.title = title
        self.description = description

    def __repr__(self):
        return f"SearchResult(url={self.url}, title={self.title}, description={self.description})"


def search(term, num_results=10, lang="en", proxy=None, advanced=False, sleep_interval=0, timeout=5):
    """Search the Google search engine"""

    escaped_term = term.replace(" ", "+")

    # Proxy
    proxies = None
    if proxy:
        if proxy.startswith("https"):
            proxies = {"https": proxy}
        else:
            proxies = {"http": proxy}

    # Fetch
    start = 0
    while start < num_results:
        # Send request
        print('request...', flush=True)
        resp = _req(escaped_term, num_results - start,
                    lang, start, proxies, timeout)
        print('now parse...', flush=True)
        # Parse
        soup = BeautifulSoup(resp.text, "html.parser")
        result_block = soup.find_all("div", attrs={"class": "g"})
        for result in result_block:
            # Find link, title, description
            link = result.find("a", href=True)
            title = result.find("h3")
            description_box = result.find(
                "div", {"style": "-webkit-line-clamp:2"})
            if description_box:
                description = description_box.text
                if link and title and description:
                    start += 1
                    if advanced:
                        yield SearchResult(link["href"], title.text, description)
                    else:
                        yield link["href"]
        print('sleep...')
        sleep(sleep_interval)
