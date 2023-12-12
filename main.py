from lexer import main_loop_lexer, save_queue
from syntaxer import main_loop_syntaxer


def main():
    # filename = input("Input filename: ")
    filename = "prog.lng"
    lexems = main_loop_lexer(filename)
    save_queue(lexems, "lexems.out")

    main_loop_syntaxer("lexems.out")


if __name__ == "__main__":
    main()
