import requests
import folium
import webbrowser
import tkinter as tk
from tkinter import messagebox


class GeoTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GeoLocator Pro")
        self.root.geometry("650x500")
        self.root.configure(bg="#0F172A")
        self.root.resizable(False, False)

        self.create_ui()

    def create_ui(self):
        # Header
        tk.Label(
            self.root,
            text="🌍 GeoLocator Pro",
            font=("Arial", 24, "bold"),
            bg="#0F172A",
            fg="#38BDF8"
        ).pack(pady=20)

        tk.Label(
            self.root,
            text="Enter an IP Address to Locate",
            font=("Arial", 13),
            bg="#0F172A",
            fg="white"
        ).pack()

        # Input Frame
        input_frame = tk.Frame(self.root, bg="#0F172A")
        input_frame.pack(pady=20)

        self.ip_entry = tk.Entry(
            input_frame,
            font=("Arial", 16),
            width=25,
            bd=3
        )
        self.ip_entry.pack(side=tk.LEFT, padx=10)

        tk.Button(
            input_frame,
            text="Locate",
            font=("Arial", 14, "bold"),
            bg="#38BDF8",
            fg="black",
            command=self.fetch_location
        ).pack(side=tk.LEFT)

        # Result Frame
        self.result_frame = tk.Frame(
            self.root,
            bg="#1E293B",
            bd=2,
            relief="ridge"
        )
        self.result_frame.pack(pady=30, padx=40, fill="both", expand=True)

        self.result_label = tk.Label(
            self.result_frame,
            text="Location details will appear here",
            font=("Arial", 14),
            bg="#1E293B",
            fg="white",
            justify="left"
        )
        self.result_label.pack(pady=40)

    def fetch_location(self):
        ip = self.ip_entry.get().strip()

        if not ip:
            messagebox.showwarning("Input Error", "Please enter an IP address")
            return

        try:
            url = f"http://ip-api.com/json/{ip}"
            response = requests.get(url)
            data = response.json()

            if data["status"] == "success":
                city = data["city"]
                country = data["country"]
                region = data["regionName"]
                lat = data["lat"]
                lon = data["lon"]
                isp = data["isp"]

                result = (
                    f"📍 City: {city}\n\n"
                    f"🌎 Country: {country}\n\n"
                    f"🏙 Region: {region}\n\n"
                    f"📡 ISP: {isp}\n\n"
                    f"📌 Latitude: {lat}\n"
                    f"📌 Longitude: {lon}"
                )

                self.result_label.config(text=result)

                self.generate_map(lat, lon, city, country)

            else:
                messagebox.showerror("Error", "Invalid IP Address")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def generate_map(self, lat, lon, city, country):
        user_map = folium.Map(location=[lat, lon], zoom_start=12)

        folium.Marker(
            [lat, lon],
            popup=f"{city}, {country}",
            tooltip="IP Location"
        ).add_to(user_map)

        file_name = "ip_location_map.html"
        user_map.save(file_name)
        webbrowser.open(file_name)


# Run App
root = tk.Tk()
app = GeoTrackerApp(root)
root.mainloop()