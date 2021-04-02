import os
import sqlite3
from sqlite3 import Cursor
from jinja2 import Environment, FileSystemLoader
from tabulate import tabulate


def build_table_jinja2(title, data, headers):
    env = Environment(
        loader=FileSystemLoader(os.path.join("templates")),
        block_start_string=r"\BLOCK{",
        block_end_string="}",
        variable_start_string=r"\VAR{",
        variable_end_string="}",
        comment_start_string=r"\#{",
        comment_end_string="}",
        line_statement_prefix="%%",
        line_comment_prefix="%#",
        trim_blocks=True,
        autoescape=False,
    )
    template = env.get_template("latex_tables.tex.jinja2")

    column_format = []
    for field in data[0]:
        fmt = "r"
        if isinstance(field, str):
            fmt = "l"
        column_format.append(fmt)

    header_str = "\t & \t".join(
        [r"\textbf{\textit{%s}}" % header for header in headers]
    )
    tablulated = tabulate(
        data,
        tablefmt="latex",
    )
    data_strs = [
        line.strip() for line in tablulated.splitlines() if not line.startswith("\\")
    ]

    return template.render(
        title=title,
        data_strs=data_strs,
        column_str="|".join(column_format),
        headers=headers,
        header_str=header_str,
    )


def build_sql_latex_table(title, curs: Cursor):
    return build_table_jinja2(
        title=title,
        data=[row for row in curs],
        headers=[c[0].title().replace("_", " ") for c in curs.description],
    )


if __name__ == "__main__":
    conn = sqlite3.connect("database.sqlite3")
    latex_table = build_sql_latex_table(
        "Generic Table Title Goes Here", conn.execute("SELECT * FROM table_name")
    )
    print(latex_table)
