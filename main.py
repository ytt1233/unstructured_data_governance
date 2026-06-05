import argparse

from runner.dataset_runner import DatasetRunner


def main():

    parser = argparse.ArgumentParser(
        description="AI Document Governance Pipeline"
    )

    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to a PDF file or a folder containing PDFs"
    )

    parser.add_argument(
        "--mode",
        type=str,
        default="batch",
        choices=["batch"],
        help="Processing mode (currently only batch supported)"
    )

    args = parser.parse_args()

    runner = DatasetRunner()

    print("\n" + "=" * 60)
    print("STARTING DATASET PIPELINE")
    print("=" * 60)

    # =========================
    # 批处理模式（目前唯一模式）
    # =========================
    if args.mode == "batch":

        report = runner.run(args.input) 

        print("\n" + "=" * 60)
        print("PIPELINE FINISHED")
        print("=" * 60)

        print("\nFinal Dataset Report Generated")

        return report


if __name__ == "__main__":
    main()