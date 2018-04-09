"""
This module represents the ability of the user to define "user defined" files.
If  a user creates files for special purposes e.g. files containing model
definition commands then these file will always be archived if the file has the
same name as the model and the extension starts with the letter u(U).

e.g.
<Filename>.UM will be archived.
<Filename>.UM_txt will be archived.
<Filename>.UM.txt will NOT be archived.

The aim is that this module provides equivalent functionality to the user as
being able to manually manipulate text files and file extensions. The module
should function across multiple tasks i.e. ModelDefinition, LoadDefinition etc.

Designing the object hierarchy this way allows multiple ModelDefinitions to be
defined in a pyFS list and these can be used  with single or multiple Load,
Analysis of Post-Processing objects in a single pyFS model.
"""


class UserDefinition:
    """
    Represents all the functionality required to write user defined .U files
    for use and archiving in FS2000.
    """
