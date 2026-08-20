import os
import subprocess

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHONW_PATH = os.path.join(PROJECT_DIR, "wordpop-env", "Scripts", "pythonw.exe")
SCRIPT_PATH = os.path.join(PROJECT_DIR, "dictionary_popup.py")
STARTUP_DIR = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
SHORTCUT_PATH = os.path.join(STARTUP_DIR, "WordPop.lnk")

VBS_TEMPLATE = '''Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{shortcut_path}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{pythonw_path}"
oLink.Arguments = "{script_path}"
oLink.WorkingDirectory = "{working_dir}"
oLink.Save
'''


def main():
    if not os.path.exists(PYTHONW_PATH):
        print(f"ERROR: could not find pythonw.exe at:\n  {PYTHONW_PATH}")
        print("Run this from inside the WordPop project folder, with the venv already created.")
        return

    if not os.path.exists(SCRIPT_PATH):
        print(f"ERROR: could not find dictionary_popup.py at:\n  {SCRIPT_PATH}")
        return

    vbs_content = VBS_TEMPLATE.format(
        shortcut_path=SHORTCUT_PATH,
        pythonw_path=PYTHONW_PATH,
        script_path=SCRIPT_PATH,
        working_dir=PROJECT_DIR
    )

    vbs_path = os.path.join(PROJECT_DIR, "_temp_create_shortcut.vbs")
    with open(vbs_path, "w") as f:
        f.write(vbs_content)

    try:
        subprocess.run(["cscript", "//nologo", vbs_path], check=True)
        print("Success! WordPop will now start automatically the next time you log in.")
        print(f"Shortcut created at:\n  {SHORTCUT_PATH}")
    except subprocess.CalledProcessError:
        print("ERROR: failed to create the startup shortcut.")
    finally:
        if os.path.exists(vbs_path):
            os.remove(vbs_path)


if __name__ == "__main__":
    main()