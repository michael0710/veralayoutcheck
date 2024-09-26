# L I C E N S E # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#  Copyright 2019 Michael Schaechinger
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# implements rules for local coding guidelines to be checked with vera++
import sys
import os
import re

# All functions return at least a status code. The status code has the
# following meaning:
#   - 0  if the function was executed successfully (postive or negative result)
#        and further checks can be performed
#   - -1 if it failed and the remaining checks cannot be performed

class CheckContext:
    """A small class to hold the context for the style checks"""
    # note that all members are public so that no other methods are needed
    def __init__(self, fileName, templateFile, templateTokens, templateTokenCounter, fileTokens, fileTokenCounter):
        """Initializes the context"""
        self.fileName             = fileName
        self.templateFile         = templateFile
        self.templateTokens       = templateTokens
        self.templateTokenCounter = templateTokenCounter
        self.fileTokens           = fileTokens
        self.fileTokenCounter     = fileTokenCounter

# definition of all check functions
def check_anything(context):
    """Called when $ANYTHING is found in the template file"""
    return -1

def check_defines(context):
    """Called when $DEFINES is found in the template file"""
    print("ERROR defines are not supported yet")
    return -1

def check_doxycomment(context):
    """Called when $DOXYCOMMENT is found in the template file"""
    # ignore preceeding newlines
    # the context counters shall not be changend if the check fails
    oldTemplateTokenCounter = context.templateTokenCounter
    oldFileTokenCounter = context.fileTokenCounter

    while context.fileTokens[context.fileTokenCounter].type == "newline":
        context.fileTokenCounter += 1
    # next token must be a comment
    if context.fileTokens[context.fileTokenCounter].type != "ccomment":
        # go back to the last token that was valid
        context.fileTokenCounter = oldFileTokenCounter
        return -1

    # get the tag list
    rvGetArgList, argList, argIndexList = get_arg_list(context)

    if context.fileTokens[context.fileTokenCounter].value.startswith("/**<") == True:
        return check_doxycomment_Javadoc_after(context, argList)
    
    if context.fileTokens[context.fileTokenCounter].value.startswith("/**") == True:
        return check_doxycomment_Javadoc(context, argList)
    
    # go back to the last token that was valid
    context.fileTokenCounter = oldFileTokenCounter
    context.templateTokenCounter = oldTemplateTokenCounter
    return -1

def check_include(context):
    """Called when $INCLUDE is found in the template file"""
    oldFileTokenCounter = context.fileTokenCounter
    # ignore preceeding newlines
    while context.fileTokens[context.fileTokenCounter].type == "newline":
        context.fileTokenCounter += 1

    # get the parameter list
    rvGetArgList, argList, argIndexList = get_arg_list(context)

    # next token must be a include directive 
    if context.fileTokens[context.fileTokenCounter].type in ["pp_qheader", "pp_hheader"]:
        context.fileTokenCounter += 1
        if argList == [] or argList[0].value == "ANY":
            return 0
        elif (   (context.fileTokens[oldFileTokenCounter].type == "pp_qheader" and argList[0].value == "LIB")
              or (context.fileTokens[oldFileTokenCounter].type == "pp_hheader" and argList[0].value == "LOC")):
            reportString = ""
            if argList[0].value == "LOC":
                reportString = "quotation marks"
            else:
                reportString = "angle brackets"
            vera.report(context.fileName, context.fileTokens[context.fileTokenCounter].line, "Expected include statement with " + reportString)
            return 0
        else:
            return 0
    else:
        context.fileTokenCounter = oldFileTokenCounter
        return -1

def check_sequence(context):
    rvGetArgList, argList, argIndexList = get_arg_list(context)
    endOfSequenceTemplateTokenCounter = context.templateTokenCounter
    sequenceCounter = 0
    # Check if the tokens in the sequence are in the file by calling
    # process_valid_style_check_tokens(context) recursively
    while True:
        rvProcessTokens = -1
        for i in range(len(argList)):
            if argList[i].type == "identifier" and (argList[i].value in VALID_STYLE_CHECK_TOKENS):
                # set the token counter to the first token of the sequence
                context.templateTokenCounter = argIndexList[i]
                # call the function that corresponds to the found token
                rvProcessTokens = process_valid_style_check_tokens(context)
                if rvProcessTokens != 0:
                    break
        if rvProcessTokens != 0:
            break
        else:
            sequenceCounter += 1
    context.templateTokenCounter = endOfSequenceTemplateTokenCounter
    
    # back-iterate the trailing newlines so that they can be handeled by the
    # next token or the content of the template file
    # TODO going back and forth in the token list is not a good idea. Find a
    #      fancier way to do this.
    while context.fileTokens[context.fileTokenCounter].type == "newline":
        context.fileTokenCounter -= 1
    context.fileTokenCounter += 1
    
    # Check if the sequenceCounter matches the number in the last argument of the list
    if argList[-1].value == "*":
        return 0
    else:
        try:
            expectedReps = int(argList[-1].value)
        except ValueError as e:
            print("ERROR malformed code template file in line " + context.templateTokens[context.templateTokenCounter].line)
            return -1
        if sequenceCounter != expectedReps:
            vera.report(context.fileName, context.fileTokens[context.fileTokenCounter].line, "Expected exactly " + str(expectedReps) + " repetitions of the sequence but got " + str(sequenceCounter))
        return 0

# NOTE: the check_... functions must appear here before the STYLE_CHECK_FCNS list is defined
VALID_STYLE_CHECK_TOKENS =  [
                                "$ANYTHING",
                                "$DOXYCOMMENT",
                                "$INCLUDE",
                                "$SEQUENCE"
                            ]

STYLE_CHECK_FCNS =  [
                        check_anything,
                        check_doxycomment,
                        check_include,
                        check_sequence
                    ]

def get_arg_list(context):
    """Returns a list of arguments for the current token in the template file"""
    argList = []
    argIndexList = []
    parenLevel = 0
    if context.templateTokens[context.templateTokenCounter].value == "(":
        while True:
            if context.templateTokens[context.templateTokenCounter].value == "(":
                parenLevel += 1
            elif context.templateTokens[context.templateTokenCounter].value == ")":
                parenLevel -= 1
                if parenLevel <= 0:
                    break
            elif parenLevel > 1:
                argList.append(context.templateTokens[context.templateTokenCounter])
                argIndexList.append(context.templateTokenCounter)
            elif parenLevel == 1 and context.templateTokens[context.templateTokenCounter].value not in [",", "(", ")", " "]:
                argList.append(context.templateTokens[context.templateTokenCounter])
                argIndexList.append(context.templateTokenCounter)

            context.templateTokenCounter += 1
    else:
        # prevent the templateTokenCounter from being increased by one if no parenthesis is found
        context.templateTokenCounter -= 1
    
    # increase the counter one more time so that the right parenthesis of the
    # template file is behind the current position
    context.templateTokenCounter += 1
    # a special layout-token without parenthesis is also valid, in that case return an empty list
    return 0, argList, argIndexList

def check_doxycomment_Javadoc(context, argList):
    # TODO the comment below sounds like it shall be outsourced to a seperate vera++ rule
    # each Javadoc style doxygen comment shall introduce a new line with "*" vertically below the first "*"
    firstAsteriskColumn = context.fileTokens[context.fileTokenCounter].column + 1
    for line in context.fileTokens[context.fileTokenCounter].value.splitlines():
        if re.match(r"[ ]{firstAsteriskColumn}*[^\n]*", line) == False and not line.startswith("/**"):
            vera.report(context.fileName, context.fileTokens[context.fileTokenCounter].line, "Malformed Javadoc style doxygen comment")
            context.fileTokenCounter += 1
            return -2
    # check if all mandatory tags are present
    for tag in argList:
        if context.fileTokens[context.fileTokenCounter].value.find(" \\" + tag.value) == -1:
            vera.report(context.fileName, context.fileTokens[context.fileTokenCounter].line, "Missing mandatory doxygen tag. Expected to contain \\" + tag.value)
    context.fileTokenCounter += 1
    return 0

def check_doxycomment_Javadoc_after(context, argList):
    print("ERROR doxygen comments beginning with /**< are not supported yet")
    return -1
    
def process_valid_style_check_tokens(context):
    position = 0
    try:
        # Find the index of the string in the list
        position = VALID_STYLE_CHECK_TOKENS.index(context.templateTokens[context.templateTokenCounter].value)
    except ValueError:
        print("ERROR The string \'" + context.templateTokens[context.templateTokenCounter].value + "\' is not found in the list.")
        return -1

    # call the function that corresponds to the found token
    context.templateTokenCounter += 1
    rv = STYLE_CHECK_FCNS[position](context)
    return rv

# returns 0 if the file structure is according to the template file
# returns the line number of the first deviation from the template file
#         if the file structure does not match the template file
def check_file_vs_template(paramContext):
    context = CheckContext(paramContext.fileName,
                           paramContext.templateFile,
                           vera.getTokens(paramContext.templateFile, 1, 0, -1, -1, []),
                           0,
                           vera.getTokens(paramContext.fileName, 1, 0, -1, -1, []),
                           0)
    
    print("Checking file " + context.fileName)

    while context.templateTokenCounter < len(context.templateTokens):
        # check the template token list for tokens that represent the file structure
        if context.templateTokens[context.templateTokenCounter].type == "identifier" and (context.templateTokens[context.templateTokenCounter].value in VALID_STYLE_CHECK_TOKENS):
            rvProcessTokens = process_valid_style_check_tokens(context)
            if rvProcessTokens == -1:
                return context.fileTokens[context.fileTokenCounter].line

        # if the type is "eof", the file must end here
        elif context.templateTokens[context.templateTokenCounter].type == "eof":
            if context.fileTokens[context.fileTokenCounter].type != "eof":
                vera.report(context.fileName, context.fileTokens[context.fileTokenCounter].line, "Expected end of file but was " + context.fileTokens[context.fileTokenCounter].type)
                return context.fileTokens[context.fileTokenCounter].line
            return 0

        # if the type is not a special token and is not eof, the template file must exactly match the file
        else:
            if context.fileTokens[context.fileTokenCounter].type != context.templateTokens[context.templateTokenCounter].type:
                # TODO printing the token type of vera++ can be very cryptic. Probably add a mapping from the vera++ token type to a more readable token type.
                vera.report(context.fileName, context.fileTokens[context.fileTokenCounter].line, "Expected token " + context.templateTokens[context.templateTokenCounter].type + " but was " + context.fileTokens[context.fileTokenCounter].type)
                vera.report(context.fileName, context.fileTokens[context.fileTokenCounter].line, "Token-No in template: " + str(context.templateTokenCounter) + " in file: " + str(context.fileTokenCounter))
                return context.fileTokens[context.fileTokenCounter].line
            if context.fileTokens[context.fileTokenCounter].value != context.templateTokens[context.templateTokenCounter].value:
                vera.report(context.fileName, context.fileTokens[context.fileTokenCounter].line, "Expected exact file content \"" + context.templateTokens[context.templateTokenCounter].value + "\"")
                vera.report(context.fileName, context.fileTokens[context.fileTokenCounter].line, "File content was \"" + context.fileTokens[context.fileTokenCounter].value + "\"")
                return context.fileTokens[context.fileTokenCounter].line
            context.fileTokenCounter += 1
            context.templateTokenCounter += 1
    return 0

if __name__ == "__main__":
    # search for the coding guidelines file (is a .vcst file)
    # if there are multiple guidelines files, the first one specified is used
    sourceFiles = vera.getSourceFileNames()
    guidelinesFile = None
    # search for the first file with the .vcst extension
    for fileName in sourceFiles:
        if fileName.endswith(".vcst"):
            guidelinesFile = fileName
            break
        
    if guidelinesFile == None:
        print("WARNING No coding guidelines file found! No style checks will be performed.")
        sys.exit(0)
    print("Guidelines specified in " + guidelinesFile + " will be used for style checks.")

    for fileName in sourceFiles:
        if fileName.endswith(".vcst"):
            continue
        context = CheckContext(fileName, guidelinesFile, None, 0, None, 0)
        check_file_vs_template(context)
