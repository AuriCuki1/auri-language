#!/usr/bin/env python3
import sys
import os
import subprocess
import time

variables = {}

def resolve_vars(text):
    for k, v in variables.items():
        text = text.replace(f"${k}", str(v))
    return text

def run_auri_line(line):
    line = line.strip()
    if not line or line.startswith("~") or (line.startswith("[") and line.endswith("]")):
        return

    parts = line.split(" ")
    cmd = parts[0]

    # Clean Python-style variable assignment: name = "Alex"
    if len(parts) >= 3 and parts[1] == "=":
        var_name = parts[0]
        raw_val = " ".join(parts[2:]).strip('"\'')
        variables[var_name] = int(raw_val) if raw_val.isdigit() else raw_val

    # Clean print command: print "Hello $name"
    elif cmd in ("print", "say"):
        msg = " ".join(parts[1:]).strip('"\'')
        print(resolve_vars(msg))

    # Clean ask command: ask "Your name? " -> username
    elif cmd == "ask" and "->" in parts:
        arrow_idx = parts.index("->")
        question = " ".join(parts[1:arrow_idx]).strip('"\'')
        var_name = parts[arrow_idx + 1]
        ans = input(resolve_vars(question) + " ")
        variables[var_name] = int(ans) if ans.isdigit() else ans

    # Math commands: add score 10
    elif cmd in ("add", "sub", "mul"):
        var_name, amount = parts[1], int(parts[2])
        if var_name in variables and isinstance(variables[var_name], int):
            if cmd == "add": variables[var_name] += amount
            elif cmd == "sub": variables[var_name] -= amount
            elif cmd == "mul": variables[var_name] *= amount

    elif cmd == "wait":
        time.sleep(float(parts[1]))

def run_auri_file(filepath):
    print("✨ [Detected: Auri (.auri) - Your Fanmade Language]")
    print("--------------------------------------------------")
    with open(filepath, "r") as f:
        for line in f:
            run_auri_line(line)

def detect_and_run(filepath):
    if not os.path.exists(filepath):
        print(f"[Error] File '{filepath}' does not exist.")
        return

    # Extract the file extension (e.g., .auri, .py, .js)
    _, ext = os.path.splitext(filepath)
    ext = ext.lower()

    # Language Registry
    languages = {
        ".auri": ("Auri (Custom Fanmade Language)", "auri"),
        ".py":   ("Python", "python"),
        ".js":   ("JavaScript (Node.js)", "node"),
        ".sh":   ("Bash / Shell Script", "bash"),
        ".html": ("HTML Webpage", "preview"),
        ".css":  ("CSS Stylesheet", "preview"),
        ".json": ("JSON Data", "preview"),
        ".md":   ("Markdown Document", "preview"),
        ".c":    ("C Source Code", "c"),
        ".cpp":  ("C++ Source Code", "cpp"),
        ".java": ("Java Source Code", "java"),
        ".rb":   ("Ruby", "ruby"),
        ".php":  ("PHP", "php"),
    }

    if ext == ".auri":
        run_auri_file(filepath)
    elif ext in languages:
        lang_name, runner = languages[ext]
        print(f"🔍 [Detected Language: {lang_name} ({ext})]")
        print("--------------------------------------------------")
        if runner == "preview":
            with open(filepath, "r") as f:
                print(f.read())
        elif runner in ("python", "node", "bash", "ruby", "php"):
            subprocess.run([runner, filepath])
        else:
            print(f"Detected {lang_name}. Compile it first to run!")
    else:
        print(f"❓ [Unknown Extension: '{ext or 'none'}'] - Not .auri or a recognized language.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: auri <filename>")
        sys.exit(1)
    detect_and_run(sys.argv[1])
