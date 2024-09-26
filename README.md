# veralayoutcheck
A rule for the vera++ code checker, to see if a given code file matches the layout of a given template file

## use of this check
Copy the `veralayoutcheck.py` file to the rules folder of the vera++ installation (`\lib\vera++\rules`)

Create a code template file as specified in the next section

Run the vera++ code checker from the command line and specify the code template file as an additional source file, e.g.
```
vera++
    --show-rule
    --quiet
    --rule veralayoutcheck
    --xml-report ./testreports/vera++.xml
    c_source_codingguidelines.vcst
    foo.c
    bar.c
```

## layout of the code template file
The code template file is specified with the file-ending `.vcst` among the other source files to be checked. If multiple template files are specified, only the first one is used. All the other template files will be ignored. 

Besides the different file-ending, the code template file can be considered an almost normal source file, as it can hold any valid C or C++ syntax.
Additionally, there are special tokens that can be used in the template file:

* `$ANYTHING` matches everything, i.e. after this token appears, the rest of the file is not checked to conform any style.
* `$COMMENT` expects one comment with any content.
* `$DEFINE` expects one define directive
* `$DOXYCOMMENT` expects one doxygen documentation comment. The parameter list contains specific doxygen-tags that must appear within the doxygen comment. If such a doxygen-tag is missing, a style error will be recorded.
* `$ENUM` expects one enum definition.
* `$FUNCTIONDECL` expects one function declaration containing all the keywords given as parameters.
* `$FUNCTIONDEF` expects one function definition containing all the keywords given as parameters.
* `$GLOBVARDECL` expects one global variable declaration containing all the keywords given as parameters.
* `$GLOBVARDEF` expects one global variable definition containing all the keywords given as parameters.
* `$INCLUDE` expects one include directives. A parameter can be used to provide the type of the include directive that is expected: ANY (refers to any type of include), LIB (refers to an include with angular brackets) or LOC (refers to an include with quotation marks) .
* `$OPTIONAL` expects one token as parameter, which might or might not appear in the file to be checked.
* `$SEQUENCE` expects a sequence of special tokens as well as a number as the last parameter. The style checker then checks the file if the sequence appears as defined (e.g. `$SEQUENCE($DOXYCOMMENT(details, returns),$FUNCTIONDEF(static, inline), 5)` to check for five function definitions with the keywords static and inline that is preceeded with a doxygen comment which contains the \details and \returns tags).
* `$STRUCT` expects one struct definition.
* `$TYPEDEF` expects one type definition. Note that a typedef including a struct or enum definition is covered completely by this token.

Each style token except the `$ANYTHING` can be followed by a parameter list enclosed in parenthesis. If no parameter list is provided, the default parameters are used. A detailed documentation about which parameters can be speciefied is given in the [token documentation](TOKEN_DOCS.md)

## viewing the results
The test results can be exported to a xml file using the command line option `--xml-report` (other file formats are also available). The xml reports can be compiled into a html file using the vera-style.xslt file of this repository.

## what this rule (not) is
This rule was created for the purpose of checking a syntactically correct source code against a template. With this it shall be possible to test all source files of a project if they follow a certain structure.

It is not the purpose of this rule to check the code for syntax errors, correct indentation, or smaller more detailed rules e.g. naming conventions or the order of keywords like `static inline` or `inline static`.

This rule shall not alter existing source code.

## useful links
* https://manpages.org/vera
* https://github.com/verateam/vera

## useful notes
* other than stated in the official vera++ docs, the starting column of a token cannot be retrieved by accessing the attribute `columnNumber`. Instead the attribute `column` works in Python
* to use multiple rules in one vera command, the `--rule` option can be used multiple times in one command

## TODO list
* [x] implement the `$ANYTHING` token
* [ ] implement the `$COMMENT` token
* [ ] implement the `$DEFINE` token
* [x] implement the `$DOXYCOMMENT` token
* [ ] implement the `$ENUM` token
* [ ] implement the `$FUNCTIONDECL` token
* [ ] implement the `$FUNCTIONDEF` token
* [ ] implement the `$GLOBVARDECL` token
* [ ] implement the `$GLOBVARDEF` token
* [x] implement the `$INCLUDES` token
* [ ] implement the `$OPTIONAL` token
* [x] implement the `$SEQUENCE` token
* [x] implement the `$STRUCT` token
* [ ] implement the `$TYPEDEF` token
