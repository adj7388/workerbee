import argparse
import sys

from .bee import get_beewords, get_beewords_grouped, get_groupings
from .utils import error_check, write_to_buffer
from . import config


def get_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-r", "--required", type=str, required=True, help="The required Bee letter"
    )
    parser.add_argument(
        "-a",
        "--allowed",
        type=str,
        required=True,
        help=f"The non-required Bee letters (must be {config.NUM_ALLOWED_LETTERS})",
    )
    parser.add_argument(
        "-d",
        "--dictionary",
        type=str,
        required=False,
        choices=[config.WIKT, config.MW, config.FREE, config.DICT],
        default=config.WIKT,
        help="Dictionary for lookups",
    )
    parser.add_argument(
        "-g",
        "--groupby",
        type=str,
        choices=[config.INITIALS, config.LENGTH, config.NO_GROUPING],
        default=config.NO_GROUPING,
        help="Output grouped by initials, word length, or no grouping (plain list)",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-p",
        "--print",
        action="store_true",
        help="Send human readable output to stdout (default)",
    )
    group.add_argument("-j", "--json", action="store_true", help="Send json to stdout")
    group.add_argument(
        "-c", "--csv", action="store_true", help="Send csv to stdout (no metadata)"
    )
    return parser


def get_commandline_args() -> argparse.Namespace:
    parser = get_argparser()
    args = parser.parse_args()
    error = error_check(vars(args))
    if error:
        print(error)
        sys.exit(-1)
    return args


def print_meta_data(metadata: dict):
    print()
    print(f"Number Beewords:  {metadata[config.NUM_BEEWORDS]}")
    print(f"Required letters: {metadata[config.REQUIRED_LETTER]}")
    print(f"Allowed letters:  {metadata[config.ALLOWED_LETTERS]}")
    print(
        f'Perfect pangrams: {", ".join([word[config.WORD] for word in metadata[config.PERFECT_PANGRAMS]]) }'
    )
    print(
        f'Other pangrams:   {", ".join([word[config.WORD] for word in metadata[config.NONPERFECT_PANGRAMS]]) }'
    )
    print(f"Bingo:            {metadata[config.BINGO]}")
    print(f"Pangrams marked with {config.PANGRAM_MARKER}")
    print(f"Perfect pangrams marked with {config.PERFECT_MARKER}")
    print()


def print_beewords_grouped(beewords: dict) -> None:
    SPACING = "   "
    print_meta_data(beewords[config.METADATA])
    for first_level_label, first_level_words in beewords[config.DATA].items():
        print(first_level_label)
        for second_level_label, words in first_level_words.items():
            print(f"{SPACING * 1}{second_level_label}")
            for word in words:
                marker = (
                    config.PERFECT_MARKER
                    if word[config.IS_PERFECT]
                    else config.PANGRAM_MARKER if word[config.IS_PANGRAM] else ""
                )
                print(f"{SPACING * 2}{word[config.WORD]} {marker}")
    print_meta_data(beewords[config.METADATA])


def print_beewords_list(beewords: dict) -> None:
    print_meta_data(beewords[config.METADATA])
    for word in beewords[config.DATA]:
        marker = (
            config.PERFECT_MARKER
            if word[config.IS_PERFECT]
            else config.PANGRAM_MARKER if word[config.IS_PANGRAM] else ""
        )
        print(f"{word[config.WORD]} {marker}")
    print_meta_data(beewords[config.METADATA])


############ main ############
def main():
    args = get_commandline_args()

    if args.groupby == config.NO_GROUPING:
        beewords = get_beewords(
            args.required,
            args.allowed,
            dictionary=config.Dictionaries[args.dictionary],
        )
    elif args.groupby in [config.INITIALS, config.LENGTH]:
        beewords = get_beewords_grouped(
            args.required,
            args.allowed,
            grouping=get_groupings(args.groupby),
            dictionary=config.Dictionaries[args.dictionary],
        )
    else:
        raise ValueError("Error: Don't know how to get beewords.")

    ### check for csv or json output first, if they're specified in args ...
    if args.csv:
        buffer = write_to_buffer(beewords, file_type="csv")
        print(buffer.getvalue())
    elif args.json:
        buffer = write_to_buffer(beewords, file_type="json")
        print(buffer.getvalue())
    ### ... if not csv/json (above), then print to stdout based on groupby
    elif args.groupby == config.NO_GROUPING:
        print_beewords_list(beewords=beewords)
    elif args.groupby in [config.INITIALS, config.LENGTH]:
        print_beewords_grouped(beewords=beewords)
    else:
        raise ValueError("Error: Don't know how to output.")


if __name__ == "__main__":
    main()
