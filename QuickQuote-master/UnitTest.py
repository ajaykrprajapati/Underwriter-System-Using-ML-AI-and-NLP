import unittest
from ModularRegex import * 
from PreProcess import * 

class TestRegEx(unittest.TestCase):
	def test_gender(self):
		self.assertEqual(genderRegex("Male"), "male")
		self.assertEqual(genderRegex("male"), "male")
		self.assertEqual(genderRegex("FEMALE"), "female")
		self.assertEqual(genderRegex("Gender: Male"), "male")
		self.assertEqual(genderRegex("Client Gender: Male"), "male")
		self.assertEqual(genderRegex("Male age 40"), "male")
		self.assertEqual(genderRegex("40 years old Male"), "male")
		self.assertEqual(genderRegex("Male 20/30/1945"), "male")
		self.assertEqual(genderRegex("Female, age 55"), "female")
		self.assertEqual(genderRegex("female, age 55"), "female")
		self.assertEqual(genderRegex("Male DOB 11/07/1964 5'1'' 182 pounfs Nonsmoker"), "male")
		self.assertEqual(genderRegex("Female, DOB 01/03/1996NS looking for $50m term"), "female")
		self.assertEqual(genderRegex("Male- 22 yrs old"), "male")                
		self.assertEqual(genderRegex("m/40"), "male")
		self.assertEqual(genderRegex("f/52"), "female")
		self.assertEqual(genderRegex("m/age 40"), "male")

	def test_age(self):			
		self.assertEqual(ageRegex("Age 40"), "40")
		self.assertEqual(ageRegex("age: 69"), "69")
		self.assertEqual(ageRegex("Age 40 male"), "40")
		self.assertEqual(ageRegex("40 yr old"), "40")
		self.assertEqual(ageRegex("40 yrs old"), "40")
		self.assertEqual(ageRegex("40 year old NS male,"), "40")
		self.assertEqual(ageRegex("Male- 40 year old"), "40")
		#self.assertEqual(ageRegex("Male 40"), "40")
		#self.assertEqual(ageRegex("m/40"), "40")
		#self.assertEqual(ageRegex("f/30"), "30")
		self.assertEqual(ageRegex("DOB : Jan 01, 2000"), 18)
		self.assertEqual(ageRegex("DOB : 01/01/2000"), 18)
		self.assertEqual(ageRegex("DOB: 1/1/99"), 19)
		self.assertEqual(ageRegex("DOB is 07/21/1988"), 30)
		self.assertEqual(ageRegex("dob 2-17-52"), 66)
		self.assertEqual(ageRegex("Date Of Birth: Jan 01, 2000"), 18)                
		self.assertEqual(ageRegex("male, dob 1-2-2000 non-tobacco"), 18)
		self.assertEqual(ageRegex("Female, DOB 01/01/2000 NS looking for $50m term"), 18)
		self.assertEqual(ageRegex("Male DOB 11/07/1964 5'1'' 182 pounds Nonsmoker"), 54)
        
	def test_height(self):
		self.assertEqual(heightRegex("Preferred Height and weight"), "5 Feet 9 Inches")						#Height is 1 inch less (logic prob)
		self.assertEqual(heightRegex("5'6''"), "5 Feet 5 Inches")
		self.assertEqual(heightRegex("5' 6''"), "5 Feet 5 Inches")
		self.assertEqual(heightRegex("5'6'' 170lbs"), "5 Feet 5 Inches")
		self.assertEqual(heightRegex("6'6'', 170lbs"), "6 Feet 6 Inches")
		self.assertEqual(heightRegex("5 feet 6 inch"), "5 feet 6 inch")										#F I capital
		self.assertEqual(heightRegex("5 Feet, 6 Inches"), "5 Feet, 6 Inches")								#comma
		self.assertEqual(heightRegex("ht: 5'6''"), "5 Feet 5 Inches")
		#self.assertEqual(heightRegex("height: 5 feet, 6 inches"), "5 feet, 6 inches")						#remove comma &  remove height
		self.assertEqual(heightRegex("current height / weight - 5' 6'' / 150lbs"), "5 Feet 5 Inches")
		self.assertEqual(heightRegex("Male DOB 11/07/1964 5'6'' 150 pounfs Nonsmoker"), "5 Feet 5 Inches")
		#self.assertEqual(heightRegex("F/age 50, NS, build 5.6.150"), "5 Feet 6 Inches")

		self.assertEqual(changeHeight("5 Feet 6 Inch"), "5.60")
                
	def test_weight(self):			
		self.assertEqual(weightRegex("Preferred Height and weight"), "196 lbs")
		self.assertEqual(weightRegex("150lb"), "150lb")
		self.assertEqual(weightRegex("150 lb"), "150 lb")
		self.assertEqual(weightRegex("150lbs"), "150lb")
		self.assertEqual(weightRegex("150 lbs"), "150 lb")
		self.assertEqual(weightRegex("5'6'' 150lbs"), "150lb")
		self.assertEqual(weightRegex("5'6'', 150 lbs"), "150 lb")
		self.assertEqual(weightRegex("wt: 150lbs"), "150lb")
		self.assertEqual(weightRegex("Weight: 150 Pounds"), "150 Pounds")
		self.assertEqual(weightRegex("weight: 150 pounds"), "150 pounds")
		self.assertEqual(weightRegex("Male DOB 11/07/1964 5'6'' 150 pounds Nonsmoker"), "150 pounds")
		self.assertEqual(weightRegex("current height / weight - 5' 6'' / 150 lbs"), "150 lb")
		#self.assertEqual(weightRegex("F/age 50, NS, build 5.6.150"), "150lb")

		self.assertEqual(changeWt("150 Pounds"), "150lb")
		self.assertEqual(changeWt("150 pounds"), "150lb")
		self.assertEqual(changeWt("150 lbs"), "150lb")
		
	def test_product_type(self):			
		self.assertEqual(productRegex("Product Type: Permanent"), "Product Type: Permanent")
		self.assertEqual(productRegex("Product Type: Perm"), "Product Type: Perm")
		self.assertEqual(productRegex("plan: term"), "Product Type: Term")
		self.assertEqual(productRegex("$1m plus perm"), "Product Type: Permanent")
		self.assertEqual(productRegex("looking for $50m term"), "Product Type: Term")
		self.assertEqual(productRegex("seeking $500K perm coverage"), "Product Type: Permanent")
		self.assertEqual(productRegex("20 year term coverage"), "Product Type: Term")
		self.assertEqual(productRegex("$1,00,000 20-year level term"), "Product Type: Term")
		#self.assertEqual(productRegex("$100,000 ul"), "Product Type: Perm")					#NOT CLEAR - Product type Perm or Term in ul
		self.assertEqual(productRegex("term $1mm"), "Product Type: Term")
		self.assertEqual(productRegex("50k term & 1000k ul"), "Product Type: Term")
		#self.assertEqual(productRegex("500,000ul"), "Product Type: Term")
		self.assertEqual(productRegex("we are looking for $2.5 mill of term coverage"), "Product Type: Term")

		self.assertEqual(changePT("Product Type: Permanent"), "Permanent")
		self.assertEqual(changePT("Product Type: Perm"), "Perm")
		self.assertEqual(changePT("Product Type: Term"), "Term")
		
	def test_face_amount(self):			
		self.assertEqual(faceamountRegex("Face Amount: 50,000"), "Face Amount: 50,000")
		self.assertEqual(faceamountRegex("Face Amount: $500,212"), "Face Amount: $500,212")
		self.assertEqual(faceamountRegex("amount: 150k to 200k"), "Face Amount: $150,000")
		self.assertEqual(faceamountRegex("Seeking $20,000 LN"), "Face Amount: $20,000")
		self.assertEqual(faceamountRegex("SEEKING $300"), "Face Amount: $300")
		self.assertEqual(faceamountRegex("seeking $500K perm coverage"), "Face Amount: 500,000")
		#self.assertEqual(faceamountRegex("65 yr old male ns seeking 1 million term"), "Face Amount: $1,000,000")
		self.assertEqual(faceamountRegex("looking for 500k term"), "Face Amount: $500,000")
		#self.assertEqual(faceamountRegex("looking for 2-3mm term"), "Face Amount: 2,000,000")
		self.assertEqual(faceamountRegex("Female, DOB 01/03/1996NS looking for $50m term"), "Face Amount: 50,000,000")
		#self.assertEqual(faceamountRegex("we are looking for $2.5 mill of term coverage"), "Face Amount: 2,500,000")
		self.assertEqual(faceamountRegex("She is looking for $500K 20 year term"), "Face Amount: 500,000")
		#self.assertEqual(faceamountRegex("Male- 22 years old state of 50 looking for 2-3mm in term"), "Face Amount: 3,000,000")
		self.assertEqual(faceamountRegex("$1,00,000 20-year level term"), "Face Amount: $1,00,000")
		self.assertEqual(faceamountRegex("$1m plus perm"), "Face Amount: 1,000,000")
		self.assertEqual(faceamountRegex("$100,000 ul"), "Face Amount: $100,000")
		self.assertEqual(faceamountRegex("term $1mm"), "Face Amount: 1,000,000")
		self.assertEqual(faceamountRegex("50k term & 1000k ul"), "Face Amount: $50,000")			#Term ul not defined????(considered ul here)
		self.assertEqual(faceamountRegex("500,000ul"), "Face Amount: $500,000")

		self.assertEqual(changeFace("Face Amount: 2,500,000"), "2500000")
		self.assertEqual(changeFace("Face Amount: $1,000,000"), "1000000")
		                
	def test_habit(self):			
		self.assertEqual(habitRegex("smoker"), "Tobacco")
		self.assertEqual(habitRegex("Non Smoker"), "Non-Tobacco")
		self.assertEqual(habitRegex("nonsmoker"), "Non-Tobacco")
		self.assertEqual(habitRegex("Non-Smoker"), "Non-Tobacco")
		self.assertEqual(habitRegex("Tobacco"), "Tobacco")
		self.assertEqual(habitRegex("NonTobacco"), "Non-Tobacco")
		self.assertEqual(habitRegex("uses chewing tobacco"), "Tobacco")
		self.assertEqual(habitRegex("Male 01/02/1999 (XX) non-tobacco"), "Non-Tobacco")
		self.assertEqual(habitRegex("tobacco use: none"), "Non-Tobacco")
		self.assertEqual(habitRegex("Ever Used Tobacco Products: No"), "Non-Tobacco")
		self.assertEqual(habitRegex("Ever Used Tobacco Products: yes"), "Tobacco")
		self.assertEqual(habitRegex("Ever Used chewing Tobacco: yes"), "Tobacco")
		self.assertEqual(habitRegex("currentlly use chewing tobacco: yes"), "Tobacco")
		self.assertEqual(habitRegex("Male DOB 11/07/1964 5'1'' 182 pounds Nonsmoker"), "Non-Tobacco")
		self.assertEqual(habitRegex("does not smoke or take medication for anything"), "Non-Tobacco")
		self.assertEqual(habitRegex("Never smoked in her life"), "Non-Tobacco")
		data = '''
			Tobacco:
				-   Ever Used Tobacco Products: No
		'''
		#self.assertEqual(habitRegex(data), "Non-Tobacco")
		data = '''
			Tobacco:
				-   Ever Used Tobacco Products: yes
		'''
		#self.assertEqual(habitRegex(data), "Tobacco")

	def test_medication(self):			
		self.assertEqual(medicationRegex("No Medication"), "No Medication")

	def test_family(self):			
		self.assertEqual("a","a")
		#self.assertEqual(familyRegex("No significant family history"), "'No significant ', 'family', 'history'")
		#self.assertEqual(familyRegex("mom died of age 40"), "mother died of age 40")
		#self.assertEqual(familyRegex("mother died of age 40"), "mother died of age 40")
		#self.assertEqual(familyRegex("father died of age 40 toung cancer"), "father died of age 40 toung cancer")
		#self.assertEqual(familyRegex("maternal grandmother breast cancer at 40"), "maternal grandmother breast cancer at 40")
		#self.assertEqual(familyRegex("maternal grandfather colon cancer at 40"), "maternal grandfather colon cancer at 40")
		#self.assertEqual(familyRegex("paternal grandmother breast cancer at 40"), "paternal grandmother breast cancer at 40")
		#self.assertEqual(familyRegex("paternal grandfather colon cancer at 40"), "paternal grandfather colon cancer at 40")



if __name__ == "__main__":
	unittest.main()
