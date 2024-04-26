# 202402270909 Documentation: Problems and Solutions
#helpers #problem #solution


**Problems**

# [[202402270935]] current parser lacks clarity and contains duplicate code

# Problem
- docstrings missing
- function and argument names imprecise
- low level of encapsulation and abstraction


> interpretability somewhat difficult
> testing difficult
> maintaining code and tests difficult

In my opinion, writing tests for the current state of the parser is a waste of time.


# Solution

Write a new parser and aim for the following:
- clear and precise wording for functions and arguments
- encapsulation: separation of functionalities with respect to logical steps involved in parsing and transforming the data
- generalization and abstraction where possible
- combine operations (functions) through a main function
- use verbose variable names to clearly describe purpose



[[202402271111]] Testing a parser requires high quality dummy data

# Problem
Without a well-tested 100 % functional parser, testing a new parser is cumbersome.

In general, test data (aka. dummy data) is supposed to be written in the test's source code. This is in stark contrast to testing procedures by many programmers.

For source code-defined dummy data, the ubiquitous challenge is to write the minimum required amount of lines while still simulating the intrinsic structure of data.


## Parser-specific problems

For parsers, not only the data structure must be modelled for dummy data. Formatting principles of the file to be parsed must be included carefully.

## General testing concerns
Testing is supposed to be as granular as possible, meaning that one testcase tests only one feature or function of the script/software, if possible.

For this, test design must respect e.g. nested functions and simulate intermediate objects to avoid function interdependency that compromises the granularity aspect of tests.


# Solution

Tests will be done section-wise. By this, generated dummy data is less verbose, increasing readability, which additionally acts as a caveat to include correct formatting.
> granularity, precise data modelling, error-proof


# Gemini: Additional thoughts on this Zettel content

Additional thoughts on important aspects of parser tests:

    Equivalence partitioning: Divide the input space into equivalence classes where all inputs within a class are expected to behave similarly by the parser. This helps create focused test cases for different scenarios.
    Boundary value analysis: Test inputs at the edges of expected ranges (e.g., empty lines, minimum/maximum values) to uncover potential edge cases.
    Negative testing: Include test cases with invalid or unexpected inputs to ensure the parser handles them gracefully (e.g., raising exceptions, returning appropriate error messages).
    Mutation testing: Modify parts of the input data slightly to observe if the parser behaves as expected with these variations.
    Test coverage: Aim for a reasonable test coverage metric (e.g., statement coverage, branch coverage) to ensure a comprehensive set of tests.
    Mocking and stubbing: Utilize mocking and stubbing techniques to isolate specific units of the parser for testing, bypassing dependencies on external components.
    Parameterized testing: Create test cases that can be run with different input data sets, improving code reusability and efficiency.

Addressing your specific concerns:

    Bootstrapping issue: Consider using a well-tested, minimal reference parser or a domain-specific language (DSL) to create reliable test data for the new parser.
    Dummy data limitations: Focus on capturing the core elements and structure of the data, avoiding unnecessary complexity in test data. You can also create multiple test cases with different data sets to cover a broader range of scenarios.
    Granularity: Utilize mocking and stubbing techniques to isolate units for testing, and potentially break down complex test cases into smaller, more manageable ones.

Remember: Testing is an iterative process. Start with a solid foundation of tests, and gradually refine and expand them as you iterate on the parser development and identify potential issues.





[[202402271325]] Semi-automated dummy data generation combines speed, precision and readability

## define a function to generate dummy data
### example function for atoms sections

- read par_bv.prm to list of lines
- write out simple commands to slice desired data
    - e.g. find list idx where atom section starts + where next section starts, then use lines between
- check if any line of section should not count as data row
- manually assign number of data rows
- use the information extracted here to test "group_lines_by_sections" macroscopically

_further steps:_
- maybe copy and paste raw strings and elaborate how u generated them
- use these to manually assign readable snippets for downstream (microscopic) tests 


# Inspect:
can these functions be reused to enable semi-specific testing of multiple prm files?





[[202402280904]] Group lines by sections should be tested with snippets of all sections

# Test group lines by sections
This function uses data with multiple sections as input.
Granular, section-wise testing could be done by using a proper section data snippet for the section under test and some dummy lines for a new section separated by the section headline.
However, in that case not all operations of that function may be under test.

# Solution
Get dummy data snippets for each section, concatenate them to a dummy list_of_lines and use this as input.
Then, the resulting object can be validated section-wise and all operations are covered in the test.




[[202402280954]] Most consistent way to read comment value properly is by using space splitting and join

# Problem
To extract values from a pmf file line, I'd prefer to use str.split or re.split to maximize readability and cleanness of code.
Sadly, human errors such as multiple subsequent spaces in the comment part of a line prevent me from doing so.
Those errors would require some more lines of code for validation of values.

# Solution
Therefore, I stick to the solution of using any whitespace as field separators and then join the comment value.
This solution additionally ensures stripping of the _newline character after comment value_.


      values = line.split()

    # join comment fragments    
    comment = " ".join(values[comment_column_index:])
    
    # slice of values containing actual data
    data_values = values[:comment_column_index]

    # append comment value to data_values
    data_values.append(comment)
    
    # data_values = re.split(r" {2,9}|\t", line)
    
    if "proline CA" in data_values[-1]:
        print(data_values)
    
    
    

[[202402290916]] Basic datatype and format validation seems adequate due to variability in source data

# Problem
I observed inconsistencies in the format of lines within a subsection (fields), and also within values (decimal places).
Limited information on required number of decimal places for downstream usage of data prevents me from designing more precise and thus robust tests for datatype/dataformat validation.

## Dihedrals Inconsistencies

kchi:
- mostly 4 decimal places
- sometimes only 2

delta:
- always 2 decimal places

## Angles section

    CG321    SG311    CG321    34.00     95.00 ! PROTNA sahc
    
    CG311    CG2O2    OG2D1    70.00    125.00   20.00   2.44200 ! PROT adm jr. 5/02/91, acetic acid pure solvent; LIPID methyl acetate

in above example, the latter line seems to contain additional angular information; the old parser, as well as my version, interpret the two floating point values as part of the comment.
> Supposed to be like that?

## atom section information loss: !MASS rows

    ! Patch for ring-a-cys
    !MASS  -1  C         12.01100 ! carbonyl C, peptide backbone
    !MASS  -1  CT1       12.01100 ! aliphatic sp3 C for CH
    !MASS  -1  O         15.99900 ! carbonyl oxygen
    !MASS  -1  H          1.00800 ! polar H
    !MASS  -1  NH1       14.00700 ! peptide nitrogen
    
> are not transferred to dataframe/new file. loss of information is ok?
    

**Assumption**
due to the observed variability in decimal places in the prm files, I assume checking for specific number of decimal places is not required.

# Solution

just validate datatype in first parser version

