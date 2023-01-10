# Authors

+ Pedro Fernandes - Department of Computer Engineering; Limerick Institute of Technology; Limerick, Ireland; Pedro.Fernandes@lit.ie
; Mathematics Department; Polytechnic Institute of Leiria; Leiria, Portugal; pedro.a.fernandes@ipleiria.pt
                  

+ Mário Antunes - Computer Science and Communication Research Centre (CIIC), School of Technology and Management, Polytechnic of Leiria; Leiria; Portugal;   mario.antunes@ipleiria.pt
INESC TEC, CRACS; Porto; Portugal

# Benford's law-based method

Several scripts are presented, some built-in Python (Conversion, Extract-features) and others in Matlab (Extract first digits, Tables CVM, Spearman and Pearson). The procedure is started by extracting the first digits from a database containing manipulated and authentic images (Extract-features). 
Subsequently, the obtained values are stored in a database and converted from .py format to .xls format (Conversion). The first digit is extracted from this database, and the hypothesis tests (Pearson, Spearman and Cramer Von Mises) are applied. 
This procedure will allow the classifications. This entire classification procedure can be carried out by calculating the P-Value obtained from the correlation between the empirical frequency of occurrence of the digits from Benford's law and the relative frequencies of the digits extracted from the set of images.

# Database containing manipulated and authentic images






The database used for the tests is available [here](ddd)


# General architecture of the method based on Benford's law








