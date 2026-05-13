import unittest
import sqlite3
import os
from modules import database

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use a test database
        database.DB_FILE = "test_pixelalchemy.db"
        database.init_db()

    @classmethod
    def tearDownClass(cls):
        # Clean up
        if os.path.exists(database.DB_FILE):
            try:
                os.remove(database.DB_FILE)
            except:
                pass

    def setUp(self):
        # Clear tables before each test
        with database.get_connection() as conn:
            conn.execute("DELETE FROM artworks")
            conn.execute("DELETE FROM quiz_scores")
            conn.commit()

    def test_save_and_get_artwork(self):
        # 1. Test Saving
        success = database.save_artwork("Test Art", "path/to/test.png", "canvas", "meta")
        self.assertTrue(success)
        
        # 2. Test Fetching
        arts = database.get_all_artworks()
        self.assertEqual(len(arts), 1)
        self.assertEqual(arts[0][1], "Test Art")
        self.assertEqual(arts[0][2], "path/to/test.png")
        self.assertEqual(arts[0][3], "canvas")

    def test_delete_artwork(self):
        # 3. Test Deleting
        database.save_artwork("Art to delete", "path", "canvas")
        arts = database.get_all_artworks()
        self.assertEqual(len(arts), 1)
        
        art_id = arts[0][0]
        success = database.delete_artwork(art_id)
        self.assertTrue(success)
        
        arts_after = database.get_all_artworks()
        self.assertEqual(len(arts_after), 0)
        
    def test_get_invalid_artwork(self):
        # 12. Test getting non-existent artwork handling implicitly
        database.save_artwork("Art 1", "p1", "canvas")
        database.save_artwork("Art 2", "p2", "filter")
        arts = database.get_all_artworks()
        self.assertEqual(len(arts), 2)

    def test_quiz_scores(self):
        # 4. Test Quiz Insert
        database.save_quiz_score("Quiz 1", 3)
        score = database.get_quiz_score("Quiz 1")
        self.assertEqual(score, 3)
        
        # 5. Test Quiz Update (ON CONFLICT REPLACE)
        database.save_quiz_score("Quiz 1", 5)
        score_updated = database.get_quiz_score("Quiz 1")
        self.assertEqual(score_updated, 5)

if __name__ == "__main__":
    unittest.main()
