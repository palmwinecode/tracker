from threading import Thread

import emoji

import phonenumbers
from phonenumbers import geocoder
from phonenumbers import carrier

from opencage.geocoder import OpenCageGeocode

import folium

import tkinter as tk
from tkinter import messagebox, ttk, filedialog

# Open cage API key
API_KEY = "0a4f8548cfc44676a7d0b8ad8d8b6ceb"

class TrackApp:

    def __init__(self, root):
        # Create instance variables
        self.root = root
        self.phone_number = tk.StringVar()
        self.carrier = tk.StringVar()
        self.country = tk.StringVar()
        self.flag = tk.StringVar()
        self.long = tk.StringVar()
        self.lat = tk.StringVar()
        self.save = tk.BooleanVar()

        # Intilize UI
        self.initilize_ui()

    def initilize_ui(self):
        # Add an observer to the phone number entry field
        self.phone_number.trace_add("write", self.check_field)

        # Main frame
        main_frame = ttk.Frame(self.root, padding=(3, 3, 12, 12))
        # Center main_frame
        main_frame.grid(column=1, row=0, sticky="NWE")

        # Head label
        head_label = ttk.Label(main_frame, text="Location Tracker", font=("Helvetica", 16, "bold"))
        head_label.grid(column=0, row=0, sticky="NW")

        # Phone label
        phone_label = ttk.Label(main_frame, text="Enter Phone Number")
        phone_label.grid(column=0, row=1, sticky="NEW")

        # Phone entry
        self.phone_entry = ttk.Entry(main_frame, textvariable=self.phone_number)
        self.phone_entry.grid(column=0, row=2, sticky="NSEW")
        
        # Insert "+" for country code
        self.phone_entry.insert(0, "+")

        # Set focus to phone entry field
        self.phone_entry.focus()

        # Track button
        self.track_btn = ttk.Button(main_frame, text="Track", command=self.on_track, state="disabled")
        self.track_btn.grid(column=1, row=2, sticky="NEW")

        # self.root.bind("<enter>", self.on_track)

        # Result frame
        self.result_frame = ttk.Frame(main_frame, borderwidth=2, relief="solid")
        # self.result_frame.grid(column=0, row=3, columnspan=2, sticky="SEW")

        # Result labels
        # Country
        ttk.Label(self.result_frame, text="Country: ").grid(row=0, column=0, sticky="NSW")
        country_label = ttk.Label(self.result_frame, textvariable=self.country)
        country_label.grid(row=0, column=1, columnspan=2, sticky="NSEW")

        # Flag
        flag_label = ttk.Label(self.result_frame, textvariable=self.flag)
        flag_label.grid(row=0, column=2, sticky="NSEW")
        
        # Carrier
        ttk.Label(self.result_frame, text="Carrier: ").grid(row=1, column=0, sticky="NSW")
        carrier_label = ttk.Label(self.result_frame, textvariable=self.carrier)
        carrier_label.grid(row=1, column=1, sticky="NSEW")

        # Longitude
        ttk.Label(self.result_frame, text="Longitude: ").grid(row=2, column=0, sticky="NSW")
        long_label = ttk.Label(self.result_frame, textvariable=self.long)
        long_label.grid(row=2, column=1, sticky="NW")

        # Latitude
        ttk.Label(self.result_frame, text="Latitude: ").grid(row=3, column=0, sticky="NSW")
        lat_label = ttk.Label(self.result_frame, textvariable=self.lat)
        lat_label.grid(row=3, column=1, sticky="NW")

        # Check button
        check_btn = ttk.Checkbutton(self.result_frame, text="Save map file?", onvalue=True, offvalue=False, variable=self.save)
        check_btn.grid(row=4, column=0, columnspan=2, sticky="NSEW")

        # Map generate button
        generate_btn = ttk.Button(self.result_frame, text="Generate Map?", command=self.on_generate_map)
        # generate_btn = ttk.Button(self.result_frame, text="Generate Map?", command=Thread(target=self.on_generate_map).start)
        generate_btn.grid(row=5, column=0, columnspan=2, sticky="NSEW")
        
        # Configure root grid
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)

        # Configure main frame grid
        main_frame.columnconfigure(0, weight=1)

    def check_field(self, *args):
        # Check if phone number field has a value other than "+"
        if not self.phone_number.get() or len(self.phone_number.get()) < 1 and self.phone_number.get() != "+":
            # Insert "+" for country code
            self.phone_entry.insert(0, "+")

            # Disable track button
            self.track_btn.config(state="disabled")
        else:
            # Enable track button
            self.track_btn.config(state="normal")
            
    def on_track(self):
        # Check for input
        if not self.phone_number.get():
            return
        
        # Contruct phone number object
        parsed_number = phonenumbers.parse(self.phone_number.get())

        # Find country
        location = geocoder.description_for_number(parsed_number, "en")

        # Get carrier name
        carrier_name = carrier.name_for_number(parsed_number, "en")

        # Display Carrier
        self.carrier.set(carrier_name)

        # Construct open cage geocode object
        open_cage = OpenCageGeocode(API_KEY)

        # Query geocoder for details of the location tracked
        results = open_cage.geocode(str(location))
        
        # Get country flag
        flag = results[0]["annotations"]["flag"]

        # # Turn unicode to emoji
        # flag = emoji.emojize(str(flag))

        # Display location and flag
        self.country.set(f"{location} {flag}")
        # self.flag.set(flag)

        # Access longitude and latitude from JSON file
        lat = results[0]["geometry"]["lat"]
        long = results[0]["geometry"]["lng"]

        # Display longitude and latitude
        self.long.set(long)
        self.lat.set(lat)

        # Display result frame
        self.result_frame.grid(column=0, row=3, columnspan=2, sticky="SEW")

        # Expend window to accomodate result frame
        self.root.geometry("300x210")

    def on_generate_map(self):
        # Generate map
        my_map = folium.Map(location=[self.lat.get(), self.long.get()], zoom_start=9)

        # Mark location on map
        folium.Marker([float(self.lat.get()), float(self.long.get())], popup=self.country).add_to(my_map)
        folium.CircleMarker([float(self.lat.get()), float(self.long.get())], radius=300, fill_color="red").add_to(my_map)

        # Does user want to save html file?
        if self.save.get():
            save_file = filedialog.asksaveasfilename(title="Save HTML file", filetypes=[("HyperTextMarkupLanguage(HTML)", "*.html")])

            # Add extension
            save_file = save_file + ".html"

            # Save HTML file
            my_map.save(save_file)

            # Show sucess message
            messagebox.showinfo("Saved", "File has been saved successfully")

        # Open Map
        my_map.show_in_browser()
        
def main():
    # Instantiate Tk window
    root = tk.Tk()

    # Add window title
    root.title("Location Tracker")

    # Set window dimensions
    root.geometry("300x100")

    # Make window non-resizable
    root.resizable(False, False)

    # Instantiate app
    app = TrackApp(root)

    # Bind return key to on_track method
    root.bind("<Return>", app.on_track)

    # Run mainloop event
    root.mainloop()

if __name__ == "__main__":
    main()