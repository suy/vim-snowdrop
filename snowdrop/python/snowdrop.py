import clang.cindex
from clang.cindex import Index
from clang.cindex import Config
from clang.cindex import Cursor
from clang.cindex import SourceLocation

clang.cindex.functionList.append(
  ("clang_getClangVersion",
   [],
   clang.cindex._CXString,
   clang.cindex._CXString.from_result
   ),
)


def set_library_path(path):
	if path != "":
		Config.loaded = False
		Config.set_library_path(path)

def get_library_file():
	conf = Config()
	return conf.get_filename()


def get_clang_version():
	conf = Config()
	return conf.lib.clang_getClangVersion()


def includes(source, options, name):
	index = Index.create()
	tree = index.parse(name, args = options, unsaved_files = [ (name, source) ])
	return list(set(map((lambda x: x.source.name), tree.get_includes())))


def definition(source, filename, options, line, col):
	index = Index.create()
	tu = index.parse(filename, args = options, unsaved_files = [ (filename, source) ])
	location = tu.get_location(filename, (line, col))
	cursor = Cursor.from_location(tu, location)
	defs = [cursor.get_definition(), cursor.referenced]
	for d in defs:
		if d is not None and location != d.location:
			location = d.location
			return [location.file.name, location.line, location.column]
	return ["", 0, 0]


