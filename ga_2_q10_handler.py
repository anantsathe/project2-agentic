import subprocess
import requests
import os
import time
import json

async def solve_ga_2_q10(question: str):
    try: 
        # Define paths
        download_dir = "/mnt/c/tmp/llamafile_setup"
        os.makedirs(download_dir, exist_ok=True)  # Ensure directory exists
        
        llamafile_path = os.path.join(download_dir, "llamafile.exe")  # Updated filename
        model_path = os.path.join(download_dir, "Llama-3.2-1B-Instruct.Q6_K.llamafile")

        llamafile_url = "https://github.com/Mozilla-Ocho/llamafile/releases/latest/download/llamafile"
        model_url = "https://huggingface.co/Mozilla/Llama-3.2-1B-Instruct-llamafile/blob/main/Llama-3.2-1B-Instruct.Q6_K.llamafile?download=true"

        # Download Llamafile only if not present
        if not os.path.exists(llamafile_path):
            print("📥 Downloading Llamafile...")
            response = requests.get(llamafile_url, stream=True)
            with open(llamafile_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            os.chmod(llamafile_path, 0o755)  # Make executable
        else:
            print("✅ Llamafile already exists, skipping download.")

        # Download model only if not present
        if not os.path.exists(model_path):
            print("📥 Downloading Llama-3.2-1B-Instruct model...")
            response = requests.get(model_url, stream=True)
            with open(model_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        else:
            print("✅ Model file already exists, skipping download.")

        # Run Llamafile model
        print("🚀 Starting Llamafile model server...")
        server_process = subprocess.Popen([llamafile_path, model_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        time.sleep(10)

        # Check if the server is running
        llamafile_running = False
        for _ in range(5):  # Retry 5 times
            try:
                response = requests.get("http://127.0.0.1:8081", timeout=3)  # Corrected port
                if response.status_code in [200, 404]:  
                    llamafile_running = True
                    break
            except requests.exceptions.RequestException:
                time.sleep(2)
        
        if not llamafile_running:
            return {"answer": "Error: Llamafile server is not responding"}

        # Start ngrok tunnel to correct port
        print("🌍 Creating ngrok tunnel...")
        subprocess.Popen(["ngrok", "http", "8081"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(10)  # Increased delay

        # Fetch ngrok URL with retry mechanism
        ngrok_url = None
        for _ in range(5):  # Retry 5 times
            try:
                ngrok_api = "http://127.0.0.1:4040/api/tunnels"
                response = requests.get(ngrok_api).json()
                
                # Find the HTTPS tunnel
                ngrok_url = next((t["public_url"] for t in response.get("tunnels", []) if t["proto"] == "https"), None)
                
                if ngrok_url:
                    print(f"🔗 Ngrok URL: {ngrok_url}")
                    break
            except Exception:
                time.sleep(2)  # Retry delay
        
        if not ngrok_url:
            return {"answer": "Error retrieving ngrok URL"}

        return {"answer": f"ngrok URL: {ngrok_url}"}

    except Exception as e:
        return {"answer": f"Error: {str(e)}"}
