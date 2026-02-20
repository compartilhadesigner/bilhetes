import os
import json


class DataManager:
    def __init__(self, filename="dados.json"):
        self.filename = filename

        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=4)

    def _read_all(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return {}

        # 🔥 Se estiver no formato antigo (lista), converte
        if isinstance(data, list):
            converted = {}
            for item in data:
                customer = item.get("customer")
                if not customer:
                    continue

                entry = {k: v for k, v in item.items() if k != "customer"}

                if customer not in converted:
                    converted[customer] = []

                converted[customer].append(entry)

            # já salva convertido
            self._write_all(converted)
            return converted

        return data

    def _write_all(self, data):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def add(self, data: dict):
        all_data = self._read_all()

        customer = data.get("customer")
        if not customer:
            raise ValueError("Campo 'customer' é obrigatório")

        entry = {k: v for k, v in data.items() if k != "customer"}

        if customer not in all_data:
            all_data[customer] = []

        all_data[customer].append(entry)

        self._write_all(all_data)

    def list_all(self):
        return self._read_all()

    def list_by_customer(self, customer: str):
        all_data = self._read_all()
        return all_data.get(customer, [])