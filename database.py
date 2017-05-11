# coding=utf-8
from collections import defaultdict, namedtuple

Record = namedtuple('record', 'Name Code Answer')

example_data = dict()

def get_example(id):
    if id in example_data:
        return example_data[id].Code
    return None

def get_answer(id):
    if not id in example_data:
        return None, None
    result = example_data[id].Answer
    if '<fillintheblank>' in result:
        return result.split('<fillintheblank>', maxsplit=1)
    if 'Think about it' in result:
        a, b = result.split('Think about it', maxsplit=1)
        return a, 'Think about it'+b
    return result, None


example = '''


problem = 1.1 Calculation of Density

<h3>Example 1.1: Calculation of Density</h3>

<p>
<h4>Calculation of Density</h4>
Gold—in bricks, bars, and coins—has been a form of currency for centuries. In order to swindle people into paying for a brick of gold without actually investing in a brick of gold, people have considered filling the centers of hollow gold bricks with lead to fool buyers into thinking that the entire brick is gold. It does not work: Lead is a dense substance, but its density is not as great as that of gold, 19.3 g/cm<sup>3</sup>. What is the density of lead if a cube of lead has an edge length of 2.00 cm and a mass of 90.7 g?</p>
<p>
<h4>Solution</h4>
The density of a substance can be calculated by dividing its mass by its volume. The volume of a cube is calculated by cubing the edge length.</p>
volume of lead cube=2.00 cm×2.00 cm×2.00 cm=8.00 cm3
density=mass/volume=90.7 g/8.00 cm3=11.3 g/1.00 cm3=11.3 g/cm3
<p>(We will discuss the reason for rounding to the first decimal place in the next section.)</p>
<p>
<h4>Check Your Learning</h4>
(a) To three decimal places, what is the volume of a cube (cm<sup>3</sup>) with an edge length of 0.843 cm?</p>
<p>(b) If the cube in part (a) is copper and has a mass of 5.34 g, what is the density of copper to two decimal places?</p>

<h4>Answer:</h4>
<p>(a) 0.599 cm<sup>3</sup>; (b) 8.91 g/cm<sup>3</sup>
</p>

problem = 2.1b Testing Dalton’s Atomic Theory
<h3>Example 2.1b: Testing Dalton’s Atomic Theory</h3>
In the following drawing, the green spheres represent atoms of a certain element. The purple spheres represent atoms of another element. If the spheres touch, they are part of a single unit of a compound. Does the following chemical change represented by these symbols violate any of the ideas of Dalton’s atomic theory? If so, which one?
{"https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_02_01_Dalton8_img.jpg"}
<h4>Answer:</h4>
The starting materials consist of four green spheres and two purple spheres. The products consist of four green spheres and two purple spheres. This does not violate any of Dalton’s postulates: Atoms are neither created nor destroyed, but are redistributed in small, whole-number ratios.
problem = 2.2b Laws of Definite and Multiple Proportions
<h3>Example 2.2b: Laws of Definite and Multiple Proportions</h3>
A sample of compound X (a clear, colorless, combustible liquid with a noticeable odor) is analyzed and found to contain 14.13 g carbon and 2.96 g hydrogen. A sample of compound Y (a clear, colorless, combustible liquid with a noticeable odor that is slightly different from X’s odor) is analyzed and found to contain 19.91 g carbon and 3.34 g hydrogen. Are these data an example of the law of definite proportions, the law of multiple proportions, or neither? What do these data tell you about substances X and Y?
<h4>Answer:</h4>
In compound X, the mass ratio of carbon to hydrogen is 14.13 g C/2.96 g H. In compound Y, the mass ratio of carbon to oxygen is 19.91 g C/3.34 g H. The ratio of these ratios is 14.13 g C/2.96 g H/19.91 g C/3.34 g H=4.77 g C/g H/5.96 g C/g H=0.800=4/5. This small, whole-number ratio supports the law of multiple proportions. This means that X and Y are different compounds.
problem = 2.3b Composition of an Atom
<h3>Example 2.3b: Composition of an Atom</h3>
An ion of platinum has a mass number of 195 and contains 74 electrons. How many protons and neutrons does it contain, and what is its charge?
<h4>Answer:</h4>
78 protons; 117 neutrons; charge is 4+
problem = 2.4b Calculation of Average Atomic Mass
<h3>Example 2.4b: Calculation of Average Atomic Mass</h3>
A sample of magnesium is found to contain 78.70% of ^24Mg atoms (mass 23.98 amu), 10.13% of ^25Mg atoms (mass 24.99 amu), and 11.17% of ^26Mg atoms (mass 25.98 amu). Calculate the average mass of a Mg atom.
<h4>Answer:</h4>
24.31 amu
problem = 2.5b Calculation of Percent Abundance
<h3>Example 2.5b: Calculation of Percent Abundance</h3>
Naturally occurring copper consists of ^63Cu (mass 62.9296 amu) and ^65Cu (mass 64.9278 amu), with an average mass of 63.546 amu. What is the percent composition of Cu in terms of these two isotopes?
<h4>Answer:</h4>
69.15% Cu-63 and 30.85% Cu-65
problem = 2.6b Empirical and Molecular Formulas
<h3>Example 2.6b: Empirical and Molecular Formulas</h3>
A molecule of metaldehyde (a pesticide used for snails and slugs) contains 8 carbon atoms, 16 hydrogen atoms, and 4 oxygen atoms. What are the molecular and empirical formulas of metaldehyde?
<h4>Answer:</h4>
Molecular formula, C8H16O4; empirical formula, C2H4O
problem = 2.7b Naming Groups of Elements
<h3>Example 2.7b: Naming Groups of Elements</h3>
Give the group name for each of the following elements:
(a) krypton
(b) selenium
(c) barium
(d) lithium
<h4>Answer:</h4>
(a) noble gas; (b) chalcogen; (c) alkaline earth metal; (d) alkali metal
problem = 2.8b Composition of Ions
<h3>Example 2.8b: Composition of Ions</h3>
Give the symbol and name for the ion with 34 protons and 36 electrons.
<h4>Answer:</h4>
Se^2-, the selenide ion
problem = 2.9b Formation of Ions
<h3>Example 2.9b: Formation of Ions</h3>
Aluminum and carbon react to form an ionic compound. Predict which forms an anion, which forms a cation, and the charges of each ion. Write the symbol for each ion and name them.
<h4>Answer:</h4>
Al will form a cation with a charge of 3+: Al^3+, an aluminum ion. Carbon will form an anion with a charge of 4-: C^4-, a carbide ion.
problem = 2.10b Predicting the Formula of an Ionic Compound
<h3>Example 2.10b: Predicting the Formula of an Ionic Compound</h3>
Predict the formula of the ionic compound formed between the sodium cation, Na^+, and the sulfide anion, S^2-.
<h4>Answer:</h4>
Na2S
problem = 2.11b Predicting the Formula of a Compound with a Polyatomic Anion
<h3>Example 2.11b: Predicting the Formula of a Compound with a Polyatomic Anion</h3>
Predict the formula of the ionic compound formed between the lithium ion and the peroxide ion, O22- (Hint: Use the periodic table to predict the sign and the charge on the lithium ion.)
<h4>Answer:</h4>
Li2O2
problem = 2.12b Predicting the Type of Bonding in Compounds
<h3>Example 2.12b: Predicting the Type of Bonding in Compounds</h3>
Using the periodic table, predict whether the following compounds are ionic or covalent:
(a) SO2
(b) CaF2
(c) N2H4
(d) Al2(SO4)3
<h4>Answer:</h4>
(a) molecular; (b) ionic; (c) molecular; (d) ionic
problem = 2.13b Naming Ionic Compounds
<h3>Example 2.13b: Naming Ionic Compounds</h3>
Write the formulas of the following ionic compounds:
(a) chromium(III) phosphide
(b) mercury(II) sulfide
(c) manganese(II) phosphate
(d) copper(I) oxide
(e) chromium(VI) fluoride
<h4>Answer:</h4>
(a) CrP; (b) HgS; (c) Mn3(PO4)2; (d) Cu2O; (e) CrF6
problem = 2.14b Naming Covalent Compounds
<h3>Example 2.14b: Naming Covalent Compounds</h3>
Write the formulas for the following compounds:
(a) phosphorus pentachloride
(b) dinitrogen monoxide
(c) iodine heptafluoride
(d) carbon tetrachloride
<h4>Answer:</h4>
(a) PCl5; (b) N2O; (c) IF7; (d) CCl4

problem = 2.1 Testing Dalton’s Atomic Theory

<h3>Example 2.1: Testing Dalton’s Atomic Theory</h3>
In the following drawing, the green spheres represent atoms of a certain element. The purple spheres represent atoms of another element. If the spheres touch, they are part of a single unit of a compound. Does the following chemical change represented by these symbols violate any of the ideas of Dalton’s atomic theory? If so, which one?
{"https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_02_01_Dalton6_img.jpg"}
<h4>Solution</h4>
The starting materials consist of two green spheres and two purple spheres. The products consist of only one green sphere and one purple sphere. This violates Dalton’s postulate that atoms are neither created nor destroyed during a chemical change, but are merely redistributed. (In this case, atoms appear to have been destroyed.)

problem = 2.2 Laws of Definite and Multiple Proportions

<h3>Example 2.2: Laws of Definite and Multiple Proportions</h3>
A sample of compound A (a clear, colorless gas) is analyzed and found to contain 4.27 g carbon and 5.69 g oxygen. A sample of compound B (also a clear, colorless gas) is analyzed and found to contain 5.19 g carbon and 13.84 g oxygen. Are these data an example of the law of definite proportions, the law of multiple proportions, or neither? What do these data tell you about substances A and B?
<h4>Solution</h4>
In compound A, the mass ratio of carbon to oxygen is:
1.33 g O/1 g C
In compound B, the mass ratio of carbon to oxygen is:
2.67 g O/1 g C
The ratio of these ratios is:
1.33 g O/1 g C/2.67 g O/1 g C=1/2
This supports the law of multiple proportions. This means that A and B are different compounds, with A having one-half as much carbon per amount of oxygen (or twice as much oxygen per amount of carbon) as B. A possible pair of compounds that would fit this relationship would be A = CO2 and B = CO.

problem = 2.3 Composition of an Atom

<h3>Example 2.3: Composition of an Atom</h3>
Iodine is an essential trace element in our diet; it is needed to produce thyroid hormone. Insufficient iodine in the diet can lead to the development of a goiter, an enlargement of the thyroid gland (<a href="https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_02_03_Iodine.jpg">Figure 12</a>).
<img src="https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_02_03_Iodine.jpg">Figure 12(a) Insufficient iodine in the diet can cause an enlargement of the thyroid gland called a goiter. (b) The addition of small amounts of iodine to salt, which prevents the formation of goiters, has helped eliminate this concern in the US where salt consumption is high. (credit a: modification of work by “Almazi”/Wikimedia Commons; credit b: modification of work by Mike Mozart)
The addition of small amounts of iodine to table salt (iodized salt) has essentially eliminated this health concern in the United States, but as much as 40% of the world’s population is still at risk of iodine deficiency. The iodine atoms are added as anions, and each has a 1- charge and a mass number of 127. Determine the numbers of protons, neutrons, and electrons in one of these iodine anions.
<h4>Solution</h4>The atomic number of iodine (53) tells us that a neutral iodine atom contains 53 protons in its nucleus and 53 electrons outside its nucleus. Because the sum of the numbers of protons and neutrons equals the mass number, 127, the number of neutrons is 74 (127 - 53 = 74). Since the iodine is added as a 1- anion, the number of electrons is 54 [53 – (1–) = 54].

problem = 2.4 Calculation of Average Atomic Mass

<h3>Example 2.4: Calculation of Average Atomic Mass</h3>
A meteorite found in central Indiana contains traces of the noble gas neon picked up from the solar wind during the meteorite’s trip through the solar system. Analysis of a sample of the gas showed that it consisted of 91.84% ^20Ne (mass 19.9924 amu), 0.47% ^21Ne (mass 20.9940 amu), and 7.69% ^22Ne (mass 21.9914 amu). What is the average mass of the neon in the solar wind?
<h4>Solution</h4>
average mass=(0.9184×19.9924 amu)+(0.0047×20.9940 amu)+(0.0769×21.9914 amu)=(18.36+0.099+1.69)amu=20.15 amu
The average mass of a neon atom in the solar wind is 20.15 amu. (The average mass of a terrestrial neon atom is 20.1796 amu. This result demonstrates that we may find slight differences in the natural abundance of isotopes, depending on their origin.)

problem = 2.5 Calculation of Percent Abundance

<h3>Example 2.5: Calculation of Percent Abundance</h3>
Naturally occurring chlorine consists of ^35Cl (mass 34.96885 amu) and ^37Cl (mass 36.96590 amu), with an average mass of 35.453 amu. What is the percent composition of Cl in terms of these two isotopes?
<h4>Solution</h4>
The average mass of chlorine is the fraction that is ^35Cl times the mass of ^35Cl plus the fraction that is ^37Cl times the mass of ^37Cl.
average mass=(fraction of35Cl×mass of35Cl)+(fraction of37Cl×mass of37Cl)If we let x represent the fraction that is ^35Cl, then the fraction that is ^37Cl is represented by 1.00 - x.
(The fraction that is ^35Cl + the fraction that is ^37Cl must add up to 1, so the fraction of ^37Cl must equal 1.00 - the fraction of ^35Cl.)
Substituting this into the average mass equation, we have:
35.453 amu=(x×34.96885 amu)+[(1.00-x)×36.96590 amu]35.453=34.96885x+36.96590-36.96590x1.99705x=1.513x=1.513/1.99705=0.7576
So solving yields: x = 0.7576, which means that 1.00 - 0.7576 = 0.2424. Therefore, chlorine consists of 75.76% ^35Cl and 24.24% ^37Cl.

problem = 2.6 Empirical and Molecular Formulas

<h3>Example 2.6: Empirical and Molecular Formulas</h3>
Molecules of glucose (blood sugar) contain 6 carbon atoms, 12 hydrogen atoms, and 6 oxygen atoms. What are the molecular and empirical formulas of glucose?
<h4>Solution</h4>
The molecular formula is C6H12O6 because one molecule actually contains 6 C, 12 H, and 6 O atoms. The simplest whole-number ratio of C to H to O atoms in glucose is 1:2:1, so the empirical formula is CH2O.

problem = 2.7 Naming Groups of Elements

<h3>Example 2.7: Naming Groups of Elements</h3>
Atoms of each of the following elements are essential for life. Give the group name for the following elements:
(a) chlorine
(b) calcium
(c) sodium
(d) sulfur
<h4>Solution</h4>
The family names are as follows:
(a) halogen
(b) alkaline earth metal
(c) alkali metal
(d) chalcogen

problem = 2.8 Composition of Ions

<h3>Example 2.8: Composition of Ions</h3>
An ion found in some compounds used as antiperspirants contains 13 protons and 10 electrons. What is its symbol?
<h4>Solution</h4>
Because the number of protons remains unchanged when an atom forms an ion, the atomic number of the element must be 13. Knowing this lets us use the periodic table to identify the element as Al (aluminum). The Al atom has lost three electrons and thus has three more positive charges (13) than it has electrons (10). This is the aluminum cation, Al^3+.

problem = 2.9 Formation of Ions

<h3>Example 2.9: Formation of Ions</h3>
Magnesium and nitrogen react to form an ionic compound. Predict which forms an anion, which forms a cation, and the charges of each ion. Write the symbol for each ion and name them.
<h4>Solution</h4>
Magnesium’s position in the periodic table (group 2) tells us that it is a metal. Metals form positive ions (cations). A magnesium atom must lose two electrons to have the same number electrons as an atom of the previous noble gas, neon. Thus, a magnesium atom will form a cation with two fewer electrons than protons and a charge of 2+. The symbol for the ion is Mg^2+, and it is called a magnesium ion.
Nitrogen’s position in the periodic table (group 15) reveals that it is a nonmetal. Nonmetals form negative ions (anions). A nitrogen atom must gain three electrons to have the same number of electrons as an atom of the following noble gas, neon. Thus, a nitrogen atom will form an anion with three more electrons than protons and a charge of 3-. The symbol for the ion is N^3-, and it is called a nitride ion.

problem = 2.10 Predicting the Formula of an Ionic Compound

<h3>Example 2.10: Predicting the Formula of an Ionic Compound</h3>
The gemstone sapphire (<a href="https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_02_06_Sapphire.jpg">Figure 31</a>) is mostly a compound of aluminum and oxygen that contains aluminum cations, Al^3+, and oxygen anions, O^2-. What is the formula of this compound?
<img src="https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_02_06_Sapphire.jpg">Figure 31Although pure aluminum oxide is colorless, trace amounts of iron and titanium give blue sapphire its characteristic color. (credit: modification of work by Stanislav Doronenko)
<h4>Solution</h4>
Because the ionic compound must be electrically neutral, it must have the same number of positive and negative charges. Two aluminum ions, each with a charge of 3+, would give us six positive charges, and three oxide ions, each with a charge of 2-, would give us six negative charges. The formula would be Al2O3.

problem = 2.11 Predicting the Formula of a Compound with a Polyatomic Anion

<h3>Example 2.11: Predicting the Formula of a Compound with a Polyatomic Anion</h3>
Baking powder contains calcium dihydrogen phosphate, an ionic compound composed of the ions Ca^2+ and H2PO4-. What is the formula of this compound?
<h4>Solution</h4>
The positive and negative charges must balance, and this ionic compound must be electrically neutral. Thus, we must have two negative charges to balance the 2+ charge of the calcium ion. This requires a ratio of one Ca^2+ ion to two H2PO4- ions. We designate this by enclosing the formula for the dihydrogen phosphate ion in parentheses and adding a subscript 2. The formula is Ca(H2PO4)2.

problem = 2.12 Predicting the Type of Bonding in Compounds

<h3>Example 2.12: Predicting the Type of Bonding in Compounds</h3>
Predict whether the following compounds are ionic or molecular:
(a) KI, the compound used as a source of iodine in table salt
(b) H2O2, the bleach and disinfectant hydrogen peroxide
(c) CHCl3, the anesthetic chloroform
(d) Li2CO3, a source of lithium in antidepressants
<h4>Solution</h4>
(a) Potassium (group 1) is a metal, and iodine (group 17) is a nonmetal; KI is predicted to be ionic.
(b) Hydrogen (group 1) is a nonmetal, and oxygen (group 16) is a nonmetal; H2O2 is predicted to be molecular.
(c) Carbon (group 14) is a nonmetal, hydrogen (group 1) is a nonmetal, and chlorine (group 17) is a nonmetal; CHCl3 is predicted to be molecular.
(d) Lithium (group 1) is a metal, and carbonate is a polyatomic ion; Li2CO3 is predicted to be ionic.

problem = 2.13 Naming Ionic Compounds

<h3>Example 2.13: Naming Ionic Compounds</h3>
Name the following ionic compounds, which contain a metal that can have more than one ionic charge:
(a) Fe2S3
(b) CuSe
(c) GaN
(d) CrCl3
(e) Ti2(SO4)3
<h4>Solution</h4>The anions in these compounds have a fixed negative charge (S^2-, Se^2- , N^3-, Cl^-, and SO42-), and the compounds must be neutral. Because the total number of positive charges in each compound must equal the total number of negative charges, the positive ions must be Fe^3+, Cu^2+, Ga^3+, Cr^3+, and Ti^3+. These charges are used in the names of the metal ions:
(a) iron(III) sulfide
(b) copper(II) selenide
(c) gallium(III) nitride
(d) chromium(III) chloride
(e) titanium(III) sulfate

problem = 2.14 Naming Covalent Compounds

<h3>Example 2.14: Naming Covalent Compounds</h3>
Name the following covalent compounds:
(a) SF6
(b) N2O3
(c) Cl2O7
(d) P4O6
<h4>Solution</h4>
Because these compounds consist solely of nonmetals, we use prefixes to designate the number of atoms of each element:
(a) sulfur hexafluoride
(b) dinitrogen trioxide
(c) dichlorine heptoxide
(d) tetraphosphorus hexoxide

problem = 9.1b Conversion of Pressure Units
<h3>Example 9.1b: Conversion of Pressure Units</h3>
A typical barometric pressure in Kansas City is 740 torr. What is this pressure in atmospheres, in millimeters of mercury, in kilopascals, and in bar?
<h4>Answer:</h4>
0.974 atm; 740 mm Hg; 98.7 kPa; 0.987 bar
problem = 9.2b Calculation of Barometric Pressure
<h3>Example 9.2b: Calculation of Barometric Pressure</h3>
Calculate the height of a column of water at 25 °C that corresponds to normal atmospheric pressure. The density of water at this temperature is 1.0 g/cm^3.
<h4>Answer:</h4>
10.3 m
problem = 9.3b Calculation of Pressure Using a Closed-End Manometer
<h3>Example 9.3b: Calculation of Pressure Using a Closed-End Manometer</h3>
The pressure of a sample of gas is measured with a closed-end manometer. The liquid in the manometer is mercury. Determine the pressure of the gas in:
(a) torr
(b) Pa
(c) bar
{"https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_09_01_Manometer2_img.jpg"}
<h4>Answer:</h4>
(a) ~150 torr; (b) ~20,000 Pa; (c) ~0.20 bar
problem = 9.4b Calculation of Pressure Using an Open-End Manometer
<h3>Example 9.4b: Calculation of Pressure Using an Open-End Manometer</h3>
The pressure of a sample of gas is measured at sea level with an open-end Hg manometer, as shown to the right. Determine the pressure of the gas in:
(a) mm Hg
(b) atm
(c) kPa
{"https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_09_01_manometer4_img.jpg"}
<h4>Answer:</h4>
(a) 642 mm Hg; (b) 0.845 atm; (c) 85.6 kPa
problem = 9.5b Predicting Change in Pressure with Temperature
<h3>Example 9.5b: Predicting Change in Pressure with Temperature</h3>
A sample of nitrogen, N2, occupies 45.0 mL at 27 °C and 600 torr. What pressure will it have if cooled to –73 °C while the volume remains constant?
<h4>Answer:</h4>
400 torr
problem = 9.6b Predicting Change in Volume with Temperature
<h3>Example 9.6b: Predicting Change in Volume with Temperature</h3>
A sample of oxygen, O2, occupies 32.2 mL at 30 °C and 452 torr. What volume will it occupy at –70 °C and the same pressure?
<h4>Answer:</h4>
21.6 mL
problem = 9.7b Measuring Temperature with a Volume Change
<h3>Example 9.7b: Measuring Temperature with a Volume Change</h3>
What is the volume of a sample of ethane at 467 K and 1.1 atm if it occupies 405 mL at 298 K and 1.1 atm?
<h4>Answer:</h4>
635 mL
problem = 9.8b Volume of a Gas Sample
<h3>Example 9.8b: Volume of a Gas Sample</h3>
The sample of gas in <a href="https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_09_03_BoylesLaw1.jpg">Figure 13</a> has a volume of 30.0 mL at a pressure of 6.5 psi. Determine the volume of the gas at a pressure of 11.0 psi, using:
(a) the P-V graph in <a href="https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_09_03_BoylesLaw1.jpg">Figure 13</a>
(b) the 1/P vs. V graph in <a href="https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_09_03_BoylesLaw1.jpg">Figure 13</a>
(c) the Boyle’s law equation
Comment on the likely accuracy of each method.
<h4>Answer:</h4>
(a) about 17–18 mL; (b) ~18 mL; (c) 17.7 mL; it was more difficult to estimate well from the P-V graph, so (a) is likely more inaccurate than (b); the calculation will be as accurate as the equation and measurements allow
problem = 9.9b Using the Ideal Gas Law
<h3>Example 9.9b: Using the Ideal Gas Law</h3>
Calculate the pressure in bar of 2520 moles of hydrogen gas stored at 27 °C in the 180-L storage tank of a modern hydrogen-powered car.
<h4>Answer:</h4>
350 bar
problem = 9.10b Using the Combined Gas Law
<h3>Example 9.10b: Using the Combined Gas Law</h3>
A sample of ammonia is found to occupy 0.250 L under laboratory conditions of 27 °C and 0.850 atm. Find the volume of this sample at 0 °C and 1.00 atm.
<h4>Answer:</h4>
0.193 L
problem = 9.11b Derivation of a Density Formula from the Ideal Gas Law
<h3>Example 9.11b: Derivation of a Density Formula from the Ideal Gas Law</h3>
A gas was found to have a density of 0.0847 g/L at 17.0 °C and a pressure of 760 torr. What is its molar mass? What is the gas?
<h4>Answer:</h4>
ρ=Pℳ/RT
0.0847g/L=760torr×1atm/760torr×ℳ/0.0821 Latm/mol K×290 K
ℳ = 2.02 g/mol; therefore, the gas must be hydrogen (H2, 2.02 g/mol)
problem = 9.12b Empirical/Molecular Formula Problems Using the Ideal Gas Law and Density of a Gas
<h3>Example 9.12b: Empirical/Molecular Formula Problems Using the Ideal Gas Law and Density of a Gas</h3>
Acetylene, a fuel used welding torches, is comprised of 92.3% C and 7.7% H by mass. Find the empirical formula. If 1.10 g of acetylene occupies of volume of 1.00 L at 1.15 atm and 59.5 °C, what is the molecular formula for acetylene?
<h4>Answer:</h4>
Empirical formula, CH; Molecular formula, C2H2
problem = 9.13b Determining the Molar Mass of a Volatile Liquid
<h3>Example 9.13b: Determining the Molar Mass of a Volatile Liquid</h3>
A sample of phosphorus that weighs 3.243 × 10^-2 g exerts a pressure of 31.89 kPa in a 56.0-mL bulb at 550 °C. What are the molar mass and molecular formula of phosphorus vapor?
<h4>Answer:</h4>
124 g/mol P4
problem = 9.14b The Pressure of a Mixture of Gases
<h3>Example 9.14b: The Pressure of a Mixture of Gases</h3>
A 5.73-L flask at 25 °C contains 0.0388 mol of N2, 0.147 mol of CO, and 0.0803 mol of H2. What is the total pressure in the flask in atmospheres?
<h4>Answer:</h4>
1.137 atm
problem = 9.15b The Pressure of a Mixture of Gases
<h3>Example 9.15b: The Pressure of a Mixture of Gases</h3>
What is the pressure of a mixture of 0.200 g of H2, 1.00 g of N2, and 0.820 g of Ar in a container with a volume of 2.00 L at 20 °C?
<h4>Answer:</h4>
1.87 atm
problem = 9.16b Pressure of a Gas Collected Over Water
<h3>Example 9.16b: Pressure of a Gas Collected Over Water</h3>
A sample of oxygen collected over water at a temperature of 29.0 °C and a pressure of 764 torr has a volume of 0.560 L. What volume would the dry oxygen have under the same conditions of temperature and pressure?
<h4>Answer:</h4>
0.583 L
problem = 9.17b Reaction of Gases
<h3>Example 9.17b: Reaction of Gases</h3>
An acetylene tank for an oxyacetylene welding torch provides 9340 L of acetylene gas, C2H2, at 0 °C and 1 atm. How many tanks of oxygen, each providing 7.00 × 10^3 L of O2 at 0 °C and 1 atm, will be required to burn the acetylene?
!2C2H2 +5O2 -> 4CO2 +2H2O
<h4>Answer:</h4>
3.34 tanks (2.34 × 10^4 L)
problem = 9.18b Volumes of Reacting Gases
<h3>Example 9.18b: Volumes of Reacting Gases</h3>
What volume of O2(g) measured at 25 °C and 760 torr is required to react with 17.0 L of ethylene, C2H4(g), measured under the same conditions of temperature and pressure? The products are CO2 and water vapor.
<h4>Answer:</h4>
51.0 L
problem = 9.19b Volume of Gaseous Product
<h3>Example 9.19b: Volume of Gaseous Product</h3>
Sulfur dioxide is an intermediate in the preparation of sulfuric acid. What volume of SO2 at 343 °C and 1.21 atm is produced by burning l.00 kg of sulfur in oxygen?
<h4>Answer:</h4>
1.30 × 10^3 L
problem = 9.20b Applying Graham’s Law to Rates of Effusion
<h3>Example 9.20b: Applying Graham’s Law to Rates of Effusion</h3>
At a particular pressure and temperature, nitrogen gas effuses at the rate of 79 mL/s. Using the same apparatus at the same temperature and pressure, at what rate will sulfur dioxide effuse?
<h4>Answer:</h4>
52 mL/s
problem = 9.21b Effusion Time Calculations
<h3>Example 9.21b: Effusion Time Calculations</h3>
A party balloon filled with helium deflates to 2/3 of its original volume in 8.0 hours. How long will it take an identical balloon filled with the same number of moles of air (ℳ = 28.2 g/mol) to deflate to 1/2 of its original volume?
<h4>Answer:</h4>
32 h
problem = 9.22b Determining Molar Mass Using Graham’s Law
<h3>Example 9.22b: Determining Molar Mass Using Graham’s Law</h3>
Hydrogen gas effuses through a porous container 8.97-times faster than an unknown gas. Estimate the molar mass of the unknown gas.
<h4>Answer:</h4>
163 g/mol
problem = 9.23b Calculation of urms
<h3>Example 9.23b: Calculation of urms</h3>
Calculate the root-mean-square velocity for an oxygen molecule at –23 °C.
<h4>Answer:</h4>
441 m/s
problem = 9.24b Comparison of Ideal Gas Law and van der Waals Equation
<h3>Example 9.24b: Comparison of Ideal Gas Law and van der Waals Equation</h3>

problem = 9.1 Conversion of Pressure Units

<h3>Example 9.1: Conversion of Pressure Units</h3>
The United States National Weather Service reports pressure in both inches of Hg and millibars. Convert a pressure of 29.2 in. Hg into:
(a) torr
(b) atm
(c) kPa
(d) mbar
<h4>Solution</h4>
This is a unit conversion problem. The relationships between the various pressure units are given in <a href="https://opentextbc.ca/chemistry/chapter/9-1-gas-pressure/#fs-idp189967312">Table 1</a>.
(a) 29.2in Hg×25.4mm/1in
×1 torr/1mm Hg
=742 torr
(b) 742torr×1 atm/760torr=0.976 atm
(c) 742torr×101.325 kPa/760torr=98.9 kPa
(d) 98.9kPa×1000Pa/1kPa×1bar/100,000Pa×1000 mbar/1bar=989 mbar

problem = 9.2 Calculation of Barometric Pressure

<h3>Example 9.2: Calculation of Barometric Pressure</h3>
Show the calculation supporting the claim that atmospheric pressure near sea level corresponds to the pressure exerted by a column of mercury that is about 760 mm high. The density of mercury = 13.6 g/cm^3.
<h4>Solution</h4>
The hydrostatic pressure is given by p = hρg, with h = 760 mm, ρ = 13.6 g/cm^3, and g = 9.81 m/s^2. Plugging these values into the equation and doing the necessary unit conversions will give us the value we seek. (Note: We are expecting to find a pressure of ~101,325 Pa:)
101,325N/m2=101,325kg·m/s2/m2=101,325kg/m·s2
p=(760 mm×1 m/1000 mm)×(13.6 g/1cm3×1 kg/1000 g×(  100 cm )3/(  1 m )3)×(9.81 m/1s2)
=(0.760 m)(13,600kg/m3)(9.81m/s2)=1.01×105kg/ms2=1.01×105N/m2
=1.01×105Pa

problem = 9.3 Calculation of Pressure Using a Closed-End Manometer

<h3>Example 9.3: Calculation of Pressure Using a Closed-End Manometer</h3>
The pressure of a sample of gas is measured with a closed-end manometer, as shown to the right. The liquid in the manometer is mercury. Determine the pressure of the gas in:
(a) torr
(b) Pa
(c) bar
{"https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_09_01_Manometer1_img.jpg"}
<h4>Solution</h4>
The pressure of the gas is equal to a column of mercury of height 26.4 cm. (The pressure at the bottom horizontal line is equal on both sides of the tube. The pressure on the left is due to the gas and the pressure on the right is due to 26.4 cm Hg, or mercury.) We could use the equation p = hρg as in <a href="https://opentextbc.ca/chemistry/chapter/9-1-gas-pressure/#fs-idm5509408">Example 1</a>, but it is simpler to just convert between units using <a href="https://opentextbc.ca/chemistry/chapter/9-1-gas-pressure/#fs-idp189967312">Table 1</a>.
(a) 26.4cm Hg×10mm Hg/1cm Hg×1 torr/1mm Hg=264 torr
(b) 264torr×1atm/760torr×101,325 Pa/1atm=35,200 Pa
(c) 35,200Pa×1 bar/100,000Pa=0.352 bar

problem = 9.4 Calculation of Pressure Using an Open-End Manometer

<h3>Example 9.4: Calculation of Pressure Using an Open-End Manometer</h3>
The pressure of a sample of gas is measured at sea level with an open-end Hg (mercury) manometer, as shown to the right. Determine the pressure of the gas in:
(a) mm Hg
(b) atm
(c) kPa
{"https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_09_01_Manometer3_img.jpg"}
<h4>Solution</h4>
The pressure of the gas equals the hydrostatic pressure due to a column of mercury of height 13.7 cm plus the pressure of the atmosphere at sea level. (The pressure at the bottom horizontal line is equal on both sides of the tube. The pressure on the left is due to the gas and the pressure on the right is due to 13.7 cm of Hg plus atmospheric pressure.)
(a) In mm Hg, this is: 137 mm Hg + 760 mm Hg = 897 mm Hg
(b) 897mm Hg×1 atm/760mm Hg=1.18 atm
(c) 1.18atm×101.325 kPa/1atm=1.20×102kPa

problem = 9.5 Predicting Change in Pressure with Temperature

<h3>Example 9.5: Predicting Change in Pressure with Temperature</h3>
A can of hair spray is used until it is empty except for the propellant, isobutane gas.
(a) On the can is the warning “Store only at temperatures below 120 °F (48.8 °C). Do not incinerate.” Why?
(b) The gas in the can is initially at 24 °C and 360 kPa, and the can has a volume of 350 mL. If the can is left in a car that reaches 50 °C on a hot day, what is the new pressure in the can?
<h4>Solution</h4>
(a) The can contains an amount of isobutane gas at a constant volume, so if the temperature is increased by heating, the pressure will increase proportionately. High temperature could lead to high pressure, causing the can to burst. (Also, isobutane is combustible, so incineration could cause the can to explode.)
(b) We are looking for a pressure change due to a temperature change at constant volume, so we will use Amontons’s/Gay-Lussac’s law. Taking P1 and T1 as the initial values, T2 as the temperature where the pressure is unknown and P2 as the unknown pressure, and converting °C to K, we have:
P1/T1=P2/T2which means that360kPa/297K=P2/323K
Rearranging and solving gives: P2=360kPa×323K/297K=390kPa

problem = 9.6 Predicting Change in Volume with Temperature

<h3>Example 9.6: Predicting Change in Volume with Temperature</h3>
A sample of carbon dioxide, CO2, occupies 0.300 L at 10 °C and 750 torr. What volume will the gas have at 30 °C and 750 torr?
<h4>Solution</h4>
Because we are looking for the volume change caused by a temperature change at constant pressure, this is a job for Charles’s law. Taking V1 and T1 as the initial values, T2 as the temperature at which the volume is unknown and V2 as the unknown volume, and converting °C into K we have:
V1/T1=V2/T2which means that0.300L/283K=V2/303K
Rearranging and solving gives: V2=0.300L×303K/283K=0.321L
This answer supports our expectation from Charles’s law, namely, that raising the gas temperature (from 283 K to 303 K) at a constant pressure will yield an increase in its volume (from 0.300 L to 0.321 L).

problem = 9.7 Measuring Temperature with a Volume Change

<h3>Example 9.7: Measuring Temperature with a Volume Change</h3>
Temperature is sometimes measured with a gas thermometer by observing the change in the volume of the gas as the temperature changes at constant pressure. The hydrogen in a particular hydrogen gas thermometer has a volume of 150.0 cm^3 when immersed in a mixture of ice and water (0.00 °C). When immersed in boiling liquid ammonia, the volume of the hydrogen, at the same pressure, is 131.7 cm^3. Find the temperature of boiling ammonia on the kelvin and Celsius scales.
<h4>Solution</h4>
A volume change caused by a temperature change at constant pressure means we should use Charles’s law. Taking V1 and T1 as the initial values, T2 as the temperature at which the volume is unknown and V2 as the unknown volume, and converting °C into K we have:
V1/T1=V2/T2which means that150.0cm3/273.15K=131.7cm3/T2
Rearrangement gives T2=131.7cm3×273.15K/150.0cm3=239.8K
Subtracting 273.15 from 239.8 K, we find that the temperature of the boiling ammonia on the Celsius scale is –33.4 °C.

problem = 9.8 Volume of a Gas Sample

<h3>Example 9.8: Volume of a Gas Sample</h3>
The sample of gas in <a href="https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_09_03_BoylesLaw1.jpg">Figure 13</a> has a volume of 15.0 mL at a pressure of 13.0 psi. Determine the pressure of the gas at a volume of 7.5 mL, using:
(a) the P-V graph in <a href="https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_09_03_BoylesLaw1.jpg">Figure 13</a>
(b) the 1/P vs. V graph in <a href="https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_09_03_BoylesLaw1.jpg">Figure 13</a>
(c) the Boyle’s law equation
Comment on the likely accuracy of each method.
<h4>Solution</h4>
(a) Estimating from the P-V graph gives a value for P somewhere around 27 psi.
(b) Estimating from the 1/P versus V graph give a value of about 26 psi.
(c) From Boyle’s law, we know that the product of pressure and volume (PV) for a given sample of gas at a constant temperature is always equal to the same value. Therefore we have P1V1 = k and P2V2 = k which means that P1V1 = P2V2.
Using P1 and V1 as the known values 13.0 psi and 15.0 mL, P2 as the pressure at which the volume is unknown, and V2 as the unknown volume, we have:
P1V1=P2V2or13.0psi×15.0mL=P2×7.5mL
Solving:
P2=13.0psi×15.0mL/7.5mL=26psiIt was more difficult to estimate well from the P-V graph, so (a) is likely more inaccurate than (b) or (c). The calculation will be as accurate as the equation and measurements allow.

problem = 9.9 Using the Ideal Gas Law

<h3>Example 9.9: Using the Ideal Gas Law</h3>
Methane, CH4, is being considered for use as an alternative automotive fuel to replace gasoline. One gallon of gasoline could be replaced by 655 g of CH4. What is the volume of this much methane at 25 °C and 745 torr?
<h4>Solution</h4>
We must rearrange PV = nRT to solve for V: V=nRT/P
If we choose to use R = 0.08206 L atm mol^–1 K^–1, then the amount must be in moles, temperature must be in kelvin, and pressure must be in atm.
Converting into the “right” units:
n=655gCH4×1mol/16.043g CH4=40.8molT=25°C+273=298K
P=745torr×1atm/760torr=0.980atm
V=nRT/P=(40.8mol)(0.08206Latm mol–1K–1)(298K)/0.980atm=1.02×103L
It would require 1020 L (269 gal) of gaseous methane at about 1 atm of pressure to replace 1 gal of gasoline. It requires a large container to hold enough methane at 1 atm to replace several gallons of gasoline.

problem = 9.10 Using the Combined Gas Law

<h3>Example 9.10: Using the Combined Gas Law</h3>
When filled with air, a typical scuba tank with a volume of 13.2 L has a pressure of 153 atm (<a href="https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_09_02_Scuba.jpg">Figure 16</a>). If the water temperature is 27 °C, how many liters of air will such a tank provide to a diver’s lungs at a depth of approximately 70 feet in the ocean where the pressure is 3.13 atm?
<img src="https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_09_02_Scuba.jpg">Figure 16Scuba divers use compressed air to breathe while underwater. (credit: modification of work by Mark Goodchild)
Letting 1 represent the air in the scuba tank and 2 represent the air in the lungs, and noting that body temperature (the temperature the air will be in the lungs) is 37 °C, we have:
!P1V1/T1=P2V2/T2 -> (153atm)(13.2L)/(300K)=(3.13atm)(V2)/(310K)
Solving for V2:
V2=(153atm)(13.2L)(310K)/(300K)(3.13atm)=667L(Note: Be advised that this particular example is one in which the assumption of ideal gas behavior is not very reasonable, since it involves gases at relatively high pressures and low temperatures. Despite this limitation, the calculated volume can be viewed as a good “ballpark” estimate.)

problem = 9.11 Derivation of a Density Formula from the Ideal Gas Law

<h3>Example 9.11: Derivation of a Density Formula from the Ideal Gas Law</h3>
Use PV = nRT to derive a formula for the density of gas in g/L
<h4>Solution</h4>
PV = nRT
Rearrange to get (mol/L): n/v=P/RT
Multiply each side of the equation by the molar mass, ℳ. When moles are multiplied by ℳ in g/mol, g are obtained:
(ℳ)(n/V)=(P/RT)(ℳ)
g/L=ρ=Pℳ/RT

problem = 9.12 Empirical/Molecular Formula Problems Using the Ideal Gas Law and Density of a Gas

<h3>Example 9.12: Empirical/Molecular Formula Problems Using the Ideal Gas Law and Density of a Gas</h3>
Cyclopropane, a gas once used with oxygen as a general anesthetic, is composed of 85.7% carbon and 14.3% hydrogen by mass. Find the empirical formula. If 1.56 g of cyclopropane occupies a volume of 1.00 L at 0.984 atm and 50 °C, what is the molecular formula for cyclopropane?
<h4>Solution</h4>
Strategy: First solve the empirical formula problem using methods discussed earlier. Assume 100 g and convert the percentage of each element into grams. Determine the number of moles of carbon and hydrogen in the 100-g sample of cyclopropane. Divide by the smallest number of moles to relate the number of moles of carbon to the number of moles of hydrogen. In the last step, realize that the smallest whole number ratio is the empirical formula:
85.7 g C×1 mol C/12.01 g C=7.136 mol C7.136/7.136=1.00 mol C
14.3 g H×1 mol H/1.01 g H=14.158 mol H14.158/7.136=1.98 mol H
Empirical formula is CH2 [empirical mass (EM) of 14.03 g/empirical unit].
Next, use the density equation related to the ideal gas law to determine the molar mass:
d=Pℳ/RT1.56 g/1.00 L=0.984 atm×ℳ/0.0821 L atm/mol K×323 K
ℳ = 42.0 g/mol, ℳ/Eℳ=42.0/14.03=2.99, so (3)(CH2) = C3H6 (molecular formula)

problem = 9.13 Determining the Molar Mass of a Volatile Liquid

<h3>Example 9.13: Determining the Molar Mass of a Volatile Liquid</h3>
The approximate molar mass of a volatile liquid can be determined by:
Heating a sample of the liquid in a flask with a tiny hole at the top, which converts the liquid into gas that may escape through the hole
Removing the flask from heat at the instant when the last bit of liquid becomes gas, at which time the flask will be filled with only gaseous sample at ambient pressure
Sealing the flask and permitting the gaseous sample to condense to liquid, and then weighing the flask to determine the sample’s mass (see <a href="https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_09_03_liquidgas.jpg">Figure 19</a>)
<img src="https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_09_03_liquidgas.jpg">Figure 19When the volatile liquid in the flask is heated past its boiling point, it becomes gas and drives air out of the flask. At
Using this procedure, a sample of chloroform gas weighing 0.494 g is collected in a flask with a volume of 129 cm^3 at 99.6 °C when the atmospheric pressure is 742.1 mm Hg. What is the approximate molar mass of chloroform?
<h4>Solution</h4>
Since ℳ=m/n and n=PV/RT, substituting and rearranging gives ℳ=mRT/PV,
then
ℳ=mRT/PV=(0.494 g)×0.08206 L·atm/mol K×372.8 K/0.976 atm×0.129 L=120g/mol.

problem = 9.14 The Pressure of a Mixture of Gases

<h3>Example 9.14: The Pressure of a Mixture of Gases</h3>
A 10.0-L vessel contains 2.50 × 10^-3 mol of H2, 1.00 × 10^-3 mol of He, and 3.00 × 10^-4 mol of Ne at 35 °C.
(a) What are the partial pressures of each of the gases?
(b) What is the total pressure in atmospheres?
<h4>Solution</h4>The gases behave independently, so the partial pressure of each gas can be determined from the ideal gas equation, using P=nRT/V:
PH2=(2.50×10-3mol)(0.08206Latmmol-1K-1)(308K)/10.0L=6.32×10-3atmPHe=(1.00×10-3mol)(0.08206Latmmol-1K-1)(308K)/10.0L=2.53×10-3atmPNe=(3.00×10-4mol)(0.08206Latmmol-1K-1)(308K)/10.0L=7.58×10-4atmThe total pressure is given by the sum of the partial pressures:
PT=PH2+PHe+PNe=(0.00632+0.00253+0.00076)atm=9.61×10-3atm

problem = 9.15 The Pressure of a Mixture of Gases

<h3>Example 9.15: The Pressure of a Mixture of Gases</h3>
A gas mixture used for anesthesia contains 2.83 mol oxygen, O2, and 8.41 mol nitrous oxide, N2O. The total pressure of the mixture is 192 kPa.
(a) What are the mole fractions of O2 and N2O?
(b) What are the partial pressures of O2 and N2O?
<h4>Solution</h4>
The mole fraction is given by XA=nA/nTotal and the partial pressure is PA = XA × PTotal.
For O2,
XO2=nO2/nTotal=2.83 mol/(2.83+8.41)mol=0.252
and PO2=XO2×PTotal=0.252×192 kPa=48.4 kPa
For N2O,
XN2=nN2/nTotal=8.41 mol/(2.83+8.41)mol=0.748
and
PN2=XN2×PTotal=0.748×192 kPa=143.6 kPa

problem = 9.16 Pressure of a Gas Collected Over Water

<h3>Example 9.16: Pressure of a Gas Collected Over Water</h3>
If 0.200 L of argon is collected over water at a temperature of 26 °C and a pressure of 750 torr in a system like that shown in <a href="https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_09_03_WaterVapor.jpg">Figure 21</a>, what is the partial pressure of argon?
<h4>Solution</h4>
According to Dalton’s law, the total pressure in the bottle (750 torr) is the sum of the partial pressure of argon and the partial pressure of gaseous water:
PT=PAr+PH2O
Rearranging this equation to solve for the pressure of argon gives:
PAr=PT-PH2O
The pressure of water vapor above a sample of liquid water at 26 °C is 25.2 torr (<a href="https://opentextbc.ca/chemistry/back-matter/water-properties/">Appendix E</a>), so:
PAr=750torr-25.2torr=725torr

problem = 9.17 Reaction of Gases

<h3>Example 9.17: Reaction of Gases</h3>
Propane, C3H8(g), is used in gas grills to provide the heat for cooking. What volume of O2(g) measured at 25 °C and 760 torr is required to react with 2.7 L of propane measured under the same conditions of temperature and pressure? Assume that the propane undergoes complete combustion.
<h4>Solution</h4>
The ratio of the volumes of C3H8 and O2 will be equal to the ratio of their coefficients in the balanced equation for the reaction:
!C3H8(g) +5O2(g)   ->   3CO2(g) +4H2O(l)1 volume +5 volumes3 volumes +4 volumesFrom the equation, we see that one volume of C3H8 will react with five volumes of O2:
2.7LC3H8×5 LO2/1LC3H8=13.5 LO2
A volume of 13.5 L of O2 will be required to react with 2.7 L of C3H8.

problem = 9.18 Volumes of Reacting Gases

<h3>Example 9.18: Volumes of Reacting Gases</h3>
Ammonia is an important fertilizer and industrial chemical. Suppose that a volume of 683 billion cubic feet of gaseous ammonia, measured at 25 °C and 1 atm, was manufactured. What volume of H2(g), measured under the same conditions, was required to prepare this amount of ammonia by reaction with N2?
!N2(g) +3H2(g) -> 2NH3(g)
<h4>Solution</h4>
Because equal volumes of H2 and NH3 contain equal numbers of molecules and each three molecules of H2 that react produce two molecules of NH3, the ratio of the volumes of H2 and NH3 will be equal to 3:2. Two volumes of NH3, in this case in units of billion ft^3, will be formed from three volumes of H2:
683billionft3NH3×3 billionft3H2/2billionft3NH3=1.02×103billionft3H2
The manufacture of 683 billion ft^3 of NH3 required 1020 billion ft^3 of H2. (At 25 °C and 1 atm, this is the volume of a cube with an edge length of approximately 1.9 miles.)

problem = 9.19 Volume of Gaseous Product

<h3>Example 9.19: Volume of Gaseous Product</h3>
What volume of hydrogen at 27 °C and 723 torr may be prepared by the reaction of 8.88 g of gallium with an excess of hydrochloric acid?
!2Ga(s) +6HCl(aq) -> 2GaCl3(aq) +3H2(g)
<h4>Solution</h4>
To convert from the mass of gallium to the volume of H2(g), we need to do something like this:
{"https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_09_03_Example3_img.jpg"}
The first two conversions are:
8.88g Ga×1mol Ga/69.723g Ga×3 molH2/2mol Ga=0.191mol H2
Finally, we can use the ideal gas law:
VH2=(nRT/P)H2=0.191mol×0.08206 Latmmol-1K-1×300 K/0.951atm=4.94 L

problem = 9.20 Applying Graham’s Law to Rates of Effusion

<h3>Example 9.20: Applying Graham’s Law to Rates of Effusion</h3>
Calculate the ratio of the rate of effusion of hydrogen to the rate of effusion of oxygen.
<h4>Solution</h4>
From Graham’s law, we have:
rate of effusion of hydrogen/rate of effusion of oxygen=1.43g L-1/0.0899g L-1=1.20/0.300=4/1
Using molar masses:
rate of effusion of hydrogen/rate of effusion of oxygen=32g mol-1/2g mol-1=16/1=4/1
Hydrogen effuses four times as rapidly as oxygen.

problem = 9.21 Effusion Time Calculations

<h3>Example 9.21: Effusion Time Calculations</h3>
It takes 243 s for 4.46 × 10^-5 mol Xe to effuse through a tiny hole. Under the same conditions, how long will it take 4.46 × 10^-5 mol Ne to effuse?
<h4>Solution</h4>
It is important to resist the temptation to use the times directly, and to remember how rate relates to time as well as how it relates to mass. Recall the definition of rate of effusion:
rate of effusion=amount of gas transferred/time
and combine it with Graham’s law:
rate of effusion of gas Xe/rate of effusion of gas Ne=ℳNe/ℳXe
To get:
amount of Xe transferred/time for Xe/amount of Ne transferred/time for Ne=ℳNe/ℳXe
Noting that amount of A = amount of B, and solving for time for Ne:
amount of Xe/time for Xe/amount of Ne/time for Ne=time for Ne/time for Xe=ℳNe/ℳXe=ℳNe/ℳXe
and substitute values:
time for Ne/243s=20.2g mol/131.3g mol=0.392
Finally, solve for the desired quantity:
time for Ne=0.392×243s=95.3s
Note that this answer is reasonable: Since Ne is lighter than Xe, the effusion rate for Ne will be larger than that for Xe, which means the time of effusion for Ne will be smaller than that for Xe.

problem = 9.22 Determining Molar Mass Using Graham’s Law

<h3>Example 9.22: Determining Molar Mass Using Graham’s Law</h3>
An unknown gas effuses 1.66 times more rapidly than CO2. What is the molar mass of the unknown gas? Can you make a reasonable guess as to its identity?
<h4>Solution</h4>
From Graham’s law, we have:
rate of effusion of Unknown/rate of effusion of CO2=ℳCO2/ℳUnknown
Plug in known data:
1.66/1=44.0g/mol/ℳUnknown
Solve:
ℳUnknown=44.0g/mol/(1.66)2=16.0g/mol
The gas could well be CH4, the only gas with this molar mass.

problem = 9.23 Calculation of urms

<h3>Example 9.23: Calculation of urms</h3>
<h4>Solution</h4>
Convert the temperature into Kelvin:
30°C+273=303 K
Determine the mass of a nitrogen molecule in kilograms:
28.0g/1 mol×1 kg/1000g=0.028kg/mol
Replace the variables and constants in the root-mean-square velocity equation, replacing Joules with the equivalent kg m^2s^–2:
urms=3RT/m
urms=3(8.314J/mol K)(303 K)/(0.028kg/mol)=2.70×105m2s-2=519m/s

problem = 9.24 Comparison of Ideal Gas Law and van der Waals Equation

<h3>Example 9.24: Comparison of Ideal Gas Law and van der Waals Equation</h3>

problem = 16.1b Redistribution of Matter during a Spontaneous Process
<h3>Example 16.1b: Redistribution of Matter during a Spontaneous Process</h3>
Describe how matter and/or energy is redistributed when you empty a canister of compressed air into a room.
<h4>Answer:</h4>
This is also a dilution process, analogous to example (c). It entails both a greater and more uniform dispersal of matter as the compressed air in the canister is permitted to expand into the lower-pressure air of the room.
problem = 16.2b Determination of ΔS
<h3>Example 16.2b: Determination of ΔS</h3>
Consider the system shown in <a href="https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_16_03_Energy.jpg">Figure 9</a>. What is the change in entropy for the process where all the energy is transferred from the hot object (AB) to the cold object (CD)?
<h4>Answer:</h4>
0 J/K
problem = 16.3b Predicting the Sign of ∆S
<h3>Example 16.3b: Predicting the Sign of ∆S</h3>
Predict the sign of the enthalpy change for the following processes. Give a reason for your prediction.
!(a) NaNO3(s) -> Na +(aq) +NO3-(aq)
(b) the freezing of liquid water
!(c) CO2(s) -> CO2(g)
!(d) CaCO(s) -> CaO(s) +CO2(g)
<h4>Answer:</h4>
(a) Positive; The solid dissolves to give an increase of mobile ions in solution. (b) Negative; The liquid becomes a more ordered solid. (c) Positive; The relatively ordered solid becomes a gas. (d) Positive; There is a net production of one mole of gas.
problem = 16.4b Will Ice Spontaneously Melt?
<h3>Example 16.4b: Will Ice Spontaneously Melt?</h3>
Using this information, determine if liquid water will spontaneously freeze at the same temperatures. What can you say about the values of Suniv?
<h4>Answer:</h4>
Entropy is a state function, and freezing is the opposite of melting. At -10.00 °C spontaneous,  +0.7 J/K; at  +10.00 °C nonspontaneous, -0.9 J/K.
problem = 16.5b Determination of ΔS°
<h3>Example 16.5b: Determination of ΔS°</h3>
Calculate the standard entropy change for the following process:
!H2(g) +C2H4(g) -> C2H6(g)
<h4>Answer:</h4>
-120.6 J mol^-1 K^-1
problem = 16.6b Determination of ΔS°
<h3>Example 16.6b: Determination of ΔS°</h3>
Calculate the standard entropy change for the following reaction:
!Ca(OH)2(s) -> CaO(s) +H2O(l)
<h4>Answer:</h4>
24.7 J/mol·K
problem = 16.7b Evaluation of ΔG° Change from ΔH° and ΔS°
<h3>Example 16.7b: Evaluation of ΔG° Change from ΔH° and ΔS°</h3>
Use standard enthalpy and entropy data from <a href="https://opentextbc.ca/chemistry/back-matter/standard-thermodynamic-properties-for-selected-substances/">Appendix G</a> to calculate the standard free energy change for the reaction shown here (298 K). What does the computed value for ΔG° say about the spontaneity of this process?
!C2H6(g) -> H2(g) +C2H4(g)
<h4>Answer:</h4>
ΔG298°=102.0 kJ/mol; the reaction is nonspontaneous (not spontaneous) at 25 °C.
problem = 16.8b Calculation of ΔG298°
<h3>Example 16.8b: Calculation of ΔG298°</h3>
Calculate ΔG° using (a) free energies of formation and (b) enthalpies of formation and entropies (<a href="https://opentextbc.ca/chemistry/back-matter/standard-thermodynamic-properties-for-selected-substances/">Appendix G</a>). Do the results indicate the reaction to be spontaneous or nonspontaneous at 25 °C?
!C2H4(g) -> H2(g) +C2H2(g)
<h4>Answer:</h4>
-141.5 kJ/mol, nonspontaneous
problem = 16.9b Predicting the Temperature Dependence of Spontaneity
<h3>Example 16.9b: Predicting the Temperature Dependence of Spontaneity</h3>
Popular chemical hand warmers generate heat by the air-oxidation of iron:
!4Fe(s) +3O2(g) -> 2Fe2O3(s)
How does the spontaneity of this process depend upon temperature?
<h4>Answer:</h4>
ΔH and ΔS are negative; the reaction is spontaneous at low temperatures.
problem = 16.10b Equilibrium Temperature for a Phase Transition
<h3>Example 16.10b: Equilibrium Temperature for a Phase Transition</h3>
Use the information in <a href="https://opentextbc.ca/chemistry/back-matter/standard-thermodynamic-properties-for-selected-substances/">Appendix G</a> to estimate the boiling point of CS2.
<h4>Answer:</h4>
313 K (accepted value 319 K)
problem = 16.11b Calculating ΔG under Nonstandard Conditions
<h3>Example 16.11b: Calculating ΔG under Nonstandard Conditions</h3>
Calculate the free energy change for this same reaction at 875 °C in a 5.00 L mixture containing 0.100 mol of each gas. Is the reaction spontaneous under these conditions?
<h4>Answer:</h4>
ΔG = -136 kJ; yes
problem = 16.12b Calculating an Equilibrium Constant using Standard Free Energy Change
<h3>Example 16.12b: Calculating an Equilibrium Constant using Standard Free Energy Change</h3>
Use the thermodynamic data provided in <a href="https://opentextbc.ca/chemistry/back-matter/standard-thermodynamic-properties-for-selected-substances/">Appendix G</a> to calculate the equilibrium constant for the dissociation of dinitrogen tetroxide at 25 °C.
2NO2(g)⇌N2O4(g)
<h4>Answer:</h4>
K = 6.9

problem = 16.1 Redistribution of Matter during a Spontaneous Process

<h3>Example 16.1: Redistribution of Matter during a Spontaneous Process</h3>
Describe how matter is redistributed when the following spontaneous processes take place:
(a) A solid sublimes.
(b) A gas condenses.
(c) A drop of food coloring added to a glass of water forms a solution with uniform color.
<h4>Solution</h4>
<img src="https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_16_02_Process.jpg">Figure 6(credit a: modification of work by Jenny Downing; credit b: modification of work by “Fuzzy Gerdes”/Flickr; credit c: modification of work by Sahar Atwa)
(a) Sublimation is the conversion of a solid (relatively high density) to a gas (much lesser density). This process yields a much greater dispersal of matter, since the molecules will occupy a much greater volume after the solid-to-gas transition.
(b) Condensation is the conversion of a gas (relatively low density) to a liquid (much greater density). This process yields a much lesser dispersal of matter, since the molecules will occupy a much lesser volume after the solid-to-gas transition.
(c) The process in question is dilution. The food dye molecules initially occupy a much smaller volume (the drop of dye solution) than they occupy once the process is complete (in the full glass of water). The process therefore entails a greater dispersal of matter. The process may also yield a more uniform dispersal of matter, since the initial state of the system involves two regions of different dye concentrations (high in the drop, zero in the water), and the final state of the system contains a single dye concentration throughout.

problem = 16.2 Determination of ΔS

<h3>Example 16.2: Determination of ΔS</h3>
Consider the system shown here. What is the change in entropy for a process that converts the system from distribution (a) to (c)?
{"https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_16_03_Matter_img.jpg"}
<h4>Solution</h4>
We are interested in the following change:
The initial number of microstates is one, the final six:
ΔS=klnWc/Wa=1.38×10-23J/K×ln6/1=2.47×10-23J/K
The sign of this result is consistent with expectation; since there are more microstates possible for the final state than for the initial state, the change in entropy should be positive.

problem = 16.3 Predicting the Sign of ∆S

<h3>Example 16.3: Predicting the Sign of ∆S</h3>
Predict the sign of the entropy change for the following processes. Indicate the reason for each of your predictions.
!(a) One mole liquid water at room temperature  ->  one mole liquid water at 50 °C
!(b) Ag +(aq) +Cl-(aq) -> AgCl(s)
!(c) C6H6(l) +15/2O2(g) -> 6CO2(g) +3H2O(l)
!(d) NH3(s) -> NH3(l)
<h4>Solution</h4>
(a) positive, temperature increases
(b) negative, reduction in the number of ions (particles) in solution, decreased dispersal of matter
(c) negative, net decrease in the amount of gaseous species
(d) positive, phase transition from solid to liquid, net increase in dispersal of matter

problem = 16.4 Will Ice Spontaneously Melt?

<h3>Example 16.4: Will Ice Spontaneously Melt?</h3>
The entropy change for the process
!H2O(s) -> H2O(l)
is 22.1 J/K and requires that the surroundings transfer 6.00 kJ of heat to the system. Is the process spontaneous at -10.00 °C? Is it spontaneous at  +10.00 °C?
<h4>Solution</h4>
We can assess the spontaneity of the process by calculating the entropy change of the universe. If ΔSuniv is positive, then the process is spontaneous. At both temperatures, ΔSsys = 22.1 J/K and qsurr = -6.00 kJ.
At -10.00 °C (263.15 K), the following is true:
ΔSuniv=ΔSsys +ΔSsurr=ΔSsys +qsurr/T=22.1 J/K +-6.00×103J/263.15 K=-0.7J/K
Suniv < 0, so melting is nonspontaneous (not spontaneous) at -10.0 °C.
At 10.00 °C (283.15 K), the following is true:
ΔSuniv=ΔSsys +qsurr/T=22.1J/K +-6.00×103J/283.15 K= +0.9 J/K
Suniv > 0, so melting is spontaneous at 10.00 °C.

problem = 16.5 Determination of ΔS°

<h3>Example 16.5: Determination of ΔS°</h3>
Calculate the standard entropy change for the following process:
!H2O(g) -> H2O(l)<h4>Solution</h4>
The value of the standard entropy change at room temperature, ΔS298°, is the difference between the standard entropy of the product, H2O(l), and the standard entropy of the reactant, H2O(g).
ΔS298°=S298°(H2O(l))-S298°(H2O(g))=(70.0 Jmol-1K-1)-(188.8 Jmol-1K-1)=-118.8Jmol-1K-1
The value for ΔS298° is negative, as expected for this phase transition (condensation), which the previous section discussed.

problem = 16.6 Determination of ΔS°

<h3>Example 16.6: Determination of ΔS°</h3>
Calculate the standard entropy change for the combustion of methanol, CH3OH:
!2CH3OH(l) +3O2(g) -> 2CO2(g) +4H2O(l)<h4>Solution</h4>
The value of the standard entropy change is equal to the difference between the standard entropies of the products and the entropies of the reactants scaled by their stoichiometric coefficients.
ΔS°=ΔS298°=∑νS298°(products)-∑νS298°(reactants)
[2S298°(CO2(g)) +4S298°(H2O(l))]-[2S298°(CH3OH(l)) +3S298°(O2(g))]={[2(213.8) +4×70.0]-[2(126.8) +3(205.03)]}=-161.1J/mol·K

problem = 16.7 Evaluation of ΔG° Change from ΔH° and ΔS°

<h3>Example 16.7: Evaluation of ΔG° Change from ΔH° and ΔS°</h3>
Use standard enthalpy and entropy data from <a href="https://opentextbc.ca/chemistry/back-matter/standard-thermodynamic-properties-for-selected-substances/">Appendix G</a> to calculate the standard free energy change for the vaporization of water at room temperature (298 K). What does the computed value for ΔG° say about the spontaneity of this process?
<h4>Solution</h4>
The process of interest is the following:
!H2O(l) -> H2O(g)The standard change in free energy may be calculated using the following equation:
ΔG298°=ΔH°-TΔS°
From <a href="https://opentextbc.ca/chemistry/back-matter/standard-thermodynamic-properties-for-selected-substances/">Appendix G</a>, here is the data:
Substance
ΔHf°(kJ/mol)
S298°(J/K·mol)
H2O(l)
-286.83
70.0
H2O(g)
-241.82
188.8
Combining at 298 K:
ΔH°=ΔH298°=ΔHf°(H2O(g))-ΔHf°(H2O(l))=[-241.82 kJ-(-285.83)]kJ/mol=44.01 kJ/mol
ΔS°=ΔS298°=S298°(H2O(g))-S298°(H2O(l))=188.8J/mol·K-70.0J/K=118.8J/mol·K
ΔG°=ΔH°-TΔS°
Converting everything into kJ and combining at 298 K:
ΔG298°=ΔH°-TΔS°=44.01 kJ/mol-(298 K×118.8J/mol·K)×1 kJ/1000 J
44.01 kJ/mol-35.4 kJ/mol=8.6 kJ/mol
At 298 K (25 °C) ΔG298°>0, and so boiling is nonspontaneous (not spontaneous).

problem = 16.8 Calculation of ΔG298°

<h3>Example 16.8: Calculation of ΔG298°</h3>
Consider the decomposition of yellow mercury(II) oxide.
!HgO(s,yellow) -> Hg(l) +1/2O2(g)Calculate the standard free energy change at room temperature, ΔG298°, using (a) standard free energies of formation and (b) standard enthalpies of formation and standard entropies. Do the results indicate the reaction to be spontaneous or nonspontaneous under standard conditions?
<h4>Solution</h4>
The required data are available in <a href="https://opentextbc.ca/chemistry/back-matter/standard-thermodynamic-properties-for-selected-substances/">Appendix G</a> and are shown here.
Compound
ΔGf°(kJ/mol)
ΔHf°(kJ/mol)
S298°(J/K·mol)
HgO (s, yellow)
-58.43
-90.46
71.13
Hg(l)
0
0
75.9
O2(g)
0
0
205.2
(a) Using free energies of formation:
ΔG298°=∑νGS298°(products)-∑νΔG298°(reactants)
=[1ΔG298°Hg(l) +1/2ΔG298°O2(g)]-1ΔG298°HgO(s,yellow)
=[1mol(0 kJ/mol) +1/2mol(0 kJ/mol)]-1 mol(-58.43 kJ/mol)=58.43 kJ/mol
(b) Using enthalpies and entropies of formation:
ΔH298°=∑νΔH298°(products)-∑νΔH298°(reactants)
=[1ΔH298°Hg(l) +1/2ΔH298°O2(g)]-1ΔH298°HgO(s,yellow)
=[1 mol(0 kJ/mol) +1/2mol(0 kJ/mol)]-1 mol(-90.46 kJ/mol)=90.46 kJ/mol
ΔS298°=∑νΔS298°(products)-∑νΔS298°(reactants)
=[1ΔS298°Hg(l) +1/2ΔS298°O2(g)]-1ΔS298°HgO(s,yellow)
=[1 mol(75.9 J/mol K) +1/2mol(205.2 J/mol K)]-1 mol(71.13 J/mol K)=107.4 J/mol K
ΔG°=ΔH°-TΔS°=90.46 kJ-298.15 K×107.4 J/K·mol×1 kJ/1000 J
ΔG°=(90.46-32.01)kJ/mol=58.45 kJ/mol
Both ways to calculate the standard free energy change at 25 °C give the same numerical value (to three significant figures), and both predict that the process is nonspontaneous (not spontaneous) at room temperature.

problem = 16.9 Predicting the Temperature Dependence of Spontaneity

<h3>Example 16.9: Predicting the Temperature Dependence of Spontaneity</h3>
The incomplete combustion of carbon is described by the following equation:
!2C(s) +O2(g) -> 2CO(g)How does the spontaneity of this process depend upon temperature?
<h4>Solution</h4>
Combustion processes are exothermic (ΔH < 0). This particular reaction involves an increase in entropy due to the accompanying increase in the amount of gaseous species (net gain of one mole of gas, ΔS > 0). The reaction is therefore spontaneous (ΔG < 0) at all temperatures.

problem = 16.10 Equilibrium Temperature for a Phase Transition

<h3>Example 16.10: Equilibrium Temperature for a Phase Transition</h3>
As defined in the chapter on liquids and solids, the boiling point of a liquid is the temperature at which its solid and liquid phases are in equilibrium (that is, when vaporization and condensation occur at equal rates). Use the information in <a href="https://opentextbc.ca/chemistry/back-matter/standard-thermodynamic-properties-for-selected-substances/">Appendix G</a> to estimate the boiling point of water.
<h4>Solution</h4>
The process of interest is the following phase change:
!H2O(l) -> H2O(g)
When this process is at equilibrium, ΔG = 0, so the following is true:
0=ΔH°-TΔS°orT=ΔH°/ΔS°
Using the standard thermodynamic data from <a href="https://opentextbc.ca/chemistry/back-matter/standard-thermodynamic-properties-for-selected-substances/">Appendix G</a>,
ΔH°=ΔHf°(H2O(g))-ΔHf°(H2O(l))=-241.82 kJ/mol-(-285.83 kJ/mol)=44.01 kJ/mol
ΔS°=ΔS298°(H2O(g))-ΔS298°(H2O(l))=188.8 J/K·mol-70.0 J/K·mol=118.8 J/K·mol
T=ΔH°/ΔS°=44.01×103J/mol/118.8J/K·mol=370.5K=97.3°C
The accepted value for water’s normal boiling point is 373.2 K (100.0 °C), and so this calculation is in reasonable agreement. Note that the values for enthalpy and entropy changes data used were derived from standard data at 298 K (<a href="https://opentextbc.ca/chemistry/back-matter/standard-thermodynamic-properties-for-selected-substances/">Appendix G</a>). If desired, you could obtain more accurate results by using enthalpy and entropy changes determined at (or at least closer to) the actual boiling point.

problem = 16.11 Calculating ΔG under Nonstandard Conditions

<h3>Example 16.11: Calculating ΔG under Nonstandard Conditions</h3>
What is the free energy change for the process shown here under the specified conditions?
T = 25 °C, PN2=0.870 atm, PH2=0.250 atm, and PNH3=12.9 atm
!2NH3(g) -> 3H2(g) +N2(g)ΔG°=33.0 kJ/mol
<h4>Solution</h4>
The equation relating free energy change to standard free energy change and reaction quotient may be used directly:
ΔG=ΔG° +RTlnQ=33.0kJ/mol +(8.314J/mol K×298 K×ln(0.2503)×0.870/12.92)=9680J/molor 9.68 kJ/mol
Since the computed value for ΔG is positive, the reaction is nonspontaneous under these conditions.

problem = 16.12 Calculating an Equilibrium Constant using Standard Free Energy Change

<h3>Example 16.12: Calculating an Equilibrium Constant using Standard Free Energy Change</h3>
Given that the standard free energies of formation of Ag^+(aq), Cl^-(aq), and AgCl(s) are 77.1 kJ/mol, -131.2 kJ/mol, and -109.8 kJ/mol, respectively, calculate the solubility product, Ksp, for AgCl.
<h4>Solution</h4>
The reaction of interest is the following:
AgCl(s)⇌Ag+(aq)+Cl-(aq)Ksp=[Ag+][Cl-]
The standard free energy change for this reaction is first computed using standard free energies of formation for its reactants and products:
ΔG°=ΔG298°=[ΔGf°(Ag+(aq))+ΔGf°(Cl-(aq))]-[ΔGf°(AgCl(s))]=[77.1 kJ/mol-131.2 kJ/mol]-[-109.8 kJ/mol]=55.7 kJ/mol
The equilibrium constant for the reaction may then be derived from its standard free energy change:
Ksp=e-ΔG°/RT=exp(-ΔG°/RT)=exp(-55.7×103J/mol/8.314J/mol·K×298.15K)=exp(-22.470)=e-22.470=1.74×10-10
This result is in reasonable agreement with the value provided in <a href="https://opentextbc.ca/chemistry/back-matter/solubility-products/">Appendix J</a>.

problem = 13.1b Ion Concentrations in Pure Water
<h3>Example 13.1b: Ion Concentrations in Pure Water</h3>
The ion product of water at 80 °C is 2.4 × 10^-13. What are the concentrations of hydronium and hydroxide ions in pure water at 80 °C?
<h4>Answer:</h4>
[H3O^+] = [OH^-] = 4.9 × 10^-7 M
problem = 13.2b The Inverse Proportionality of [H3O+] and [OH−]
<h3>Example 13.2b: The Inverse Proportionality of [H3O+] and [OH−]</h3>
What is the hydronium ion concentration in an aqueous solution with a hydroxide ion concentration of 0.001 M at 25 °C?
<h4>Answer:</h4>
[H3O^+] = 1 × 10^-11 M
problem = 13.3b Representing the Acid-Base Behavior of an Amphoteric Substance
<h3>Example 13.3b: Representing the Acid-Base Behavior of an Amphoteric Substance</h3>
Write separate equations representing the reaction of H2PO4-
(a) as a base with HBr
(b) as an acid with OH^-
<h4>Answer:</h4>
(a) H2PO4-(aq)+HBr(aq)⇌H3PO4(aq)+Br-(aq); (b) H2PO4-(aq)+OH-(aq)⇌HPO42-(aq)+H2O(l)
problem = 13.4b Calculation of pH from [H3O+]
<h3>Example 13.4b: Calculation of pH from [H3O+]</h3>
Water exposed to air contains carbonic acid, H2CO3, due to the reaction between carbon dioxide and water:
CO2(aq)+H2O(l)⇌H2CO3(aq)
Air-saturated water has a hydronium ion concentration caused by the dissolved CO2 of 2.0 × 10^-6 M, about 20-times larger than that of pure water. Calculate the pH of the solution at 25 °C.
<h4>Answer:</h4>5.70
problem = 13.5b Calculation of Hydronium Ion Concentration from pH
<h3>Example 13.5b: Calculation of Hydronium Ion Concentration from pH</h3>
Calculate the hydronium ion concentration of a solution with a pH of -1.07.
<h4>Answer:</h4>
12 M
problem = 13.6b Calculation of pOH
<h3>Example 13.6b: Calculation of pOH</h3>
The hydronium ion concentration of vinegar is approximately 4 × 10^-3 M. What are the corresponding values of pOH and pH?
<h4>Answer:</h4>
pOH = 11.6, pH = 2.4
problem = 13.7b Calculation of Percent Ionization from pH
<h3>Example 13.7b: Calculation of Percent Ionization from pH</h3>
Calculate the percent ionization of a 0.10-M solution of acetic acid with a pH of 2.89.
<h4>Answer:</h4>
1.3% ionized
problem = 13.8b The Product Ka × Kb = Kw
<h3>Example 13.8b: The Product Ka × Kb = Kw</h3>
We can determine the relative acid strengths of NH4+ and HCN by comparing their ionization constants. The ionization constant of HCN is given in <a href="https://opentextbc.ca/chemistry/back-matter/ionization-constants-of-weak-acids/">Appendix H</a> as 4.9 × 10^-10. The ionization constant of NH4+ is not listed, but the ionization constant of its conjugate base, NH3, is listed as 1.8 × 10^-5. Determine the ionization constant of NH4+, and decide which is the stronger acid, HCN or NH4+.
<h4>Answer:</h4>
NH4+ is the slightly stronger acid (Ka for NH4+ = 5.6 × 10^-10).
problem = 13.9b Determination of Ka from Equilibrium Concentrations
<h3>Example 13.9b: Determination of Ka from Equilibrium Concentrations</h3>
What is the equilibrium constant for the ionization of the HSO4- ion, the weak acid used in some household cleansers:
HSO4-(aq)+H2O(l)⇌H3O+(aq)+SO42-(aq)
In one mixture of NaHSO4 and Na2SO4 at equilibrium, [H3O+] = 0.027 M; [HSO4-]=0.29M; and [SO42-]=0.13M.
<h4>Answer:</h4>
Ka for HSO4- = 1.2 × 10^-2
problem = 13.10b Determination of Kb from Equilibrium Concentrations
<h3>Example 13.10b: Determination of Kb from Equilibrium Concentrations</h3>
What is the equilibrium constant for the ionization of the HPO42- ion, a weak base:
HPO42-(aq)+H2O(l)⇌H2PO4-(aq)+OH-(aq)
In a solution containing a mixture of NaH2PO4 and Na2HPO4 at equilibrium, [OH^-] = 1.3 × 10^-6 M; [H2PO4-]=0.042M; and [HPO42-]=0.341M.
<h4>Answer:</h4>
Kb for HPO42-=1.6×10-7
problem = 13.11b Determination of Ka or Kb from pH
<h3>Example 13.11b: Determination of Ka or Kb from pH</h3>
The pH of a solution of household ammonia, a 0.950-M solution of NH3, is 11.612. What is Kb for NH3.
<h4>Answer:</h4>
Kb = 1.8 × 10^-5
problem = 13.12b Equilibrium Concentrations in a Solution of a Weak Acid
<h3>Example 13.12b: Equilibrium Concentrations in a Solution of a Weak Acid</h3>
Only a small fraction of a weak acid ionizes in aqueous solution. What is the percent ionization of acetic acid in a 0.100-M solution of acetic acid, CH3CO2H?
CH3CO2H(aq)+H2O(l)⇌H3O+(aq)+CH3CO2-(aq)Ka=1.8×10-5
(Hint: Determine [CH3CO2-] at equilibrium.) Recall that the percent ionization is the fraction of acetic acid that is ionized × 100, or [CH3CO2-]/[CH3CO2H]initial×100.
<h4>Answer:</h4>
percent ionization = 1.3%
problem = 13.13b Equilibrium Concentrations in a Solution of a Weak Base
<h3>Example 13.13b: Equilibrium Concentrations in a Solution of a Weak Base</h3>
(a) Show that the calculation in Step 2 of this example gives an x of 4.0 × 10^-3 and the calculation in Step 3 shows Kb = 6.3 × 10^-5.
(b) Find the concentration of hydroxide ion in a 0.0325-M solution of ammonia, a weak base with a Kb of 1.76 × 10^-5. Calculate the percent ionization of ammonia, the fraction ionized × 100, or [NH4+]/[NH3]×100
<h4>Answer:</h4>
7.56 × 10^-4 M, 2.33%
problem = 13.14b Equilibrium Concentrations in a Solution of a Weak Acid
<h3>Example 13.14b: Equilibrium Concentrations in a Solution of a Weak Acid</h3>
(a) Show that the quadratic formula gives x = 7.2 × 10^-2.
(b) Calculate the pH in a 0.010-M solution of caffeine, a weak base:
C8H10N4O2(aq)+H2O(l)⇌C8H10N4O2H+(aq)+OH-(aq)Kb=2.5×10-4
(Hint: It will be necessary to convert [OH^-] to [H3O+] or pOH to pH toward the end of the calculation.)
<h4>Answer:</h4>
pH 11.16
problem = 13.15b The pH of a Solution of a Salt of a Weak Base and a Strong Acid
<h3>Example 13.15b: The pH of a Solution of a Salt of a Weak Base and a Strong Acid</h3>
(a) Do the calculations and show that the hydronium ion concentration for a 0.233-M solution of C6H5NH3+ is 2.3 × 10^-3 and the pH is 2.64.
(b) What is the hydronium ion concentration in a 0.100-M solution of ammonium nitrate, NH4NO3, a salt composed of the ions NH4+ and NO3-. Use the data in <a href="https://opentextbc.ca/chemistry/chapter/13-3-shifting-equilibria-le-chateliers-principle/#fs-idm84795184">Table 3</a> to determine Kb for the ammonium ion. Which is the stronger acid C6H5NH3+ or NH4+?
<h4>Answer:</h4>
(a) Ka(forNH4+)=5.6×10-10, [H3O^+] = 7.5 × 10^-6 M; (b) C6H5NH3+ is the stronger acid.
problem = 13.16b Equilibrium in a Solution of a Salt of a Weak Acid and a Strong Base
<h3>Example 13.16b: Equilibrium in a Solution of a Salt of a Weak Acid and a Strong Base</h3>
What is the pH of a 0.083-M solution of CN^-? Use 4.9 × 10^-10 as Ka for HCN. Hint: We will probably need to convert pOH to pH or find [H3O^+] using [OH^-] in the final stages of this problem.
<h4>Answer:</h4>
11.11
problem = 13.17b Determining the Acidic or Basic Nature of Salts
<h3>Example 13.17b: Determining the Acidic or Basic Nature of Salts</h3>
Determine whether aqueous solutions of the following salts are acidic, basic, or neutral:
(a) K2CO3
(b) CaCl2
(c) KH2PO4
(d) (NH4)2CO3
(e) AlBr3
<h4>Answer:</h4>
(a) basic; (b) neutral; (c) basic; (d) basic; (e) acidic
problem = 13.18b Hydrolysis of [Al(H2O)6]3+
<h3>Example 13.18b: Hydrolysis of [Al(H2O)6]3+</h3>
What is [Al(H2O)5(OH)2+] in a 0.15-M solution of Al(NO3)3 that contains enough of the strong acid HNO3 to bring [H3O^+] to 0.10 M?
<h4>Answer:</h4>
2.1 × 10^-5 M
problem = 13.19b Ionization of a Diprotic Acid
<h3>Example 13.19b: Ionization of a Diprotic Acid</h3>
The concentration of H2S in a saturated aqueous solution at room temperature is approximately 0.1 M. Calculate [H3O+], [HS^-], and [S^2-] in the solution:
H2S(aq)+H2O(l)⇌H3O+(aq)+HS-(aq)Ka1=8.9×10-8HS-(aq)+H2O(l)⇌H3O+(aq)+S2-(aq)Ka2=1.0×10-19
<h4>Answer:</h4>
[H2S] = 0.1 M; [H3O+] = [HS^-] = 0.000094 M; [S^2-] = 1 × 10^-19 M
We note that the concentration of the sulfide ion is the same as Ka2. This is due to the fact that each subsequent dissociation occurs to a lesser degree (as acid gets weaker).
problem = 13.20b pH Changes in Buffered and Unbuffered Solutions
<h3>Example 13.20b: pH Changes in Buffered and Unbuffered Solutions</h3>
Show that adding 1.0 mL of 0.10 M HCl changes the pH of 100 mL of a 1.8 × 10^-5 M HCl solution from 4.74 to 3.00.
<h4>Answer:</h4>
Initial pH of 1.8 × 10^-5 M HCl; pH = -log[H3O^+] = -log[1.8 × 10^-5] = 4.74
Moles of H3O^+ in 100 mL 1.8 × 10^-5 M HCl; 1.8 × 10^-5 moles/L × 0.100 L = 1.8 × 10^-6
Moles of H3O^+ added by addition of 1.0 mL of 0.10 M HCl: 0.10 moles/L × 0.0010 L = 1.0 × 10^-4 moles; final pH after addition of 1.0 mL of 0.10 M HCl:
pH=-log[H3O+]=-log(total molesH3O+/total volume)=-log(1.0×10-4mol+1.8×10-6mol/101mL(1L/1000mL))=3.00
problem = 13.21b Calculating pH for Titration Solutions: Strong Acid/Strong Base
<h3>Example 13.21b: Calculating pH for Titration Solutions: Strong Acid/Strong Base</h3>
Calculate the pH for the strong acid/strong base titration between 50.0 mL of 0.100 M HNO3(aq) and 0.200 M NaOH (titrant) at the listed volumes of added base: 0.00 mL, 15.0 mL, 25.0 mL, and 40.0 mL.
<h4>Answer:</h4>
0.00: 1.000; 15.0: 1.5111; 25.0: 7; 40.0: 12.523
problem = 13.22b Titration of a Weak Acid with a Strong Base
<h3>Example 13.22b: Titration of a Weak Acid with a Strong Base</h3>
Calculate the pH for the weak acid/strong base titration between 50.0 mL of 0.100 M HCOOH(aq) (formic acid) and 0.200 M NaOH (titrant) at the listed volumes of added base: 0.00 mL, 15.0 mL, 25.0 mL, and 30.0 mL.
<h4>Answer:</h4>
0.00 mL: 2.37; 15.0 mL: 3.92; 25.00 mL: 8.29; 30.0 mL: 12.097

problem = 13.1 Ion Concentrations in Pure Water

<h3>Example 13.1: Ion Concentrations in Pure Water</h3>
What are the hydronium ion concentration and the hydroxide ion concentration in pure water at 25 °C?
<h4>Solution</h4>
The autoionization of water yields the same number of hydronium and hydroxide ions. Therefore, in pure water, [H3O^+] = [OH^-]. At 25 °C:
Kw=[H3O+][OH-]=[H3O+]2=[OH-]2=1.0×10-14So:
[H3O+]=[OH-]=1.0×10-14=1.0×10-7M
The hydronium ion concentration and the hydroxide ion concentration are the same, and we find that both equal 1.0 × 10^-7 M.

problem = 13.2 The Inverse Proportionality of [H3O+] and [OH−]

<h3>Example 13.2: The Inverse Proportionality of [H3O+] and [OH−]</h3>
A solution of carbon dioxide in water has a hydronium ion concentration of 2.0 × 10^-6 M. What is the concentration of hydroxide ion at 25 °C?
<h4>Solution</h4>
We know the value of the ion-product constant for water at 25 °C:
2H2O(l)⇌H3O+(aq)+OH-(aq)Kw=[H3O+][OH-]=1.0×10-14
Thus, we can calculate the missing equilibrium concentration.
Rearrangement of the Kw expression yields that [OH^-] is directly proportional to the inverse of [H3O^+]:
[OH-]=Kw/[H3O+]=1.0×10-14/2.0×10-6=5.0×10-9
The hydroxide ion concentration in water is reduced to 5.0 × 10^-9 M as the hydrogen ion concentration increases to 2.0 × 10^-6 M. This is expected from Le Châtelier’s principle; the autoionization reaction shifts to the left to reduce the stress of the increased hydronium ion concentration and the [OH^-] is reduced relative to that in pure water.
A check of these concentrations confirms that our arithmetic is correct:
Kw=[H3O+][OH-]=(2.0×10-6)(5.0×10-9)=1.0×10-14

problem = 13.3 Representing the Acid-Base Behavior of an Amphoteric Substance

<h3>Example 13.3: Representing the Acid-Base Behavior of an Amphoteric Substance</h3>
Write separate equations representing the reaction of HSO3-
(a) as an acid with OH^-
(b) as a base with HI
<h4>Solution</h4>
(a) HSO3-(aq)+OH-(aq)⇌SO32-(aq)+H2O(l)
(b) HSO3-(aq)+HI(aq)⇌H2SO3(aq)+I-(aq)

problem = 13.4 Calculation of pH from [H3O+]

<h3>Example 13.4: Calculation of pH from [H3O+]</h3>
What is the pH of stomach acid, a solution of HCl with a hydronium ion concentration of 1.2 × 10^-3 M?
<h4>Solution</h4>
pH=-log[H3O+]
=-log(1.2×10-3)
=-(-2.92)=2.92
(The use of logarithms is explained in <a href="https://opentextbc.ca/chemistry/back-matter/essential-mathematics/">Appendix B</a>. Recall that, as we have done here, when taking the log of a value, keep as many decimal places in the result as there are significant figures in the value.)

problem = 13.5 Calculation of Hydronium Ion Concentration from pH

<h3>Example 13.5: Calculation of Hydronium Ion Concentration from pH</h3>
Calculate the hydronium ion concentration of blood, the pH of which is 7.3 (slightly alkaline).
<h4>Solution</h4>
pH=-log[H3O+]=7.3
log[H3O+]=-7.3
[H3O+]=10-7.3or[H3O+]=antilog of -7.3
[H3O+]=5×10-8M
(On a calculator take the antilog, or the “inverse” log, of -7.3, or calculate 10^-7.3.)

problem = 13.6 Calculation of pOH

<h3>Example 13.6: Calculation of pOH</h3>
What are the pOH and the pH of a 0.0125-M solution of potassium hydroxide, KOH?
<h4>Solution</h4>
Potassium hydroxide is a highly soluble ionic compound and completely dissociates when dissolved in dilute solution, yielding [OH^-] = 0.0125 M:
pOH=-log[OH-]=-log0.0125
=-(-1.903)=1.903
The pH can be found from the pOH:
pH+pOH=14.00
pH=14.00-pOH=14.00-1.903=12.10

problem = 13.7 Calculation of Percent Ionization from pH

<h3>Example 13.7: Calculation of Percent Ionization from pH</h3>
Calculate the percent ionization of a 0.125-M solution of nitrous acid (a weak acid), with a pH of 2.09.
<h4>Solution</h4>
The percent ionization for an acid is:
[H3O+]eq/[HNO2]0×100
The chemical equation for the dissociation of the nitrous acid is: HNO2(aq)+H2O(l)⇌NO2-(aq)+H3O+(aq). Since 10^-pH = [H3O+], we find that 10^-2.09 = 8.1 × 10^-3 M, so that percent ionization is:
8.1×10-3/0.125×100=6.5%
Remember, the logarithm 2.09 indicates a hydronium ion concentration with only two significant figures.

problem = 13.8 The Product Ka × Kb = Kw

<h3>Example 13.8: The Product Ka × Kb = Kw</h3>
Use the Kb for the nitrite ion, NO2-, to calculate the Ka for its conjugate acid.
<h4>Solution</h4>Kb for NO2- is given in this section as 2.17 × 10^-11. The conjugate acid of NO2- is HNO2; Ka for HNO2 can be calculated using the relationship:
Ka×Kb=1.0×10-14=Kw
Solving for Ka, we get:
Ka=Kw/Kb=1.0×10-14/2.17×10-11=4.6×10-4This answer can be verified by finding the Ka for HNO2 in <a href="https://opentextbc.ca/chemistry/back-matter/ionization-constants-of-weak-acids/">Appendix H</a>.

problem = 13.9 Determination of Ka from Equilibrium Concentrations

<h3>Example 13.9: Determination of Ka from Equilibrium Concentrations</h3>
Acetic acid is the principal ingredient in vinegar (<a href="https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_14_03_Vinegar.jpg">Figure 11</a>); that's why it tastes sour. At equilibrium, a solution contains [CH3CO2H] = 0.0787 M and [H3O+]=[CH3CO2-]=0.00118M. What is the value of Ka for acetic acid?
<img src="https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_14_03_Vinegar.jpg">Figure 11Vinegar is a solution of acetic acid, a weak acid. (credit: modification of work by “HomeSpot HQ”/Flickr)
<h4>Solution</h4>
We are asked to calculate an equilibrium constant from equilibrium concentrations. At equilibrium, the value of the equilibrium constant is equal to the reaction quotient for the reaction:
CH3CO2H(aq)+H2O(l)⇌H3O+(aq)+CH3CO2-(aq)
Ka=[H3O+][CH3CO2-]/[CH3CO2H]=(0.00118)(0.00118)/0.0787=1.77×10-5

problem = 13.10 Determination of Kb from Equilibrium Concentrations

<h3>Example 13.10: Determination of Kb from Equilibrium Concentrations</h3>
Caffeine, C8H10N4O2 is a weak base. What is the value of Kb for caffeine if a solution at equilibrium has [C8H10N4O2] = 0.050 M, [C8H10N4O2H+] = 5.0 × 10^-3 M, and [OH^-] = 2.5 × 10^-3 M?
<h4>Solution</h4>
At equilibrium, the value of the equilibrium constant is equal to the reaction quotient for the reaction:
C8H10N4O2(aq)+H2O(l)⇌C8H10N4O2H+(aq)+OH-(aq)
Kb=[C8H10N4O2H+][OH-]/[C8H10N4O2]=(5.0×10-3)(2.5×10-3)/0.050=2.5×10-4

problem = 13.11 Determination of Ka or Kb from pH

<h3>Example 13.11: Determination of Ka or Kb from pH</h3>
The pH of a 0.0516-M solution of nitrous acid, HNO2, is 2.34. What is its Ka?
HNO2(aq)+H2O(l)⇌H3O+(aq)+NO2-(aq)
<h4>Solution</h4>
We determine an equilibrium constant starting with the initial concentrations of HNO2, H3O+, and NO2- as well as one of the final concentrations, the concentration of hydronium ion at equilibrium. (Remember that pH is simply another way to express the concentration of hydronium ion.)
We can solve this problem with the following steps in which x is a change in concentration of a species in the reaction:
{"https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_14_03_steps_img.jpg"}
We can summarize the various concentrations and changes as shown here (the concentration of water does not appear in the expression for the equilibrium constant, so we do not need to consider its concentration):
{"https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_14_03_ICETable1_img.jpg"}
To get the various values in the ICE (Initial, Change, Equilibrium) table, we first calculate [H3O+], the equilibrium concentration of H3O+, from the pH:
[H3O+]=10-2.34=0.0046M
The change in concentration of H3O+, x[H3O+], is the difference between the equilibrium concentration of H3O^+, which we determined from the pH, and the initial concentration, [H3O+]i. The initial concentration of H3O+ is its concentration in pure water, which is so much less than the final concentration that we approximate it as zero (~0).
The change in concentration of NO2- is equal to the change in concentration of [H3O+]. For each 1 mol of H3O+ that forms, 1 mol of NO2- forms. The equilibrium concentration of HNO2 is equal to its initial concentration plus the change in its concentration.
Now we can fill in the ICE table with the concentrations at equilibrium, as shown here:
{"https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_14_03_ICETable2_img.jpg"}
Finally, we calculate the value of the equilibrium constant using the data in the table:
Ka=[H3O+][NO2-]/[HNO2]=(0.0046)(0.0046)/(0.0470)=4.5×10-4

problem = 13.12 Equilibrium Concentrations in a Solution of a Weak Acid

<h3>Example 13.12: Equilibrium Concentrations in a Solution of a Weak Acid</h3>
Formic acid, HCO2H, is the irritant that causes the body’s reaction to ant stings (<a href="https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_14_03_AntSting.jpg">Figure 12</a>).
<img src="https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_14_03_AntSting.jpg">Figure 12The pain of an ant’s sting is caused by formic acid. (credit: John Tann)
What is the concentration of hydronium ion and the pH in a 0.534-M solution of formic acid?
HCO2H(aq)+H2O(l)⇌H3O+(aq)+HCO2-(aq)Ka=1.8×10-4
<h4>Solution</h4>
Determine x and equilibrium concentrations. The equilibrium expression is:
HCO2H(aq)+H2O(l)⇌H3O+(aq)+HCO2-(aq)
The concentration of water does not appear in the expression for the equilibrium constant, so we do not need to consider its change in concentration when setting up the ICE table.
The table shows initial concentrations (concentrations before the acid ionizes), changes in concentration, and equilibrium concentrations follows (the data given in the problem appear in color):
{"https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_14_03_ICETable3_img.jpg"}
Solve for x and the equilibrium concentrations. At equilibrium:
Ka=1.8×10-4=[H3O+][HCO2-]/[HCO2H]
=(x)(x)/0.534-x=1.8×10-4
Now solve for x. Because the initial concentration of acid is reasonably large and Ka is very small, we assume that x << 0.534, which permits us to simplify the denominator term as (0.534 - x) = 0.534. This gives:
Ka=1.8×10-4=x2+/0.534
Solve for x as follows:
x2+=0.534×(1.8×10-4)=9.6×10-5
x=9.6×10-5
=9.8×10-3
To check the assumption that x is small compared to 0.534, we calculate:
x/0.534=9.8×10-3/0.534=1.8×10-2(1.8%of 0.534)
x is less than 5% of the initial concentration; the assumption is valid.
We find the equilibrium concentration of hydronium ion in this formic acid solution from its initial concentration and the change in that concentration as indicated in the last line of the table:
[H3O+]=~0+x=0+9.8×10-3M.
=9.8×10-3M
The pH of the solution can be found by taking the negative log of the [H3O+], so:
-log(9.8×10-3)=2.01

problem = 13.13 Equilibrium Concentrations in a Solution of a Weak Base

<h3>Example 13.13: Equilibrium Concentrations in a Solution of a Weak Base</h3>
Find the concentration of hydroxide ion in a 0.25-M solution of trimethylamine, a weak base:
(CH3)3N(aq)+H2O(l)⇌(CH3)3NH+(aq)+OH-(aq)Kb=6.3×10-5<h4>Solution</h4>
This problem requires that we calculate an equilibrium concentration by determining concentration changes as the ionization of a base goes to equilibrium. The solution is approached in the same way as that for the ionization of formic acid in <a href="https://opentextbc.ca/chemistry/chapter/13-3-shifting-equilibria-le-chateliers-principle/#fs-idm159829376">Example 11</a>. The reactants and products will be different and the numbers will be different, but the logic will be the same:
{"https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_14_03_steps4_img.jpg"}
Determine x and equilibrium concentrations. The table shows the changes and concentrations:
{"https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_14_03_ICETable4_img.jpg"}
Solve for x and the equilibrium concentrations. At equilibrium:
Kb=[(CH3)3NH+][OH-]/[(CH3)3N]=(x)(x)/0.25-x=6.3×10-5
If we assume that x is small relative to 0.25, then we can replace (0.25 - x) in the preceding equation with 0.25. Solving the simplified equation gives:
x=4.0×10-3
This change is less than 5% of the initial concentration (0.25), so the assumption is justified.
Recall that, for this computation, x is equal to the equilibrium concentration of hydroxide ion in the solution (see earlier tabulation):
[OH-]=~0+x=x=4.0×10-3M
=4.0×10-3M
Then calculate pOH as follows:
pOH=-log(4.0×10-3)=2.40
Using the relation introduced in the previous section of this chapter:
pH+pOH=pKw=14.00
permits the computation of pH:
pH=14.00-pOH=14.00-2.40=11.60
Check the work. A check of our arithmetic shows that Kb = 6.3 × 10^-5.

problem = 13.14 Equilibrium Concentrations in a Solution of a Weak Acid

<h3>Example 13.14: Equilibrium Concentrations in a Solution of a Weak Acid</h3>
Sodium bisulfate, NaHSO4, is used in some household cleansers because it contains the HSO4- ion, a weak acid. What is the pH of a 0.50-M solution of HSO4-?
HSO4-(aq)+H2O(l)⇌H3O+(aq)+SO42-(aq)Ka=1.2×10-2
<h4>Solution</h4>
We need to determine the equilibrium concentration of the hydronium ion that results from the ionization of HSO4- so that we can use [H3O+] to determine the pH. As in the previous examples, we can approach the solution by the following steps:
{"https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_14_03_steps5_img.jpg"}
Determine x and equilibrium concentrations. This table shows the changes and concentrations:
{"https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_14_03_ICETable5_img.jpg"}
Solve for x and the concentrations. As we begin solving for x, we will find this is more complicated than in previous examples. As we discuss these complications we should not lose track of the fact that it is still the purpose of this step to determine the value of x.
At equilibrium:
Ka=1.2×10-2=[H3O+][SO42-]/[HSO4-]=(x)(x)/0.50-x
If we assume that x is small and approximate (0.50 - x) as 0.50, we find:
x=7.7×10-2
When we check the assumption, we calculate:
x/[HSO4-]i
x/0.50=7.7×10-2/0.50=0.15(15%)
The value of x is not less than 5% of 0.50, so the assumption is not valid. We need the quadratic formula to find x.
The equation:
Ka=1.2×10-2=(x)(x)/0.50-x
gives
6.0×10-3-1.2×10-2x=x2+
or
x2++1.2×10-2x-6.0×10-3=0
This equation can be solved using the quadratic formula. For an equation of the form
ax2++bx+c=0,
x is given by the equation:
x=-b±b2+-4ac/2a
In this problem, a = 1, b = 1.2 × 10^-3, and c = -6.0 × 10^-3.
Solving for x gives a negative root (which cannot be correct since concentration cannot be negative) and a positive root:
x=7.2×10-2
Now determine the hydronium ion concentration and the pH:
[H3O+]=~0+x=0+7.2×10-2M
=7.2×10-2M
The pH of this solution is:
pH=-log[H3O+]=-log7.2×10-2=1.14

problem = 13.15 The pH of a Solution of a Salt of a Weak Base and a Strong Acid

<h3>Example 13.15: The pH of a Solution of a Salt of a Weak Base and a Strong Acid</h3>
Aniline is an amine that is used to manufacture dyes. It is isolated as aniline hydrochloride, [C6H5NH3+]Cl, a salt prepared by the reaction of the weak base aniline and hydrochloric acid. What is the pH of a 0.233 M solution of aniline hydrochloride?
C6H5NH3+(aq)+H2O(l)⇌H3O+(aq)+C6H5NH2(aq)
<h4>Solution</h4>The new step in this example is to determine Ka for the C6H5NH3+ ion. The C6H5NH3+ ion is the conjugate acid of a weak base. The value of Ka for this acid is not listed in <a href="https://opentextbc.ca/chemistry/back-matter/ionization-constants-of-weak-acids/">Appendix H</a>, but we can determine it from the value of Kb for aniline, C6H5NH2, which is given as 4.3 × 10^-10 (<a href="https://opentextbc.ca/chemistry/chapter/13-3-shifting-equilibria-le-chateliers-principle/#fs-idm84795184">Table 3</a> and <a href="https://opentextbc.ca/chemistry/back-matter/ionization-constants-of-weak-bases/">Appendix I</a>):
Ka(forC6H5NH3+)×Kb(forC6H5NH2)=Kw=1.0×10-14
Ka(forC6H5NH3+)=Kw/Kb(forC6H5NH2)=1.0×10-14/4.3×10-10=2.3×10-5Now we have the ionization constant and the initial concentration of the weak acid, the information necessary to determine the equilibrium concentration of H3O^+, and the pH:
{"https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_14_04_steps1_img.jpg"}
With these steps we find [H3O^+] = 2.3 × 10^-3 M and pH = 2.64

problem = 13.16 Equilibrium in a Solution of a Salt of a Weak Acid and a Strong Base

<h3>Example 13.16: Equilibrium in a Solution of a Salt of a Weak Acid and a Strong Base</h3>
Determine the acetic acid concentration in a solution with [CH3CO2-]=0.050M and [OH^-] = 2.5 × 10^-6 M at equilibrium. The reaction is:
CH3CO2-(aq)+H2O(l)⇌CH3CO2H(aq)+OH-(aq)
<h4>Solution</h4>We are given two of three equilibrium concentrations and asked to find the missing concentration. If we can find the equilibrium constant for the reaction, the process is straightforward.
The acetate ion behaves as a base in this reaction; hydroxide ions are a product. We determine Kb as follows:
Kb(forCH3CO2-)=Kw/Ka(forCH3CO2H)=1.0×10-14/1.8×10-5=5.6×10-10
Now find the missing concentration:
Kb=[CH3CO2H][OH-]/[CH3CO2-]=5.6×10-10
=[CH3CO2H](2.5×10-6)/(0.050)=5.6×10-10
Solving this equation we get [CH3CO2H] = 1.1 × 10^-5 M.

problem = 13.17 Determining the Acidic or Basic Nature of Salts

<h3>Example 13.17: Determining the Acidic or Basic Nature of Salts</h3>
Determine whether aqueous solutions of the following salts are acidic, basic, or neutral:
(a) KBr
(b) NaHCO3
(c) NH4Cl
(d) Na2HPO4
(e) NH4F
<h4>Solution</h4>Consider each of the ions separately in terms of its effect on the pH of the solution, as shown here:
(a) The K^+ cation and the Br^- anion are both spectators, since they are the cation of a strong base (KOH) and the anion of a strong acid (HBr), respectively. The solution is neutral.
(b) The Na^+ cation is a spectator, and will not affect the pH of the solution; while the HCO3- anion is amphiprotic, it could either behave as an acid or a base. The Ka of HCO3- is 5.6 × 10^-11, so the Kb of its conjugate base is 1.0×10-14/5.6×10-11=1.8×10-4.
Since Kb >> Ka, the solution is basic.
(c) The NH4+ ion is acidic and the Cl^- ion is a spectator. The solution will be acidic.
(d) The Na^+ ion is a spectator, while the HPO42- ion is amphiprotic, with a Ka of 4.2 × 10^-13
so that the Kb of its conjugate base is 1.0×10-14/4.2×10-13=2.4×10-2. Because Kb >> Ka, the solution is basic.
(e) The NH4+ ion is listed as being acidic, and the F^- ion is listed as a base, so we must directly compare the Ka and the Kb of the two ions. Ka of NH4+ is 5.6 × 10^-10, which seems very small, yet the Kb of F^- is 1.4 × 10^-11, so the solution is acidic, since Ka > Kb.

problem = 13.18 Hydrolysis of [Al(H2O)6]3+

<h3>Example 13.18: Hydrolysis of [Al(H2O)6]3+</h3>
Calculate the pH of a 0.10-M solution of aluminum chloride, which dissolves completely to give the hydrated aluminum ion [Al(H2O)6]3+ in solution.
<h4>Solution</h4>In spite of the unusual appearance of the acid, this is a typical acid ionization problem.
{"https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_14_04_steps2_img.jpg"}
Determine the direction of change. The equation for the reaction and Ka are:
Al(H2O)63+(aq)+H2O(l)⇌H3O+(aq)+Al(H2O)5(OH)2+(aq)Ka=1.4×10-5
The reaction shifts to the right to reach equilibrium.
Determine x and equilibrium concentrations. Use the table:
{"https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_14_04_ICETable13_img.jpg"}
Solve for x and the equilibrium concentrations. Substituting the expressions for the equilibrium concentrations into the equation for the ionization constant yields:
Ka=[H3O+][Al(H2O)5(OH)2+]/[Al(H2O)63+]
=(x)(x)/0.10-x=1.4×10-5
Solving this equation gives:
x=1.2×10-3M
From this we find:
[H3O+]=0+x=1.2×10-3M
pH=-log[H3O+]=2.92(an acidic solution)
Check the work. The arithmetic checks; when 1.2 × 10^-3 M is substituted for x, the result = Ka.

problem = 13.19 Ionization of a Diprotic Acid

<h3>Example 13.19: Ionization of a Diprotic Acid</h3>
When we buy soda water (carbonated water), we are buying a solution of carbon dioxide in water. The solution is acidic because CO2 reacts with water to form carbonic acid, H2CO3. What are [H3O+], [HCO3-], and [CO32-] in a saturated solution of CO2 with an initial [H2CO3] = 0.033 M?
H2CO3(aq)+H2O(l)⇌H3O+(aq)+HCO3-(aq)Ka1=4.3×10-7
HCO3-(aq)+H2O(l)⇌H3O+(aq)+CO32-(aq)Ka2=5.6×10-11<h4>Solution</h4>
As indicated by the ionization constants, H2CO3 is a much stronger acid than HCO3-, so H2CO3 is the dominant producer of hydronium ion in solution. Thus there are two parts in the solution of this problem: (1) Using the customary four steps, we determine the concentration of H3O^+ and HCO3- produced by ionization of H2CO3. (2) Then we determine the concentration of CO32- in a solution with the concentration of H3O^+ and HCO3- determined in (1). To summarize:
{"https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_14_05_steps1_img.jpg"}
Determine the concentrations of H3O+ and HCO3-.
H2CO3(aq)+H2O(l)⇌H3O+(aq)+HCO3-(aq)Ka1=4.3×10-7
As for the ionization of any other weak acid:
{"https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_14_05_steps2_img.jpg"}
An abbreviated table of changes and concentrations shows:
{"https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_14_05_ICETable1_img.jpg"}
Substituting the equilibrium concentrations into the equilibrium gives us:
KH2CO3=[H3O+][HCO3-]/[H2CO3]=(x)(x)/0.033-x=4.3×10-7
Solving the preceding equation making our standard assumptions gives:
x=1.2×10-4
Thus:
[H2CO3]=0.033M
[H3O+]=[HCO3-]=1.2×10-4M
Determine the concentration of CO32- in a solution at equilibrium with [H3O+] and [HCO3-] both equal to 1.2 × 10^-4 M.
HCO3-(aq)+H2O(l)⇌H3O+(aq)+CO32-(aq)
KHCO3-=[H3O+][CO32-]/[HCO3-]=(1.2×10-4)[CO32-]/1.2×10-4
[CO32-]=(5.6×10-11)(1.2×10-4)/1.2×10-4=5.6×10-11M
To summarize: In part 1 of this example, we found that the H2CO3 in a 0.033-M solution ionizes slightly and at equilibrium [H2CO3] = 0.033 M; [H3O+] = 1.2 × 10^-4; and [HCO3-]=1.2×10-4M. In part 2, we determined that [CO32-]=5.6×10-11M.

problem = 13.20 pH Changes in Buffered and Unbuffered Solutions

<h3>Example 13.20: pH Changes in Buffered and Unbuffered Solutions</h3>
(a) Calculate the pH of an acetate buffer that is a mixture with 0.10 M acetic acid and 0.10 M sodium acetate.
<h4>Solution</h4>
To determine the pH of the buffer solution we use a typical equilibrium calculation (as illustrated in earlier Examples):
{"https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_14_06_steps1_img.jpg"}
Determine the direction of change. The equilibrium in a mixture of H3O^+, CH3CO2-, and CH3CO2H is:
CH3CO2H(aq)+H2O(l)⇌H3O+(aq)+CH3CO2-(aq)
The equilibrium constant for CH3CO2H is not given, so we look it up in <a href="https://opentextbc.ca/chemistry/back-matter/ionization-constants-of-weak-acids/">Appendix H</a>: Ka = 1.8 × 10^-5. With [CH3CO2H] = [CH3CO2-] = 0.10 M and [H3O^+] = ~0 M, the reaction shifts to the right to form H3O^+.
Determine x and equilibrium concentrations. A table of changes and concentrations follows:
{"https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_14_06_ICETable16_img.jpg"}
Solve for x and the equilibrium concentrations. We find:
x=1.8×10-5M
and
[H3O+]=0+x=1.8×10-5M
Thus:
pH=-log[H3O+]=-log(1.8×10-5)
=4.74
Check the work. If we calculate all calculated equilibrium concentrations, we find that the equilibrium value of the reaction coefficient, Q = Ka.
(b) Calculate the pH after 1.0 mL of 0.10 M NaOH is added to 100 mL of this buffer, giving a solution with a volume of 101 mL.
First, we calculate the concentrations of an intermediate mixture resulting from the complete reaction between the acid in the buffer and the added base. Then we determine the concentrations of the mixture at the new equilibrium:
{"https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_14_06_steps2_img.jpg"}
Determine the moles of NaOH. One milliliter (0.0010 L) of 0.10 M NaOH contains:
0.0010L×(0.10mol NaOH/1L)=1.0×10-4mol NaOH
Determine the moles of CH2CO2H. Before reaction, 0.100 L of the buffer solution contains:
0.100L×(0.100molCH3CO2H/1L)=1.00×10-2molCH3CO2H
Solve for the amount of NaCH3CO2 produced. The 1.0 × 10^-4 mol of NaOH neutralizes 1.0 × 10^-4 mol of CH3CO2H, leaving:
(1.0×10-2)-(0.01×10-2)=0.99×10-2molCH3CO2H
and producing 1.0 × 10^-4 mol of NaCH3CO2. This makes a total of:
(1.0×10-2)+(0.01×10-2)=1.01×10-2molNaCH3CO2
Find the molarity of the products. After reaction, CH3CO2H and NaCH3CO2 are contained in 101 mL of the intermediate solution, so:
[CH3CO2H]=9.9×10-3mol/0.101L=0.098M
[NaCH3CO2]=1.01×10-2mol/0.101L=0.100M
Now we calculate the pH after the intermediate solution, which is 0.098 M in CH3CO2H and 0.100 M in NaCH3CO2, comes to equilibrium. The calculation is very similar to that in part (a) of this example:
{"https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_14_06_steps3_img.jpg"}
This series of calculations gives a pH = 4.75. Thus the addition of the base barely changes the pH of the solution (<a href="https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_14_06_compare.jpg">Figure 17</a>).
(c) For comparison, calculate the pH after 1.0 mL of 0.10 M NaOH is added to 100 mL of a solution of an unbuffered solution with a pH of 4.74 (a 1.8 × 10^-5-M solution of HCl). The volume of the final solution is 101 mL.
<h4>Solution</h4>
This 1.8 × 10^-5-M solution of HCl has the same hydronium ion concentration as the 0.10-M solution of acetic acid-sodium acetate buffer described in part (a) of this example. The solution contains:
0.100L×(1.8×10-5mol HCl/1L)=1.8×10-6mol HCl
As shown in part (b), 1 mL of 0.10 M NaOH contains 1.0 × 10^-4 mol of NaOH. When the NaOH and HCl solutions are mixed, the HCl is the limiting reagent in the reaction. All of the HCl reacts, and the amount of NaOH that remains is:
(1.0×10-4)-(1.8×10-6)=9.8×10-5M
The concentration of NaOH is:
9.8×10-5MNaOH/0.101L=9.7×10-4M
The pOH of this solution is:
pOH=-log[OH-]=-log(9.7×10-4)=3.01
The pH is:
pH=14.00-pOH=10.99
The pH changes from 4.74 to 10.99 in this unbuffered solution. This compares to the change of 4.74 to 4.75 that occurred when the same amount of NaOH was added to the buffered solution described in part (b).

problem = 13.21 Calculating pH for Titration Solutions: Strong Acid/Strong Base

<h3>Example 13.21: Calculating pH for Titration Solutions: Strong Acid+Strong Base</h3>
A titration is carried out for 25.00 mL of 0.100 M HCl (strong acid) with 0.100 M of a strong base NaOH the titration curve is shown in <a href="https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_14_07_titration.jpg">Figure 21</a>. Calculate the pH at these volumes of added base solution:
(a) 0.00 mL
(b) 12.50 mL
(c) 25.00 mL
(d) 37.50 mL
<h4>Solution</h4>
Since HCl is a strong acid, we can assume that all of it dissociates. The initial concentration of H3O^+ is [H3O+]0=0.100M. When the base solution is added, it also dissociates completely, providing OH^- ions. The H3O^+ and OH^- ions neutralize each other, so only those of the two that were in excess remain, and their concentration determines the pH. Thus, the solution is initially acidic (pH < 7), but eventually all the hydronium ions present from the original acid are neutralized, and the solution becomes neutral. As more base is added, the solution turns basic.
The total initial amount of the hydronium ions is:
n(H+)0=[H3O+]0×0.02500 L=0.002500 mol
Once X mL of the 0.100-M base solution is added, the number of moles of the OH^- ions introduced is:
n(OH-)0=0.100M×X mL×(1 L/1000 mL)
The total volume becomes: V=(25.00 mL+X mL)(1 L/1000 mL)
The number of moles of H3O^+ becomes:
n(H+)=n(H+)0-n(OH-)0=0.002500 mol-0.100M×X mL×(1 L/1000 mL)
The concentration of H3O^+ is:
[H3O+]=n(H+)/V=0.002500 mol-0.100M×X mL×(1 L/1000 mL)/(25.00 mL+X mL)(1 L/1000 mL)=0.002500 mol×(1000 mL/1 L)-0.100M×X mL/25.00 mL+X mL
pH=-log([H3O+])
The preceding calculations work if n(H+)0-n(OH-)0>0 and so n(H^+) > 0. When n(H+)0=n(OH-)0, the H3O^+ ions from the acid and the OH^- ions from the base mutually neutralize. At this point, the only hydronium ions left are those from the autoionization of water, and there are no OH^- particles to neutralize them. Therefore, in this case:
[H3O+]=[OH-],[H3O+]=Kw=1.0×10-14;[H3O+]=1.0×10-7
pH=-log(1.0×10-7)=7.00
Finally, when n(OH-)0>n(H+)0, there are not enough H3O^+ ions to neutralize all the OH^- ions, and instead of n(H+)=n(H+)0-n(OH-)0, we calculate: n(OH-)=n(OH-)0-n(H+)0
In this case:
[OH-]=n(OH-)/V=0.100M×X mL×(1 L/1000 mL)-0.002500 mol/(25.00 mL+X mL)(1 L/1000 mL)=0.100M×X mL-0.002500 mol×(1000 mL/1 L)/25.00 mL+X mL
pH=14-pOH=14+log([OH-])
Let us now consider the four specific cases presented in this problem:
(a) X = 0 mL
[H3O+]=n(H+)/V=0.002500 mol×(1000 mL/1 L)/25.00 mL=0.1M
pH = -log(0.100) = 1.000
(b) X = 12.50 mL
[H3O+]=n(H+)/V=0.002500 mol×(1000 mL/1 L)-0.100M×12.50 mL/25.00 mL+12.50 mL=0.0333M
pH = -log(0.0333) = 1.477
(c) X = 25.00 mL
Since the volumes and concentrations of the acid and base solutions are the same: n(H+)0=n(OH-)0, and pH = 7.000, as described earlier.
(d) X = 37.50 mL
In this case:
n(OH-)0>n(H+)0
[OH-]=n(OH-)/V=0.100M×35.70 mL-0.002500 mol×(1000 mL/1 L)/25.00 mL+37.50 mL=0.0200M
pH = 14 - pOH = 14 + log([OH^-]) = 14 + log(0.0200) = 12.30

problem = 13.22 Titration of a Weak Acid with a Strong Base

<h3>Example 13.22: Titration of a Weak Acid with a Strong Base</h3>
The titration curve shown in <a href="https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_14_07_titration2.jpg">Figure 23</a> is for the titration of 25.00 mL of 0.100 M CH3CO2H with 0.100 M NaOH. The reaction can be represented as:
!CH3CO2H +OH- -> CH3CO2- +H2O
(a) What is the initial pH before any amount of the NaOH solution has been added? Ka = 1.8 × 10^-5 for CH3CO2H.
(b) Find the pH after 25.00 mL of the NaOH solution have been added.
(c) Find the pH after 12.50 mL of the NaOH solution has been added.
(d) Find the pH after 37.50 mL of the NaOH solution has been added.
<h4>Solution</h4>
(a) Assuming that the dissociated amount is small compared to 0.100 M, we find that:
Ka=[H3O +][CH3CO2-]/[CH3CO2H]≈[H3O +]2/[CH3CO2H]0, and [H3O +]=Ka×[CH3CO2H]=1.8×10-5×0.100=1.3×10-3
pH=-log(1.3×10-3)=2.87
(b) After 25.00 mL of NaOH are added, the number of moles of NaOH and CH3CO2H are equal because the amounts of the solutions and their concentrations are the same. All of the CH3CO2H has been converted to CH3CO2-. The concentration of the CH3CO2- ion is:
0.00250 mol/0.0500 L=0.0500 MCH3CO2-
The equilibrium that must be focused on now is the basicity equilibrium for CH3CO2-:
CH3CO2-(aq) +H2O(l)⇌CH3CO2H(aq) +OH-(aq)
so we must determine Kb for the base by using the ion product constant for water:
Kb=[CH3CO2H][OH-]/[CH3CO2-]
Ka=[CH3CO2-][H +]/[CH3CO2H],so[CH3CO2H]/[CH3CO2-]=[H +]/Ka.
Since Kw = [H^ +][OH^-]:
Kb=[H +][OH-]/Ka=Kw/Ka=1.0×10-14/1.8×10-5=5.6×10-10
Let us denote the concentration of each of the products of this reaction, CH3CO2H and OH^-, as x. Using the assumption that x is small compared to 0.0500 M, Kb=x2/0.0500M, and then:
x=[OH-]=5.3×10-6
pOH=-log(5.3×10-6)=5.28
pH=14.00-5.28=8.72
Note that the pH at the equivalence point of this titration is significantly greater than 7.
(c) In (a), 25.00 mL of the NaOH solution was added, and so practically all the CH3CO2H was converted into CH3CO2-. In this case, only 12.50 mL of the base solution has been introduced, and so only half of all the CH3CO2H is converted into CH3CO2-. The total initial number of moles of CH3CO2H is 0.02500L × 0.100 M = 0.00250 mol, and so after adding the NaOH, the numbers of moles of CH3CO2H and CH3CO2- are both approximately equal to 0.00250 mol/2=0.00125 mol, and their concentrations are the same.
Since the amount of the added base is smaller than the original amount of the acid, the equivalence point has not been reached, the solution remains a buffer, and we can use the Henderson-Hasselbalch equation:
pH=pKa +log[Base]/[Acid]=-log(Ka) +log[CH3CO2-]/[CH3CO2H]=-log(1.8×10-5) +log(1)
(as the concentrations of CH3CO2- and CH3CO2H are the same)
Thus:
pH=-log(1.8×10-5)=4.74
(the pH = the pKa at the halfway point in a titration of a weak acid)
(d) After 37.50 mL of NaOH is added, the amount of NaOH is 0.03750 L × 0.100 M = 0.003750 mol NaOH. Since this is past the equivalence point, the excess hydroxide ions will make the solution basic, and we can again use stoichiometric calculations to determine the pH:
[OH-]=(0.003750 mol-0.00250 mol)/0.06250 L=2.00×10-2M
So:
pOH=-log(2.00×10-2)=1.70, and pH=14.00-1.70=12.30
Note that this result is the same as for the strong acid-strong base titration example provided, since the amount of the strong base added moves the solution past the equivalence point.


problem = 5.1b Measuring Heat
<h3>Example 5.1b: Measuring Heat</h3>
How much heat, in joules, must be added to a 5.00 × 10^2-g iron skillet to increase its temperature from 25 °C to 250 °C? The specific heat of iron is 0.451 J/g °C.
<h4>Answer:</h4>
5.05 × 10^4 J
problem = 5.2b Determining Other Quantities
<h3>Example 5.2b: Determining Other Quantities</h3>
A piece of unknown metal weighs 217 g. When the metal piece absorbs 1.43 kJ of heat, its temperature increases from 24.5 °C to 39.1 °C. Determine the specific heat of this metal, and predict its identity.
<h4>Answer:</h4>
c = 0.45 J/g °C; the metal is likely to be iron
problem = 5.3b Heat Transfer between Substances at Different Temperatures
<h3>Example 5.3b: Heat Transfer between Substances at Different Temperatures</h3>
A 248-g piece of copper is dropped into 390 mL of water at 22.6 °C. The final temperature of the water was measured as 39.9 °C. Calculate the initial temperature of the piece of copper. Assume that all heat transfer occurs between the copper and the water.
<h4>Answer:</h4>
The initial temperature of the copper was 335.6 °C.
<h4>Check Your Learning</h4>
A 248-g piece of copper initially at 314 °C is dropped into 390 mL of water initially at 22.6 °C. Assuming that all heat transfer occurs between the copper and the water, calculate the final temperature.
<h4>Answer:</h4>
The final temperature (reached by both copper and water) is 38.8 °C.
problem = 5.4b Identifying a Metal by Measuring Specific Heat
<h3>Example 5.4b: Identifying a Metal by Measuring Specific Heat</h3>
A 92.9-g piece of a silver/gray metal is heated to 178.0 °C, and then quickly transferred into 75.0 mL of water initially at 24.0 °C. After 5 minutes, both the metal and the water have reached the same temperature: 29.7 °C. Determine the specific heat and the identity of the metal. (Note: You should find that the specific heat is close to that of two different metals. Explain how you can confidently determine the identity of the metal).
<h4>Answer:</h4>
cmetal= 0.13 J/g °C
This specific heat is close to that of either gold or lead. It would be difficult to determine which metal this was based solely on the numerical values. However, the observation that the metal is silver/gray in addition to the value for the specific heat indicates that the metal is lead.
problem = 5.5b Heat Produced by an Exothermic Reaction
<h3>Example 5.5b: Heat Produced by an Exothermic Reaction</h3>
When 100 mL of 0.200 M NaCl(aq) and 100 mL of 0.200 M AgNO3(aq), both at 21.9 °C, are mixed in a coffee cup calorimeter, the temperature increases to 23.5 °C as solid AgCl forms. How much heat is produced by this precipitation reaction? What assumptions did you make to determine your value?
<h4>Answer:</h4>
1.34 × 10^3 J; assume no heat is absorbed by the calorimeter, no heat is exchanged between the calorimeter and its surroundings, and that the specific heat and mass of the solution are the same as those for water
problem = 5.6b Heat Flow in an Instant Ice Pack
<h3>Example 5.6b: Heat Flow in an Instant Ice Pack</h3>
When a 3.00-g sample of KCl was added to 3.00 × 10^2 g of water in a coffee cup calorimeter, the temperature decreased by 1.05 °C. How much heat is involved in the dissolution of the KCl? What assumptions did you make?
<h4>Answer:</h4>
1.33 kJ; assume that the calorimeter prevents heat transfer between the solution and its external environment (including the calorimeter itself) and that the specific heat of the solution is the same as that for water
problem = 5.7b Bomb Calorimetry
<h3>Example 5.7b: Bomb Calorimetry</h3>
When 0.963 g of benzene, C6H6, is burned in a bomb calorimeter, the temperature of the calorimeter increases by 8.39 °C. The bomb has a heat capacity of 784 J/°C and is submerged in 925 mL of water. How much heat was produced by the combustion of the glucose sample?
<h4>Answer:</h4>
39.0 kJ
problem = 5.8b Measurement of an Enthalpy Change
<h3>Example 5.8b: Measurement of an Enthalpy Change</h3>
When 1.34 g Zn(s) reacts with 60.0 mL of 0.750 M HCl(aq), 3.14 kJ of heat are produced. Determine the enthalpy change per mole of zinc reacting for the reaction:
!Zn(s) +2HCl(aq) -> ZnCl2(aq) +H2(g)
<h4>Answer:</h4>
ΔH = -153 kJ
problem = 5.9b Another Example of the Measurement of an Enthalpy Change
<h3>Example 5.9b: Another Example of the Measurement of an Enthalpy Change</h3>
When 1.42 g of iron reacts with 1.80 g of chlorine, 3.22 g of FeCl2(s) and 8.60 kJ of heat is produced. What is the enthalpy change for the reaction when 1 mole of FeCl2(s) is produced?
<h4>Answer:</h4>
ΔH = -338 kJ
problem = 5.10b Using Enthalpy of Combustion
<h3>Example 5.10b: Using Enthalpy of Combustion</h3>
How much heat is produced by the combustion of 125 g of acetylene?
<h4>Answer:</h4>
6.25 × 10^3 kJ
problem = 5.11b Evaluating an Enthalpy of Formation
<h3>Example 5.11b: Evaluating an Enthalpy of Formation</h3>
Hydrogen gas, H2, reacts explosively with gaseous chlorine, Cl2, to form hydrogen chloride, HCl(g). What is the enthalpy change for the reaction of 1 mole of H2(g) with 1 mole of Cl2(g) if both the reactants and products are at standard state conditions? The standard enthalpy of formation of HCl(g) is -92.3 kJ/mol.
<h4>Answer:</h4>
!For the reaction H2(g) +Cl2(g) -> 2HCl(g)ΔH298°=-184.6kJ
problem = 5.12b Writing Reaction Equations for ΔHf°
<h3>Example 5.12b: Writing Reaction Equations for ΔHf°</h3>
Write the heat of formation reaction equations for:
(a) C2H5OC2H5(l)
(b) Na2CO3(s)
<h4>Answer:</h4>
!(a) 4C(s,graphite) +5H2(g) +1/2O2(g) -> C2H5OC2H5(l); (b) 2Na(s) +C(s,graphite) +3/2O2(g)⟶Na2CO3(s)
problem = 5.13b Stepwise Calculation of ΔHf° Using Hess’s Law
<h3>Example 5.13b: Stepwise Calculation of ΔHf° Using Hess’s Law</h3>
Calculate ΔH for the process:
!N2(g) +2O2(g) -> 2NO2(g)from the following information:
!N2(g) +O2(g) -> 2NO(g)ΔH=180.5kJ!NO(g) +1/2O2(g) -> NO2(g)ΔH=-57.06kJ
<h4>Answer:</h4>
66.4 kJ
problem = 5.14b A More Challenging Problem Using Hess’s Law
<h3>Example 5.14b: A More Challenging Problem Using Hess’s Law</h3>
Aluminum chloride can be formed from its elements:
!(i) 2Al(s) +3Cl2(g) -> 2AlCl3(s)ΔH°=?
Use the reactions here to determine the ΔH° for reaction (i):
!(ii) HCl(g) -> HCl(aq)ΔH(ii)°=-74.8kJ
!(iii) H2(g) +Cl2(g) -> 2HCl(g)ΔH(iii)°=-185kJ
!(iv) AlCl3(aq) -> AlCl3(s)ΔH(iv)°= +323kJ/mol
!(v) 2Al(s) +6HCl(aq) -> 2AlCl3(aq) +3H2(g)ΔH(v)°=-1049kJ
<h4>Answer:</h4>
-1407 kJ
problem = 5.15b Using Hess’s Law
<h3>Example 5.15b: Using Hess’s Law</h3>
Calculate the heat of combustion of 1 mole of ethanol, C2H5OH(l), when H2O(l) and CO2(g) are formed. Use the following enthalpies of formation: C2H5OH(l), -278 kJ/mol; H2O(l), -286 kJ/mol; and CO2(g), -394 kJ/mol.
<h4>Answer:</h4>
-1368 kJ/mol

'''

examples = example.split('problem = ')
from collections import OrderedDict


exdict = OrderedDict()
exhtml = []
index = ['The index below shows examples from OpenStax Chemistry, which is available for free at http://cnx.org/content/col11760/1.9. To explore how these examples are solved using PQcalc, click on the links. To browse other examples and see the content, skip to the bottom of this page.']

chapter = 0
for ex in examples:
    if "\n" not in ex:
        continue
    head2, prob = ex.split("\n", 1)
    if not head2:
        continue
    url = head2.split()[0]
    if not chapter and head2.endswith('Density'):
        chapter = 1
        index.append('<h4>Chapter 1</h4>')
    if chapter:
        try:
            ch = int(head2.split('.')[0])
            if ch != chapter:
                index.append('<h4>Chapter %d</h4>' % ch)
                chapter = ch
        except:
            pass
    if head2.startswith('Ex'):
        exhtml.append('<a href="/example%s">Exercise %s</a><br>' % (url, head2[2:]))
        if chapter:
            index.append('<a href="/workedexample%s">Exercise %s</a> <a href="/example%s">(text)</a><br>' % (url, head2[2:]), url)
    else:
        exhtml.append('<a href="/example%s">Example %s</a><br>' % (url, head2))
        if chapter:
            index.append('<a href="/workedexample%s">Example %s</a> <a href="/example%s">(text)</a><br>' % (url, head2, url))
    exhtml.append('<br>\n'.join(prob.replace('<', '&lt;').replace('>', '&gt;').splitlines()))
    exdict[url] = prob

inhtml = "".join(index)
exhtml = "".join(exhtml)
exhtml = inhtml + '<hr>' + exhtml
trackinglog = defaultdict(list)

with open('./mysite/logfile.txt', 'r', encoding='utf-8') as exfromfile:
    exfrom = ''.join([line for line in exfromfile])
    for i, exman in enumerate(exfrom.split('<h3>')):
        key = exman.splitlines()[0]
        if ' ' in key:
            if key.startswith('Chapter'):
                _, section, _, number = key.split()
                shortk = 'Ex' + section[:-1] + '.' + number[:-5]
            else:
                shortk = key.split()[1][:-1]
        else:
            shortk = key[:]
        exman = exman.replace('\n\n', '\n')
        if shortk == '3.10b':
            pass #rint('exman', exman)
        if '<h4>Answer:</h4>' in exman:
            question, answer = exman.split('<h4>Answer:</h4>', maxsplit=1)
        else:
            question, answer = exman, ''
        while len(question) > 2 and question.endswith('\n\n'):
            question = question[:-1]
        while len(answer) > 2 and answer.endswith('\n\n'):
            answer = answer[:-1]

        example_data[shortk] = Record(shortk, '<h3>'+question, answer)
        if not shortk.startswith('Ex') and '.' in shortk:
            ch, prob = shortk.split('.')
            try:
                if len(prob) == 1 or prob[1] == 'b':
                    prob = '0' + prob
                trackinglog[int(ch)].append(prob)
            except:
                print(shortk)

for ch in range(1,25):
    if ch in trackinglog:
        print('Chapter', ch, ':', ' '.join((a[1:] if a[0] == '0' else a) for a in sorted(trackinglog[ch])))


'''for key in exdict:
    get_example(key)
'''
#print(exhtml)

def check_one(ex):
    print(ex[2])
    print('*******************************************************')
    print(ex[3])
    answer = input('ok?')

'''def check_examples():
    exadict = defaultdict(list)
    connection = sqlite3.connect(database='examples')
    cursor = connection.cursor()
    cursor.execute("SELECT * from homework")
    for example in cursor:
        if example[1].startswith('q4') and example[1].endswith('b'):
            print('****', example[1], '****')
            lines = example[3].splitlines()
            while lines and '=' not in lines[0]:
                lines.pop(0)
            for l in lines:
                if l.startswith('Think about'):
                    break
                if l:
                    print(l)
        exadict[example[1]].append(example[0])
    #connection.close()
    #return
    k = exadict.keys()
    k2 = []
    for a in k:
        try:
            if '.' not in a or not a[0].isdigit():
                continue
            before, after = a.split(".", maxsplit=1)
            b = ''
            if after.endswith('b'):
                after = after[:-1]
                b = 'b'
            if len(exadict[a])>1:
                b = b + ' duplicated'
            k2.append(f'{int(before):02d}.{int(after):02d}{b}')
        except ValueError:
            print(f'trouble with {a}')
    for ex in sorted(k2):
        print(ex)
    for exa in exadict:
        if not exa.startswith('3'):
            continue

        if len(exadict[exa]) > 1:
            print(f'duplicate example {exa}: {exadict[exa]}')
        cursor.execute("SELECT * from homework WHERE Id = ?;", (exadict[exa][0],))
        check_one(cursor.fetchone())
    connection.close()


#check_examples()
'''