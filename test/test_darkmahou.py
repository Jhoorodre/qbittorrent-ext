import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/darkmahou-qb')))

class MockNovaPrinter:
    def prettyPrinter(self, item):
        print("----- TORRENT FOUND -----")
        for key, value in item.items():
            print(f"{key}: {value}")
        print("-------------------------\n")

sys.modules['novaprinter'] = MockNovaPrinter()

from darkmahou import darkmahou

def test_search():
    plugin = darkmahou()
    plugin.search("A Lenda de Vox Machina")

if __name__ == '__main__':
    test_search()
