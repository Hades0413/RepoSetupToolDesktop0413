import os
import random
import subprocess
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
from datetime import datetime

# Configuración visual
LINEA = "═" * 50
EMOJI = {
    "config": "⚙️",
    "commit": "📌",
    "mes": "📅",
    "progreso": "🔄",
    "exito": "✅",
    "error": "❌",
    "usuario": "👤",
    "push": "🚀"
}

def mostrar_titulo(texto, output_text):
    output_text.insert(tk.END, f"\n{LINEA}\n")
    output_text.insert(tk.END, f"{EMOJI['mes']} {texto.center(48)} {EMOJI['mes']}\n")
    output_text.insert(tk.END, f"{LINEA}\n")

def crear_archivo_dotenv(entry_token, entry_repo_owner, entry_repo_name, entry_base_branch, entry_user_email):
    """Crea un archivo .env con las configuraciones ingresadas"""
    try:
        with open('.env', 'w') as f:
            f.write(f"GITHUB_TOKEN={entry_token}\n")
            f.write(f"REPO_OWNER={entry_repo_owner}\n")
            f.write(f"REPO_NAME={entry_repo_name}\n")
            f.write(f"BASE_BRANCH={entry_base_branch}\n")
            f.write(f"USER_EMAIL={entry_user_email}\n")
        messagebox.showinfo("Éxito", "Archivo .env creado correctamente")
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un error al crear el archivo .env: {str(e)}")

def ejecutar_script(entry_token, entry_repo_owner, entry_repo_name, entry_base_branch, entry_user_email,
                    entry_mes_inicio, entry_mes_fin, entry_commits, entry_anio, output_text):
    # Obtener los datos del formulario
    mes_inicio = int(entry_mes_inicio.get())
    mes_fin = int(entry_mes_fin.get())
    commits_por_mes = int(entry_commits.get())
    año = int(entry_anio.get())

    if not (1 <= mes_inicio <= 12 and 1 <= mes_fin <= 12):
        messagebox.showerror("Error", "Los meses deben estar entre 1 y 12")
        return

    # Crear archivo .env
    crear_archivo_dotenv(entry_token.get(), entry_repo_owner.get(), entry_repo_name.get(),
                         entry_base_branch.get(), entry_user_email.get())

    # Cargar las variables de entorno desde el archivo .env
    load_dotenv()

    # Obtener las variables desde el archivo .env
    token = os.getenv('GITHUB_TOKEN')  
    repo_owner = os.getenv('REPO_OWNER')  
    repo_name = os.getenv('REPO_NAME')  
    base_branch = os.getenv('BASE_BRANCH')  
    user_email = os.getenv('USER_EMAIL')

    # Verificar que todas las variables estén presentes
    if not all([token, repo_owner, repo_name, base_branch, user_email]):
        messagebox.showerror("Error", "Faltan variables en .env")
        return

    # Configurar el entorno para subprocess
    env = os.environ.copy()
    env['GITHUB_TOKEN'] = token

    def run_git_command(command, print_output=True):
        """Ejecuta comandos git con manejo de errores"""
        try:
            if print_output:
                output_text.insert(tk.END, f"{EMOJI['progreso']} Ejecutando: {command}\n")
            resultado = subprocess.run(
                command, 
                shell=True, 
                check=True, 
                env=env,
                capture_output=True,
                text=True
            )
            if print_output and resultado.stdout:
                output_text.insert(tk.END, resultado.stdout + '\n')
            return True
        except subprocess.CalledProcessError as e:
            output_text.insert(tk.END, f"\n{EMOJI['error']} Error en comando: {command}\n")
            output_text.insert(tk.END, f"{EMOJI['error']} Detalles: {e.stderr.strip()}\n")
            exit()

    # Configuración inicial
    mostrar_titulo("INICIANDO PROCESO DE COMMITS", output_text)
    output_text.insert(tk.END, f"{EMOJI['config']} Configurando entorno...\n")

    # Sincronizar repositorio
    output_text.insert(tk.END, f"\n{EMOJI['progreso']} Sincronizando con el repositorio remoto\n")
    run_git_command(f'git pull https://{repo_owner}:{token}@github.com/{repo_owner}/{repo_name}.git {base_branch}', False)

    # Configurar usuario Git
    output_text.insert(tk.END, f"\n{EMOJI['usuario']} Configurando identidad Git:\n")
    run_git_command(f'git config --local user.name "{repo_owner}"', False)
    run_git_command(f'git config --local user.email "{user_email}"', False)

    # Mostrar configuración
    output_text.insert(tk.END, f"\n{EMOJI['config']} Configuración actual:\n")
    run_git_command('git config user.name', True)
    run_git_command('git config user.email', True)

    # Función para generar fecha
    def generar_fecha_aleatoria(mes, año):
        dias_por_mes = {
            1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
            7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
        }
        return random.randint(1, dias_por_mes[mes])

    # Función para crear commits
    def crear_commit(mes, i, año):
        rand_day = generar_fecha_aleatoria(mes, año)
        commit_date = datetime(año, mes, rand_day, 17, 51)

        with open('test.txt', 'a') as file:
            file.write(f"Commit {(mes - 1) * commits_por_mes + i + 1}\n")

        # Mostrar progreso
        output_text.insert(tk.END, f"{EMOJI['progreso']} [{i+1}/{commits_por_mes}] Creando commit para {commit_date.strftime('%d/%m/%Y')}\n")

        run_git_command(f'git add test.txt', False)
        run_git_command(f'git commit --date="{commit_date.isoformat()}" -m "Commit {(mes - 1) * commits_por_mes + i + 1}"', False)

    # Parámetros de ejecución
    total_meses = mes_fin - mes_inicio + 1
    commits_totales = commits_por_mes * total_meses

    mostrar_titulo("CONFIGURACIÓN INICIAL", output_text)
    output_text.insert(tk.END, f"{EMOJI['mes']} Rango seleccionado: {mes_inicio:02d}-{mes_fin:02d}/{año}\n")
    output_text.insert(tk.END, f"{EMOJI['commit']} Commits por mes: {commits_por_mes}\n")
    output_text.insert(tk.END, f"{EMOJI['exito']} Total estimado: {commits_totales} commits\n")

    for mes in range(mes_inicio, mes_fin + 1):
        mostrar_titulo(f"PROCESANDO MES {mes:02d}/{año}", output_text)

        for i in range(commits_por_mes):
            crear_commit(mes, i, año)

        output_text.insert(tk.END, f"\n{EMOJI['exito']} Mes {mes:02d} completado: {commits_por_mes} commits\n")

    # Push final
    mostrar_titulo("ENVIANDO CAMBIOS", output_text)
    output_text.insert(tk.END, f"{EMOJI['push']} Realizando push de {commits_totales} commits...\n")
    run_git_command(f'git push https://{repo_owner}:{token}@github.com/{repo_owner}/{repo_name}.git {base_branch}', True)

    # Confirmación final
    output_text.insert(tk.END, f"\n{LINEA}\n")
    output_text.insert(tk.END, f"{EMOJI['exito']} PUSH EXITOSO!\n")
    output_text.insert(tk.END, f"{LINEA}\n")
    output_text.insert(tk.END, f"🗓️  Rango de meses: {mes_inicio:02d}-{mes_fin:02d}/{año}\n")
    output_text.insert(tk.END, f"📌 Total commits: {commits_totales}\n")
    output_text.insert(tk.END, f"{EMOJI['usuario']} Autor: {repo_owner} <{user_email}>\n")
    output_text.insert(tk.END, f"🌐 Repositorio: github.com/{repo_owner}/{repo_name}\n")
    output_text.insert(tk.END, f"{LINEA}\n")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Generador de Commits")

# Campos de entrada
tk.Label(ventana, text="Token de Github:").pack()
entry_token = tk.Entry(ventana)
entry_token.pack()

tk.Label(ventana, text="Owner del repositorio:").pack()
entry_repo_owner = tk.Entry(ventana)
entry_repo_owner.pack()

tk.Label(ventana, text="Nombre del repositorio:").pack()
entry_repo_name = tk.Entry(ventana)
entry_repo_name.pack()

tk.Label(ventana, text="Branch base (main, master):").pack()
entry_base_branch = tk.Entry(ventana)
entry_base_branch.pack()

tk.Label(ventana, text="Email del Usuario:").pack()
entry_user_email = tk.Entry(ventana)
entry_user_email.pack()

tk.Label(ventana, text="Mes de inicio (1-12):").pack()
entry_mes_inicio = tk.Entry(ventana)
entry_mes_inicio.pack()

tk.Label(ventana, text="Mes de fin (1-12):").pack()
entry_mes_fin = tk.Entry(ventana)
entry_mes_fin.pack()

tk.Label(ventana, text="Commits por mes:").pack()
entry_commits = tk.Entry(ventana)
entry_commits.pack()

tk.Label(ventana, text="Año:").pack()
entry_anio = tk.Entry(ventana)
entry_anio.pack()

# Botón para ejecutar
tk.Button(ventana, text="Ejecutar", command=lambda: ejecutar_script(
    entry_token, entry_repo_owner, entry_repo_name, entry_base_branch, entry_user_email,
    entry_mes_inicio, entry_mes_fin, entry_commits, entry_anio, output_text
)).pack()

# Text widget para mostrar la salida
output_text = tk.Text(ventana, height=20, width=80)
output_text.pack()

ventana.mainloop()
