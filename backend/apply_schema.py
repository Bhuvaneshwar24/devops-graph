"""
Apply the graph schema constraints to CognoDB.

The script reuses the existing database driver from app.database.
"""

from pathlib import Path

from app.database import driver


SCHEMA_FILE = Path(__file__).resolve().parent.parent / "cypher" / "schema.cypher"


def apply_schema() -> None:
    schema_text = SCHEMA_FILE.read_text(encoding="utf-8")

    statements = [
        statement.strip()
        for statement in schema_text.split(";")
        if statement.strip()
        and not statement.strip().startswith("//")
    ]

    with driver.session() as session:
        for statement in statements:
            print(f"Running: {statement[:80]}...")
            session.run(statement)

    print("Schema applied successfully.")


if __name__ == "__main__":
    try:
        apply_schema()
    finally:
        driver.close()