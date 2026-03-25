import json
import os

WEBSITES_FILE = os.path.join(os.path.dirname(__file__), "websites.json")


def load_websites():
    with open(WEBSITES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_websites(websites):
    with open(WEBSITES_FILE, "w", encoding="utf-8") as f:
        json.dump(websites, f, indent=2, ensure_ascii=False)


def add_website(name, link, isSA=False):
    websites = load_websites()
    for w in websites:
        if w["name"].upper() == name.upper():
            print(f"Website '{name}' ja existe.")
            return
    entry = {"name": name.upper(), "link": link}
    if isSA:
        entry["isSA"] = True
    websites.append(entry)
    save_websites(websites)
    print(f"Website '{name.upper()}' adicionado.")


def remove_website(name):
    websites = load_websites()
    new_list = [w for w in websites if w["name"].upper() != name.upper()]
    if len(new_list) == len(websites):
        print(f"Website '{name}' nao encontrado.")
        return
    save_websites(new_list)
    print(f"Website '{name.upper()}' removido.")


def list_websites():
    websites = load_websites()
    if not websites:
        print("Nenhum website cadastrado.")
        return
    for i, w in enumerate(websites, 1):
        sa = " (SA)" if w.get("isSA") else ""
        print(f"{i}. {w['name']}{sa} - {w['link']}")


if __name__ == "__main__":
    while True:
        print("\n--- Gerenciar Websites ---")
        print("1. Listar websites")
        print("2. Adicionar website")
        print("3. Remover website")
        print("4. Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            list_websites()
        elif opcao == "2":
            name = input("Nome: ").strip()
            link = input("Link: ").strip()
            is_sa = input("E SA? (s/n): ").strip().lower() == "s"
            add_website(name, link, is_sa)
        elif opcao == "3":
            list_websites()
            name = input("Nome do website para remover: ").strip()
            remove_website(name)
        elif opcao == "4":
            break
