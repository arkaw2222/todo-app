import os
import sys
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT =  Path(__file__).parent.parent

def run(env: str = "development"):
    env_file = PROJECT_ROOT / f".env.{env}"
    
    if not env_file.exists():
        print(f"❌ Error: Environment file {env_file.name} not found")
        sys.exit(1)
    
    print(f"🚀 Starting in {env} mode ({env_file.name})")
    
    # Загрузка переменных окружения
    load_dotenv(env_file, override=True)
    
    # Параметры запуска
    reload_flag = "--reload" if env == "development" else ""
    host = "127.0.0.1" if env == "production" else "127.0.0.1"
    
    cmd = f"uvicorn main:app --host {host} --port 8001 {reload_flag}"
    print(f"🔧 Executing: {cmd}")
    os.system(cmd)

def start():
    print("🟢 Starting with default .env (no overrides)")
    load_dotenv(PROJECT_ROOT / '.env')
    os.system("uvicorn main:app --host=0.0.0.0 --port=8001")

if __name__ == "__main__":
    commands = {
        "dev": lambda: run("development"),
        "prod": lambda: run("production"),
        "start": start
    }
    
    try:
        cmd = sys.argv[1] if len(sys.argv) > 1 else "dev"
        commands.get(cmd, lambda: print("❌ Unknown command"))()
    except Exception as e:
        print(f"🔥 Critical error: {str(e)}")
        sys.exit(1)
