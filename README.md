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

 * `$DOXYCOMMENT` expects one doxygen documentation comment. The parameter list contains specific doxygen-tags that must appear within the doxygen comment. If such a doxygen-tag is missing, a style error will be recorded.
 * `$COMMENT` expects one 
 * `$ANYINCLUDES` expects an undefined number of include directives. A parameter can be used to provide the amount of include directives that are expected. An asterix can be used to explicitly specify an undefined amount of include directives.
 * `$LIBINCLUDES` expects an undefined number of include directives with the include file specified as `<...>`. A parameter can be used to provide the amount of include directives that are expected. An asterix can be used to explicitly specify an undefined amount of include directives.
 * `$LOCINCLUDES` expects an undefined number of include directives with the include file specified as `"..."`. A parameter can be used to provide the amount of include directives that are expected. An asterix can be used to explicitly specify an undefined amount of include directives.
 * `$TYPEDEF` expects one type definition
 * `$GLOBVARDEC` expects one global variable declaration containing all the keywords given as parameters.
 * `$GLOBVARDEF` expects one global variable definition containing all the keywords given as parameters.
 * `$FUNCTIONDEC` expects one function declaration containing all the keywords given as parameters.
 * `$FUNCTIONDEF` expects one function definition containing all the keywords given as parameters.
 * `$SEQUENCE` expects a sequence of special tokens as well as a number as the last parameter. The style checker then checks the file if the sequence appears as defined (e.g. `$SEQUENCE($DOXYCOMMENT(details, returns),$FUNCTION(static, inline), 5)` to check for five function definitions with the keywords static and inline that is preceeded with a doxygen comment which contains the \details and \returns tags).
 * `$ANYTHING` matches everything, i.e. after this token appears, the rest of the file is not checked to conform any style

Each style token except the `$ANYTHING` can be followed by a parameter list enclosed in parenthesis. If no parameter list is provided, the default parameters are used.

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
* [ ] implement the `$DOXYCOMMENT` token
* [ ] implement the `$COMMENT` token
* [ ] implement the `$ANYINCLUDES` token
* [ ] \(low priority) implement the `$LIBINCLUDES` token
* [ ] \(low priority) implement the `$LOCINCLUDES` token
* [ ] implement the `$TYPEDEF` token
* [ ] implement the `$GLOBVARDEC` token
* [ ] implement the `$GLOBVARDEF` token
* [ ] implement the `$FUNCTIONDEC` token
* [ ] implement the `$FUNCTIONDEF` token
* [ ] \(HIGH PRIORITY) implement the `$SEQUENCE` token
* [ ] implement the `$ANYTHING` token
* [ ] once the `$SEQUENCE` token is implemented, get rid of the parameter for the `$...INCLUDES` token, cause then the preferred way to expect multiple includes would be `$SECUENCE($ANYINCLUDE, *)`