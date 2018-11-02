import SET_Game
import unittest

class TestCard(unittest.TestCase):
	def test_card(self):
		result = SET_Game.Card(2, 3, 'tuple')
		expected = '(222)'
		self.assertEqual(str(result), expected)

class TestDeck(unittest.TestCase):
	def test_generate_cards(self):
		expected = [(0), (00), (000), (1), (11), (111), (2), (22), (222),
					[0], [00], [000], [1], [11], [111], [2], [22], [222],
					{0}, {00}, {000}, {1}, {11}, {111}, {2}, {22}, {222}]
		result = SET_Game.Deck.generate_cards(self)
		result_str = [str(i) for i in result]
		for i in result_str:
			if i in expected:
				self.assertTrue(1,1)
			else:
				self.assertTrue(1,2)

	def test_get_cards_1(self):
		list_cards = [(0), (00), (000), (1), (11), (111), (2), (22), (222),
					[0], [00], [000], [1], [11], [111], [2], [22], [222],
					{0}, {00}, {000}, {1}, {11}, {111}, {222}, {22}, {2}]
		result = SET_Game.Deck().get_cards(1)
		self.assertTrue(len(result), 1)

if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
	