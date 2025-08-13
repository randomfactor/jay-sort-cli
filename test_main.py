import unittest
from click.testing import CliRunner
from main import sort_albums

class TestAlbumSorter(unittest.TestCase):

    def test_sorting_logic_with_sample_10(self):
        """
        Tests the main script with sample-10.txt and compares the output
        with expected-10.txt.
        """
        runner = CliRunner()
        
        # Read the expected output from the file
        with open('expected-10.txt', 'r') as f:
            expected_output = f.read()

        # Invoke the CLI command with the sample file
        result = runner.invoke(sort_albums, ['sample-10.txt'])

        # Assert that the command executed successfully
        self.assertEqual(result.exit_code, 0)

        # Assert that the output matches the expected output
        # We use strip() to account for any trailing newlines
        self.assertEqual(result.output.strip(), expected_output.strip())

if __name__ == '__main__':
    unittest.main()
