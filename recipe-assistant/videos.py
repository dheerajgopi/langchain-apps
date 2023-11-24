from typing import List, Any

from duckduckgo_search import DDGS


def search_video(search_term: str, max_results: int = 10) -> List[dict[str, Any]]:
    """
    Utility for searching videos in DuckDuckGo.

    :param search_term: search term
    :param max_results: max number of items to be fetched from the search engine
    :returns: a list of dicts having the details of the search results
    """
    with DDGS() as ddgs:
        videos = ddgs.videos(
            keywords=search_term,
            max_results=max_results
        )

        if not videos:
            return []

        return [v for v in videos]


if __name__ == '__main__':
    vids = search_video("chicken biryani recipe")
    print(vids[0])