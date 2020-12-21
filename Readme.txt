Team Members And Roll Number-
Shubham Nemani & 203050011
Pooja Verma & 203050072
Anish M M & 203050066

Project Topic - Automated Paraphrase Dataset Creation for Hindi and Malayalam

Project Description-We aimed to provide a semi-automated process for creating 
such a dataset for Hindi and Malayalam and provide 
(1) a large automatically created,unedited dataset with noisy labels, 
(2) a relatively smaller subset of the above which is manually edited/checked and has labels with no noise, 
(3) the code for the automated candidate pairs generation. Similar datasets are available for English where
 a large set of noisily labeled pairs augment a smaller correctly labeled dataset.

How to execute code-

1. For Hindi :
 	Install pyiwn and stanfordnlp - 
 	
 	!pip install pyiwn
 	!pip install stanfordnlp
 	
 	To generate positive paraphrase:
 	
 	1. Run Positive.py
 	2. Create object of class Positive_Paraphrases
 	3. Use any of below two methods and give hindi sentences as input:
 		a) get_paraphrase_by_synonym()
 		b) get_paraphrase_by_change_conj()
 		
 	To generate negative paraphrase:
 	
 	1. Run Negative.py
 	2. Create object of class Negative_Paraphrases
 	3. Use any of below two methods and give hindi sentences as input:
 		a) proper_noun_swap()
 		b) negation_by_compound()
 		
2. For Malayalam :
 	
 	To generate positive paraphrase:
 	
 	1. Run Positive.py
 	2. Create object of class PositiveParaphrases
 	3. Use any of below two methods and give hindi sentences as input:
 		a) generate() , input is 1 malayalam sentence
 		b) generate_for_pair() , input is sentences pair and their languages accordingly
 		
 	To generate negative paraphrase:
 	
 	1. Run Negative.py
 	2. Create object of class NegativeParaphrases
 	3. Use any of below two methods and give hindi sentences as input:
 		a) generate() , input is 1 malayalam sentence
