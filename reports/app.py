import commands
from settings import settings


def main():
    df_input_issue_report = commands.read_issue_report_csv(settings["path_input_issue_report"])

    commands.enrich_board(df_input_issue_report, settings["enums_mappings"]["status_mapping"])

    commands.persist_reports_in_csv(
        settings["path_input_issue_report"], settings["path_output_reports_path"]
    )

    commands.persist_enum_csv(settings["enums_mappings"], settings["path_output_reports_path"])


if __name__ == "__main__":
    main()
