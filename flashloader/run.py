from .cli import FlasherCLI


def main():
    cli = FlasherCLI()
    cli.cmdloop()


if __name__ == '__main__':
    main()
