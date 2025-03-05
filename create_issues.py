import requests
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from dotenv import load_dotenv
from datetime import datetime

# Configuración visual
LINEA = "═" * 60
EMOJI = {
    "config": "⚙️",
    "error": "❌",
    "success": "✅",
    "warning": "⚠️",
    "issue": "📌",
    "progress": "🔄",
    "link": "🔗"
}

GITHUB_API_URL = 'https://api.github.com'

class GitHubIssueCreatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GitHub Issue Creator v1.0")
        self.geometry("800x600")
        self.resizable(True, True)
        self._configure_styles()
        self._create_widgets()
        self._load_env_if_exists()

    def _configure_styles(self):
        self.configure(bg="#121212")
        style = ttk.Style(self)
        style.theme_create("dark", settings={
            "TLabel": {
                "configure": {
                    "background": "#121212",
                    "foreground": "#E0E0E0"
                }
            },
            "TEntry": {
                "configure": {
                    "fieldbackground": "#333333",
                    "foreground": "#E0E0E0"
                }
            },
            "TButton": {
                "configure": {
                    "background": "#444444",
                    "foreground": "#E0E0E0",
                    "padding": 5
                }
            },
        })
        style.theme_use("dark")

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        config_frame = ttk.LabelFrame(main_frame, text="Configuración de GitHub", padding=10)
        config_frame.pack(fill=tk.X, pady=5)

        fields = [
            ("Token de GitHub:", 'GITHUB_TOKEN'),
            ("Dueño del Repo:", 'REPO_OWNER'),
            ("Nombre del Repo:", 'REPO_NAME')
        ]

        self.entries = {}
        for text, key in fields:
            row = ttk.Frame(config_frame)
            row.pack(fill=tk.X, pady=2)
            ttk.Label(row, text=text, width=15).pack(side=tk.LEFT)
            entry = ttk.Entry(row)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.entries[key] = entry

        params_frame = ttk.LabelFrame(main_frame, text="Parámetros de Issues", padding=10)
        params_frame.pack(fill=tk.X, pady=5)

        self.entries['TOTAL_ISSUES'] = self._create_spinbox(params_frame, "Total de Issues:", 1, 100)

        exec_frame = ttk.Frame(main_frame)
        exec_frame.pack(fill=tk.X, pady=10)
        ttk.Button(exec_frame, text="Crear Issues", command=self._execute).pack(side=tk.LEFT, padx=5)

        # Botones para limpiar la consola y los campos
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=5)
        ttk.Button(control_frame, text="Limpiar Consola", command=self.clear_console).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Limpiar Campos", command=self.clear_fields).pack(side=tk.LEFT, padx=5)

        self.output = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            height=15,
            bg="#1E1E1E",
            fg="#E0E0E0",
            insertbackground="#E0E0E0"
        )
        self.output.pack(fill=tk.BOTH, expand=True)

    def _create_spinbox(self, parent, label_text, from_, to):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=2)
        ttk.Label(frame, text=label_text, width=12).pack(side=tk.LEFT)
        spinbox = ttk.Spinbox(frame, from_=from_, to=to, width=8)
        spinbox.pack(side=tk.LEFT)
        return spinbox

    def _load_env_if_exists(self):
        if os.path.exists('.env'):
            load_dotenv()
            for key in self.entries:
                if key in os.environ:
                    self.entries[key].insert(0, os.getenv(key))

    def _validate_inputs(self):
        try:
            data = {
                'total_issues': int(self.entries['TOTAL_ISSUES'].get())
            }

            if data['total_issues'] < 1:
                messagebox.showerror("Error", "El número de issues debe ser mayor que 0")
                return None

            return data

        except ValueError:
            messagebox.showerror("Error", "El valor de Total de Issues debe ser un número entero válido")
            return None

    def _create_issue(self, title, body, issue_num, total):
        try:
            url = f"{GITHUB_API_URL}/repos/{self.entries['REPO_OWNER'].get()}/{self.entries['REPO_NAME'].get()}/issues"
            headers = {
                'Authorization': f'token {self.entries["GITHUB_TOKEN"].get()}',
                'Accept': 'application/vnd.github.v3+json'
            }
            data = {
                'title': title,
                'body': body
            }

            progress = f"[{issue_num}/{total}]"
            self.output_insert(f"{EMOJI['progress']} {progress} Creando issue: {title[:30]}...\n")

            start_time = datetime.now()
            response = requests.post(url, headers=headers, json=data)
            elapsed = (datetime.now() - start_time).total_seconds()

            if response.status_code == 201:
                issue = response.json()
                self.output_insert(f"{EMOJI['success']} {progress} Issue creado en {elapsed:.2f}s\n")
                self.output_insert(f"{EMOJI['link']} URL: {issue['html_url']}")
                return True
            else:
                self.output_insert(f"{EMOJI['error']} {progress} Error {response.status_code}\n")
                self.output_insert(f"Respuesta: {response.text[:200]}...\n")
                return False

        except Exception as e:
            self.output_insert(f"{EMOJI['error']} Error crítico: {str(e)}")
            return False

    def output_insert(self, text: str):
        self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.update_idletasks()

    def clear_console(self):
        """Limpiar la consola de salida."""
        self.output.delete(1.0, tk.END)

    def clear_fields(self):
        """Limpiar los campos de entrada."""
        for key, entry in self.entries.items():
            entry.delete(0, tk.END)

    def _execute(self):
        self.output.delete(1.0, tk.END)

        params = self._validate_inputs()
        if not params:
            return

        load_dotenv()
        github_token = os.getenv('GITHUB_TOKEN')
        repo_owner = os.getenv('REPO_OWNER')
        repo_name = os.getenv('REPO_NAME')

        if not github_token or not repo_owner or not repo_name:
            messagebox.showerror("Error", "Faltan variables en el archivo .env")
            return

        total_issues = params['total_issues']
        success_count = 0
        failed_count = 0

        self.output_insert(f"\n{EMOJI['success']} INICIANDO CREACIÓN DE {total_issues} ISSUES\n")

        for i in range(1, total_issues + 1):
            title = f'Issue {i} - {datetime.now().strftime("%Y-%m-%d")}'
            body = f"""## Descripción del issue {i}

Este es un issue generado automáticamente el {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

**Detalles:**
- Prioridad: Alta
- Tipo: Mejora
- Asignado: Equipo de desarrollo"""

            if self._create_issue(title, body, i, total_issues):
                success_count += 1
            else:
                failed_count += 1

        self.output_insert(f"\n{EMOJI['success']} Issues exitosos: {success_count}\n")
        self.output_insert(f"{EMOJI['error']} Issues fallidos: {failed_count}\n")
        self.output_insert(f"{EMOJI['issue']} Total procesados: {success_count + failed_count}\n")

        if failed_count == 0:
            self.output_insert("\n¡TODOS LOS ISSUES SE CREARON EXITOSAMENTE!\n")
        else:
            self.output_insert(f"\n{EMOJI['warning']} ALGUNOS ISSUES TUVIERON PROBLEMAS\n")

        self.output_insert(f"{EMOJI['success']} PROCESO COMPLETADO\n")

if __name__ == "__main__":
    app = GitHubIssueCreatorApp()
    app.mainloop()
