import os
from datetime import datetime

class ImageInfo:
    def __init__(self, image: str, rank: str, date):
        self.image = image
        self.rank = rank
        if isinstance(date, str):
            self.date = datetime.strptime(date, "%d-%m-%Y").date()
        else:
            self.date = date

    @classmethod
    def from_filename(cls, filename: str):
        # filename esperado: [rank]_[date]#x.png
        # Exemplo: 1_16-05-2025#1.png
        basename = os.path.basename(filename)
        try:
            prefix, _ = basename.split("#")
            rank, date_str = prefix.split("_")
            return cls(image=filename, rank=rank, date=date_str)
        except Exception as e:
            raise ValueError(f"Nome de arquivo inválido: {filename}") from e

    def __repr__(self):
        return f"ImageInfo(image='{self.image}', rank='{self.rank}', date={self.date})"
