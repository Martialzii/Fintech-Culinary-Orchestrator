import subprocess
import sys
import json
import urllib.request

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "deepseek-coder-v2:16b"

def run_target_script(script_path):
    print(f"[*] Executing target script: {script_path}")
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def ask_local_model_for_patch(script_path, code, error_log):
    print("[!] Script crashed. Consulting local model for surgical hot-patch...")
    prompt = f"""
You are an autonomous self-healing engineering loop. The script '{script_path}' failed.
Here is the original source code:
---
{code}
---
Here is the exact terminal error/stack trace:
---
{error_log}
---
Provide ONLY the corrected, fixed python code. Do not include explanations, markdown formatting, or backticks. Just the raw valid Python code.
"""
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    
    req = urllib.request.Request(
        OLLAMA_URL, 
        data=json.dumps(payload).encode('utf-8'), 
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data.get("response", "").strip()
    except Exception as e:
        print(f"[-] Failed to communicate with Ollama: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python self_healer.py <target_script.py>")
        sys.exit(1)
        
    target = sys.argv[1]
    
    # Run loop up to 3 times to achieve successful execution
    for attempt in range(1, 4):
        print(f"\n[--- Attempt {attempt} ---]")
        return_code, stdout, stderr = run_target_script(target)
        
        if return_code == 0:
            print("[+] Success! Script executed with exit code 0.")
            if stdout: print(f"Output:\n{stdout}")
            break
        else:
            print(f"[-] Execution Failed on attempt {attempt}.")
            with open(target, 'r', encoding='utf-8') as f:
                current_code = f.read()
                
            fixed_code = ask_local_model_for_patch(target, current_code, stderr)
            if fixed_code:
                # Clean up any lingering markdown blocks the model might return safely on a single line
                if fixed_code.startswith("```python"): fixed_code = fixed_code[9:]
                if fixed_code.endswith("
```"): fixed_code = fixed_code[:-3]
                
                with open(target, 'w', encoding='utf-8') as f:
                    f.write(fixed_code.strip())
                print(f"[+] Hot-patch applied to {target}. Retrying execution...")
            else:
                print("[-] Could not retrieve patch. Aborting.")
                break

if __name__ == "__main__":
    main()
