# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwidget.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QLabel, QSizePolicy,
    QWidget)

from qfluentwidgets import (LineEdit, PrimaryPushButton, IndeterminateProgressBar, PushButton,
    RadioButton)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(640, 424)
        self.FolderButton = PushButton(Form)
        self.FolderButton.setObjectName(u"FolderButton")
        self.FolderButton.setGeometry(QRect(30, 30, 171, 32))
        self.FolderLabel = QLabel(Form)
        self.FolderLabel.setObjectName(u"FolderLabel")
        self.FolderLabel.setGeometry(QRect(220, 40, 401, 21))
        font = QFont()
        font.setFamilies([u"Yu Gothic UI"])
        font.setPointSize(13)
        font.setBold(True)
        font.setItalic(False)
        self.FolderLabel.setFont(font)
        self.TargetButton = PushButton(Form)
        self.TargetButton.setObjectName(u"TargetButton")
        self.TargetButton.setGeometry(QRect(30, 90, 171, 32))
        self.TargetLabel = QLabel(Form)
        self.TargetLabel.setObjectName(u"TargetLabel")
        self.TargetLabel.setGeometry(QRect(220, 100, 401, 21))
        self.TargetLabel.setFont(font)
        self.SearchEdit_1 = LineEdit(Form)
        self.SearchEdit_1.setObjectName(u"SearchEdit_1")
        self.SearchEdit_1.setGeometry(QRect(30, 180, 81, 33))
        self.SearchEdit_2 = LineEdit(Form)
        self.SearchEdit_2.setObjectName(u"SearchEdit_2")
        self.SearchEdit_2.setGeometry(QRect(130, 180, 81, 33))
        self.SearchEdit_3 = LineEdit(Form)
        self.SearchEdit_3.setObjectName(u"SearchEdit_3")
        self.SearchEdit_3.setGeometry(QRect(230, 180, 391, 33))
        self.TextLabel = QLabel(Form)
        self.TextLabel.setObjectName(u"TextLabel")
        self.TextLabel.setGeometry(QRect(40, 150, 401, 21))
        font1 = QFont()
        font1.setFamilies([u"Yu Gothic UI"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.TextLabel.setFont(font1)
        self.SheetGroup = QGroupBox(Form)
        self.SheetGroup.setObjectName(u"SheetGroup")
        self.SheetGroup.setGeometry(QRect(330, 230, 271, 81))
        font2 = QFont()
        font2.setFamilies([u"Yu Gothic UI"])
        self.SheetGroup.setFont(font2)
        self.SheetGroup.setStyleSheet(u"QGroupBox{\n"
"\n"
"border-width:2px;\n"
"\n"
"border-style:solid;\n"
"\n"
"border-radius: 10px;\n"
"\n"
"border-color:gray;\n"
"\n"
"margin-top:0.5ex;\n"
"\n"
"}\n"
"\n"
"QGroupBox::title{\n"
"\n"
"subcontrol-origin:margin;\n"
"\n"
"subcontrol-position:top left;\n"
"\n"
"left:10px;\n"
"\n"
"margin-left:0px;\n"
"\n"
"padding:0 1px;\n"
"\n"
"}")
        self.NoFDRadio = RadioButton(self.SheetGroup)
        self.NoFDRadio.setObjectName(u"NoFDRadio")
        self.NoFDRadio.setGeometry(QRect(10, 30, 112, 24))
        self.FDRadio = RadioButton(self.SheetGroup)
        self.FDRadio.setObjectName(u"FDRadio")
        self.FDRadio.setGeometry(QRect(140, 30, 112, 24))
        self.FunctionGroup = QGroupBox(Form)
        self.FunctionGroup.setObjectName(u"FunctionGroup")
        self.FunctionGroup.setGeometry(QRect(40, 230, 251, 121))
        self.FunctionGroup.setFont(font2)
        self.FunctionGroup.setStyleSheet(u"QGroupBox{\n"
"\n"
"border-width:2px;\n"
"\n"
"border-style:solid;\n"
"\n"
"border-radius: 10px;\n"
"\n"
"border-color:gray;\n"
"\n"
"margin-top:0.5ex;\n"
"\n"
"}\n"
"\n"
"QGroupBox::title{\n"
"\n"
"subcontrol-origin:margin;\n"
"\n"
"subcontrol-position:top left;\n"
"\n"
"left:10px;\n"
"\n"
"margin-left:0px;\n"
"\n"
"padding:0 1px;\n"
"\n"
"}")
        self.DistinguishRadio = RadioButton(self.FunctionGroup)
        self.DistinguishRadio.setObjectName(u"DistinguishRadio")
        self.DistinguishRadio.setGeometry(QRect(30, 80, 112, 24))
        self.ProblemRadio = RadioButton(self.FunctionGroup)
        self.ProblemRadio.setObjectName(u"ProblemRadio")
        self.ProblemRadio.setGeometry(QRect(30, 30, 221, 24))
        self.AllRadio = RadioButton(self.FunctionGroup)
        self.AllRadio.setObjectName(u"AllRadio")
        self.AllRadio.setGeometry(QRect(150, 80, 112, 24))
        self.RunButton = PushButton(Form)
        self.RunButton.setObjectName(u"RunRadio")
        self.RunButton.setGeometry(QRect(330, 320, 102, 32))
        self.ExitButton = PrimaryPushButton(Form)
        self.ExitButton.setObjectName(u"ExitButton")
        self.ExitButton.setGeometry(QRect(450, 320, 153, 32))
        self.IndeterminateProgressBar = IndeterminateProgressBar(Form)
        self.IndeterminateProgressBar.setObjectName(u"IndeterminateProgressBar")
        self.IndeterminateProgressBar.setGeometry(QRect(40, 400, 571, 4))
        self.LogsLabel = QLabel(Form)
        self.LogsLabel.setObjectName(u"LogsLabel")
        self.LogsLabel.setGeometry(QRect(40, 360, 561, 20))
        font3 = QFont()
        font3.setPointSize(10)
        self.LogsLabel.setFont(font3)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.FolderButton.setText(QCoreApplication.translate("Form", u"BitAssgin\u683c\u7d0d\u30d1\u30b9", None))
        self.FolderLabel.setText(QCoreApplication.translate("Form", u"\u4f5c\u696d\u30d5\u30a9\u30eb\u30c0\u672a\u9078\u629e\u3067\u3059", None))
        self.TargetButton.setText(QCoreApplication.translate("Form", u"\u66f4\u65b0\u5bfe\u8c61\u30c9\u30ad\u30e5\u30e1\u30f3\u30c8", None))
        self.TargetLabel.setText(QCoreApplication.translate("Form", u"\u5bfe\u8c61\u30d5\u30a1\u30a4\u30eb\u3092\u9078\u629e\u3057\u3066\u3044\u307e\u305b\u3093", None))
        self.TextLabel.setText(QCoreApplication.translate("Form", u"\u8eca\u4e21\u60c5\u5831\uff08\u958b\u767a\u30d5\u30a7\u30fc\u30ba\uff09(\u203b\u624b\u52d5\u5165\u529b\u3059\u308b\u5fc5\u8981)", None))
        self.SheetGroup.setTitle(QCoreApplication.translate("Form", u"BITASSIGN(sheet)", None))
        self.NoFDRadio.setText(QCoreApplication.translate("Form", u"Transmit", None))
        self.FDRadio.setText(QCoreApplication.translate("Form", u"Transmit(FD)", None))
        self.FunctionGroup.setTitle(QCoreApplication.translate("Form", u"\u6a5f\u80fd\u9078\u629e\u3067\u3059", None))
        self.DistinguishRadio.setText(QCoreApplication.translate("Form", u"\u5224\u5225\u4ed5\u69d8", None))
        self.ProblemRadio.setText(QCoreApplication.translate("Form", u"CCD\u306eCCSSIF\u306e\u554f\u984c\u70b9\u6574\u7406", None))
        self.AllRadio.setText(QCoreApplication.translate("Form", u"ALL", None))
        self.RunButton.setText(QCoreApplication.translate("Form", u"\u5b9f\u884c", None))
        self.ExitButton.setText(QCoreApplication.translate("Form", u"\u30d7\u30ed\u30b0\u30e9\u30e0\u7d42\u4e86\u3067\u3059", None))
        self.LogsLabel.setText("")
    # retranslateUi

