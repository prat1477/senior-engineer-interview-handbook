---
name: serve-handbook
description: Starts the Senior Engineer Interview Handbook MkDocs dev server from the current workspace. Use when the user asks to start, serve, or preview the handbook, run mkdocs serve, or open the local docs site.
---

# Serve handbook

Start the MkDocs dev server for this repository from the workspace root (the directory that contains `mkdocs.yml`).

## Steps

1. Confirm `mkdocs.yml` is in the workspace root. If it is missing, stop and say this workspace is not the handbook.
2. Check the terminals folder for a `mkdocs serve` process that is already running in this repo. If one is running, report its URL and do not start another server.
3. If `.venv/Scripts/mkdocs.exe` (Windows) or `.venv/bin/mkdocs` (Unix) is missing, create the venv and install dependencies:

   Windows (PowerShell):

   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\pip install -r requirements.txt
   ```

   Unix:

   ```bash
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   ```

4. Start the server in the background from the workspace root. Do not use `make serve` on Windows.

   Windows:

   ```powershell
   .\.venv\Scripts\mkdocs serve
   ```

   Unix:

   ```bash
   .venv/bin/mkdocs serve
   ```

5. Read the server output until it prints the local URL (default `http://127.0.0.1:8000/`). If the port is taken, report the error and the URL MkDocs actually bound.
6. Tell the user the site URL. The progress tracker is that origin plus `/PROGRESS/`.

Leave the server running. Stop it only when the user asks.
