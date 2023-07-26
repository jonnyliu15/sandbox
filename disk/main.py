class Disk:
    pages: list[bool]
    page_size: int
    size: int

    def __init__(self, page_size: int, size: int):
        self.page_size = page_size
        self.size = size

    def store_page(self, page: str):
        pass

    def read_page(self, page_num: int):
        if page_num > self.size:
            raise OverflowError(
                "Tried to read page num {page_num} which exceeds max size of {self.size}"
            )
