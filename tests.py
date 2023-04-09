import unittest
import json

from parser import logEntryParser
from parser import inputHandler

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
		dashDate = "2021-02-28"
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
		hardTest2 = "On 2021-02-28 @Zutroy was observed to perform to an excellent standard. \
		This was evidenced by his successful troubleshooting of the reactor's cooling system, which prevented a potential meltdown. \
		His actions show #technical expertise and #calmness under pressure."

		successList = [dashDate, americanDate, americanDateShort, longDate, mediumDate, shortNoYear, longNoYear, longNoYear2, hardTest, hardTest2]

		for test in successList:
			self.assertEqual(self.lp_dates.parseDates(test, "2021"), "2021-02-28")


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
			self.assertNotEqual(self.lp_dates.parseDates(test, "2021"), "2021-02-34")

class testTagExtraction(unittest.TestCase):
	

	def setUp(self):
		self.lp_tags = logEntryParser()

	def testSuccessModes(self):
		singleTag = "#Test1"
		singleTagNoisy = "Return #Test1"
		singleTagHard = hardTest = "On January 15th, 2021, @HomerSimpson was observed to perform to a \
		satisfactory standard. This was evidenced by his successful completion of a \
		routine safety check on Reactor 4. His actions show #competence"

		multiTag = "#Test1, #Test2"
		multiTagContiguous = "Return #Test1 #Test2"
		multiTagNonContiguous = "Return #Test1 and then also #Test2"
		multiTagHard = "On January 15th, 2021, @HomerSimpson was observed to perform to a \
		satisfactory standard. This was evidenced by his successful completion of a \
		routine safety check on Reactor 4. His actions show #competence #attentiontodetail \
		#safetyconsciousness."

		successListSingle = [singleTag, singleTagNoisy]

		successListMulti = [multiTag, multiTagContiguous, multiTagNonContiguous]


		for test in successListSingle:
			self.assertEqual(self.lp_tags.parseTags(test), ["Test1"])
		self.assertEqual(self.lp_tags.parseTags(singleTagHard), ["competence"])

		for test in successListMulti:
			self.assertEqual(self.lp_tags.parseTags(test), ["Test1", "Test2"])

		self.assertEqual(self.lp_tags.parseTags(multiTagHard), ["competence", "attentiontodetail", "safetyconsciousness"])



	def testFailureModes(self):
		justTag = "#"
		floatingTag = " # "
		noTag = "Don't return anything"



class testSentimentAnalysis():
	print("testSentimentAnalysis not implemented")


class testJSONOutput(unittest.TestCase):

	def setUp(self):
		self.lp_json = logEntryParser()
		self.namedEntites = ["HomerSimpson", "CarlCarlson", "MindySimmons"]

	def testOutputSuccess(self):

		logEntry1 = "On January 15th, 2021, @HomerSimpson was observed to perform to a satisfactory standard. \
		This was evidenced by his successful completion of a routine safety check on Reactor 4. \
		His actions show #competence #attentiontodetail #safetyconsciousness."

		entity1 = "HomerSimpson"
		date1 = "2021-01-15"
		tags1 = ["competence", "attentiontodetail", "safetyconsciousness"]

		returnedDict = self.lp_json.convertLogToJSON(logEntry1, self.namedEntites, "2021")

		self.assertEqual(returnedDict["entity"], entity1)
		self.assertEqual(returnedDict["date"], date1)
		self.assertEqual(returnedDict["tagList"], tags1)
		self.assertEqual(returnedDict["observation"], logEntry1)

		js = json.dumps(returnedDict, indent=4)

		print(js)

class testInputHandling(unittest.TestCase):
	def setUp(self):
		self.fileName = "observations.txt"
		self.handler = inputHandler()
		self.namedEntites = ["HomerSimpson", "CarlCarlson", "MindySimmons"]

	def testBulkImport(self):
		observationList = self.handler.bulkImport(self.fileName)

		self.lp = logEntryParser()

		for observation in observationList:
			print(self.lp.convertLogToJSON(observation, self.namedEntites, "2021"))


if __name__ == '__main__':
	unittest.main()