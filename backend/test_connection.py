from app.database import driver, verify_connection


try:
    verify_connection()
    print("Successfully connected to CognoDB!")

except Exception as error:
    print("CognoDB connection failed:")
    print(error)

finally:
    driver.close()