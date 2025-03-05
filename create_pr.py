import os
import random
import subprocess
import requests
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno si existen
load_dotenv()

class GitHubPRCreatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GitHub PR Creator v1.0")
        self.geometry("800x700")
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
            ("Nombre del Repo:", 'REPO_NAME'),
            ("Base Branch:", 'BASE_BRANCH'),
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

        params_frame = ttk.LabelFrame(main_frame, text="Parámetros de PR", padding=10)
        params_frame.pack(fill=tk.X, pady=5)

        self.entries['PRS_POR_MES'] = self._create_spinbox(params_frame, "PRs por mes:", 1, 10)
        self.entries['AÑO'] = self._create_spinbox(params_frame, "Año:", 2008, 2025)
        self.entries['MES_INICIO'] = self._create_spinbox(params_frame, "Mes inicio:", 1, 12)
        self.entries['MES_FIN'] = self._create_spinbox(params_frame, "Mes fin:", 1, 12)
        self.entries['HORA_INICIO'] = self._create_spinbox(params_frame, "Hora inicio:", 0, 23)
        self.entries['HORA_FIN'] = self._create_spinbox(params_frame, "Hora fin:", 0, 23)

        exec_frame = ttk.Frame(main_frame)
        exec_frame.pack(fill=tk.X, pady=10)
        ttk.Button(exec_frame, text="Generar PRs", command=self._execute).pack(side=tk.LEFT, padx=5)
        ttk.Button(exec_frame, text="Limpiar Consola", command=self.clear_console).pack(side=tk.LEFT, padx=5)

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
                'prs_por_mes': int(self.entries['PRS_POR_MES'].get()),
                'año': int(self.entries['AÑO'].get()),
                'mes_inicio': int(self.entries['MES_INICIO'].get()),
                'mes_fin': int(self.entries['MES_FIN'].get()),
                'hora_inicio': int(self.entries['HORA_INICIO'].get()),
                'hora_fin': int(self.entries['HORA_FIN'].get())
            }

            if data['prs_por_mes'] < 1 or data['prs_por_mes'] > 10:
                messagebox.showerror("Error", "El número de PRs por mes debe estar entre 1 y 10")
                return None

            return data

        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos")
            return None

    def _execute(self):
        self.output.delete(1.0, tk.END)

        params = self._validate_inputs()
        if not params:
            return

        load_dotenv()
        token = os.getenv('GITHUB_TOKEN')
        repo_owner = os.getenv('REPO_OWNER')
        repo_name = os.getenv('REPO_NAME')
        base_branch = os.getenv('BASE_BRANCH')
        user_email = os.getenv('USER_EMAIL')

        if not all([token, repo_owner, repo_name, base_branch, user_email]):
            messagebox.showerror("Error", "Faltan variables en el archivo .env")
            return

        # Aquí empieza el proceso de creación y fusión de PRs, similar al script original
        print("🏁 Iniciando generación y merge de PRs históricos")
        for mes in range(params['mes_inicio'], params['mes_fin'] + 1):
            self.output_insert(f"\n📅 Procesando {mes:02d}/{params['año']}\n")
            for pr_num in range(1, params['prs_por_mes'] + 1):
                self.output_insert(f"🔄 Procesando PR {pr_num}/{params['prs_por_mes']}\n")
                self.crear_y_mergear_pr(mes, params['año'], pr_num)

        self.output_insert("\n✅ Todos los PRs han sido mergeados correctamente\n")
        self.output_insert("⚠️ Verifica en GitHub que los commits y merges muestren las fechas correctas\n")

    def output_insert(self, text: str):
        self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.update_idletasks()

    def clear_console(self):
        """Limpiar el área de texto de la consola"""
        self.output.delete(1.0, tk.END)

    def run_git_command(self, command, print_output=True, custom_env=None):
        """Ejecuta comandos git con manejo de errores mejorado"""
        try:
            if print_output:
                self.output_insert(f"Ejecutando: {command}")
            subprocess.run(
                command,
                shell=True,
                check=True,
                env=custom_env if custom_env else os.environ,
                capture_output=not print_output
            )
        except subprocess.CalledProcessError as e:
            self.output_insert(f"Error en comando: {command}")
            self.output_insert(f"Detalles: {e.stderr.decode().strip()}")
            exit()

    def generar_fecha_aleatoria(self, mes, año):
        """Genera fechas válidas considerando años bisiestos"""
        if mes == 2:
            bisiesto = (año % 4 == 0 and (año % 100 != 0 or año % 400 == 0))
            return random.randint(1, 29 if bisiesto else 28)
        dias_por_mes = {
            1: 31, 3: 31, 4: 30, 5: 31, 6: 30,
            7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
        }
        return random.randint(1, dias_por_mes.get(mes, 30))

    def crear_pr(self, datos_pr):
        """Crea un PR usando la API de GitHub"""
        url = f"https://api.github.com/repos/{os.getenv('REPO_OWNER')}/{os.getenv('REPO_NAME')}/pulls"
        headers = {
            "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        try:
            response = requests.post(url, json=datos_pr, headers=headers)
            response.raise_for_status()
            return response.json()['number']
        except requests.exceptions.RequestException as e:
            self.output_insert(f"Error creando PR: {str(e)}")
            return None

    def configurar_entorno_fechas(self, fecha):
        """Configura variables de entorno para fechas específicas"""
        fecha_str = fecha.strftime("%Y-%m-%d %H:%M:%S") + "-0500"
        return {
            'GIT_AUTHOR_DATE': fecha_str,
            'GIT_COMMITTER_DATE': fecha_str
        }

    def crear_y_mergear_pr(self, mes, año, pr_num):
        """Crea y mergea un PR con fecha histórica"""
        dia = self.generar_fecha_aleatoria(mes, año)
        hora = random.randint(9, 18)
        minuto = random.randint(0, 59)
        fecha_commit = datetime(año, mes, dia, hora, minuto)
        
        # Configurar entorno con fechas
        env_commit = os.environ.copy()
        env_commit.update(self.configurar_entorno_fechas(fecha_commit))
        
        branch_name = f"pr/{fecha_commit.strftime('%Y%m%d')}-{pr_num:03d}"
        
        try:
            # Configuración inicial
            self.run_git_command('git checkout main', False)
            self.run_git_command('git pull origin main', False)
            
            # Crear rama y commit
            self.run_git_command(f'git checkout -b {branch_name}', False, env_commit)
            with open('historial.txt', 'a') as f:
                f.write(f"PR {pr_num} - {fecha_commit.isoformat()}\n")
            
            self.run_git_command('git add historial.txt', False, env_commit)
            commit_msg = f"PR {pr_num} - {fecha_commit.strftime('%Y-%m-%d %H:%M')}"
            self.run_git_command(f'git commit -m "{commit_msg}"', False, env_commit)
            
            # Push con fecha histórica
            self.run_git_command(f'git push -u origin {branch_name}', False, env_commit)
            
            # Crear PR
            pr_data = {
                "title": f"PR {pr_num} - {fecha_commit.strftime('%Y-%m')}",
                "head": branch_name,
                "base": os.getenv('BASE_BRANCH'),
                "body": f"PR generado automáticamente\nFecha: {fecha_commit}"
            }
            pr_number = self.crear_pr(pr_data)
            
            if pr_number:
                # Merge con fecha histórica
                merge_env = env_commit.copy()
                
                # Realizar merge local
                self.run_git_command('git checkout main', False, merge_env)
                merge_msg = f"Merge PR #{pr_number} ({fecha_commit.strftime('%Y-%m-%d')})"
                self.run_git_command(
                    f'git merge --no-ff {branch_name} -m "{merge_msg}"',
                    False,
                    merge_env
                )
                
                # Push del merge con fecha correcta
                self.run_git_command('git push origin main', False, merge_env)
        finally:
            # Limpieza de ramas
            self.run_git_command('git checkout main', False)
            self.run_git_command(f'git branch -D {branch_name}', False)
            self.run_git_command(f'git push origin --delete {branch_name}', False)


# Ejecutando la aplicación
if __name__ == "__main__":
    app = GitHubPRCreatorApp()
    app.mainloop()
