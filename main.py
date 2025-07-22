from interface import *

def main():
    try:
        interface()
    except Exception as e:
        print(f"\n Ocorreu um erro inesperado: {e}")
if __name__ == "__main__":
    main()
