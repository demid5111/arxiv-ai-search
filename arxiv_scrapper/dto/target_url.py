class TargetURL:
    base_template = 'https://arxiv.org/list/cs/{year}{month}?skip={cur_page_index}&show={max_links_per_page}'
    max_links_per_page = 2000

    def __init__(self, year, month):
        self._year = year
        self._month = month

    def build(self, cur_page_index=0) -> str:
        return self.base_template.format(
            year=str(self._year)[-2:],
            month=str(self._month).rjust(2, '0'),  # padding months: 1 -> '01', 11 -> '11',
            cur_page_index=cur_page_index * self.max_links_per_page,
            max_links_per_page=self.max_links_per_page
        )


class ArticleURL:
    base_url='https://arxiv.org{}'
    def __init__(self, relative_url) -> None:
        self._url = self.base_url.format(relative_url)
    
    @property
    def url(self):
        return self._url        
