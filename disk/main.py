class Disk:
    pages: list[bool]
    pageSize: int
    size: int

    def __init__(self, pageSize: int, size: int):
        self.pageSize = pageSize
        self.size = size

    def store_page(self, page: str):
        pass

    def read_page(self, pageNum: int):
        if pageNum > self.size:
            raise Exception(
                "Tried to read page num {pageNum} which exceeds max size of {self.size}"
            )
