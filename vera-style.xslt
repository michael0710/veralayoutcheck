<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" encoding="UTF-8"/>

    <xsl:template match="/">
        <html>
            <head>
                <title>Vera++ Results</title>
                <style>
                    body { font-family: Arial, sans-serif; }
                    table { border-collapse: collapse; width: 100%; }
                    th, td { border: 1px solid #ddd; padding: 8px; }
                    th { background-color: #e0e0e0; }
                    tr:nth-child(even) { background-color: #f0f0f0; }
                </style>
            </head>
            <body>
                <h1>Vera++ Results</h1>
                <xsl:for-each select="vera/file">
                    <h4> File: <xsl:value-of select="@name"/> </h4>
                    <table>
                        <tr>
                            <th>Line</th>
                            <th>Rule</th>
                            <th>Message</th>
                        </tr>
                        <xsl:for-each select="report">
                            <tr>
                                <td> <xsl:value-of select="@line"/> </td>
                                <td> <xsl:value-of select="@rule"/> </td>
                                <td> <xsl:value-of disable-output-escaping="yes" select="substring(.,9, string-length(.)-1-9)"/> </td>
                            </tr>
                        </xsl:for-each>
                    </table>
                </xsl:for-each>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>