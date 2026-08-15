from app.database import driver


LABELS = [
    "Service",
    "Team",
    "Engineer",
    "Incident",
    "Alert",
    "Deployment",
    "Environment",
    "Database",
    "Runbook",
]


try:
    with driver.session() as session:
        print("Node counts:")
        print("-" * 30)

        for label in LABELS:
            result = session.run(
                f"MATCH (n:{label}) RETURN count(n) AS count"
            )
            count = result.single()["count"]
            print(f"{label:15} {count}")

finally:
    driver.close()