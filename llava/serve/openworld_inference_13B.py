from llava.serve.inference_13B import build_parser, main


if __name__ == "__main__":
    parser = build_parser()
    parser.set_defaults(output_root="outputs/openworld")
    args = parser.parse_args()
    main(args)
