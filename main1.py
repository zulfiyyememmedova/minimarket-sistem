import json
import os
import time
from datetime import datetime

# Fayl adları
USERS_FILE = 'users.json'
PRODUCTS_FILE = 'products.json'

class MiniMarket:
    def __init__(self):
        self.current_user = None
        self.products = self.load_json(PRODUCTS_FILE, self.get_default_products())
        self.users = self.load_json(USERS_FILE, self.get_default_users())

    # --- Fayl İdarəetməsi ---
    def load_json(self, filename, default_data):
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(default_data, f, indent=4)
            return default_data
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_data(self, filename, data):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def log_event(self, message):
        log_file = f"history_{self.current_user['username']}.log"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {message}\n")

    # --- Default Məlumatlar ---
    def get_default_users(self):
        return [{"username": "student1", "password": "1234", "balance": 100.0, "failed_attempts": 0, "lock_until": None}]

    def get_default_products(self):
        return {
            "Geyimlər": [{"id": 1, "name": "T-Shirt", "price": 12.50}, {"id": 2, "name": "Hoodie", "price": 45.00}, {"id": 3, "name": "Jeans", "price": 60.00}],
            "Elektronika": [{"id": 1, "name": "Qulaqlıq", "price": 35.00}, {"id": 2, "name": "Powerbank", "price": 25.00}, {"id": 3, "name": "Siçan", "price": 15.00}],
            "Kitablar": [{"id": 1, "name": "Algorithms 101", "price": 20.00}, {"id": 2, "name": "Clean Code", "price": 55.00}, {"id": 3, "name": "Python Basics", "price": 30.00}]
        }

    # --- Login Sistemi ---
    def login(self):
        while True:
            username = input("İstifadəçi adı: ")
            user = next((u for u in self.users if u['username'] == username), None)
            
            if not user:
                print("İstifadəçi tapılmadı.")
                continue

            # Cooldown yoxlanışı
            if user['lock_until'] and time.time() < user['lock_until']:
                remaining = int(user['lock_until'] - time.time())
                print(f"Hesab bloklanıb. {remaining} saniyə gözləyin.")
                time.sleep(1)
                continue

            password = input("Şifrə: ")
            if user['password'] == password:
                user['failed_attempts'] = 0
                user['lock_until'] = None
                self.current_user = user
                self.save_data(USERS_FILE, self.users)
                self.log_event("LOGIN_SUCCESS")
                print(f"\nXoş gəldiniz, {username}!")
                return True
            else:
                user['failed_attempts'] += 1
                self.log_event("LOGIN_FAIL (wrong password)")
                if user['failed_attempts'] >= 3:
                    user['lock_until'] = time.time() + 10
                    user['failed_attempts'] = 0
                    print("3 dəfə səhv cəhd! 10 saniyə cooldown tətbiq edildi.")
                else:
                    print(f"Səhv şifrə! Qalan cəhd: {3 - user['failed_attempts']}")
                self.save_data(USERS_FILE, self.users)

    # --- Əsas Menyular ---
    def main_menu(self):
        while True:
            print("\n--- ƏSAS MENYU ---")
            print("1) Kateqoriyalar\n2) Səbətim\n3) Favoritlərim\n4) Tarixçə\n5) Settings\n6) Balans\n0) Çıxış")
            choice = input("Seçiminiz: ")

            if choice == '1': self.show_categories()
            elif choice == '2': self.show_basket()
            elif choice == '3': self.show_favorites()
            elif choice == '4': self.show_history()
            elif choice == '5': self.change_password()
            elif choice == '6': print(f"Balansınız: {self.current_user['balance']} AZN")
            elif choice == '0': break

    def show_categories(self):
        categories = list(self.products.keys())
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        
        c_idx = int(input("Kateqoriya seçin (və ya 0): ")) - 1
        if 0 <= c_idx < len(categories):
            cat_name = categories[c_idx]
            print(f"\n--- {cat_name} ---")
            for p in self.products[cat_name]:
                print(f"[{p['id']}] {p['name']} - {p['price']} AZN")
            
            p_id = int(input("Məhsul ID seçin: "))
            product = next((p for p in self.products[cat_name] if p['id'] == p_id), None)
            
            if product:
                qty = int(input("Miqdar: "))
                if qty <= 0: return print("Səhv miqdar!")
                
                opt = input("B (Səbət), F (Favorit), X (Ləğv): ").upper()
                if opt == 'B':
                    self.add_to_basket(cat_name, product, qty)
                elif opt == 'F':
                    self.add_to_favorites(cat_name, product)

    # --- Səbət və Checkout ---
    def add_to_basket(self, cat, prod, qty):
        basket_file = f"basket_{self.current_user['username']}.json"
        basket = self.load_json(basket_file, [])
        item = {
            "category": cat, "product": prod['name'], 
            "unit": prod['price'], "qty": qty, 
            "line_total": prod['price'] * qty
        }
        basket.append(item)
        self.save_data(basket_file, basket)
        self.log_event(f"BASKET_ADD ({cat}/{prod['name']} x{qty})")
        print("Səbətə əlavə edildi.")

    def show_basket(self):
        basket_file = f"basket_{self.current_user['username']}.json"
        basket = self.load_json(basket_file, [])
        total = sum(item['line_total'] for item in basket)
        
        print("\n--- SƏBƏT ---")
        for i, item in enumerate(basket):
            print(f"{i}. {item['product']} x{item['qty']} = {item['line_total']} AZN")
        print(f"Cəmi: {total} AZN")
        
        cmd = input("list | qty <id> <new_qty> | remove <id> | clear | checkout | back: ").split()
        if not cmd: return
        
        if cmd[0] == 'checkout':
            if self.current_user['balance'] >= total:
                self.current_user['balance'] -= total
                self.save_data(USERS_FILE, self.users)
                # Alışları qeyd et
                p_file = f"purchases_{self.current_user['username']}.json"
                purchases = self.load_json(p_file, [])
                purchases.append({"ts": datetime.now().isoformat(), "items": basket, "total": total})
                self.save_data(p_file, purchases)
                # Təmizləmə
                self.save_data(basket_file, [])
                self.log_event(f"CHECKOUT_SUCCESS total={total}")
                print("Alış uğurla tamamlandı!")
            else:
                self.log_event("CHECKOUT_FAIL (insufficient balance)")
                print("Balans kifayət deyil!")

    # --- Favoritlər və Settings ---
    def add_to_favorites(self, cat, prod):
        fav_file = f"favorites_{self.current_user['username']}.json"
        favs = self.load_json(fav_file, [])
        if not any(f['name'] == prod['name'] for f in favs):
            favs.append({"category": cat, "id": prod['id'], "name": prod['name'], "price": prod['price']})
            self.save_data(fav_file, favs)
            self.log_event(f"FAVORITE_ADD ({prod['name']})")
            print("Favoritlərə əlavə edildi.")

    def show_favorites(self):
        fav_file = f"favorites_{self.current_user['username']}.json"
        favs = self.load_json(fav_file, [])
        print("\n--- FAVORİTLƏR ---")
        for i, f in enumerate(favs):
            print(f"{i}. {f['name']} ({f['price']} AZN)")
        
        choice = input("Səbətə atmaq üçün ID seçin (və ya 'back'): ")
        if choice.isdigit() and int(choice) < len(favs):
            item = favs[int(choice)]
            qty = int(input("Miqdar: "))
            self.add_to_basket(item['category'], {"name": item['name'], "price": item['price']}, qty)

    def change_password(self):
        old = input("Köhnə şifrə: ")
        if old == self.current_user['password']:
            new = input("Yeni şifrə (min 4 simvol): ")
            if len(new) >= 4:
                self.current_user['password'] = new
                self.save_data(USERS_FILE, self.users)
                self.log_event("PASSWORD_CHANGED")
                print("Şifrə dəyişdirildi.")
            else: print("Şifrə çox qısadır!")
        else: print("Köhnə şifrə səhvdir!")

    def show_history(self):
        log_file = f"history_{self.current_user['username']}.log"
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                lines = f.readlines()
                print("\n--- SON 20 TARİXÇƏ ---")
                for line in lines[-20:]:
                    print(line.strip())
        else: print("Tarixçə tapılmadı.")

if __name__ == "__main__":
    app = MiniMarket()
    if app.login():
        app.main_menu()