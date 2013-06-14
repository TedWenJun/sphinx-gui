from PySide import QtGui, QtCore
from unipath import Path

from editor import Editor
from preview import Preview
from tree import Tree


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.tree =  Tree()
        self.editor = Editor()
        self.preview = Preview()
        self.setCentralWidget(splitter)        
        splitter.addWidget(self.tree)
        splitter.addWidget(self.editor)
        splitter.addWidget(self.preview)

        self.setWindowTitle("RST Previewer")
        self.showMaximized()
        
        self.setupActions()

    def setupActions(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.openAction = QtGui.QAction(
                                QtGui.QIcon(":/images/open.png"), 
                                "&Open", 
                                self, 
                                shortcut="Ctrl+O",
                                statusTip="Open File", 
                                triggered=self.openFile
                            )
        self.fileMenu.addAction(self.openAction)

    def openFile(self, path=None):
        if not path:
            path = QtGui.QFileDialog.getOpenFileName(self, "Open File",
                    '', "ReStructuredText Files (*.rst)")
    
        if path:
            inFile = QtCore.QFile(path[0])
            if inFile.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
                text = inFile.readAll()
    
                try:
                    # Python v3.
                    text = str(text, encoding='ascii')
                except TypeError:
                    # Python v2.
                    text = str(text)
    
                self.editor.setPlainText(text)
                
                # Link the tree to a model
                model = QtGui.QFileSystemModel()
                file_path = Path(path[0])
                tree_dir = file_path.parent.absolute()
                model.setRootPath(tree_dir)
                self.tree.setModel(model)
                
                # Set the tree's index to the root of the model
                indexRoot = model.index(model.rootPath())
                self.tree.setRootIndex(indexRoot)
                
                # Hide tree size and date columns
                self.tree.hideColumn(1)
                self.tree.hideColumn(2)
                self.tree.hideColumn(3)
                
                # Hide tree header
                self.tree.setHeaderHidden(True)
                
                # Load corresponding HTML file from pre-built Sphinx docs
                file_stem = str(file_path.stem)
                html_str = "_build/html/{0}.html".format(file_stem)
                output_html_path = Path(file_path.parent, html_str).absolute()
                self.preview.load_html(output_html_path)
                