# Bill of Materials Tool
---------------------------

This tool converts Eagle CAD BOM (Bill of Material files) to:
- an intermediate tabbed version with Bill of Materials withouth header info (Tabbed / space separated CSV);
- a comma separated file (CSV) with the Bill of Materials (partslist) without header information;
- a comma separated file (CSV) with the Bill of Materials (partslist) without header information but then grouped per part and including totals.

Uses: 

    Python3 (3.7.6+)
    
Tested with Eagle Version:

    9.6.2

Enjoy!

---------------------------

## Usage:

    python3 BOMTool.py filename.bom


E.g.:

    python3 BOMTool.py example.bom
    
Produces:

    example.tab
    example.csv
    example.sum.csv

