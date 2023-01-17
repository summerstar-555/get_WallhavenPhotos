from colorama import Fore, Back, Style, init


def warning(msg: str) -> None:
    init(autoreset=True)
    print(Fore.RED + msg)
