from PyQt5 import QtWidgets, QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.logoLabel = QtWidgets.QLabel(self.centralwidget)
        self.logoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.logoLabel.setFixedSize(250, 200)
        self.verticalLayout.addWidget(self.logoLabel, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        
        self.tablesListWidget = QtWidgets.QListWidget(self.centralwidget)
        self.tablesListWidget.setObjectName("tablesListWidget")
        self.verticalLayout.addWidget(self.tablesListWidget)
        
        self.searchLayout = QtWidgets.QHBoxLayout()
        self.searchLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.searchLineEdit.setObjectName("searchLineEdit")
        self.searchButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchButton.setObjectName("searchButton")
        self.searchButton.setText("Search")
        self.searchLayout.addWidget(self.searchLineEdit)
        self.searchLayout.addWidget(self.searchButton)
        self.verticalLayout.addLayout(self.searchLayout)

        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.addButton = QtWidgets.QPushButton(self.centralwidget)
        self.addButton.setObjectName("addButton")
        self.addButton.setText("Add")
        self.editButton = QtWidgets.QPushButton(self.centralwidget)
        self.editButton.setObjectName("editButton")
        self.editButton.setText("Edit")
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setObjectName("deleteButton")
        self.deleteButton.setText("Delete")
        self.buttonLayout.addWidget(self.addButton)
        self.buttonLayout.addWidget(self.editButton)
        self.buttonLayout.addWidget(self.deleteButton)
        self.verticalLayout.addLayout(self.buttonLayout)
        
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        
        self.menuFile.addAction(self.actionOpen)
        self.menubar.addAction(self.menuFile.menuAction())
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Turan's SQLite Browser"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
