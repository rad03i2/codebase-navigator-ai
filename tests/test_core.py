import tempfile, unittest
from pathlib import Path
from codebase_navigator import build_index, find_symbols, search_text, context

class NavigatorTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
        (self.root/"app.py").write_text("class Greeter:\n    def hello(self, name):\n        return f'Hello {name}'\n",encoding="utf-8")
        (self.root/"notes.md").write_text("Hello architecture\n",encoding="utf-8")
        (self.root/"node_modules").mkdir(); (self.root/"node_modules"/"x.js").write_text("secret ignored",encoding="utf-8")
        self.idx=build_index(self.root)
    def tearDown(self): self.tmp.cleanup()
    def test_index_and_symbols(self):
        self.assertEqual(self.idx.summary()["files"],2)
        self.assertEqual([s.name for s in find_symbols(self.idx,"greet")],["Greeter"])
        self.assertEqual(find_symbols(self.idx,"hello")[0].signature,"hello(self, name)")
    def test_text_search_and_glob(self):
        self.assertEqual(len(search_text(self.idx,"hello")),2)
        self.assertEqual(search_text(self.idx,"architecture",glob="*.md")[0].path,"notes.md")
    def test_context(self):
        rows=context(self.idx,"app.py",2,1); self.assertEqual([n for n,_ in rows],[1,2,3])
    def test_path_escape_rejected(self):
        with self.assertRaises(ValueError): context(self.idx,"../outside",1)
    def test_bad_root_rejected(self):
        with self.assertRaises(ValueError): build_index(self.root/"missing")

if __name__=="__main__": unittest.main()
