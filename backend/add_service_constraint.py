from app.database import driver


try:
    with driver.session() as session:
        session.run("""
            CREATE CONSTRAINT service_id IF NOT EXISTS
            FOR (s:Service)
            REQUIRE s.id IS UNIQUE
        """)

    print("Service constraint created successfully.")

finally:
    driver.close()