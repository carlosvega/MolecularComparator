# MolecularComparator
Molecular Formulæ Comparator

# Molecular Formulae Comparator

This program checks if two columns of chemical equations are the same.
Asumes numbers can have multiple digits. Asumes elements have ONLY one letter
And if there is a letter without number, it assumes there is a "1" besides

It ignores the following characters: ' ) ( n
It replaces the letter A to R for the radical

Examples:

C6H8N2O2R2'             would yield true compared to:   A2C6H8N2O2'

C4H7N2O3R(C2H2NOR)n'    would yield true compared to:   A2C6H9N3O4'

C5H8N2O2'               would yield FALSE compared to:  A2C6H9N3O3'
