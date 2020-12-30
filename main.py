# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

# HOW TO USE:
# install PyQt5 by typing pip install pyqt5 into cmd
# run as usual :>

from PyQt5 import QtCore, QtGui, QtWidgets
import lexical_analyzer3 as la, semantics_analyzer as sea, syntax_analyzer as sya, re

import os,sys
from pathlib import Path

running = True
current_line = 0
lexemes = ""
symbol_table = ""
initialized_flag = False
finished_flag = True
tokenized_flag = False
syntactically_correct_flag = False
final = ""

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 599)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.code_input = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.code_input.setGeometry(QtCore.QRect(10, 10, 381, 261))
        self.code_input.setObjectName("code_input")
        self.lexemes_label = QtWidgets.QLabel(self.centralwidget)
        self.lexemes_label.setGeometry(QtCore.QRect(450, 0, 91, 31))
        self.lexemes_label.setAlignment(QtCore.Qt.AlignCenter)
        self.lexemes_label.setObjectName("lexemes_label")
        self.code_output = QtWidgets.QTextBrowser(self.centralwidget)
        self.code_output.setGeometry(QtCore.QRect(10, 310, 781, 181))
        self.code_output.setObjectName("code_output")
        self.execute_button = QtWidgets.QPushButton(self.centralwidget)
        self.execute_button.setGeometry(QtCore.QRect(10, 280, 781, 23))
        self.execute_button.setObjectName("execute_button")
        self.symboltable_label = QtWidgets.QLabel(self.centralwidget)
        self.symboltable_label.setGeometry(QtCore.QRect(650, 0, 91, 31))
        self.symboltable_label.setAlignment(QtCore.Qt.AlignCenter)
        self.symboltable_label.setObjectName("symboltable_label")
        self.lexemes_list = QtWidgets.QTableWidget(self.centralwidget)
        self.lexemes_list.setGeometry(QtCore.QRect(400, 30, 191, 241))
        self.lexemes_list.setColumnCount(2)
        self.lexemes_list.setObjectName("lexemes_list")
        self.lexemes_list.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.lexemes_list.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.lexemes_list.setHorizontalHeaderItem(1, item)
        self.symboltable_list = QtWidgets.QTableWidget(self.centralwidget)
        self.symboltable_list.setGeometry(QtCore.QRect(600, 30, 191, 241))
        self.symboltable_list.setColumnCount(2)
        self.symboltable_list.setObjectName("symboltable_list")
        self.symboltable_list.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.symboltable_list.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.symboltable_list.setHorizontalHeaderItem(1, item)
        self.user_input = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.user_input.setGeometry(QtCore.QRect(10, 520, 371, 31))
        self.user_input.setObjectName("user_input")
        self.user_input_label = QtWidgets.QLabel(self.centralwidget)
        self.user_input_label.setGeometry(QtCore.QRect(150, 490, 91, 31))
        self.user_input_label.setAlignment(QtCore.Qt.AlignCenter)
        self.user_input_label.setObjectName("user_input_label")
        self.user_input_submit = QtWidgets.QPushButton(self.centralwidget)
        self.user_input_submit.setGeometry(QtCore.QRect(390, 520, 75, 31))
        self.user_input_submit.setObjectName("user_input_submit")
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

        self.execute_button.clicked.connect(self.execute_clicked)
        self.user_input_submit.clicked.connect(self.user_input_clicked)
        self.actionOpen.triggered.connect(self.file_dialog_open)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "LOLCode Interpreter - Team Kanin"))
        MainWindow.setAccessibleName(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.lexemes_label.setText(_translate("MainWindow", "Lexemes"))
        self.execute_button.setText(_translate("MainWindow", "Execute"))
        self.symboltable_label.setText(_translate("MainWindow", "Symbol Table"))
        item = self.lexemes_list.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Lexeme"))
        item = self.lexemes_list.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Classification"))
        item = self.symboltable_list.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Identifier"))
        item = self.symboltable_list.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Value"))
        self.user_input_label.setText(_translate("MainWindow", "User Input"))
        self.user_input_submit.setText(_translate("MainWindow", "Submit"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
    
    def user_input_clicked(self, MainWindow):
        global running
        global current_line
        global lexemes
        global symbol_table
        global finished_flag
        global final

        if finished_flag == False:
            user_input = self.user_input.toPlainText()
            # check if var is in symbol table
            for j in range(0, len(final[3])):
                if final[3][j][0] == lexemes[0][current_line][1]:
                    final[3][j][2] = user_input
                    self.symboltable_list.setItem(j,1,QtWidgets.QTableWidgetItem(final[3][j][2]))
                    break
            current_line += 1
            running = True
            print("i was clicked!")
            self.execute_clicked(MainWindow)

    def execute_clicked(self, MainWindow):
        global running
        global current_line
        global lexemes
        global symbol_table
        global initialized_flag
        global finished_flag
        global tokenized_flag
        global syntactically_correct_flag
        global final

        if initialized_flag == False and finished_flag == True:
            # clears the tables bago simulan yung pagaanalyze
            while self.lexemes_list.rowCount() > 0:
                self.lexemes_list.removeRow(0)

            while self.symboltable_list.rowCount() > 0:
                self.symboltable_list.removeRow(0)

            #clears the input/output text box
            QtWidgets.QTextBrowser.clear(self.code_output)
            QtWidgets.QPlainTextEdit.clear(self.user_input)

            # takes text from code_input
            code = self.code_input.toPlainText()
            if tokenized_flag == False:
                # ieexecute and lexical analyzer
                lexemes = la.LexicalAnalyzer(code)
                
                tokenized_flag = True

            # check lang if hindi line # yung nirereturn ni lexeme, if int yung nireturn ibig sabihin may maling token
            if not isinstance(lexemes, int):
                
                for i in range(0, len(lexemes[1])):
                    self.lexemes_list.insertRow(i)
                    self.lexemes_list.setItem(i,0,QtWidgets.QTableWidgetItem(lexemes[1][i].lexeme))
                    self.lexemes_list.setItem(i,1,QtWidgets.QTableWidgetItem(lexemes[1][i].type))

                #execute na yung syntax analyzer
                if syntactically_correct_flag == False:
                    symbol_table = sya.SyntaxAnalyzer(lexemes[0],lexemes[1])
                    #magpprint kapag error message lang nireturn ni syntax analyzer
                    if isinstance(symbol_table, str):
                        self.code_output.append(symbol_table)
                        finished_flag = True
                        current_line = 0
                        initialized_flag = False
                        tokenized_flag = False
                        syntactically_correct_flag = False
                        return
                    syntactically_correct_flag = True

                # check lang if tama yung nirereturn ng syntax analyzer
                if len(symbol_table) == 4:
                    
                    # initialize lang ng symbol table based sa syntax analyzer
                    for i in range(0, len(symbol_table[2])):
                        self.symboltable_list.insertRow(i)
                        self.symboltable_list.setItem(i,0,QtWidgets.QTableWidgetItem(symbol_table[2][i][0]))
                        if isinstance(symbol_table[2][i][2], str):
                            self.symboltable_list.setItem(i,1,QtWidgets.QTableWidgetItem(symbol_table[2][i][2]))
                        elif symbol_table[2][i][2] == None:
                            self.symboltable_list.setItem(i,1,QtWidgets.QTableWidgetItem("NOOB"))
                        else:
                            self.symboltable_list.setItem(i,1,QtWidgets.QTableWidgetItem(str(symbol_table[2][i][2])))
                    initialized_flag = True
                    finished_flag = False

            else:
                finished_flag = True
                current_line = 0
                initialized_flag = False
                error_message = "LEXICAL ERROR AT LINE " + str(lexemes+1)
                self.code_output.append(error_message)
                return
            
        if tokenized_flag == True and syntactically_correct_flag == True:
            #idadaan na sa semantics analyzer and ieexecute :>
            final = sea.SemanticsAnalyzer(current_line,symbol_table[0],symbol_table[1],symbol_table[2],symbol_table[3])

            # if there is an error
            if len(final) == 2:
                #print yung lines bago magkaerror
                for j in range(0, len(final[0])):
                    self.code_output.append(str(final[0][j]))
                #ayusin symbol table bago magkaerror
                for j in range(0, len(final[1])):
                    if isinstance(final[1][j][2], str):
                        self.symboltable_list.setItem(j,1,QtWidgets.QTableWidgetItem(final[1][j][2]))
                    elif final[1][j][2] == None:
                        self.symboltable_list.setItem(j,1,QtWidgets.QTableWidgetItem("NOOB"))
                    else:
                        self.symboltable_list.setItem(j,1,QtWidgets.QTableWidgetItem(str(final[1][j][2])))
                finished_flag = True
                current_line = 0
                initialized_flag = False
                tokenized_flag = False
                syntactically_correct_flag = False
                return

            current_line = final[1]
            if running and current_line <= len(lexemes[0]):
                print(final[0])
                #pagprint ng VISIBLE lines
                for j in range(0, len(final[0])):
                    self.code_output.append(str(final[0][j]))
                #pag-ayos ng symbol table
                for j in range(0, len(final[3])):
                    if isinstance(final[3][j][2], str):
                        self.symboltable_list.setItem(j,1,QtWidgets.QTableWidgetItem(final[3][j][2]))
                    elif final[3][j][2] == None:
                        self.symboltable_list.setItem(j,1,QtWidgets.QTableWidgetItem("NOOB"))
                    else:
                        self.symboltable_list.setItem(j,1,QtWidgets.QTableWidgetItem(str(final[3][j][2])))
                        
            # if tapos na basahin ng program yung lexemes
            if current_line == len(lexemes[0]):
                finished_flag = True
                current_line = 0
                initialized_flag = False
                tokenized_flag = False
                syntactically_correct_flag = False
                

    def file_dialog_open(self, MainWindow):
        home_dir = str(os.path.dirname(os.path.abspath(__file__)))
        fname = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', home_dir)

        if fname[0]:
            f = open(fname[0], 'r')
            QtWidgets.QPlainTextEdit.clear(self.code_input)
            with f:
                code = f.read()
                self.code_input.appendPlainText(code)

if __name__ == "__main__":
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())

code2 = '''
BTW for assignment to variables
HAI
  I HAS A var1
  I HAS A var2
  I HAS A var3
  I HAS A var4
  I HAS A var5
  I HAS A var6
  I HAS A var7
  I HAS A var8
  
  BTW assignment of literals
  var1 R 17
  var2 R "seventeen"
  var3 R FAIL
  var4 R 2.18
  BTW printing...
  VISIBLE var1
  VISIBLE var2
  VISIBLE var3
  VISIBLE var4
  BTW assignment of expressions
  var5 R PRODUKT OF 1 AN 7
  var6 R WON OF WIN AN FAIL
  var7 R BOTH SAEM var1 AN var2
  var8 R EITHER OF FAIL AN FAIL
  BTW IT!!!!
  IT R "am IT"
  BTW printing...
  VISIBLE "var5"
  VISIBLE var6
  VISIBLE var7
  VISIBLE var8
  VISIBLE IT
KTHXBYE
'''

code5 = '''
BTW for USER INPUT/OUTPUT
HAI
  BTW printing of literals
  VISIBLE "henlo"
  VISIBLE 17
  VISIBLE 1.7
  VISIBLE WIN
  BTW infinite arity printing (concat)
  VISIBLE "hi, I'm pi. My value is " 3.14
  VISIBLE "brrr " "baaa " "fa la la," " la la"
  BTW printing of expressions
  VISIBLE SUM OF 2 AN PRODUKT OF 3 AN 5
  VISIBLE BOTH SAEM 2 AN 3
  VISIBLE EITHER OF WIN AN FAIL
  BTW printing of variables and use of GIMMEH
  I HAS A input 
  VISIBLE "gif imput "
  GIMMEH input
  VISIBLE input
  VISIBLE "u gif meh " input "!"
KTHXBYE
'''