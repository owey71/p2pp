__author__ = 'Tom Van den Eede'
__copyright__ = 'Copyright 2018-2020, Palette2 Splicer Post Processing Project'
__credits__ = ['Tom Van den Eede',
               'Tim Brookman'
               ]
__license__ = 'GPLv3'
__maintainer__ = 'Tom Van den Eede'
__email__ = 'P2PP@pandora.be'
__status__ = 'BETA'


# general version info
MajorVersion = 5
MinorVersion = 28
Build = 0

releaseinfo = {
    '4.16.0': "final release for PrusaSlicer 2.2.0",
    '5.0.0': "Development start for PrusaSlicer 2.3.0",
    '5.1.0': "Automatic detection of bed origin and size",
    '5.2.0': "Static side purge",
    '5.2.1': "Extruder clear added on static purge",
    '5.3.0': "error in minimal linear ping length error string",
    '5.4.0': "corrected is_movement_command checking",
    '5.5.0': "correction in non-synched support material handling",
    '5.6.0': "updated in Aboslute conversion post processing",
    '5.7.0': "Fixup More than 4 color print",
    "5.10.0": "General code restructuring for optimized processing",
    "5.10.1": "further process optimization",
    "5.10.2": "typo correction in TOOLSTART processing",
    "5.11.0": "memory usage optimization",
    "5.12.0": "further memory usage optimization, speed optimization",
    "5.13.0": "weekend development cut off with some bugfixes",
    "5.14.0": "rewrite path processing routines",
    "5.15.0": "taken care to retain empty comments",
    "5.16.0": "fixup Z-move after unload",
    "5.17.0": "fixup error when doing unprocessed tower entry",
    "5.18.0": "MAF file is generated as BINARY file",
    "5.19.0": "update to config parsin from prusa settings instead of parsing in full file",
    "5.20.0": "updated parseline routine to prevent repetitive function call",
    "5.21.0": "small correction in gui and filemant type processing",
    "5.22.0": "corrected tower delta",
    "5.23.0": "better tower detection",
    "5.24.0": "DO_NOT_GENERATE_M0 option added",
    "5.25.0": "possible incorrect tool select - corrected",
    "5.26.0": "remove M0 from existing output",
    "5.27.0": "correction in the tower delta calculation",
    "5.28.0": "removed GUI - tkinter issue",
    '--- RELEASE INFORMATION': 'END'
}

latest_stable_version = ""

Version = "{}.{:02}.{:03}".format(MajorVersion, MinorVersion, Build)

##################################
# UPDATE FILES FOR CURRENT VERSION
##################################
# zip_file=p2pp_mac.zip
