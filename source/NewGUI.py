"""
86868686 86    86 86868686  868686  86868686 86     86  868686  
86       86#   86 86       86    86 86       86     86 86    86 
86       8686  86 86       86       86       86     86 86       
868686   86 86 86 868686    868686  868686   86868686#  868686  
86       86  8686 86             86 86       86     86       86 
86       86   86# 86       86    86 86       86     86 86    86 
86868686 86    86 86868686  868686  86868686 86     86  868686       

Author: enesehs
Email: enesehs@protonmail.com
Website: https://www.enesehs.me
Version: 0.1 Pre-Alpha
Script: NewGUI.py
Builder: cx_Freeze
Build Script: build.py
Build Command: python build.py build
License: GNU General Public License v3.0
"""

import os
import cv2
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox, filedialog
import configparser
import pywinstyles
import winsound
from cryptography.fernet import Fernet
import win32com.client
import win32com
import winreg


class SidebarWindow:
    SIDEBAR_WIDTH = 250
    ANIMATION_STEPS = 50
    ANIMATION_DELAY = 1


class Texts:
    version = "Aether® v0.1 Pre-Alpha"

class Colors:
    bg_color = "#212121"
    sidebar_bg = "#252525" 
    button_bg = "#272727"
    button_hover_bg = "#212121"
    text_color = "#B3CEFF"

class SplashScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Splash Screen")
        self.root.geometry("800x600+{}+{}".format(
            int((self.root.winfo_screenwidth() / 2) - (800 / 2)),
            int((self.root.winfo_screenheight() / 2) - (600 / 2))
        ))
        self.root.overrideredirect(True)
        self.root.resizable(False, False)
        self.root.wm_attributes("-topmost", True)

        self.canvas = tk.Canvas(self.root, width=800, height=600, bg=Colors.bg_color, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.circles = []
        for i in range(5):
            circle = self.canvas.create_oval(400, 300, 400, 300, outline="#ffffff", width=2)
            self.circles.append(circle)

        self.animate_circles()

        logo_path = "img/Logo.png"
        if os.path.exists(logo_path):
            logo_image = Image.open(logo_path)
            logo_image = logo_image.resize((320, 320), Image.Resampling.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_image)
            self.logo_id = self.canvas.create_image(
            400, 300, image=self.logo, anchor="center")

        winsound.PlaySound("sound/intro.wav", winsound.SND_ASYNC)
        self.root.after(3000, self.close_splash)

    def animate_circles(self):
        def update_circles(step=0, size=0):
            if step < 120:
                size += 8
                for i, circle in enumerate(self.circles):
                    delay = i * 5
                    if step >= delay:
                        x1 = 400 - size + (i * 10)-9
                        y1 = 300 - size + (i * 10)-90
                        x2 = 400 + size - (i * 10)-9
                        y2 = 300 + size - (i * 10)-90
                        self.canvas.coords(circle, x1, y1, x2, y2)
                        self.canvas.itemconfig(circle, outline="#ffffff")
                self.root.after(16, lambda: update_circles(step + 1, size))
            elif step < 180:
                opacity = 1 - ((step - 120) / 60)
                for circle in self.circles:
                    self.canvas.itemconfig(circle, width=2 * opacity)
            else:
                for circle in self.circles:
                    self.canvas.delete(circle)

        update_circles()

    def close_splash(self):
        self.root.destroy()
        MainApp()



#MainApp class
class MainApp:
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Aether")
        self.root.iconbitmap("img/main.ico")
        self.root.geometry("800x600+{}+{}".format(
            int((self.root.winfo_screenwidth() / 2) - (800 / 2)),
            int((self.root.winfo_screenheight() / 2) - (600 / 2))
        ))
        self.config_file = "settings.ini"
        self.camera_var = None
        self.config = configparser.ConfigParser()
        
        self.autorun_var = tk.BooleanVar(value=False)
        self.encrypt_var = tk.BooleanVar(value=False)
        self.compress_var = tk.BooleanVar(value=False)
        self.logging_var = tk.BooleanVar(value=False)
        
        self.load_or_create_config()
        
        self.root.resizable(False, False)
        self.root.config(bg=Colors.bg_color)
        pywinstyles.apply_style(self.root, "mica")
        
        self.is_sidebar_open = True
        self.sidebar_width = SidebarWindow.SIDEBAR_WIDTH
        
        self.sidebar = tk.Frame(self.root, bg=Colors.sidebar_bg, width=self.sidebar_width)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        
        self.logo_img = tk.PhotoImage(file="img/LogoMT.png").subsample(2, 2)
        self.logo = tk.Label(self.sidebar, image=self.logo_img, bg=Colors.sidebar_bg)
        self.logo.place(x=50, y=20)

        button_frame = tk.Frame(self.sidebar, bg=Colors.sidebar_bg)
        button_frame.pack(fill="x", pady=50)
        button_frame.place(x=0, y=100, relwidth=1)

        sidebar_buttons = [
            ("Settings", self.open_settings),
            ("About", self.open_about),
            ("Config", self.open_config),
            ("Help", self.open_help),
        ]

        self.buttons = []
        for text, command in sidebar_buttons:
            button = tk.Button(
            button_frame, text=text, 
            command=command,
            bg=Colors.sidebar_bg, 
            fg=Colors.text_color,
            font=("Mona sans", 12), 
            bd=0,
            activebackground=Colors.bg_color,
            activeforeground="#ffffff",
            width=25, height=1
            )
            button.pack(pady=5)
            button.bind("<Enter>", lambda e, btn=button: self.on_hover(btn, True))
            button.bind("<Leave>", lambda e, btn=button: self.on_hover(btn, False))
            self.buttons.append(button)

        self.version_label = tk.Label(self.sidebar, text=Texts.version,  
            fg=Colors.text_color, bg=Colors.sidebar_bg,
            font=("Mona Sans Light", 10))
        self.version_label.pack(side="bottom", pady=10)

        self.content = tk.Frame(self.root, bg=Colors.bg_color)
        self.content.pack(side="right", fill="both", expand=True)

        self.open_settings()
        
        self.root.mainloop()
    on_hover = lambda self, btn, is_hover: (
            btn.config(bg=Colors.bg_color if is_hover else Colors.sidebar_bg),
            winsound.PlaySound("sound/hover.wav", winsound.SND_ASYNC) if is_hover else None
        )
    
    def open_settings(self):
        self.clear_content()
        tk.Label(self.content, text="Settings Page", font=("Mona sans", 16), fg="white", bg=Colors.bg_color).pack(pady=20)
        self.toggle_btn = tk.Button(
            self.root, text="☰", command=lambda: self.toggle_sidebar(),
            bg=Colors.button_bg, fg=Colors.text_color,
            font=("Mona sans", 12), bd=0,
            activebackground=Colors.button_hover_bg,
            activeforeground=Colors.text_color,
            width=3, height=1
        )
        self.toggle_btn.place(x=(self.sidebar_width if self.is_sidebar_open else 10) + 10, y=10)
        self.Settings()


    def open_about(self):
        self.clear_content()
        tk.Label(self.content, text="About Page", font=("Mona sans", 16), fg="white", bg=Colors.bg_color).pack(pady=20)
        self.About()

    def open_config(self):
        self.clear_content()
        tk.Label(self.content, text="Config Page", font=("Mona sans", 16), fg="white", bg=Colors.bg_color).pack(pady=20)
        self.Configs()

    def open_help(self):
        self.clear_content()
        tk.Label(self.content, text="Help Page", font=("Mona sans", 16), fg="white", bg=Colors.bg_color).pack(pady=20)
        self.Help()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()
            
    def toggle_sidebar(self):
        target_width = 0 if self.is_sidebar_open else self.sidebar_width
        start_width = self.sidebar_width if self.is_sidebar_open else 0
        steps = 30
        
        if not self.is_sidebar_open:
            self.sidebar.pack(side="left", fill="y")
            
        def animate(current_step=0):
            if current_step <= steps:
                progress = current_step / steps
                ease = 1 - pow(1 - progress, 3)
                
                current_width = int(start_width + (target_width - start_width) * ease)
                self.sidebar.config(width=current_width)
                
                button_x = current_width + 10
                self.toggle_btn.place(x=button_x, y=10)
                
                opacity = 0.5 + 0.5 * (1 - progress if self.is_sidebar_open else progress)
                for widget in self.sidebar.winfo_children():
                    widget.configure(bg=Colors.sidebar_bg)
                
                self.root.after(8, lambda: animate(current_step + 1))
            else:
                if self.is_sidebar_open:
                    self.sidebar.pack_forget()
                self.is_sidebar_open = not self.is_sidebar_open
                


        animate()






#Frontend
    def Settings(self):
            camera_section = tk.Frame(self.content, bg=Colors.bg_color)
            camera_section.pack(fill="x", padx=20, pady=10)
            
            tk.Label(camera_section, text="Camera Configuration", 
                    fg=Colors.text_color, bg=Colors.bg_color,
                    font=("Mona Sans", 14)).pack(anchor="w")
            
            camera_frame = tk.Frame(camera_section, bg=Colors.bg_color) 
            camera_frame.pack(fill="x", pady=(5,0))

            self.camera_var = tk.StringVar(value="Choose Camera")
            camera_menu = tk.OptionMenu(camera_frame, self.camera_var, *self.list_camera())
            menu = self.root.nametowidget(camera_menu.menuname)
            menu.config(bg=Colors.button_bg, fg=Colors.text_color, font=("Mona Sans", 12)) 
            camera_menu.config(bg=Colors.button_bg, fg=Colors.text_color, 
                            font=("Mona Sans", 12),
                            activebackground=Colors.button_hover_bg,
                            activeforeground=Colors.text_color,
                            highlightthickness=0, bd=0, 
                            indicatoron=0, relief="flat")
            camera_menu.pack(side="left", fill="x", expand=True)
            
            def on_hover(event, widget, enter):
                widget.config(bg=Colors.button_hover_bg if enter else Colors.button_bg)
                if enter:
                    winsound.PlaySound("sound/hover.wav", winsound.SND_ASYNC)
            
            camera_menu.bind("<Enter>", lambda e: on_hover(e, camera_menu, True))
            camera_menu.bind("<Leave>", lambda e: on_hover(e, camera_menu, False))
            camera_menu.bind("<Button-1>", lambda e: winsound.PlaySound("sound/click.wav", winsound.SND_ASYNC))

            test_btn = tk.Button(camera_frame, text="Test",
                                bg=Colors.button_bg, fg=Colors.text_color,
                                font=("Mona Sans", 10), bd=0, padx=8,
                                activebackground=Colors.button_hover_bg,
                                activeforeground="#ffffff",
                                command=self.test_camera)
            test_btn.bind("<Enter>", lambda e: on_hover(e, test_btn, True))
            test_btn.bind("<Leave>", lambda e: on_hover(e, test_btn, False))
            test_btn.bind("<Button-1>", lambda e: winsound.PlaySound("sound/click.wav", winsound.SND_ASYNC))
            test_btn.pack(side="left", padx=(5,0))

            select_btn = tk.Button(camera_section, text="Select Camera",
                                bg=Colors.button_bg, fg=Colors.text_color, 
                                font=("Mona Sans", 12), bd=0,
                                activebackground=Colors.button_hover_bg,
                                activeforeground="#ffffff",
                                command=self.select_camera)
            select_btn.bind("<Enter>", lambda e: on_hover(e, select_btn, True))
            select_btn.bind("<Leave>", lambda e: on_hover(e, select_btn, False))
            select_btn.bind("<Button-1>", lambda e: winsound.PlaySound("sound/click.wav", winsound.SND_ASYNC))
            select_btn.pack(pady=5, fill="x")
            
            config_frame = tk.Frame(self.content, bg=Colors.bg_color)
            config_frame.pack(fill="x", padx=20, pady=(20, 10))

            security_section = tk.Frame(config_frame, bg=Colors.bg_color)
            security_section.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

            tk.Label(security_section, text="Security Configuration",
                    fg=Colors.text_color, bg=Colors.bg_color,
                    font=("Mona Sans", 14)).pack(anchor="w")

            security_frame = tk.Frame(security_section, bg=Colors.bg_color)
            security_frame.pack(fill="x", pady=(5, 0))

            tooltips = {
                "Auto-Start": "Automatically starts the capture process when you log in to Windows",
                "Encryption": "Encrypts captured images using your specified password",
                "Compression": "Compresses captured images to save disk space",
                "Logging": "Keeps track of application events and activities"
            }

            toggles = [
                ("Auto-Start", self.config.getboolean("Settings", "AutoStart", fallback=False)),
                ("Encryption", self.config.getboolean("Settings", "encryption", fallback=False)),
                ("Compression", self.config.getboolean("Settings", "compress", fallback=False)), 
                ("Logging", self.config.getboolean("Settings", "logging", fallback=False))
            ]

            self.toggle_vars = {}
            for text, default in toggles:
                toggle_frame = tk.Frame(security_frame, bg=Colors.bg_color)
                toggle_frame.pack(fill="x", pady=5)

                label = tk.Label(toggle_frame, text=text,
                        bg=Colors.bg_color, fg=Colors.text_color,
                        font=("Mona Sans", 12))
                label.pack(side="left")

                def show_tooltip(event, text=text):
                    tooltip = tk.Toplevel()
                    tooltip.wm_overrideredirect(True)
                    tooltip.config(bg=Colors.bg_color)
                    
                    x = event.widget.winfo_rootx()
                    y = event.widget.winfo_rooty() - 30
                    tooltip.geometry(f"+{x}+{y}")
                    
                    tk.Label(tooltip, text=tooltips[text],
                            bg=Colors.bg_color, fg=Colors.text_color,
                            font=("Mona Sans", 10), padx=5, pady=2).pack()
                    
                    def hide_tooltip(e):
                        tooltip.destroy()
                    
                    event.widget.bind("<Leave>", hide_tooltip)
                    tooltip.bind("<Leave>", hide_tooltip)

                label.bind("<Enter>", show_tooltip)

                switch_frame = tk.Frame(toggle_frame, width=40, height=20, 
                                    bg=Colors.button_bg, relief="flat")
                switch_frame.pack(side="right")
                switch_frame.pack_propagate(False)

                var = tk.BooleanVar(value=default)
                self.toggle_vars[text] = var

                knob = tk.Frame(switch_frame, width=16, height=16, 
                            bg=Colors.text_color if default else "#666666")
                knob.place(relx=0.7 if default else 0.3, rely=0.5, anchor="center")

                def toggle(e, sf=switch_frame, k=knob, v=var, t=text):
                    v.set(not v.get())
                    k.place(relx=0.7 if v.get() else 0.3, rely=0.5, anchor="center")
                    k.config(bg=Colors.text_color if v.get() else "#666666")
                    winsound.PlaySound("sound/click.wav", winsound.SND_ASYNC)
                    
                    # Sync encryption and compression toggles
                    if t == "Encryption":
                        if v.get():
                            try:
                                comp_frame = [c for c in security_frame.winfo_children() 
                                            if isinstance(c, tk.Frame)][2]
                                comp_knob = comp_frame.winfo_children()[1].winfo_children()[0]
                                
                                self.toggle_vars["Compression"].set(True)
                                comp_knob.place(relx=0.7, rely=0.5, anchor="center")
                                comp_knob.config(bg=Colors.text_color)
                                
                                self.config["Settings"]["compress"] = "True"
                                
                            except (IndexError, AttributeError) as e:
                                print(f"Error updating compression toggle: {e}")
                                
                    elif t == "Compression":
                        if not v.get() and self.toggle_vars["Encryption"].get():
                            try:
                                enc_frame = [c for c in security_frame.winfo_children() 
                                            if isinstance(c, tk.Frame)][1]
                                enc_knob = enc_frame.winfo_children()[1].winfo_children()[0]
                                
                                self.toggle_vars["Encryption"].set(False)
                                enc_knob.place(relx=0.3, rely=0.5, anchor="center") 
                                enc_knob.config(bg="#666666")
                                
                                self.config["Settings"]["encryption"] = "False"
                                
                            except (IndexError, AttributeError) as e:
                                print(f"Error updating encryption toggle: {e}")

                    # Update config when toggle changes
                    config_keys = {
                        "Auto-Start": "AutoStart",
                        "Encryption": "encryption", 
                        "Compression": "compress",
                        "Logging": "logging"
                    }
                    self.config["Settings"][config_keys[t]] = str(v.get())
                    self.save_config()

                    if t == "Auto-Start":
                        if v.get():
                            self.create_task_scheduler()
                        else:
                            self.delete_task("AetherAutoStart")
                    
                    # Update config when toggle changes
                    config_keys = {
                        "Auto-Start": "AutoStart",
                        "Encryption": "encryption", 
                        "Compression": "compress",
                        "Logging": "logging"
                    }
                    self.config["Settings"][config_keys[t]] = str(v.get())
                    self.save_config()

                switch_frame.bind("<Button-1>", toggle)
                knob.bind("<Button-1>", toggle)

            
            # Save Location section
            save_location_section = tk.Frame(config_frame, bg=Colors.bg_color)
            save_location_section.grid(row=0, column=1, sticky="nsew")  # Add it next to security_section

            tk.Label(save_location_section, text="Save Location",
                    fg=Colors.text_color, bg=Colors.bg_color,
                    font=("Mona Sans", 14)).pack(anchor="w")

            save_location_frame = tk.Frame(save_location_section, bg=Colors.bg_color)
            save_location_frame.pack(fill="x", pady=(5, 0))

            # Save location entry
            self.save_location_var = tk.StringVar(value="")
            save_entry = tk.Entry(save_location_frame, textvariable=self.save_location_var,
                                bg=Colors.button_bg, fg=Colors.text_color,
                                insertbackground=Colors.text_color,
                                font=("Mona Sans", 12))
            save_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

            # Browse button
            browse_btn = tk.Button(save_location_frame, text="Browse",
                                bg=Colors.button_bg, fg=Colors.text_color,
                                font=("Mona Sans", 10), bd=0, padx=8,
                                activebackground=Colors.button_hover_bg,
                                activeforeground=Colors.text_color,
                                command=self.browse_loc)
            browse_btn.bind("<Enter>", lambda e: on_hover(e, browse_btn, True))
            browse_btn.bind("<Leave>", lambda e: on_hover(e, browse_btn, False))
            browse_btn.pack(side="left")

            # Save changes button
            save_btn = tk.Button(save_location_section, text="Save Location",
                                bg=Colors.button_bg, fg=Colors.text_color,
                                font=("Mona Sans", 12), bd=0,
                                activebackground=Colors.button_hover_bg,
                                activeforeground=Colors.text_color,
                                command=self.save_loc)
            save_btn.bind("<Enter>", lambda e: on_hover(e, save_btn, True))
            save_btn.bind("<Leave>", lambda e: on_hover(e, save_btn, False))
            save_btn.pack(pady=10, fill="x")

            # Configure grid weights for resizing
            config_frame.columnconfigure(0, weight=1)
            config_frame.columnconfigure(1, weight=1)
            
            # Password Management section
            password_section = tk.Frame(self.content, bg=Colors.bg_color)
            password_section.pack(fill="x", padx=20, pady=10)

            tk.Label(password_section, text="Password Management",
                fg=Colors.text_color, bg=Colors.bg_color,
                font=("Mona Sans", 14)).pack(anchor="w")

            password_frame = tk.Frame(password_section, bg=Colors.bg_color)
            password_frame.pack(fill="x", pady=5)

            password_entry = tk.Entry(password_frame, show="•",
                        bg=Colors.button_bg, fg=Colors.text_color,
                        insertbackground=Colors.text_color,
                        font=("Mona Sans", 12))
            password_entry.pack(side="left", expand=True, fill="x")

            show_var = tk.BooleanVar()
            self.show_img = tk.PhotoImage(file="img/Show.png").subsample(15)
            self.hide_img = tk.PhotoImage(file="img/Hide.png").subsample(15)

            show_label = tk.Label(password_frame, image=self.show_img, bg=Colors.bg_color)
            show_label.bind("<Button-1>", lambda e: [show_var.set(not show_var.get()),
                                self.toggle_password_visibility(password_entry, show_var, show_label),
                                winsound.PlaySound("sound/click.wav", winsound.SND_ASYNC)])
            show_label.pack(side="left")

            password_manager = PasswordManager()
            # Create frame for buttons
            btn_frame = tk.Frame(password_section, bg=Colors.bg_color)
            btn_frame.pack(fill="x", pady=20)

            # Save password button
            pass_save_btn = tk.Button(btn_frame, text="Save Password",
                        bg=Colors.button_bg, fg=Colors.text_color,
                        font=("Mona Sans", 12),
                        activebackground=Colors.bg_color,
                        bd=0, padx=20, pady=10,
                        command=lambda: [
                        password_manager.save_password(password_entry.get()),
                        winsound.PlaySound("sound/click.wav", winsound.SND_ASYNC)
                        ])
            pass_save_btn.pack(side="left", expand=True)

            # Rules tooltip text
            rules_text = """Password Tips:
            • Password security is your responsibility
            • Password must not contain non-ASCII characters (ü,ğ,ş,ı,é,α,β etc.)
            • If your file is already encrypted, delete the old file before setting a new password
            • Use different passwords for different files to enhance security
            • Make regular backups of your encrypted files"""

            # Show/hide tooltip on hover
            def show_rules(event):
                tooltip = tk.Toplevel()
                tooltip.overrideredirect(True)
                tooltip.config(bg=Colors.bg_color)
                
                x = pass_save_btn.winfo_rootx()
                y = pass_save_btn.winfo_rooty() - 120
                tooltip.geometry(f"+{x}+{y}")
                
                tk.Label(tooltip, text=rules_text,
                        bg=Colors.bg_color, fg=Colors.text_color,
                        font=("Mona Sans", 10), justify="left",
                        padx=10, pady=5).pack()
                
                def hide_tooltip(e):
                    tooltip.destroy()
                
                pass_save_btn.bind("<Leave>", hide_tooltip)
                tooltip.bind("<Leave>", hide_tooltip)
            
            # Combined hover handler
            def on_hover_combined(event, enter):
                pass_save_btn.config(bg=Colors.button_hover_bg if enter else Colors.button_bg)
                if enter:
                    winsound.PlaySound("sound/hover.wav", winsound.SND_ASYNC) 
                    show_rules(event)

            pass_save_btn.bind("<Enter>", lambda e: on_hover_combined(e, True))
            pass_save_btn.bind("<Leave>", lambda e: on_hover_combined(e, False))
            pass_save_btn.pack(side="left", padx=5)
            


    def toggle_password_visibility(self, entry, var, button):
                if var.get():
                    entry.config(show="")
                    button.config(image=self.hide_img)
                else:
                    entry.config(show="•")
                    button.config(image=self.show_img)


    def About(self):
        # Main container for about section
        about_container = tk.Frame(self.content, bg=Colors.bg_color)
        about_container.pack(expand=True, fill="both", padx=20, pady=10)
        
        # Logo
        self.about_logo_img = tk.PhotoImage(file="img/LogoMT.png").subsample(2, 2)
        tk.Label(about_container, image=self.about_logo_img, bg=Colors.bg_color).pack(pady=20)
        
        # Version
        tk.Label(about_container,
                text=Texts.version,
                font=("Mona Sans", 12),
                fg=Colors.text_color,
                bg=Colors.bg_color).pack(pady=(0, 20))
        
        # Description
        description = """Aether is an open-source software designed for privacy. It logs computer logins and captures images, encrypting and saving them localy.

Aether does not store data, connect to servers, or transmit metadata. It operates entirely locally to ensure privacy.

        Features:
        • Secure local photo capture on session sign-in
        • Advanced encryption and compression
        • Private data storage - no external servers
        • Local activity logging
        • Fully configurable privacy settings
        
    Need help? Visit: https//enesehs.me
    Contact: enesehs@protonmail.com

Made by Enesehs with ♥"""
        
        tk.Label(about_container,
                text=description,
                font=("Mona Sans", 11),
                fg=Colors.text_color,
                bg=Colors.bg_color,
                justify="left",
                wraplength=500).pack(pady=10)
        
    def Configs(self):
        # Main container
        main_container = tk.Frame(self.content, bg=Colors.bg_color)
        main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Language section
        language_section = tk.LabelFrame(main_container, text="Language Selection",
            bg=Colors.bg_color, fg=Colors.text_color,
            font=("Mona Sans", 14), bd=0, highlightthickness=0, relief="flat")
        language_section.pack(fill="x", pady=(0, 20))

        self.language_var = tk.StringVar(value=self.config.get("Settings", "Language", fallback="English"))
        languages = ["English", "Turkish", "Español", "Deutsch", "Français"]
        language_menu = tk.OptionMenu(language_section, self.language_var, *languages, 
                                    command=lambda x: [
                winsound.PlaySound("sound/sad.wav", winsound.SND_ASYNC),
                messagebox.showinfo("Under Development", 
                "This feature is currently under development.",
                icon="info")
                ])
        self._style_dropdown(language_menu)
        language_menu.pack(fill="x", padx=10, pady=10)

        # Theme section
        theme_section = tk.LabelFrame(main_container, text="Theme Selection",
            bg=Colors.bg_color, fg=Colors.text_color,
            font=("Mona Sans", 14), bd=0, highlightthickness=0, relief="flat")
        theme_section.pack(fill="x", pady=(0, 20))

        self.theme_var = tk.StringVar(value=self.config.get("Settings", "Theme", fallback="Dark"))
        themes = ["Dark", "Light", "System"]
        theme_menu = tk.OptionMenu(theme_section, self.theme_var, *themes, 
                command=lambda x: [
                winsound.PlaySound("sound/sad.wav", winsound.SND_ASYNC),
                messagebox.showinfo("Under Development", 
                "This feature is currently under development.",
                icon="info")
                ])
        self._style_dropdown(theme_menu)
        theme_menu.pack(fill="x", padx=10, pady=10)

        # Headbar menu section
        headbar_section = tk.LabelFrame(main_container, text="Menu Style",
            bg=Colors.bg_color, fg=Colors.text_color,
            font=("Mona Sans", 14), bd=0, highlightthickness=0, relief="flat")
        headbar_section.pack(fill="x")

        menu_frame = tk.Frame(headbar_section, bg=Colors.bg_color)
        menu_frame.pack(fill="x", padx=10, pady=10)
        
        
        self.style_var = tk.StringVar(value="Choose Style")
        pywstyles = ["dark", "mica", "aero", "transparent", "acrylic", "win7",
        "inverse", "popup", "native", "optimised", "light"]
        
        def apply_style(style="mica"):
            try:
                if style != "Choose Style":
                    pywinstyles.apply_style(self.root, style)
                    winsound.PlaySound("sound/success.wav", winsound.SND_ASYNC)
                    messagebox.showinfo("Success", f"Style changed to {style}")
            except Exception as e:
                winsound.PlaySound("sound/error.wav", winsound.SND_ASYNC)
                messagebox.showerror("Error", f"Could not apply style: {str(e)}")


        headbar_menu = tk.OptionMenu(menu_frame, self.style_var, *pywstyles,
                    command=apply_style)
        self._style_dropdown(headbar_menu)
        headbar_menu.pack(fill="x", padx=10, pady=10)
        
        # Add save config button
        save_config = tk.Button(main_container, text="Open Config",
                            bg=Colors.button_bg, fg=Colors.text_color,
                            font=("Mona Sans", 12), bd=0,
                            activebackground=Colors.button_hover_bg,
                            activeforeground=Colors.text_color)
        save_config.bind("<Enter>", lambda e: self.on_hover(save_config, True))
        save_config.bind("<Leave>", lambda e: self.on_hover(save_config, False))
        save_config.bind("<Button-1>", lambda e: [
            winsound.PlaySound("sound/click.wav", winsound.SND_ASYNC),
            os.system("notepad.exe settings.ini")
        ])
        save_config.pack(pady=20, fill="x", padx=10)

    def save_config_value(self, key, value):
        """Helper method to save config values"""
        if not self.config.has_section("Settings"):
            self.config.add_section("Settings")
        self.config.set("Settings", key, value)
        self.save_config()
        winsound.PlaySound("sound/click.wav", winsound.SND_ASYNC)
        
    def _style_dropdown(self, widget):
        widget.config(bg=Colors.button_bg, fg=Colors.text_color,
                    font=("Mona Sans", 12), bd=0,
                    highlightthickness=0, relief="flat",
                    activebackground=Colors.button_hover_bg,
                    activeforeground=Colors.text_color)
        menu = self.root.nametowidget(widget.menuname)
        menu.config(bg=Colors.button_bg, fg=Colors.text_color,
                font=("Mona Sans", 10), bd=0)

    def Help(self):
        # Main help container
        help_container = tk.Frame(self.content, bg=Colors.bg_color)
        help_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Title section
        title_label = tk.Label(help_container,
                        text="Help & Documentation",
                        font=("Mona Sans", 16),
                        fg=Colors.text_color,
                        bg=Colors.bg_color)
        title_label.pack(pady=(0,20))

        # Create scrollable frame
        canvas = tk.Canvas(help_container, bg=Colors.bg_color, highlightthickness=0)
        
        # Custom styled scrollbar
        scrollbar = tk.Frame(help_container, width=8, bg=Colors.bg_color)
        scroll_thumb = tk.Frame(scrollbar, bg=Colors.text_color)

        # Scrollbar functionality
        def on_scroll(event):
            canvas.yview_scroll(-1 * int(event.delta/120), "units")
            update_scroll_thumb()

        def update_scroll_thumb():
            if canvas.winfo_height() == 0:
                return
            # Get scroll position and viewport size
            first, last = canvas.yview()
            thumb_height = max(30, scrollbar.winfo_height() * (last - first))
            thumb_pos = first * (scrollbar.winfo_height() - thumb_height)
            scroll_thumb.place(x=1, y=thumb_pos, width=6, height=thumb_height)

        def start_scroll(event):
            scrollbar.bind("<B1-Motion>", drag_scroll)
            scroll_thumb.configure(bg="#ffffff")  # Brighter color when clicked

        def stop_scroll(event):
            scrollbar.unbind("<B1-Motion>")
            scroll_thumb.configure(bg=Colors.text_color)  # Return to original color

        def drag_scroll(event):
            if scrollbar.winfo_height() == 0:
                return
            fraction = event.y / scrollbar.winfo_height()
            first = min(max(fraction, 0), 1)
            canvas.yview_moveto(first)
            update_scroll_thumb()

        # Bind events
        canvas.bind_all("<MouseWheel>", on_scroll)
        scroll_thumb.bind("<Button-1>", start_scroll)
        scroll_thumb.bind("<ButtonRelease-1>", stop_scroll)
        scrollbar.bind("<Button-1>", drag_scroll)

        scrollable_frame = tk.Frame(canvas, bg=Colors.bg_color)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: [canvas.configure(scrollregion=canvas.bbox("all")), update_scroll_thumb()]
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Help sections
        sections = {
            "Camera Configuration": [
                "Select your camera from the Choose Camera section.",
                "Test your camera to ensure it is functioning correctly.",
                "Save your camera preference."
            ],
            "Storage Settings": [
                "Choose save location via Browse button",
                "Confirm location with Save button",
                "Default path is User/Pictures/Aether"
            ],
            "Security Features": [
                "Auto-Start: Automatically starts the capture process when you log in.",
                "Encryption: Encrypts captures using your specified password.",
                "Compression: Compresses captured images.",
                "Logging: Track application events and each steps."
            ],
            "Password Management": [
                "Set secure password for security.",
                "Avoid non-ASCII characters (e.g., ü, ğ, ı, ê, æ, ß)",
            ],
            "Advanced Settings": [
                "Use Task Scheduler to locate the AetherAutoStart task and",
                "customize its conditions to your preference.",
                "(e.g., Start the Capture process when a specific application launched.)",
            ],
            "Known Issues": [
                "If only Encryption is enabled in the config file, your files will",
                "neither be encrypted nor compressed.",
                "Delay on after Splash Screen is normal, is due to the OpenCV camera" 
                "detection process.",
            ]
        }

        # Create section frames
        for title, items in sections.items():
            section = tk.LabelFrame(scrollable_frame, 
                                text=title,
                                bg=Colors.bg_color,
                                fg=Colors.text_color, 
                                font=("Mona Sans", 14),
                                bd=0,
                                padx=10,
                                pady=5)
            section.pack(fill="x", pady=10)

            for item in items:
                item_label = tk.Label(section,
                                    text=f"• {item}",
                                    font=("Mona Sans", 11),
                                    fg=Colors.text_color,
                                    bg=Colors.bg_color,
                                    anchor="w",
                                    pady=2)
                item_label.pack(fill="x")

        # Support section at bottom
        support_frame = tk.Frame(scrollable_frame, bg=Colors.bg_color)
        support_frame.pack(fill="x", pady=20)

        support_label = tk.Label(support_frame,
                                text="Need additional help?",
                                font=("Mona Sans", 12),
                                fg=Colors.text_color,
                                bg=Colors.bg_color)
        support_label.pack()

        email_label = tk.Label(support_frame,
                            text="enesehs@protonmail.com",
                            font=("Mona Sans", 11),
                            fg="#0000ff",
                            bg=Colors.bg_color,
                            cursor="hand2")
        email_label.pack()

        # Pack scrollbar and canvas with better layout
        canvas.pack(side="left", fill="both", expand=True, padx=(0, 10))
        scrollbar.pack(side="right", fill="y")
        
        # Initial thumb update
        update_scroll_thumb()













        
    def load_or_create_config(self):
        try:
            if not os.path.exists(self.config_file):
                raise FileNotFoundError("Config file not found. Creating a new one.")
            
            self.config.read(self.config_file)
            if "Settings" not in self.config:
                raise KeyError("Settings section missing in config file.")
            
            
            self.autorun_var.set(self.config["Settings"].get("AutoRun", "False") == "True")
            self.compress_var.set(self.config["Settings"].get("Compression", "False") == "True")
            self.encrypt_var.set(self.config["Settings"].get("Encryption", "False") == "True")
            self.logging_var.set(self.config["Settings"].get("Logging", "False") == "True")


        except (FileNotFoundError, KeyError) as e:
            print(f"Error: {e}. Initializing default config.")
            self.config["Settings"] = {
                "autostart": "True",
                "compress": "False",
                "encryption": "False",
                "logging": "True",
                "selectedcamera": "0",
                "savelocation": os.path.expandvars(r"C:/Users/%USERNAME%/Pictures/Aether"),
                "language": "English"
            }
            self.save_config()
            winsound.PlaySound("sound/error.wav", winsound.SND_ASYNC)
            messagebox.showerror("Error", f"{e}. Default settings created.")



    def save_config(self):
        try:
            with open(self.config_file, "w") as configfile:
                self.config.write(configfile)
        except Exception as e:
            print(f"Error saving config: {e}")

    def list_camera(self):
        index = 0
        available_cameras = []
        while True:
            cap = cv2.VideoCapture(index)
            if cap.isOpened():
                available_cameras.append(f"Camera {index}")
                cap.release()  # Kamerayı serbest bırak
                index += 1
            else:
                cap.release()  # Emin olmak için serbest bırak
                break
        return available_cameras


    def select_camera(self):
        selected_camera = self.camera_var.get()
        if selected_camera == "Choose Camera":
            winsound.PlaySound("sound/error.wav", winsound.SND_ASYNC)
            messagebox.showerror("Error", "Please select a valid camera.")
            return

        camera_index = selected_camera.split(" ")[-1]
        self.config["Settings"]["SelectedCamera"] = camera_index
        self.save_config()
        winsound.PlaySound("sound/success.wav", winsound.SND_ASYNC)
        messagebox.showinfo("Camera Selected", f"Selected camera: {selected_camera}", icon = "info", parent = None)


    def test_camera(self, camera_index=None):
        if camera_index is None:
            selected_camera = self.camera_var.get()
            if selected_camera == "Select Camera":
                messagebox.showerror("Error", "Please select a valid camera.")
                return
            camera_index = int(selected_camera.split(" ")[-1])

        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            messagebox.showerror("Camera Error", "Could not open the camera.")
            return

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Error: Could not read frame.")
                    break

                cv2.imshow('Camera Test', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                if cv2.getWindowProperty('Camera Test', cv2.WND_PROP_VISIBLE) < 1:
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()

    def browse_loc(self):
        directory = filedialog.askdirectory()
        if directory:
            self.save_location_var.set(directory)
            winsound.PlaySound("sound/click.wav", winsound.SND_ASYNC)

    def save_loc(self):
        directory = self.save_location_var.get()
        if directory:
            self.config["Settings"]["SaveLocation"] = directory
            self.save_config()
            winsound.PlaySound("sound/success.wav", winsound.SND_ASYNC)
            messagebox.showinfo("Success", "Save location updated successfully.")
            
    def get_install_directory(self):
        try:
        # Registry anahtarını aç
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Aether")
            install_directory, _ = winreg.QueryValueEx(reg_key, "InstallDirectory")
            return install_directory
        except FileNotFoundError:
            return None  # Eğer anahtar bulunamazsa None döner
            
    def create_task_scheduler(self):
        install_dir = self.get_install_directory()
        if install_dir:
            exe_name = os.path.join(install_dir, "Capture.exe")
        else:
            exe_name = None  # Eğer dizin bulunamazsa, başka bir yol seçebilirsiniz
        try:
            task_name = "AetherAutoStart"
            exe_dir = install_dir


            # Task Scheduler object
            scheduler = win32com.client.Dispatch("Schedule.Service")
            scheduler.Connect()
            root_folder = scheduler.GetFolder("\\")
            task_def = scheduler.NewTask(0)

            # Trigger 1: At Logon
            logon_trigger = task_def.Triggers.Create(9)  # 9: AtLogonTrigger
            logon_trigger.Id = "LogonTrigger"
            logon_trigger.Enabled = True

            # Trigger 2: At Startup
            startup_trigger = task_def.Triggers.Create(8)  # 8: AtStartupTrigger
            startup_trigger.Id = "StartupTrigger"
            startup_trigger.Enabled = True

            # Add unlock trigger
            unlock_trigger = task_def.Triggers.Create(11)  # 11: SessionStateChangeTrigger
            unlock_trigger = win32com.client.CastTo(unlock_trigger, "ISessionStateChangeTrigger")
            unlock_trigger.Id = "UnlockTrigger" 
            unlock_trigger.StateChange = 8  # 8: SessionUnlock
            unlock_trigger.StartBoundary = "2025-01-01T00:00:00"
            unlock_trigger.EndBoundary = "2030-12-31T23:59:59"

            # Action: Run program
            action = task_def.Actions.Create(0)  # 0: Execute action
            action = win32com.client.CastTo(action, "IExecAction")  # Cast to IExecAction
            action.Path = exe_name
            action.WorkingDirectory = exe_dir
            action.Arguments = ""  # Add arguments if needed
            
            task_def.Principal.UserId = "INTERACTIVE"
            task_def.Principal.LogonType = 3  # Logon interactively
            task_def.Principal.RunLevel = 1  # Highest privileges

            task_def.Settings.Enabled = True
            task_def.Settings.Hidden = False
            task_def.Settings.Priority = 0
            task_def.Settings.DisallowStartIfOnBatteries = False
            task_def.Settings.StopIfGoingOnBatteries = False
            
            
            root_folder.RegisterTaskDefinition(
                task_name,
                task_def,
                6,  # TASK_CREATE_OR_UPDATE
                None,  # No user
                None,  # No password
                4,    # TASK_LOGON_INTERACTIVE_TOKEN
                None  # No sddl
            )

        
            print(f"Task '{task_name}' created successfully!")
        except Exception as e:
            print(f"Error creating task: {str(e)}")
            winsound.PlaySound("sound/error.wav", winsound.SND_ASYNC)
            messagebox.showerror("Error", f"Error creating task: {str(e)}")
            self.config["Settings"]["AutoStart"] = "False"


    def delete_task(self, task_name):
        try:
            from win32com import client
            import os
            from win32com.client import Dispatch
            
            scheduler = client.Dispatch("Schedule.Service")
            scheduler.Connect()
            root_folder = scheduler.GetFolder("\\")
            root_folder.DeleteTask(task_name, 0)
            print(f"Görev '{task_name}' silindi!")
        except Exception as e:
            print(f"Delete task error: {str(e)}")
            
class PasswordManager:
    def __init__(self, settings_file="settings.enc", key_file="settings.key"):
        self.settings_file = settings_file
        self.key_file = key_file

        if not os.path.exists(self.key_file):
            self.generate_key()

        with open(self.key_file, "rb") as key_file:
            self.key = key_file.read()
        self.cipher = Fernet(self.key)

    def generate_key(self):
        key = Fernet.generate_key()
        with open(self.key_file, "wb") as key_file:
            key_file.write(key)

    def save_password(self, password):
        if not password or password.isspace():
            winsound.PlaySound("sound/error.wav", winsound.SND_ASYNC)
            messagebox.showerror("Error", "Password cannot be empty")
            return
            
        encrypted_password = self.cipher.encrypt(password.encode())
        with open(self.settings_file, "wb") as settings_file:
            settings_file.write(encrypted_password)
            winsound.PlaySound("sound/success.wav", winsound.SND_ASYNC)
            messagebox.showinfo("Success", "Password saved successfully")

    def load_password(self):
        if not os.path.exists(self.settings_file):
            return None
        with open(self.settings_file, "rb") as settings_file:
            encrypted_password = settings_file.read()
        return self.cipher.decrypt(encrypted_password).decode()
    
if __name__ == "__main__":
    root = tk.Tk()
    splash = SplashScreen(root)
    root.mainloop()