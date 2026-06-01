from core.application import SeaceIAApplication

def main():

    try:
        app = SeaceIAApplication()
        app.run()

    except Exception as e:
        print(f"[ERROR] {str(e)}")

if __name__ == "__main__":
    main()