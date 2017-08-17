# coding=utf-8
from collections import defaultdict, namedtuple
from collections import OrderedDict


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

problem = 1.1b Calculation of Density
<h3>Example 1.1b: Calculation of Density</h3>
(a) To three decimal places, what is the volume of a cube (cm^3) with an edge length of 0.843 cm?
(b) If the cube in part (a) is copper and has a mass of 5.34 g, what is the density of copper to two decimal places?
<h4>Answer:</h4>
(a) 0.599 cm^3; (b) 8.91 g/cm^3
problem = 1.2b Using Displacement of Water to Determine Density
<h3>Example 1.2b: Using Displacement of Water to Determine Density</h3>
Remove all of the blocks from the water and add the green block to the tank of water, placing it approximately in the middle of the tank. Determine the density of the green block.
<h4>Answer:</h4>
2.00 kg/L
problem = 1.3b Rounding Numbers
<h3>Example 1.3b: Rounding Numbers</h3>
Round the following to the indicated number of significant figures:
(a) 0.424 (to two significant figures)
(b) 0.0038661 (to three significant figures)
(c) 421.25 (to four significant figures)
(d) 28,683.5 (to five significant figures)
<h4>Answer:</h4>
(a) 0.42; (b) 0.00387; (c) 421.2; (d) 28,684
problem = 1.4b Addition and Subtraction with Significant Figures
<h3>Example 1.4b: Addition and Subtraction with Significant Figures</h3>
(a) Add 2.334 mL and 0.31 mL.
(b) Subtract 55.8752 m from 56.533 m.
<h4>Answer:</h4>
(a) 2.64 mL; (b) 0.658 m
problem = 1.5b Multiplication and Division with Significant Figures
<h3>Example 1.5b: Multiplication and Division with Significant Figures</h3>
(a) Multiply 2.334 cm and 0.320 cm.
(b) Divide 55.8752 m by 56.53 s.
<h4>Answer:</h4>
(a) 0.747 cm^2 (b) 0.9884 m/s
problem = 1.6b Calculation with Significant Figures
<h3>Example 1.6b: Calculation with Significant Figures</h3>
What is the density of a liquid with a mass of 31.1415 g and a volume of 30.13 cm^3?
<h4>Answer:</h4>
1.034 g/mL
problem = 1.7b Experimental Determination of Density Using Water Displacement
<h3>Example 1.7b: Experimental Determination of Density Using Water Displacement</h3>
An irregularly shaped piece of a shiny yellowish material is weighed and then submerged in a graduated cylinder, with results as shown.
{"https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_01_04_CylGold.jpg"}
(a) Use these values to determine the density of this material.
(b) Do you have any reasonable guesses as to the identity of this material? Explain your reasoning.
<h4>Answer:</h4>
(a) 19 g/cm^3; (b) It is likely gold; the right appearance for gold and very close to the density given for gold in <a href="https://opentextbc.ca/chemistry/chapter/measurements/#fs-idm45639696">Table 4</a>.
problem = 1.8b Using a Unit Conversion Factor
<h3>Example 1.8b: Using a Unit Conversion Factor</h3>
Convert a volume of 9.345 qt to liters.
<h4>Answer:</h4>
8.844 L
problem = 1.9b Computing Quantities from Measurement Results and Known Mathematical Relations
<h3>Example 1.9b: Computing Quantities from Measurement Results and Known Mathematical Relations</h3>
What is the volume in liters of 1.000 oz, given that 1 L = 1.0567 qt and 1 qt = 32 oz (exactly)?
<h4>Answer:</h4>
2.956×10-2L
problem = 1.10b Computing Quantities from Measurement Results and Known Mathematical Relations
<h3>Example 1.10b: Computing Quantities from Measurement Results and Known Mathematical Relations</h3>
A Toyota Prius Hybrid uses 59.7 L gasoline to drive from San Francisco to Seattle, a distance of 1300 km (two significant digits).
(a) What (average) fuel economy, in miles per gallon, did the Prius get during this trip?
(b) If gasoline costs $3.90 per gallon, what was the fuel cost for this trip?
<h4>Answer:</h4>
(a) 51 mpg; (b) $62
problem = 1.11b Conversion from Celsius
<h3>Example 1.11b: Conversion from Celsius</h3>
Convert 80.92 °C to K and °F.
<h4>Answer:</h4>
354.07 K, 177.7 °F
problem = 1.12b Conversion from Fahrenheit
<h3>Example 1.12b: Conversion from Fahrenheit</h3>
Convert 50 °F to °C and K.
<h4>Answer:</h4>
10 °C, 280 K

problem = 1.1 Calculation of Density

<h3>Example 1.1: Calculation of Density</h3>
Gold—in bricks, bars, and coins—has been a form of currency for centuries. In order to swindle people into paying for a brick of gold without actually investing in a brick of gold, people have considered filling the centers of hollow gold bricks with lead to fool buyers into thinking that the entire brick is gold. It does not work: Lead is a dense substance, but its density is not as great as that of gold, 19.3 g/cm^3. What is the density of lead if a cube of lead has an edge length of 2.00 cm and a mass of 90.7 g?
<h4>Solution</h4>
The density of a substance can be calculated by dividing its mass by its volume. The volume of a cube is calculated by cubing the edge length.
volume of lead cube=2.00 cm×2.00 cm×2.00 cm=8.00 cm3
density=mass/volume=90.7 g/8.00 cm3=11.3 g/1.00 cm3=11.3 g/cm3
(We will discuss the reason for rounding to the first decimal place in the next section.)

problem = 1.2 Using Displacement of Water to Determine Density

<h3>Example 1.2: Using Displacement of Water to Determine Density</h3>
This <a href="https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/http://openstaxcollege.org/l/16phetmasvolden">PhET simulation</a> illustrates another way to determine density, using displacement of water. Determine the density of the red and yellow blocks.
<h4>Solution</h4>
When you open the density simulation and select Same Mass, you can choose from several 5.00-kg colored blocks that you can drop into a tank containing 100.00 L water. The yellow block floats (it is less dense than water), and the water level rises to 105.00 L. While floating, the yellow block displaces 5.00 L water, an amount equal to the weight of the block. The red block sinks (it is more dense than water, which has density = 1.00 kg/L), and the water level rises to 101.25 L.
The red block therefore displaces 1.25 L water, an amount equal to the volume of the block. The density of the red block is:
density=mass/volume=5.00 kg/1.25 L=4.00 kg/L
Note that since the yellow block is not completely submerged, you cannot determine its density from this information. But if you hold the yellow block on the bottom of the tank, the water level rises to 110.00 L, which means that it now displaces 10.00 L water, and its density can be found:
density=mass/volume=5.00 kg/10.00 L=0.500 kg/L

problem = 1.3 Rounding Numbers

<h3>Example 1.3: Rounding Numbers</h3>
Round the following to the indicated number of significant figures:
(a) 31.57 (to two significant figures)
(b) 8.1649 (to three significant figures)
(c) 0.051065 (to four significant figures)
(d) 0.90275 (to four significant figures)
<h4>Solution</h4>
(a) 31.57 rounds “up” to 32 (the dropped digit is 5, and the retained digit is even)
(b) 8.1649 rounds “down” to 8.16 (the dropped digit, 4, is less than 5)
(c) 0.051065 rounds “down” to 0.05106 (the dropped digit is 5, and the retained digit is even)
(d) 0.90275 rounds “up” to 0.9028 (the dropped digit is 5, and the retained digit is even)

problem = 1.4 Addition and Subtraction with Significant Figures

<h3>Example 1.4: Addition and Subtraction with Significant Figures</h3>
Rule: When we add or subtract numbers, we should round the result to the same number of decimal places as the number with the least number of decimal places (i.e., the least precise value in terms of addition and subtraction).
(a) Add 1.0023 g and 4.383 g.
(b) Subtract 421.23 g from 486 g.
<h4>Solution</h4>
(a) 1.0023 g+ 4.383 g/5.3853 g
Answer is 5.385 g (round to the thousandths place; three decimal places)
(b)    486 g-421.23 g/64.77 g
Answer is 65 g (round to the ones place; no decimal places)
{"https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_01_05_SigDigits4_img.jpg"}

problem = 1.5 Multiplication and Division with Significant Figures

<h3>Example 1.5: Multiplication and Division with Significant Figures</h3>
Rule: When we multiply or divide numbers, we should round the result to the same number of digits as the number with the least number of significant figures (the least precise value in terms of multiplication and division).
(a) Multiply 0.6238 cm by 6.6 cm.
(b) Divide 421.23 g by 486 mL.
<h4>Solution</h4>
!(a) 0.6238 cm×6.6cm=4.11708cm2 -> result is4.1cm2(round to two significant figures)four significant figures×two significant figures⟶two significant figures answer
!(b) 421.23 g/486 mL=0.86728... g/mL -> result is 0.867 g/mL(round to three significant figures)five significant figures/three significant figures⟶three significant figures answer

problem = 1.6 Calculation with Significant Figures

<h3>Example 1.6: Calculation with Significant Figures</h3>
One common bathtub is 13.44 dm long, 5.920 dm wide, and 2.54 dm deep. Assume that the tub is rectangular and calculate its approximate volume in liters.
<h4>Solution</h4>
V=l×w×d=13.44 dm×5.920 dm×2.54 dm=202.09459...dm3(value from calculator)=202 dm3, or 202 L(answer rounded to three significant figures)

problem = 1.7 Experimental Determination of Density Using Water Displacement

<h3>Example 1.7: Experimental Determination of Density Using Water Displacement</h3>
A piece of rebar is weighed and then submerged in a graduated cylinder partially filled with water, with results as shown.
{"https://opentextbc.ca/chemistry/wp-content/uploads/sites/150/2016/05/CNX_Chem_01_04_CylRebar.jpg"}
(a) Use these values to determine the density of this piece of rebar.
(b) Rebar is mostly iron. Does your result in (a) support this statement? How?
<h4>Solution</h4>The volume of the piece of rebar is equal to the volume of the water displaced:
volume=22.4 mL-13.5 mL=8.9 mL=8.9 cm3(rounded to the nearest 0.1 mL, per the rule for addition and subtraction)
The density is the mass-to-volume ratio:
density=mass/volume=69.658 g/8.9 cm3=7.8 g/cm3
(rounded to two significant figures, per the rule for multiplication and division)
From <a href="https://opentextbc.ca/chemistry/chapter/measurements/#fs-idm45639696">Table 4</a>, the density of iron is 7.9 g/cm^3, very close to that of rebar, which lends some support to the fact that rebar is mostly iron.

problem = 1.8 Using a Unit Conversion Factor

<h3>Example 1.8: Using a Unit Conversion Factor</h3>
The mass of a competition frisbee is 125 g. Convert its mass to ounces using the unit conversion factor derived from the relationship 1 oz = 28.349 g (<a href="https://opentextbc.ca/chemistry/chapter/mathematical-treatment-of-measurement-results/#fs-idm222237232">Table 6</a>).
<h4>Solution</h4>
If we have the conversion factor, we can determine the mass in kilograms using an equation similar the one used for converting length from inches to centimeters.
xoz=125 g×unit conversion factor
We write the unit conversion factor in its two forms:
1 oz/28.349 gand28.349 g/1 ozThe correct unit conversion factor is the ratio that cancels the units of grams and leaves ounces.
xoz=125g×1 oz/28.349g=(125/28.349)oz=4.41 oz (three significant figures)

problem = 1.9 Computing Quantities from Measurement Results and Known Mathematical Relations

<h3>Example 1.9: Computing Quantities from Measurement Results and Known Mathematical Relations</h3>
What is the density of common antifreeze in units of g/mL? A 4.00-qt sample of the antifreeze weighs 9.26 lb.
<h4>Solution</h4>
Since density=mass/volume, we need to divide the mass in grams by the volume in milliliters. In general: the number of units of B = the number of units of A × unit conversion factor. The necessary conversion factors are given in <a href="https://opentextbc.ca/chemistry/chapter/mathematical-treatment-of-measurement-results/#fs-idm222237232">Table 6</a>: 1 lb = 453.59 g; 1 L = 1.0567 qt; 1 L = 1,000 mL. We can convert mass from pounds to grams in one step:
9.26lb×453.59 g/1lb=4.20×103g
We need to use two steps to convert volume from quarts to milliliters.
Convert quarts to liters.
4.00qt×1 L/1.0567qt=3.78 L
Convert liters to milliliters.
3.78L×1000 mL/1L=3.78×103mL
Then,
density=4.20×103g/3.78×103mL=1.11 g/mLAlternatively, the calculation could be set up in a way that uses three unit conversion factors sequentially as follows:
9.26lb/4.00qt×453.59 g/1lb×1.0567qt/1L×1L/1000 mL=1.11 g/mL

problem = 1.10 Computing Quantities from Measurement Results and Known Mathematical Relations

<h3>Example 1.10: Computing Quantities from Measurement Results and Known Mathematical Relations</h3>
While being driven from Philadelphia to Atlanta, a distance of about 1250 km, a 2014 Lamborghini Aventador Roadster uses 213 L gasoline.
(a) What (average) fuel economy, in miles per gallon, did the Roadster get during this trip?
(b) If gasoline costs $3.80 per gallon, what was the fuel cost for this trip?
<h4>Solution</h4>
(a) We first convert distance from kilometers to miles:
1250 km×0.62137 mi/1 km=777 mi
and then convert volume from liters to gallons:
213L×1.0567qt/1L×1 gal/4qt=56.3 gal
Then,
(average) mileage=777 mi/56.3 gal=13.8 miles/gallon=13.8 mpg
Alternatively, the calculation could be set up in a way that uses all the conversion factors sequentially, as follows:
1250km/213L×0.62137 mi/1km×1L/1.0567qt×4qt/1 gal=13.8 mpg
(b) Using the previously calculated volume in gallons, we find:
56.3 gal×$3.80/1 gal=$214

problem = 1.11 Conversion from Celsius

<h3>Example 1.11: Conversion from Celsius</h3>
Normal body temperature has been commonly accepted as 37.0 °C (although it varies depending on time of day and method of measurement, as well as among individuals). What is this temperature on the kelvin scale and on the Fahrenheit scale?
<h4>Solution</h4>
K=°C+273.15=37.0+273.2=310.2 K
°F=9/5°C+32.0=(9/5×37.0)+32.0=66.6+32.0=98.6 °F

problem = 1.12 Conversion from Fahrenheit

<h3>Example 1.12: Conversion from Fahrenheit</h3>
Baking a ready-made pizza calls for an oven temperature of 450 °F. If you are in Europe, and your oven thermometer uses the Celsius scale, what is the setting? What is the kelvin temperature?
<h4>Solution</h4>
!°C=5/9(°F-32)=5/9(450-32)=5/9×418=232 °C -> set oven to 230 °C(two significant figures)!K=°C +273.15=230 +273=503 K -> 5.0×102K(two significant figures)

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



'''

examples = example.split('problem = ')

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
with open('./mysite/logfile.txt', 'r', encoding='utf-8') as hw_file:
    for hw_text in hw_file.read().split('<h3>'):
        if not hw_text:
            continue
        hw_title = hw_text.splitlines()[0]
        if ' ' in hw_title:
            if hw_title.startswith('Chapter'):
                _, section, _, number = hw_title.split()
                hw_id = 'Ex' + section[:-1] + '.' + number[:-5]
            else:
                hw_id = hw_title.split()[1][:-1]
        else:
            hw_id = hw_title[:]
        hw_text = hw_text.replace('\n\n', '\n')
        if hw_id == '3.10b':
            pass  # rint('exman', exman)
        if '<h4>Answer:</h4>' in hw_text:
            question, answer = hw_text.split('<h4>Answer:</h4>', maxsplit=1)
        else:
            question, answer = hw_text, ''
            if hw_id.endswith('b'):
                print(hw_id, 'has no answer')
        if hw_id.endswith('b') and 'Think about it:' not in answer:
            pass #rint(hw_id, 'has no followup')
        while len(question) > 2 and question.endswith('\n\n'):
            question = question[:-1]
        while len(answer) > 2 and answer.endswith('\n\n'):
            answer = answer[:-1]

        example_data[hw_id] = Record(hw_id, '<h3>' + question, answer)
        if not hw_id.startswith('Ex') and '.' in hw_id:
            ch, prob = hw_id.split('.')
            try:
                if len(prob) == 1 or prob[1] == 'b':
                    prob = '0' + prob
                trackinglog[int(ch)].append(prob)
            except:
                pass  # rint(shortk)

if __name__ == '__main__':

    for ch in range(1, 25):
        if ch in trackinglog:
            print('Chapter', ch, ':', ' '.join((a[1:] if a[0] == '0' else a) for a in sorted(trackinglog[ch])))
