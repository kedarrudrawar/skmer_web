import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Local Alignment of two DNA strings')
    parser.add_argument('-f', "--file", type=str, help='input file')


    return parser.parse_args()

def main():
    args = parse_args()

    f = args.file
    print(f)

    with open(f, 'r+') as file:
        for line in file:
            print(line)


if __name__ == '__main__':
    main()