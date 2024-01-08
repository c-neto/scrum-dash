import typer
from extract import commands


app = typer.Typer(add_completion=False)


@app.command()
def reports(sprint: int = typer.Argument(..., help="sprint number")):
    issues_collection = commands.get_issues_collections_from_api(sprint)
    commands.create_report_csv(issues_collection)
    commands.create_report_raw(issues_collection)
    print(">>> all reports created successfully")


@app.command()
def reports_csv(raw_report: str = typer.Argument(..., help="raw report json")):
    issues_collection = commands.get_issues_collections_from_json_file(raw_report)
    commands.create_report_csv(issues_collection)
    print(">>> all reports created successfully")


@app.command()
def reports_raw(sprint: int = typer.Argument(..., help="sprint number")):
    issues_collection = commands.get_issues_collections_from_api(sprint)
    commands.create_report_raw(issues_collection)
    print(">>> all reports created successfully")


if __name__ == "__main__":
    app()
