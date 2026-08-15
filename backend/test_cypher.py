from app.database import driver


CREATE_QUERY = """
CREATE (n:TestNode {
    name: $name
})
RETURN n.name AS name
"""

READ_QUERY = """
MATCH (n:TestNode {name: $name})
RETURN n.name AS name
"""

DELETE_QUERY = """
MATCH (n:TestNode {name: $name})
DELETE n
"""


try:
    with driver.session() as session:
        # Create
        result = session.run(
            CREATE_QUERY,
            name="CognoDB Integration Test",
        )
        record = result.single()
        print("Created:", record["name"])

        # Read
        result = session.run(
            READ_QUERY,
            name="CognoDB Integration Test",
        )
        record = result.single()
        print("Found:", record["name"])

        # Delete
        session.run(
            DELETE_QUERY,
            name="CognoDB Integration Test",
        )
        print("Deleted: TestNode")


except Exception as error:
    print("Cypher test failed:")
    print(error)

finally:
    driver.close()