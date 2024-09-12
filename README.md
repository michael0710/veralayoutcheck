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

 * `$DOXYCOMMENT` expects a doxygen documentation comment
 * `$DOXYCOMMENT(...)` expects a doxygen documentation comment that must contain the specified doxygen-tags in the parentheses
 * `$INCLUDES` works the same like `$INCLUDES(*)`
 * `$INCLUDES(...)` expects a certain number of include directives as specified in the argument. An asterix can be used to specify an undefined amount of include directives
 * TODO ...
 * `$ANYTHING` matches everything, i.e. after this token appears, the rest of the file is not checked to conform any style

## viewing the results
The test results can be exported to a xml file using the command line option `--xml-report` (other file formats are also available). The xml reports can be compiled into a html file using the vera-style.xslt file of this repository.

## useful links
* https://manpages.org/vera
* https://github.com/verateam/vera

## useful notes
* other than stated in the official vera++ docs, the starting column of a token cannot be retrieved by accessing the attribute `columnNumber`. Instead the attribute `column` works in Python