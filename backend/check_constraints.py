from app.database import driver


try:
    with driver.session() as session:
        result = session.run("SHOW CONSTRAINTS")

        print("\nCognoDB constraints:\n")

        for record in result:
            data = record.data()
            print(data)

finally:
    driver.close()