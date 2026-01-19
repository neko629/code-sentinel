import sys

def main():
    name = "world"
    if len(sys.argv) > 1:
        name = sys.argv[1]
    print(f"Hello, {name}!")

if __name__ == "__main__":
    main()

