import unittest

import pandas as pd

from app.csv_import import extract_posts


class CsvImportTests(unittest.TestCase):
    def test_accepts_canonical_xquik_header(self):
        dataframe = pd.DataFrame({"Tweet Text": ["First post", "Second post"]})

        self.assertEqual(extract_posts(dataframe), ["First post", "Second post"])

    def test_normalizes_common_header_variants(self):
        dataframe = pd.DataFrame({" Full_Text ": ["Imported post"]})

        self.assertEqual(extract_posts(dataframe), ["Imported post"])

    def test_filters_missing_and_blank_posts(self):
        dataframe = pd.DataFrame({"text": [None, " ", "Useful post"]})

        self.assertEqual(extract_posts(dataframe), ["Useful post"])

    def test_rejects_files_without_a_text_column(self):
        dataframe = pd.DataFrame({"Tweet ID": ["1"]})

        with self.assertRaisesRegex(ValueError, "Tweet Text"):
            extract_posts(dataframe)


if __name__ == "__main__":
    unittest.main()
