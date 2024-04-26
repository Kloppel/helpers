# Most important Problems/Design decisions are found in the md file "problems_and_solutions"

all questions below refer to some of these problems

# Questions
## [[202402280904]] Group lines by sections should be tested with snippets of all sections

I'd incorporate those test once dummy data exists for each section. Please provide feedback on that approach in general.

## [[202402290916]] Basic datatype and format validation seems adequate due to variability in source data

Please read carefully and comment on my observations/questions/solution.

Finally, provide me with more information on datatypes, prm line structure/format, etc. such that I can enhance testing.

## [[202402291240]] Parser and tests work for atom section, how to proceed now?

The first day I looked at the project and my tasks, I was very tempted to immediately use an object-oriented approach for the parser design.
I decided against doing so as it was not part of my task. I opted for the compromise of writing a new parser but renounce an OO design.

Now, my approach should be clear, and testing the other sections is a mostly repetitive task.
I had a quick look at .str files, too, and can say, in the current states, the old version as well as mine are incapable of dealing with .str files.
However, after some adjustments, both should be capable.

At this point, it is relevant to think about switching to an object-oriented design. Using an adequate design pattern that works well in combination with dependency injection and mocking, we could easily expand parsing + testing capability for multiple sections and even file types.

Especially if the community lacks parsers for more than just .str and .prm files, the object oriented approach seems most fit with respect to mid- to long-term scalability.

Before I expand tests and use more files for parser validation, I suggest we have a chat.