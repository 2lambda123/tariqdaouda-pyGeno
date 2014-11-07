import unittest
from pyGeno.Genome import Genome
from pyGeno.Protein import Protein

class pyGenoSNPTests(unittest.TestCase):

	def setUp(self):
		self.ref = Genome(name = 'GRCh37.75_Y-Only')

	def tearDown(self):
		pass

	def testNoModif(self) :
		from pyGeno.SNPFiltering import SNPFilter

		class MyFilter(SNPFilter) :
			def __init__(self) :
				SNPFilter.__init__(self)

			def filter(self, chromosome, dummySRY) :
				return None

		dummy = Genome(name = 'GRCh37.75_Y-Only', SNPs = 'dummySRY', SNPFilter = MyFilter())
		persProt = dummy.get(Protein, id = 'ENSP00000438917')[0]
		refProt = self.ref.get(Protein, id = 'ENSP00000438917')[0]

		self.assertEqual(persProt.transcript.cDNA[:20], refProt.transcript.cDNA[:20])
	
	def testInsert(self) :
		from pyGeno.SNPFiltering import SNPFilter

		class MyFilter(SNPFilter) :
			def __init__(self) :
				SNPFilter.__init__(self)

			def filter(self, chromosome, dummySRY) :
				from pyGeno.SNPFiltering import  SequenceInsert
					
				refAllele = chromosome.refSequence[dummySRY.start]
				return SequenceInsert('TCA')

		dummy = Genome(name = 'GRCh37.75_Y-Only', SNPs = 'dummySRY', SNPFilter = MyFilter())
		persProt = dummy.get(Protein, id = 'ENSP00000438917')[0]
		refProt = self.ref.get(Protein, id = 'ENSP00000438917')[0]

		self.assertEqual('ATGCAATCATATGCTTCTGC', refProt.transcript.cDNA[:20])
		self.assertEqual('ATGATGCAATCATATGCTTC', persProt.transcript.cDNA[:20])
	
	def testSNP(self) :
		from pyGeno.SNPFiltering import SNPFilter

		class MyFilter(SNPFilter) :
			def __init__(self) :
				SNPFilter.__init__(self)

			def filter(self, chromosome, dummySRY) :
				from pyGeno.SNPFiltering import SequenceSNP
				
				return SequenceSNP(dummySRY.alt)
		
		dummy = Genome(name = 'GRCh37.75_Y-Only', SNPs = 'dummySRY', SNPFilter = MyFilter())
		persProt = dummy.get(Protein, id = 'ENSP00000438917')[0]
		refProt = self.ref.get(Protein, id = 'ENSP00000438917')[0]
		self.assertEqual('M', refProt.sequence[0])
		self.assertEqual('L', persProt.sequence[0])
		
	def testDeletion(self) :
		from pyGeno.SNPFiltering import SNPFilter

		class MyFilter(SNPFilter) :
			def __init__(self) :
				SNPFilter.__init__(self)

			def filter(self, chromosome, dummySRY) :
				from pyGeno.SNPFiltering import SequenceDel
					
				refAllele = chromosome.refSequence[dummySRY.start]
				return SequenceDel(1)
		
		dummy = Genome(name = 'GRCh37.75_Y-Only', SNPs = 'dummySRY', SNPFilter = MyFilter())
		persProt = dummy.get(Protein, id = 'ENSP00000438917')[0]
		refProt = self.ref.get(Protein, id = 'ENSP00000438917')[0]

		self.assertEqual('ATGCAATCATATGCTTCTGC', refProt.transcript.cDNA[:20])
		self.assertEqual('TGCAATCATATGCTTCTGCT', persProt.transcript.cDNA[:20])

if __name__ == "__main__" :
	from pyGeno.bootstrap import importHumanReferenceYOnly, importDummySRY
	
	try :
		importHumanReferenceYOnly()
	except ValueError :
		print "--> Seems to already exist in db"
		
	try :
		importDummySRY()
	except ValueError :
		print "--> Seems to already exist in db"

	unittest.main()		