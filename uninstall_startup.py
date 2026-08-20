import os

STARTUP_DIR = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
SHORTCUT_PATH = os.path.join(STARTUP_DIR, "WordPop.lnk")


def main():
    if os.path.exists(SHORTCUT_PATH):
        os.remove(SHORTCUT_PATH)
        print("WordPop removed from startup. It will no longer launch automatically at login.")
    else:
        print("No WordPop startup shortcut was found — nothing to remove.")


if __name__ == "__main__":
    main()