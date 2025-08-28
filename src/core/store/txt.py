import numpy as np


class TxtStore:
    def __init__(self):
        pass

    def read(self, filename: str) -> np.ndarray:
        data = np.loadtxt(
            filename,
            delimiter=",",
            comments="#",
            encoding="utf-8",
        )

        return data

    def write(self, filename: str, data: np.ndarray, meta: dict):
        header = ""
        for k, v in meta.items():
            header += f"{k}: {v}\n"
        header = header[:-1]

        np.savetxt(
            filename,
            data,
            fmt="%.6f",
            delimiter=",",
            header=header,
            comments="#",
            encoding="utf-8",
        )


if __name__ == "__main__":
    store = TxtStore()
    store.write("test.txt", np.random.rand(10), {"a": "1", "b": "2", "c": "3"})
