import os
import random
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from dotenv import load_dotenv
from datetime import datetime
from typing import Dict, Optional

DARK_THEME = {
    "background": "#121212",
    "foreground": "#E0E0E0",
    "field_bg": "#333333",
    "text_bg": "#1E1E1E",
    "button_bg": "#444444",
    "button_fg": "#E0E0E0",
    "success": "#66BB6A",
    "error": "#FF5252"
}

LINEA = "═" * 50
EMOJI = {
    "config": "⚙️",
    "commit": "📌",
    "mes": "📅",
    "progreso": "🔄",
    "exito": "✅",
    "error": "❌",
    "usuario": "👤",
    "push": "🚀",
    "advertencia": "⚠️"
}

DIAS_POR_MES = {
    1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
    7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
}

class GitManager:
    def __init__(self, env_vars: Dict[str, str], output_widget: scrolledtext.ScrolledText):
        self.env_vars = env_vars
        self.output = output_widget
        self.env = os.environ.copy()
        self.env.update({
            'GITHUB_TOKEN': env_vars['GITHUB_TOKEN'],
            'GIT_AUTHOR_DATE': '',
            'GIT_COMMITTER_DATE': ''
        })

    def run_command(self, command: str, show_output: bool = True) -> bool:
        try:
            self.output_insert(f"{EMOJI['progreso']} Ejecutando: {command}\n")
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                env=self.env,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            if show_output and result.stdout:
                self.output_insert(f"{result.stdout}\n")
            return True
        except subprocess.CalledProcessError as e:
            self.output_insert(f"{EMOJI['error']} Error en comando: {command}\n")
            self.output_insert(f"{EMOJI['error']} Detalles: {e.stderr.strip()}\n")
            return False
        except Exception as e:
            self.output_insert(f"{EMOJI['error']} Error inesperado: {str(e)}\n")
            return False

    def output_insert(self, text: str):
        self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.update_idletasks()

    def check_and_commit_changes(self):
        status_result = subprocess.run(
            "git status --porcelain",
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=self.env
        )

        if status_result.stdout:
            self.output_insert(f"{EMOJI['advertencia']} Hay cambios no confirmados. Confirmándolos...\n")
            self.run_command("git add -A", False)
            commit_message = f"commit automático {random.randint(1000, 9999)}"
            self.run_command(f'git commit -m "{commit_message}"', False)
            self.output_insert(f"{EMOJI['commit']} Cambios confirmados con mensaje: '{commit_message}'\n")


class CommitGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Generador de Commits Automatizado v1.0")
        self.geometry("800x600")
        self.resizable(True, True)
        self._configure_styles()
        self._create_widgets()
        self._load_env_if_exists()

    def _configure_styles(self):
        self.configure(bg=DARK_THEME["background"])
        style = ttk.Style(self)
        style.theme_create("dark", settings={
            "TLabel": {
                "configure": {
                    "background": DARK_THEME["background"],
                    "foreground": DARK_THEME["foreground"]
                }
            },
            "TEntry": {
                "configure": {
                    "fieldbackground": DARK_THEME["field_bg"],
                    "foreground": DARK_THEME["foreground"]
                }
            },
            "TButton": {
                "configure": {
                    "background": DARK_THEME["button_bg"],
                    "foreground": DARK_THEME["button_fg"],
                    "padding": 5
                }
            },
            "TLabelframe": {
                "configure": {
                    "background": DARK_THEME["background"],
                    "foreground": DARK_THEME["foreground"]
                }
            },
            "TLabelframe.Label": {
                "configure": {
                    "background": DARK_THEME["background"],
                    "foreground": DARK_THEME["foreground"]
                }
            }
        })
        style.theme_use("dark")

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        config_frame = ttk.LabelFrame(main_frame, text="Configuración del Repositorio", padding=10)
        config_frame.pack(fill=tk.X, pady=5)

        fields = [
            ("Token de GitHub:", 'GITHUB_TOKEN'),
            ("Dueño del Repo:", 'REPO_OWNER'),
            ("Nombre del Repo:", 'REPO_NAME'),
            ("Rama Base:", 'BASE_BRANCH'),
            ("Email del Usuario:", 'USER_EMAIL')
        ]

        self.entries = {}
        for text, key in fields:
            row = ttk.Frame(config_frame)
            row.pack(fill=tk.X, pady=2)
            ttk.Label(row, text=text, width=15).pack(side=tk.LEFT)
            entry = ttk.Entry(row)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.entries[key] = entry

        params_frame = ttk.LabelFrame(main_frame, text="Parámetros de Commits", padding=10)
        params_frame.pack(fill=tk.X, pady=5)

        self.entries['MES_INICIO'] = self._create_spinbox(params_frame, "Mes Inicio:", 1, 12)
        self.entries['MES_FIN'] = self._create_spinbox(params_frame, "Mes Fin:", 1, 12)
        self.entries['COMMITS_MES'] = self._create_spinbox(params_frame, "Commits/Mes:", 1, 1000)
        self.entries['ANO'] = self._create_spinbox(params_frame, "Año:", 2000, datetime.now().year + 1)

        exec_frame = ttk.Frame(main_frame)
        exec_frame.pack(fill=tk.X, pady=10)
        ttk.Button(exec_frame, text="Generar Commits", command=self._execute).pack(side=tk.LEFT, padx=5)
        ttk.Button(exec_frame, text="Limpiar Salida", command=self._clear_output).pack(side=tk.LEFT, padx=5)

        self.output = scrolledtext.ScrolledText(
            main_frame, 
            wrap=tk.WORD, 
            height=15,
            bg=DARK_THEME["text_bg"],
            fg=DARK_THEME["foreground"],
            insertbackground=DARK_THEME["foreground"]
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

    def _validate_inputs(self) -> Optional[Dict[str, int]]:
        try:
            data = {
                'mes_inicio': int(self.entries['MES_INICIO'].get()),
                'mes_fin': int(self.entries['MES_FIN'].get()),
                'commits_mes': int(self.entries['COMMITS_MES'].get()),
                'ano': int(self.entries['ANO'].get())
            }
            
            if data['mes_inicio'] > data['mes_fin']:
                messagebox.showerror("Error", "El mes de inicio no puede ser mayor al mes final")
                return None
                
            current_year = datetime.now().year
            if not (1990 <= data['ano'] <= current_year + 1):
                messagebox.showerror("Error", f"Año debe estar entre 1990 y {current_year + 1}")
                return None
                
            return data
            
        except ValueError:
            messagebox.showerror("Error", "Todos los valores numéricos deben ser enteros válidos")
            return None

    def _create_env_file(self):
        try:
            with open('.env', 'w') as f:
                for key in ['GITHUB_TOKEN', 'REPO_OWNER', 'REPO_NAME', 'BASE_BRANCH', 'USER_EMAIL']:
                    f.write(f"{key}={self.entries[key].get()}\n")
            messagebox.showinfo("Éxito", "Archivo .env actualizado correctamente")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error creando .env: {str(e)}")
            return False

    def _generate_commit_dates(self, mes: int, año: int, total_commits: int) -> list:
        max_days = DIAS_POR_MES[mes]
        if mes == 2 and (año % 4 == 0 and (año % 100 != 0 or año % 400 == 0)):
            max_days = 29
            
        return sorted(
            [
                datetime(
                    año, 
                    mes, 
                    random.randint(1, max_days),
                    random.randint(0, 23),
                    random.randint(0, 59)
                )
                for _ in range(total_commits)
            ],
            key=lambda x: x.timestamp()
        )

    def _show_section_title(self, text: str):
        self.output.insert(tk.END, f"\n{LINEA}\n{EMOJI['mes']} {text.center(48)} {EMOJI['mes']}\n{LINEA}\n")

    def _clear_output(self):
        self.output.delete(1.0, tk.END)

    def output_insert(self, text: str):
        self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.update_idletasks()

    def _execute(self):
        self._clear_output()
        if not self._create_env_file():
            return
            
        params = self._validate_inputs()
        if not params:
            return
            
        load_dotenv()
        env_vars = {key: os.getenv(key) for key in ['GITHUB_TOKEN', 'REPO_OWNER', 'REPO_NAME', 'BASE_BRANCH', 'USER_EMAIL']}
        
        if None in env_vars.values():
            messagebox.showerror("Error", "Faltan variables en el archivo .env")
            return

        git = GitManager(env_vars, self.output)
        
        try:
            self._show_section_title("INICIANDO PROCESO")
            git.run_command('git config --local commit.gpgsign false', False)
            git.run_command('git config pull.rebase false', False)
            git.run_command(f'git config --local user.name "{env_vars["REPO_OWNER"]}"', False)
            git.run_command(f'git config --local user.email "{env_vars["USER_EMAIL"]}"', False)
            
            self._show_section_title("SINCRONIZANDO REPOSITORIO")
            repo_url = f'https://{env_vars["REPO_OWNER"]}:{env_vars["GITHUB_TOKEN"]}@github.com/{env_vars["REPO_OWNER"]}/{env_vars["REPO_NAME"]}.git'
            git.run_command(f'git pull --allow-unrelated-histories {repo_url} {env_vars["BASE_BRANCH"]}', True)
            
            git.check_and_commit_changes()
            
            total_commits = params['commits_mes'] * (params['mes_fin'] - params['mes_inicio'] + 1)
            self._show_section_title(f"GENERANDO {total_commits} COMMITS")
            
            for mes in range(params['mes_inicio'], params['mes_fin'] + 1):
                commit_dates = self._generate_commit_dates(mes, params['ano'], params['commits_mes'])
                self.output_insert(f"\n{EMOJI['mes']} Procesando mes {mes:02d}/{params['ano']}\n")
                
                for i, date in enumerate(commit_dates, 1):
                    with open('commits.log', 'a') as f:
                        f.write(f"Commit {date.isoformat()}\n")
                        
                    git.env['GIT_AUTHOR_DATE'] = date.isoformat()
                    git.env['GIT_COMMITTER_DATE'] = date.isoformat()
                    
                    git.run_command('git add -f commits.log', False)
                    if git.run_command(f'git commit -m "Commit del {date.strftime("%d/%m/%Y")}"', False):
                        self.output_insert(f"{EMOJI['commit']} Commit {i}/{len(commit_dates)} realizado en {date.strftime('%H:%M:%S %d/%m/%Y')}\n")
            
            # Push final
            self._show_section_title("PUSH AL REPOSITORIO REMOTO")
            git.run_command(f'git pull --rebase {repo_url} {env_vars["BASE_BRANCH"]}', True)
            git.run_command(f'git push {repo_url} {env_vars["BASE_BRANCH"]}', True)

            self.output_insert(f"\n{EMOJI['exito']} Commits generados y enviados con éxito!\n")
            
        except Exception as e:
            self.output_insert(f"{EMOJI['error']} Error general: {str(e)}\n")
            return

if __name__ == "__main__":
    app = CommitGeneratorApp()
    app.mainloop()
