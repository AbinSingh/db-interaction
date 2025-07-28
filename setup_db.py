import sqlite3

if __name__ == "__main__":
    # Connect to the database
    conn = sqlite3.connect("qa_feedback.db")
    cursor = conn.cursor()

    # Create the table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS qa_feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        prediction TEXT NOT NULL,
        ground_truth TEXT NOT NULL,
        comment TEXT
    )
    """)

    # Insert 10 example rows
    examples = [
        ("What is the capital of France?", "Paris", "Paris", None),
        ("Who wrote Hamlet?", "Shakespeare", "William Shakespeare", None),
        ("What is the boiling point of water?", "100°C", "100°C", None),
        ("What is 2 + 2?", "4", "4", None),
        ("Which planet is known as the Red Planet?", "Mars", "Mars", None),
        ("What is the chemical symbol for water?", "H2O", "H2O", None),
        ("Who painted the Mona Lisa?", "Leonardo da Vinci", "Leonardo da Vinci", None),
        ("What is the tallest mountain in the world?", "Mount Everest", "Mount Everest", None),
        ("How many continents are there?", "7", "7", None),
        ("What is the largest mammal?", "Blue Whale", "Blue Whale", None)
    ]

    cursor.executemany("""
    INSERT INTO qa_feedback (question, prediction, ground_truth, comment)
    VALUES (?, ?, ?, ?)
    """, examples)

    # Commit and close
    conn.commit()
    conn.close()

    print("Database seeded with 10 example rows.")
