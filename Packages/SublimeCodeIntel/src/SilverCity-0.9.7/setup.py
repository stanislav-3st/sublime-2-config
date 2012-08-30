#!/usr/bin/env python 
 
from distutils.core import setup, Extension 
from distutils.command.install_data import install_data
import sys 
import os

class fixed_install_data(install_data):
    """Sets install_dir to be install directory of extension
    modules, instead of the root Python directory"""
    
    def finalize_options(self):
        if self.install_dir is None:
            installobj = self.distribution.get_command_obj('install')
            self.install_dir = installobj.install_platlib
        install_data.finalize_options(self)

src_files = []

# Add Python extension source files
src_files.extend(
        [os.path.join('PySilverCity/Src', file) for file in
            ["PyLexerModule.cxx",
           "PyPropSet.cxx",
           "PySilverCity.cxx",
           "PyWordList.cxx"]
        ]
    )

# Add library source files
src_files.extend(
        [os.path.join('Lib/Src', file) for file in
            ["BufferAccessor.cxx",
             "LineVector.cxx",
             "Platform.cxx"]
         ]
    )

# Add Scintilla support files
scintilla_candidates = [os.path.join(os.pardir, 'scintilla'), 'scintilla']
for candidate in scintilla_candidates:
    if os.path.exists(os.path.join(candidate, 'src')):
        scintilla_scr = os.path.join(candidate, 'src')
        scintilla_include = os.path.join(candidate, 'include')
        break
else:
    raise OSError("couldn't find scintilla src and include dirs: '%s'"
                  % "', '".join(scintilla_candidates))
src_files.extend(
        [os.path.join(scintilla_scr, file) for file in
            ["KeyMap.cxx",
            "KeyWords.cxx",
            "PropSet.cxx",
            "StyleContext.cxx",
            "UniConversion.cxx",
            "CharClassify.cxx"]
        ]
    )

# Add Scintilla lexers
for file in os.listdir(scintilla_scr):
    file = os.path.join(scintilla_scr, file)
    if os.path.basename(file).startswith('Lex') and \
       os.path.splitext(file)[1] == '.cxx':
        src_files.append(file)
        
include_dirs = [scintilla_scr,
                scintilla_include,
                'Lib/Src']

data_files = ['CSS/default.css']
libraries = ['pcre']
defines = []

scripts = [os.path.join('PySilverCity','Scripts', script) for script in
           ['source2html.py',
            'cgi-styler.py',
            'cgi-styler-form.py']]


# Windows specific definitions
if sys.platform.startswith("win32"):
    defines.append(('WIN32',None))
    libraries.append('kernel32')
else:
    pass

    # Depending on your gcc and Python version, one of both of the following lines might
    # be necessary
    
    # libraries.append('gcc')
    # libraries.append('stdc++')
    
setup(  name = "SilverCity", 
        version = "0.9.7", 
        description = "Python interface to Scintilla lexers", 
        author = "Brian Quinlan",
        long_description =
"""SilverCity is a lexing package, based on Scintilla, that can provide lexical
analysis for over 20 programming and markup langauges. Included in the package
are modules to convert source code to syntax-styled HTML.""",
        
        author_email = "brian@sweetapp.com", 
        url = "http://silvercity.sourceforge.net",
        licence = "BSD-style",
        ext_package = "SilverCity",
        cmdclass = {'install_data': fixed_install_data},
        ext_modules = [Extension("_SilverCity", src_files,   
                        define_macros = defines, 
                        include_dirs = include_dirs,
                        libraries = libraries)],
        data_files = [('SilverCity', data_files)],
        scripts = scripts,
        package_dir = {'': 'PySilverCity'},
        py_modules =["SilverCity.__init__",
                     "SilverCity.DispatchHandler",
                     "SilverCity.HTMLGenerator",
                     "SilverCity.Keywords",
                     "SilverCity.LanguageInfo",
                     "SilverCity.Lexer",
                     "SilverCity.ScintillaConstants",
                     "SilverCity.Utils",
                     # Lexers
                     "SilverCity.CPP",
                     "SilverCity.CSS",
                     "SilverCity.HyperText",
                     "SilverCity.Java",
                     "SilverCity.NULL",
                     "SilverCity.Perl",
                     "SilverCity.Python",
                     "SilverCity.Ruby",
                     "SilverCity.SQL",
                     "SilverCity.Verilog",
                     "SilverCity.XML",
                     "SilverCity.XSLT",
                     "SilverCity.YAML",
                     ])
