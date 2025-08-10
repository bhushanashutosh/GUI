import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_BASE = "http://127.0.0.1:8000"

class MarketplaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Creator-Brand Marketplace")
        self.root.geometry("900x700")
        self.root.configure(bg="#f7f7f7")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self.creators_tab = ttk.Frame(self.notebook)
        self.brands_tab = ttk.Frame(self.notebook)
        self.collabs_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.creators_tab, text="Creators")
        self.notebook.add(self.brands_tab, text="Brands")
        self.notebook.add(self.collabs_tab, text="Collaborations")

        self.setup_creators_tab()
        self.setup_brands_tab()
        self.setup_collabs_tab()

        self.refresh_all()

    def setup_creators_tab(self):
        frame = self.creators_tab

        # Register Creator
        reg_label = tk.Label(frame, text="Register Creator", font=("Arial", 14, "bold"))
        reg_label.pack(pady=10)

        self.creator_form = {}
        fields = [("Name", "name"), ("Bio", "bio"), ("Location", "location"), ("Categories (comma separated)", "categories"), ("Followers", "followers")]
        for label, key in fields:
            row = tk.Frame(frame)
            row.pack(fill="x", padx=10, pady=2)
            tk.Label(row, text=label, width=25, anchor="w").pack(side="left")
            entry = tk.Entry(row)
            entry.pack(side="left", fill="x", expand=True)
            self.creator_form[key] = entry

        reg_btn = tk.Button(frame, text="Register", command=self.register_creator, bg="#00adb5", fg="white")
        reg_btn.pack(pady=10)

        # List Creators
        list_label = tk.Label(frame, text="Creators List", font=("Arial", 14, "bold"))
        list_label.pack(pady=10)

        self.creators_listbox = tk.Listbox(frame, width=100, height=15)
        self.creators_listbox.pack(padx=10, pady=5)

    def setup_brands_tab(self):
        frame = self.brands_tab

        # Register Brand
        reg_label = tk.Label(frame, text="Register Brand", font=("Arial", 14, "bold"))
        reg_label.pack(pady=10)

        self.brand_form = {}
        fields = [("Name", "name"), ("Description", "description"), ("Location", "location"), ("Categories (comma separated)", "categories")]
        for label, key in fields:
            row = tk.Frame(frame)
            row.pack(fill="x", padx=10, pady=2)
            tk.Label(row, text=label, width=25, anchor="w").pack(side="left")
            entry = tk.Entry(row)
            entry.pack(side="left", fill="x", expand=True)
            self.brand_form[key] = entry

        reg_btn = tk.Button(frame, text="Register", command=self.register_brand, bg="#00adb5", fg="white")
        reg_btn.pack(pady=10)

        # List Brands
        list_label = tk.Label(frame, text="Brands List", font=("Arial", 14, "bold"))
        list_label.pack(pady=10)

        self.brands_listbox = tk.Listbox(frame, width=100, height=15)
        self.brands_listbox.pack(padx=10, pady=5)

    def setup_collabs_tab(self):
        frame = self.collabs_tab

        # Propose Collaboration
        prop_label = tk.Label(frame, text="Propose Collaboration", font=("Arial", 14, "bold"))
        prop_label.pack(pady=10)

        self.collab_creator_var = tk.StringVar()
        self.collab_brand_var = tk.StringVar()
        self.collab_details_entry = tk.Entry(frame, width=60)

        row1 = tk.Frame(frame)
        row1.pack(fill="x", padx=10, pady=2)
        tk.Label(row1, text="Creator", width=25, anchor="w").pack(side="left")
        self.collab_creator_menu = ttk.Combobox(row1, textvariable=self.collab_creator_var, state="readonly")
        self.collab_creator_menu.pack(side="left", fill="x", expand=True)

        row2 = tk.Frame(frame)
        row2.pack(fill="x", padx=10, pady=2)
        tk.Label(row2, text="Brand", width=25, anchor="w").pack(side="left")
        self.collab_brand_menu = ttk.Combobox(row2, textvariable=self.collab_brand_var, state="readonly")
        self.collab_brand_menu.pack(side="left", fill="x", expand=True)

        row3 = tk.Frame(frame)
        row3.pack(fill="x", padx=10, pady=2)
        tk.Label(row3, text="Details", width=25, anchor="w").pack(side="left")
        self.collab_details_entry.pack(side="left", fill="x", expand=True)

        prop_btn = tk.Button(frame, text="Propose", command=self.propose_collab, bg="#00adb5", fg="white")
        prop_btn.pack(pady=10)

        # List Collaborations
        list_label = tk.Label(frame, text="Collaborations List", font=("Arial", 14, "bold"))
        list_label.pack(pady=10)

        self.collabs_listbox = tk.Listbox(frame, width=100, height=15)
        self.collabs_listbox.pack(padx=10, pady=5)

    def register_creator(self):
        try:
            data = {
                "id": "",
                "name": self.creator_form["name"].get(),
                "bio": self.creator_form["bio"].get(),
                "location": self.creator_form["location"].get(),
                "categories": [c.strip() for c in self.creator_form["categories"].get().split(",") if c.strip()],
                "followers": int(self.creator_form["followers"].get() or 0),
                "verified": False
            }
            resp = requests.post(f"{API_BASE}/creators/", json=data)
            if resp.status_code == 200:
                messagebox.showinfo("Success", "Creator registered!")
                self.refresh_creators()
                for entry in self.creator_form.values():
                    entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", resp.text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def register_brand(self):
        try:
            data = {
                "id": "",
                "name": self.brand_form["name"].get(),
                "description": self.brand_form["description"].get(),
                "location": self.brand_form["location"].get(),
                "categories": [c.strip() for c in self.brand_form["categories"].get().split(",") if c.strip()],
                "verified": False
            }
            resp = requests.post(f"{API_BASE}/brands/", json=data)
            if resp.status_code == 200:
                messagebox.showinfo("Success", "Brand registered!")
                self.refresh_brands()
                for entry in self.brand_form.values():
                    entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", resp.text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def propose_collab(self):
        try:
            creator_id = self.collab_creator_var.get()
            brand_id = self.collab_brand_var.get()
            details = self.collab_details_entry.get()
            if not creator_id or not brand_id:
                messagebox.showerror("Error", "Select both creator and brand.")
                return
            data = {
                "id": "",
                "creator_id": creator_id,
                "brand_id": brand_id,
                "status": "pending",
                "details": details,
                "payment_verified": False
            }
            resp = requests.post(f"{API_BASE}/collaborations/", json=data)
            if resp.status_code == 200:
                messagebox.showinfo("Success", "Collaboration proposed!")
                self.refresh_collabs()
                self.collab_details_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", resp.text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_creators(self):
        try:
            resp = requests.get(f"{API_BASE}/creators/")
            creators = resp.json()
            self.creators_listbox.delete(0, tk.END)
            self.creator_choices = []
            for c in creators:
                self.creators_listbox.insert(tk.END, f"{c['name']} ({c['location']}) - {c['followers']} followers | Categories: {', '.join(c['categories'])} | Bio: {c['bio']}")
                self.creator_choices.append((c['id'], c['name']))
            self.collab_creator_menu['values'] = [c[0] for c in self.creator_choices]
        except Exception as e:
            self.creators_listbox.delete(0, tk.END)
            self.creators_listbox.insert(tk.END, f"Error loading creators: {str(e)}")

    def refresh_brands(self):
        try:
            resp = requests.get(f"{API_BASE}/brands/")
            brands = resp.json()
            self.brands_listbox.delete(0, tk.END)
            self.brand_choices = []
            for b in brands:
                self.brands_listbox.insert(tk.END, f"{b['name']} ({b['location']}) | Categories: {', '.join(b['categories'])} | Description: {b['description']}")
                self.brand_choices.append((b['id'], b['name']))
            self.collab_brand_menu['values'] = [b[0] for b in self.brand_choices]
        except Exception as e:
            self.brands_listbox.delete(0, tk.END)
            self.brands_listbox.insert(tk.END, f"Error loading brands: {str(e)}")

    def refresh_collabs(self):
        try:
            resp = requests.get(f"{API_BASE}/collaborations/")
            collabs = resp.json()
            self.collabs_listbox.delete(0, tk.END)
            for col in collabs:
                creator_name = col['creator_id']
                brand_name = col['brand_id']
                # Try to resolve names
                if hasattr(self, 'creator_choices'):
                    for cid, cname in self.creator_choices:
                        if cid == col['creator_id']:
                            creator_name = cname
                if hasattr(self, 'brand_choices'):
                    for bid, bname in self.brand_choices:
                        if bid == col['brand_id']:
                            brand_name = bname
                self.collabs_listbox.insert(tk.END, f"Creator: {creator_name} | Brand: {brand_name} | Status: {col['status']} | Details: {col['details']}")
        except Exception as e:
            self.collabs_listbox.delete(0, tk.END)
            self.collabs_listbox.insert(tk.END, f"Error loading collaborations: {str(e)}")

    def refresh_all(self):
        self.refresh_creators()
        self.refresh_brands()
        self.refresh_collabs()

if __name__ == "__main__":
    root = tk.Tk()
    app = MarketplaceApp(root)
    root.mainloop()