import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
from PIL import Image, ImageTk
import webbrowser
from tkinter.font import Font
import os

class ModernButton(ttk.Button):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.style = ttk.Style()
        self.style.configure('Modern.TButton', 
                            font=('Segoe UI', 14, 'bold'),
                            borderwidth=0,
                            relief='flat',
                            padding=12,
                            foreground='#ffffff',
                            background='#3498db',
                            bordercolor='#2980b9',
                            focuscolor='#2ecc71',
                            anchor='center',
                            width=20,
                            borderround=10)
        self.style.map('Modern.TButton',
                      foreground=[('active', '#ffffff'), ('disabled', '#bdc3c7')],
                      background=[('active', '#2980b9'), ('pressed', '#2c3e50')])
        self.configure(style='Modern.TButton')

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RepoSetupToolDesktop 1.0")
        self.geometry("600x400")
        self.minsize(800, 500)
        self.configure(bg='#1a1a2e')
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        
        # Configuración de fuentes
        self.title_font = Font(family='Roboto', size=24, weight='bold')
        self.button_font = Font(family='Segoe UI', size=12)
        
        self.load_resources()
        self.setup_styles()
        self.setup_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.setup_bindings()

    def setup_styles(self):
        self.style.configure('TFrame', background='#1a1a2e')
        self.style.configure('Header.TLabel', 
                           font=self.title_font,
                           background='#16213e',
                           foreground='#e94560')
        self.style.configure('Status.TLabel',
                           font=('Arial', 10),
                           background='#1a1a2e',
                           foreground='#8d8d99')
        self.style.configure('Menu.TButton',
                            font=self.button_font,
                            background='#16213e',
                            foreground='#ffffff',
                            padding=8)

    def load_resources(self):
        try:
            self.logo_image = ImageTk.PhotoImage(Image.open('logo.ico').resize((220, 80)))
            self.github_icon = ImageTk.PhotoImage(Image.open('hades.jpeg').resize((30, 30)))
        except FileNotFoundError:
            messagebox.showwarning("Recursos faltantes", 
                                   "Algunos archivos de imagen no se encontraron. Se usarán placeholders.")
            # Generar placeholders
            self.logo_image = ImageTk.PhotoImage(Image.new('RGB', (220, 80), '#16213e'))
            self.github_icon = ImageTk.PhotoImage(Image.new('RGB', (30, 30), '#e94560'))

    def setup_ui(self):
        # Header Section
        header_frame = ttk.Frame(self, style='TFrame')
        header_frame.pack(fill='x', padx=20, pady=20)
        
        logo_label = ttk.Label(header_frame, image=self.logo_image)
        logo_label.pack(side='left', padx=15)
        
        title_frame = ttk.Frame(header_frame, style='TFrame')
        title_frame.pack(side='left', padx=20)
        
        ttk.Label(title_frame, text="RepoSetupToolDesktop", style='Header.TLabel').pack(anchor='w')
        ttk.Label(title_frame, text="Gestión profesional de repositorios", 
                style='Status.TLabel').pack(anchor='w')

        # Main Content
        main_frame = ttk.Frame(self, style='TFrame')
        main_frame.pack(expand=True, fill='both', padx=40, pady=20)
        
        # Action Cards
        actions = [
            ('Generar Commit', '#2ecc71', self.open_commit_generator),
            ('Generar Issue', '#e74c3c', self.open_issue_generator),
            ('Generar PR', '#3498db', self.open_pr_generator)
        ]
        
        for idx, (text, color, command) in enumerate(actions):
            card = ttk.Frame(main_frame, style='TFrame')
            card.grid(row=0, column=idx, padx=15, pady=10, sticky='nsew')
            
            btn = ModernButton(card, 
                             text=text, 
                             command=command)
            btn.pack(expand=True, fill='both')
            btn.style.configure('Modern.TButton', background=color)
            
            ttk.Label(card, 
                     text=f"Acción {idx+1}",
                     style='Status.TLabel').pack(pady=5)
        
        main_frame.columnconfigure([0,1,2], weight=1)
        
        # Status Bar
        self.status_bar = ttk.Frame(self, style='TFrame')
        self.status_bar.pack(fill='x', side='bottom', pady=10)
        
        self.status_label = ttk.Label(self.status_bar, 
                                    text="Estado: Listo",
                                    style='Status.TLabel')
        self.status_label.pack(side='left', padx=20)
        
        ttk.Button(self.status_bar, 
                 image=self.github_icon,
                 command=self.open_docs,
                 style='Menu.TButton').pack(side='right', padx=10)

        # Setup Menu
        self.setup_menu()

    def setup_menu(self):
        menu_bar = tk.Menu(self)
        
        # Archivo Menu
        file_menu = tk.Menu(menu_bar, tearoff=0, bg='#16213e', fg='white')
        file_menu.add_command(label="Nuevo Proyecto")
        file_menu.add_command(label="Abrir")
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.on_close)
        
        # Ayuda Menu
        help_menu = tk.Menu(menu_bar, tearoff=0, bg='#16213e', fg='white')
        help_menu.add_command(label="Documentación", command=self.open_docs)
        help_menu.add_command(label="Actualizaciones")
        help_menu.add_command(label="Acerca de", command=self.show_about)
        
        menu_bar.add_cascade(label="Archivo", menu=file_menu)
        menu_bar.add_cascade(label="Ayuda", menu=help_menu)
        
        self.config(menu=menu_bar)

    def setup_bindings(self):
        self.bind_all("<Control-q>", lambda e: self.on_close())
        self.bind_all("<F1>", lambda e: self.open_docs())

    def run_script(self, script_name):
        try:
            script_path = os.path.abspath(script_name)  # Get absolute path of the script
            process = subprocess.Popen([sys.executable, script_path],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                self.update_status(f"Éxito: {script_name}")
                messagebox.showinfo("Éxito", f"{script_name} ejecutado correctamente")
            else:
                raise subprocess.CalledProcessError(process.returncode, script_name, stderr)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error ejecutando {script_name}:\n{str(e)}")
            self.update_status(f"Error: {script_name}")

    def update_status(self, message):
        self.status_label.config(text=f"Estado: {message}")
        self.after(3000, lambda: self.status_label.config(text="Estado: Listo"))

    def show_about(self):
        about_content = """
        RepoSetupToolDesktop 1.0
        
        Versión: 1.0.0
        Desarrollado por: Hades0413
        Licencia: MIT
        
        Características principales:
        - Generación automatizada de commits
        - Gestión de issues integrada
        - Sistema de PRs inteligente
        - Interfaz moderna y responsive
        """
        messagebox.showinfo("Acerca de", about_content)

    # Funciones para manejar los botones
    def open_commit_generator(self):
        self.run_script("create_commits.py")

    def open_issue_generator(self):
        self.run_script("create_issues.py")

    def open_pr_generator(self):
        self.run_script("create_pr.py")
    
    def open_docs(self):
        webbrowser.open("https://github.com/Hades0413/RepoSetupToolDesktop0413.git")

    def on_close(self):
        self.quit()

if __name__ == "__main__":
    app = App()
    app.mainloop()
