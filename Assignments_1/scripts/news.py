from typing import List


class News:
    def __init__(self, _header: str) -> None:
        self.header = _header

    def is_about_token(self, tokenName: str):
        return tokenName.casefold() in self.header.casefold()
    

class NewsBox:
    crypto: str
    news: List[News]

    def __init__(self, _crypto: str) -> None:
        self.crypto = _crypto
        self.news = []

    def deliver_news(self, news: News):
        if news.is_about_token(self.crypto):
            self.news.append(news)

    def consult(self):
        print(f"All news about {self.crypto} :")
        for n in self.news:
            print(n.header)