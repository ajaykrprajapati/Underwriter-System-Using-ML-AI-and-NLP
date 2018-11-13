import unittest
from ModularRegex import * 
from PreProcess import * 
import logging

# Log configuration and initialization
logger = logging.getLogger('QQ')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
fileHandler = logging.FileHandler(config.log)
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)

class TestGeneral(unittest.TestCase):
	def assertFeaturs(data, gender, age, height, weight, product, faceAmount, habit, medication, familyHistory):	
		self.assertEqual(genderRegex(data), gender)
		self.assertEqual(ageRegex(data), age)
		self.assertEqual(changeHeight(heightRegex(data)), height) 
		self.assertEqual(changeWt(weightRegex(data)), weight)
		self.assertEqual(changePT(productRegex(data)), productType)
		self.assertEqual(changeFace(faceamountRegex(data)), faceAmount)
		self.assertEqual(habitRegex(data), habit)
		self.assertEqual(medicationRegex(data), medication)
		self.assertEqual(familyRegex(data), familyHistory)

	def test1(self):	
		data = '''
			Gender: FEMALE
			DOB : Jan 01, 2000
			Product Type: Permanent		
			Face Amount: 50,000
			200KG

			Had bypass in 2010. 
			takes following medications:
			1. Metoprolol (Blood pressure) - diagnosed 2014 - Takes 25 mg daily 
			2. Levothyroxine (Thyroid) - diagnosed 2016 - Takes 25 mg 		
		'''
		
		logger.info(data)
                
                self.assertEqual(genderRegex(data), "female")
                self.assertEqual(ageRegex(data), 18)
                self.assertEqual(heightRegex(data), "")
                self.assertEqual(weightRegex(data), "200KG")
		self.assertEqual(productRegex(data), "Product Type: Permanent")  
		self.assertEqual(faceamountRegex(data), "Face Amount: 50,000")
		self.assertEqual(habitRegex(data), "")
		self.assertEqual(medicationRegex(data), "")
		self.assertEqual(familyRegex(data), "")
		
		self.assertEqual(changeHeight(heightRegex(data)), "0")
		self.assertEqual(changeWt(weightRegex(data)), "440lb")
		self.assertEqual(changePT(productRegex(data)), "Permanent")
		self.assertEqual(changeFace(faceamountRegex(data)), "50000")
		
		#self.assertFeaturs(data, "female", 18, "0", "440lb", "Permanent", "50000", "", "")
		
	def test2(self):	
		data = '''
			Gender: male
			DOB : 01/01/2000
			Face Amount: 250,000
			
			On following medications:
			1. Warfarin (Blood thinner) - diagnosed 2000 - Takes 3.5 to 4mg daily 
			2. Atorvastatin (Cholesterol) - diagnosed 2000 - Takes 80 mg daily 
			3. Digoxin (Heart) - Diagnosed 2000 - Takes .125 mg 
		'''
		
		logger.info(data)
                
                self.assertEqual(genderRegex(data), "male")
                self.assertEqual(ageRegex(data), 18)
                self.assertEqual(heightRegex(data), "")
                self.assertEqual(weightRegex(data), "")
		self.assertEqual(productRegex(data), "")  
		self.assertEqual(faceamountRegex(data), "Face Amount: 250,000")
		self.assertEqual(habitRegex(data), "")
		self.assertEqual(medicationRegex(data), "")
		self.assertEqual(familyRegex(data), "")

		self.assertEqual(changeHeight(heightRegex(data)), "0")
		self.assertEqual(changeWt(weightRegex(data)), "")
		self.assertEqual(changePT(productRegex(data)), "")
		self.assertEqual(changeFace(faceamountRegex(data)), "250000")

	def test3(self):	
		data = '''
			Male
			01/01/2000
			5' 6'
			200 lb

			No medications
			No significant family history
			No recent traffic violations
			He had stage 3 colon cancer X years ago.  He received chemotherapy, radiation, and surgery.  
			He has been cancer free since then.

			He had his gall bladder removed in 20XX.  There were no 
		'''
		
                logger.info(data)
                
                self.assertEqual(genderRegex(data), "male")
                self.assertEqual(ageRegex(data), 18)
                #self.assertEqual(heightRegex(data), "5' 6'") 
                self.assertEqual(weightRegex(data), "200 lb")
		self.assertEqual(productRegex(data), "")  
		self.assertEqual(faceamountRegex(data), "")
		self.assertEqual(habitRegex(data), "")
		self.assertEqual(medicationRegex(data), "No Medication")
		#self.assertEqual(familyRegex(data), "No significant family history")

		#self.assertEqual(changeHeight(heightRegex(data)), "5.6")
		self.assertEqual(changeWt(weightRegex(data)), "200lb")
		self.assertEqual(changePT(productRegex(data)), "")
		self.assertEqual(changeFace(faceamountRegex(data)), "")

	def test4(self):	
		data = '''
			General:
			    -   Client Gender: Female
			    -   Date Of Birth: DEC 20, 1966
			    -   Product Type: Term
			    -   Face Amount: $500,212
			Tobacco:
			    -   Ever Used Tobacco Products: No
			Case Notes: -
				MAIN MEDICAL ISSUES: Multiple history of Basal Cell and Squamous Cell Carcinoma skin cancers
				MEDICATIONS: Metoprolol ER 50mg tab, triamterene/hydrochlorothiazide ( HCTZ) 37.5 -25 mg tabs

				NOTES: Reviewed path reports for from
				Visit dates of  1/02/99, biopsy done  5/3/05,
				Strong family history for skin cancer in both parents and siblings.   
				All path reports show NO residual malignancy identified.    
				Most recent BCC was 1.5cm x 3.9 cm at time of procedure, client was also recommended for MOHS for treatment on Rt side of nose.NoneNoneNoneNoneNoneNoneNoneNoneNoneNoneNone
		'''
		
                logger.info(data)
                
                self.assertEqual(genderRegex(data), "female")
                self.assertEqual(ageRegex(data), 52)
                self.assertEqual(heightRegex(data), "") 
                self.assertEqual(weightRegex(data), "")
		self.assertEqual(productRegex(data), "Product Type: Term")  
		self.assertEqual(faceamountRegex(data), "Face Amount: $500,212")
		#self.assertEqual(habitRegex(data), "Non-Tobacco")
		self.assertEqual(medicationRegex(data), "")
		#self.assertEqual(familyRegex(data), "Strong family history for skin cancer in both parents and siblings")

		self.assertEqual(changeHeight(heightRegex(data)), "0")
		self.assertEqual(changeWt(weightRegex(data)), "")
		self.assertEqual(changePT(productRegex(data)), "Term")
		self.assertEqual(changeFace(faceamountRegex(data)), "500212")

	def test5(self):	
		data = '''
			Female, DOB 01/03/1996NS looking for $50m term
			DO not Eat tobacco
			Lives in XXXX XXXX, She is a US Citizen

			Does not own property in US but does have retirement accounts 
			Does missionary work in XXXX XXXX
			Does not plan to be there more than 5years.
			
			Would you offer?
		'''
		
		logger.info(data)
		
                self.assertEqual(genderRegex(data), "female")
                self.assertEqual(ageRegex(data), 22)
                self.assertEqual(heightRegex(data), "") 
                self.assertEqual(weightRegex(data), "")
		self.assertEqual(productRegex(data), "Product Type: Term")  
		self.assertEqual(faceamountRegex(data), "Face Amount: 50,000,000")
		self.assertEqual(habitRegex(data), "Non-Tobacco")
		self.assertEqual(medicationRegex(data), "")
		self.assertEqual(familyRegex(data), "")

		self.assertEqual(changeHeight(heightRegex(data)), "0")
		self.assertEqual(changeWt(weightRegex(data)), "")
		self.assertEqual(changePT(productRegex(data)), "Term")
		self.assertEqual(changeFace(faceamountRegex(data)), "50000000")

	def test6(self):	
		data = '''
			Subject: [External] Pascarella Case - Potential Insd (MS Hx)
			When you get a chance, please let me know what you think?

			Female
			20/30yrs old
			5'3' 255lbs lost 10-20 lbs via diet & exercise over past 9 mos

			Father died @ 50 (Tongue Cancer)
			Fam Hx: 
			Hx of MS 5' 6' in 
			X episodeslast one X/XX
			Minimal impairment vision blurred in left eye
		'''
		
                logger.info(data)
                
                self.assertEqual(genderRegex(data), "female")
                #self.assertEqual(ageRegex(data), 20)
                #self.assertEqual(heightRegex(data), "5' 3'") 
                self.assertEqual(weightRegex(data), "255lb")
		self.assertEqual(productRegex(data), "")  
		self.assertEqual(faceamountRegex(data), "")
		self.assertEqual(habitRegex(data), "")
		self.assertEqual(medicationRegex(data), "")
		#self.assertEqual(familyRegex(data), "Father died @ 50 (Tongue Cancer)")


	def test6(self):	
		data = '''
			Male- 22 years old state of 50 looking for 2-3mm in term 
			Has Crohnic disease 

			Last flare up July 2005  
			RX- Stelara  takes every X weeks 
			Just had Endoscopy and Colonoscopy all clean 
		'''
		
                logger.info(data)
                
                self.assertEqual(genderRegex(data), "male")
                #self.assertEqual(ageRegex(data), 22)
                #self.assertEqual(heightRegex(data), "") 
                self.assertEqual(weightRegex(data), "")
		self.assertEqual(productRegex(data), "Product Type: Term")  
		#self.assertEqual(faceamountRegex(data), "Face Amount: 2mm")
		self.assertEqual(habitRegex(data), "")
		self.assertEqual(medicationRegex(data), "")
		#self.assertEqual(familyRegex(data), "Father died @ 50 (Tongue Cancer)")

		self.assertEqual(changeHeight(heightRegex(data)), "0")
		self.assertEqual(changeWt(weightRegex(data)), "")
		self.assertEqual(changePT(productRegex(data)), "Term")
		#self.assertEqual(changeFace(faceamountRegex(data)), "2,000,000")



		
if __name__ == "__main__":
	unittest.main()
		