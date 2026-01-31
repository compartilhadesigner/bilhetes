import os

class DataManager:
    SEPARATOR = "-------------"

    def __init__(self, filename="dados.txt"):
        self.filename = filename
        if not os.path.exists(self.filename):
            open(self.filename, "w", encoding="utf-8").close()

    def _read_blocks(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            content = f.read().strip()

        if not content:
            return []

        return [block.strip() for block in content.split(self.SEPARATOR) if block.strip()]

    def _write_blocks(self, blocks):
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(f"\n{self.SEPARATOR}\n".join(blocks))

    def add(self, data: dict):
        block = "\n".join(f"{k}: {v}" for k, v in data.items())
        blocks = self._read_blocks()
        blocks.append(block)
        self._write_blocks(blocks)

    def list_all(self):
        return self._read_blocks()
