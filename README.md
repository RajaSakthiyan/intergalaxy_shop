## Problem Definition: Merchant's Guide to the Galaxy - README

Problem One: Merchant&#39;s Guide to the Galaxy
 
You decided to give up on earth after the latest financial collapse left 99.99% of the
earth's population with 0.01% of the wealth. Luckily, with the scant sum of money that is
left in your account, you are able to afford to rent a spaceship, leave earth, and fly all
over the galaxy to sell common metals and dirt (which apparently is worth a lot).
 
Buying and selling over the galaxy requires you to convert numbers and units, and you
decided to write a program to help you.
 
The numbers used for intergalactic transactions follows similar convention to the roman
numerals and you have painstakingly collected the appropriate translation between
them.
 
Roman numerals are based on seven symbols:
 
Symbol Value
| Roman | Integer|
|---|----|
| V | 5  |
| X | 10 |
| L | 50 |
|C |100|
|D|500|
|M|1000|


Numbers are formed by combining symbols together and adding the values. For
example, MMVI is 1000 + 1000 + 5 + 1 = 2006. Generally, symbols are placed in order
of value, starting with the largest values. When smaller values precede larger values,
the smaller values are subtracted from the larger values, and the result is added to the
total. For example MCMXLIV = 1000 + (1000 − 100) + (50 − 10) + (5 − 1) = 1944.
 
- The symbols "I", "X", "C", and "M" can be repeated three times in succession, but
no more. (They may appear four times if the third and fourth are separated by a
smaller value, such as XXXIX.) "D", "L", and "V" can never be repeated.
-  "I" can be subtracted from "V" and "X" only. "X" can be subtracted from "L" and
"C" only. "C" can be subtracted from "D" and "M" only. "V", "L", and "D" can never
be subtracted.
-  Only one small-value symbol may be subtracted from any large-value symbol.
-  A number written in [16]Arabic numerals can be broken into digits. For example,
1903 is composed of 1, 9, 0, and 3. To write the Roman numeral, each of the
non-zero digits should be treated separately. Inthe above example, 1,000 = M,
900 = CM, and 3 = III. Therefore, 1903 = MCMIII.

(Source: Wikipedia (http://en.wikipedia.org/wiki/Roman_numerals)
 
Input to your program consists of lines of text detailing your notes on the conversion
between intergalactic units and roman numerals.
 
You are expected to handle invalid queries appropriately.
 
#### Test input
---

glob is I<br>
prok is V<br>
pish is X<br>
tegj is L<br>
glob glob Silver is 34 Credits<br>
glob prok Gold is 57800 Credits<br>
pish pish Iron is 3910 Credits<br>
how much is pish tegj glob glob ?<br>
how many Credits is glob prok Silver ?<br>
how many Credits is glob prok Gold ?<br>
how many Credits is glob prok Iron ?<br>
how much wood could a woodchuck chuck if a woodchuck could chuck wood ?<br>
 
#### Test Output
---

pish tegj glob glob is 42<br>
glob prok Silver is 68 Credits<br>
glob prok Gold is 57800 Credits<br>
glob prok Iron is 782 Credits<br>
I have no idea what you are talking about<br>


## Solutions

    Each module contains its own unit-test impleted using `unitest` module.

### main.py

This is the verification file where we can check with requirement against program. This is starting file to begin the code review.

### numerials.py

This is the module file contains number system of and its corresponding mapping with other similar number system. I said similar because each number system classes are inherited by `Numeral`. I added descriptor pattern for `Symbol` for making it non-data (read-only).

When instantiate the number system class such as `InterGalacticNumeral`, its corresponding mappings are called at instance creation time. This avoids explicit mapping and make it easy to change one mapping class to another or introduce another new inter-galaxy number system.

This auto-initiate pattern identified during the refactoring of code and one interesting recursion I found as below,

```
    # from Symbol class
    def __call__(self):
        return self.weight_value() if isinstance(self.weight_value, Symbol) else self.weight_value
```
This helps to identify its last mapping of the given symbol for a number-system.

### units.py

this is helper module contains class `Units` for treating abstraction of calculating credits for the query. (FYI, query is never coupled it here). It is composite on translation class.

### conversions.py

This module contains two class and one `RomanNumerialRules` is made to composite over `InterGalacticConversion`.
The class `RomanNumerialRules` perform both validating Roman letters by regex. (regex pattern is taken from internet due to time limitation) and iterate through letters and yield right numerical weightage. `InterGalacticConversion` contains conversion and credit evaluating methods.

### transaction.py

This is module where it handle mostly filtering out words for the query with keyword and keeps the word when it is attribute of `Units` and `Numerals`. `Translation` class responsible for getting input both conversion and credit evaluation. `Transsaction` is the class where we pass question and get the right answer based on `Tranlation` initiation. I added one factory function `main.py` for your reference and code review.

---
Thank you - Rajasakthiyan.G
  
