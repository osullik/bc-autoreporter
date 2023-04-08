import unittest

from parser import logEntryParser

class testInputHandling():
	print("testInputHandling not implemented")

class testEntityExtraction(unittest.TestCase):

	def setUp(self):
		self.namedEntites = ["HomerSimpson", "CarlCarlson", "MindySimmons"]
		self.lp = logEntryParser()	

	def testSuccessModes(self):
		#Success Mode tests
		easyTest = "@HomerSimpson"
		mediumTest1 = "Should return @HomerSimpson"
		mediumTest2 = "@HomerSimpson should be returned"
		hardTest = "On January 15th, 2021, @HomerSimpson was observed to perform to a satisfactory standard. \
		This was evidenced by his successful completion of a routine safety check on Reactor 4. \
		His actions show #competence #attentiontodetail #safetyconsciousness."

		succeedList = [easyTest, mediumTest1, mediumTest2, hardTest]

		for test in succeedList:
			self.assertEqual(self.lp.parseEntities(test, self.namedEntites), "HomerSimpson")


	def testEntityMatching(self):
		lowerCasingTest = "@homersimpson"
		upperCasingTest = "@HOMERSIMPSON"
		misspelledTest = "@HomerStimpson"
		missingLetter = "@HmerSimpson"

		entityMatchingTests = [lowerCasingTest, upperCasingTest, misspelledTest, missingLetter]
		
		for test in entityMatchingTests:
			self.assertEqual(self.lp.parseEntities(test, self.namedEntites), "HomerSimpson")

	def testFailureModes(self):
		simpleFailureTest = "HomerSimpson"
		multiEntityFailure = "Do not return HomerSimpson, return @BarneyGumble"
		multiEntityChoosing = "Return @HomerSimpson, do not return @CarlCarlson"
		distantStringFail = "Do not return @HomerThompson"
		floatingAtFail = "Do not return the party @ noon"
		noEntityTest = "Shouldnt return anything"

		failList = [simpleFailureTest, multiEntityFailure, multiEntityChoosing, distantStringFail, floatingAtFail, noEntityTest]

		for test in failList:
			self.assertNotEqual(self.lp.parseEntities(test, self.namedEntites), "HomerSimpson")

class testDateExtraction(unittest.TestCase):

	def setUp(self):
		self.lp_dates = logEntryParser()

	def testSuccessModes(self):
		americanDate = "02/28/2021"
		americanDateShort = "02/28/21"
		longDate = "February 28th 2021"
		mediumDate = "28 Feb 21"
		shortNoYear = "28 Feb"
		longNoYear = "28 February"
		longNoYear2 = "February 28th"
		hardTest = "On February 28th 2021, @HomerSimpson was observed to perform to a satisfactory standard. \
		This was evidenced by his successful completion of a routine safety check on Reactor 4. His actions \
		show #competence #attentiontodetail #safetyconsciousness."

		successList = [americanDate, americanDateShort, longDate, mediumDate, shortNoYear, longNoYear, longNoYear2, hardTest]

		for test in successList:
			self.assertEqual(self.lp_dates.parseDates(test, "2021"), "2021/02/28")


	def testFailureModes(self):
		restOfWorldObvious = "28/02/2021"
		restOfWorldNotObvious = "04/02/2021"
		restOfWorldObviousShort = "28/02/2021"
		restOfWorldNotObvious = "04/02/21"

		longDateNotExist = "February 34th 2021"
		mediumDateNotExist = "34 Feb 21"
		shortNoYearDateNotExist = "34 Feb"

		#obviousWrongFormatList = [restOfWorldObvious, restOfWorldObviousShort]
		notObviousWrongFormatList = [restOfWorldNotObvious, restOfWorldObviousShort]
		notExistList = [longDateNotExist, mediumDateNotExist, shortNoYearDateNotExist]

		#for test in obviousWrongFormatList:
		#	self.assertNotEqual(self.lp_dates.parseDates(test, "2021"), "2021/02/28")

		#for test in notObviousWrongFormatList:
		#	self.assertNotEqual(self.lp_dates.parseDates(test, "2021"), "2021/04/02")

		for test in notExistList:
			self.assertNotEqual(self.lp_dates.parseDates(test, "2021"), "2021/02/34")


class testTagExtraction():
	print("testTagExtraction not implemented")

class testSentimentAnalysis():
	print("testSentimentAnalysis not implemented")

if __name__ == '__main__':
	unittest.main()