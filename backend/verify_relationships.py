from app.database import driver


RELATIONSHIPS = [
    "DEPENDS_ON",
    "USES_DATABASE",
    "OWNS",
    "MEMBER_OF",
    "RESPONDED_TO",
    "AFFECTED",
    "TRIGGERED_BY",
    "RESOLVED_BY",
    "HAS_RUNBOOK",
    "DEPLOYED",
    "DEPLOYED_TO",
    "CREATED_BY",
    "CAUSED_BY",
]


try:
    with driver.session() as session:
        print("Relationship counts:")
        print("-" * 35)

        for relationship in RELATIONSHIPS:
            result = session.run(
                f"""
                MATCH ()-[r:{relationship}]->()
                RETURN count(r) AS count
                """
            )

            count = result.single()["count"]
            print(f"{relationship:20} {count}")

finally:
    driver.close()