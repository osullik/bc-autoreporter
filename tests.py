import unittest

from parser import logEntryParser

class testInputHandling():
	print("Tests not implemented")

class testEntityExtraction(unittest.TestCase):
		

	def testSuccessModes(self):
		#Success Mode tests
		easyTest = "@HomerSimpson"
		mediumTest1 = "Should return @HomerSimpson"
		mediumTest2 = "@HomerSimpson should be returned"
		hardTest = "On January 15th, 2021, @HomerSimpson was observed to perform to a satisfactory standard. \
		This was evidenced by his successful completion of a routine safety check on Reactor 4. \
		His actions show #competence #attentiontodetail #safetyconsciousness."
		
		lowerCasingTest = "@homersimpson"
		upperCasingTest = "@HOMERSIMPSON"
		misspelledTest = "@HomerStimpson"
		
		simpleFailureTest = "HomerSimpson"
		multiEntityFailure = "Do not return HomerSimpson, return @BarneyGumble"
		distantStringFail = "Do not return @HomerThompson"
		floatingAtFail = "Do not return the party @ noon"
		noEntityTest = "Shouldnt return anything"

		namedEntites = ["HomerSimpson", "CarlCarlson", "MindySimmons"]

		succeedList = [easyTest, mediumTest1, mediumTest2, hardTest]
		entityMatchingTests = [lowerCasingTest, upperCasingTest, misspelledTest]
		failList = [simpleFailureTest, multiEntityFailure, distantStringFail, floatingAtFail, noEntityTest]

		lp = logEntryParser()

		for test in succeedList:
			self.assertEqual(lp.parseEntities(test, namedEntites), "HomerSimpson")

		for test in entityMatchingTests:
			self.assertEqual(lp.parseEntities(test, namedEntites), "HomerSimpson")

		for test in failList:
			self.assertNotEqual(lp.parseEntities(test, namedEntites), "HomerSimpson")

class testDateExtraction():
	print("Tests not implemented")

class testTagExtraction():
	print("Tests not implemented")

class testSentimentAnalysis():
	print("Tests not implemented")


#testEntityExtractor = testEntityExtraction()

if __name__ == '__main__':
	unittest.main()