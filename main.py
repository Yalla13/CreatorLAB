
from converter.avi_to_mp4 import convert_folder


def main():
    convert_folder(
        input_folder="assets/avi_input/BG_TURBO",
        output_folder="outputs/converted"
    )


if __name__ == "__main__":
    main()
