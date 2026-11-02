import sys

def main():
    if len(sys.argv) != 3:
        print("Incorrect Usage.", file=sys.stderr)
        print("USAGE: ./volt <input_file.volt> <output_file.asm>", file=sys.stderr)
        return 1

    input_string = None
    with open(sys.argv[1]) as input_file:
        input_string = input_file.read()

    with open(sys.argv[2], "w+") as output_file:
        print(output_file.name)
        output_file.write(input_string)

if __name__ == "__main__":
    sys.exit(main())