import os
import sys

import time
import xlwings

from PySide6.QtCore import QObject, Signal, QThread
from PySide6.QtWidgets import QApplication, QFileDialog
from qfluentwidgets import MessageDialog
from qframelesswindow import FramelessDialog

from mainwidget import Ui_Form


class ExcelEditThread(QObject):
    completeSignal = Signal()
    infoSignal = Signal(str)
    errorSignal = Signal(str)

    def __init__(self):
        super().__init__()
        self.errorFlag = bool()
        self.logFileName = str()
        self.app = None
        self.logs = None

    def run(self, search, targetFileName, func, sheet, logFileName):
        self.errorFlag = False
        self.logFileName = logFileName
        self.logs = open(logFileName, 'w', encoding='UTF-8')
        self.logSend('开始运行')
        self.app = xlwings.App(visible=False, add_book=False)
        try:
            targetBook = self.app.books.open(targetFileName)
        except:
            self.errorSignal('打开表格失败 请检查表格是否被占用')
            self.app.quit()
            return
        if func == 'CCDのCCSSIFの問題点整理' or func == 'ALL':
            self.searchMount(search, targetBook, sheet, 1)
        if func == '判別仕様' or func == 'ALL':
            self.searchMount(search, targetBook, sheet, 0)
        print(self.errorFlag)
        if self.errorFlag is False:
            try:
                targetBook.save()
            except:
                self.errorSignal('保存失败 请检查表格是否被占用')
            self.logSend('保存成功 正在关闭表')
            targetBook.close()
            self.completeSignal.emit()
        self.logs.close()
        self.app.quit()

    def searchMount(self, search, targetBook, sheet, targetS):
        mountPointL = -1
        mountPointC = -1
        mountSearchL = -1
        mountSearchC = -1
        mountConfirmC = -1
        if targetS == 0:
            searchName = 'フレーム'
        else:
            searchName = 'フレーム名/シグナル名'
        targetSheet = targetBook.sheets[targetS]
        self.logSend('表格大小为%dx%d' % (targetSheet.used_range.shape[0], targetSheet.used_range.shape[1]))
        for j in range(targetSheet.used_range.shape[0]):
            searchArea = targetSheet.range((j + 1, 1), (j + 1, targetSheet.used_range.shape[1] + 1)).value
            for i in range(targetSheet.used_range.shape[1]):
                if mountPointC == -1:
                    if searchArea[i] is not None:
                        if search[0] in searchArea[i] and search[1] in searchArea[i] and search[2] in searchArea[i]:
                            mountPointC = i
                            mountPointL = j
                            self.logSend('已找到主锚定点')
                            break
                else:
                    break
            if mountSearchL == -1:
                if searchName in searchArea:
                    mountSearchL = j + 1
                    mountSearchC = searchArea.index(searchName)
                    self.logSend('已找到%s' % searchName)
            if mountPointC != -1 and mountSearchL != -1:
                break
        move = self.editContent(targetSheet, mountPointL + 1, mountPointC, mountSearchL, mountSearchC, sheet, targetS)
        if move == -2:
            return
        if move == -1:
            self.errorSignal('数据表查找错误 请检查对应数据表是否存在')
            self.errorFlag = True
            return
        Tmove = move
        while True:
            if move == -2:
                return
            if move == -1:
                break
            else:
                move = self.editContent(targetSheet, mountPointL + 1, mountPointC + Tmove, mountSearchL, mountSearchC,
                                        sheet, targetS)
                Tmove += move
        if targetSheet[(mountPointL + 2, mountPointC + Tmove + 1)].value is not None:
            if '確認結果' == targetSheet[(mountPointL + 2, mountPointC + Tmove + 1)].value:
                mountConfirmC = mountPointC + Tmove + 1
                self.logSend('已找到确认结果')
        if mountPointC == -1 or mountSearchL == -1 or mountConfirmC == -1:
            self.errorSignal("未找到子锚点,程序已终止")
            self.errorFlag = True
            return
        mountSearchLT = mountSearchL
        while True:
            if targetSheet[(mountSearchLT, mountSearchC)].value is None:
                break
            safeMod = True
            checker = True
            for i in range(mountPointC, mountConfirmC):
                if targetSheet[(mountSearchLT, i)].value is None:
                    safeMod = False
                    break
                if targetSheet[(mountSearchLT, i)].value == '非対象':
                    checker = False
            if not safeMod:
                break
            if checker:
                targetSheet[(mountSearchLT, mountConfirmC)].value = 'OK'
                self.logSend('第%s行 第%s列填充为OK' % (mountSearchLT + 1, mountConfirmC + 1))
            else:
                targetSheet[(mountSearchLT, mountConfirmC)].value = 'NG'
                targetSheet[(mountSearchLT, mountConfirmC)].color = 0x0000FF
                self.logSend('第%s行 第%s列填充为NG,设置为红色' % (mountSearchLT + 1, mountConfirmC + 1))
            mountSearchLT += 1

    def editContent(self, targetSheets, mountPointL, mountPointC, mountSearchL, mountSearchC, sheets, targetS):
        self.logSend('搜索数据表中')
        if targetSheets[(mountPointL, mountPointC)].value is not None:
            if '.xls' in targetSheets[(mountPointL, mountPointC)].value:
                bookName = targetSheets[(mountPointL, mountPointC)].value
                mod = 1
                while mod != 0:
                    if targetSheets[(mountPointL, mountPointC + mod)].value is not None:
                        if '.xls' in targetSheets[(mountPointL, mountPointC + mod)].value:
                            if bookName == targetSheets[(mountPointL, mountPointC + mod)].value:
                                mod += 1
                            else:
                                break
                        else:
                            break
                    else:
                        break
            else:
                return -1
        else:
            return -1
        self.logSend('已找到数据表')
        try:
            sourceBook = self.app.books.open(bookName)
        except:
            self.errorSignal.emit('数据表无法打开 请检查数据表是否存在或被占用')
            self.errorFlag = True
            return -2
        sourceBook.visible = False
        try:
            sourceSheets = sourceBook.sheets[sheets]
        except:
            self.errorSignal.emit('未在数据表中查询到对应页 请检查')
            self.errorFlag = True
            return -2
        msgC = -1
        dataC = -1
        csrC = -1
        csr00C = -1
        csr01C = -1
        self.logSend('锚定数据表结构中')
        self.logSend('表大小为%dx%d' % (sourceSheets.used_range.shape[0], sourceSheets.used_range.shape[1]))
        for j in range(sourceSheets.used_range.shape[0]):
            # print('正在搜索第', j, '行')
            searchTempValue = sourceSheets.range((j + 1, 1), (j + 1, sourceSheets.used_range.shape[1] + 1)).value
            if msgC == -1:
                if 'Msg. Label' in searchTempValue:
                    msgC = searchTempValue.index('Msg. Label')
                    self.logSend('已找到Msg. Label')
            if dataC == -1:
                if 'Data Label' in searchTempValue:
                    dataC = searchTempValue.index('Data Label')
                    self.logSend('已找到Data.Label')
            for i in range(sourceSheets.used_range.shape[1]):
                if csrC == -1:
                    if searchTempValue[i] is not None:
                        if 'C\nS\nR' in searchTempValue[i]:
                            csrC = i
                            if '00' in searchTempValue[i]:
                                csr00C = i
                                csr01C = i + 1
                            else:
                                csr00C = i + 1
                                csr01C = i + 2
                            self.logSend('已找到CSR')
                            break
                else:
                    break
            if msgC != -1 and dataC != -1 and csrC != -1:
                break
        if msgC == -1 or dataC == -1 or csrC == -1:
            self.errorSignal("未找到数据表锚点,程序已终止")
            self.errorFlag = True
            return -2
        for i in range(mod):
            mountSearchLT = mountSearchL
            mountSearchCT = mountSearchC
            mountPointCT = mountPointC
            mountPointLT = mountPointL
            if targetSheets[(mountPointLT + 1, mountPointCT + i)].value is not None:  # 判断表中的列
                if 'CSR00' in targetSheets[(mountPointLT + 1, mountPointCT + i)].value:
                    searchC = csr00C
                elif 'CSR01' in targetSheets[(mountPointLT + 1, mountPointCT + i)].value:
                    searchC = csr01C
                elif 'CSR' in targetSheets[(mountPointLT + 1, mountPointCT + i)].value:
                    searchC = csrC
                else:
                    self.errorSignal("未找到查询锚点,程序已终止")
                    self.errorFlag = True
                    return -2
            else:
                self.errorSignal("未找到查询锚点,程序已终止")
                self.errorFlag = True
                return -2
            while True:
                searchTL = -1
                if targetSheets[(mountSearchLT, mountSearchCT)].value is None:
                    break
                if targetSheets[(mountSearchLT, mountSearchCT)].value == '-':
                    targetSheets[(mountSearchLT, mountPointCT + i)].value = '-'
                    self.logSend('第' + str(mountSearchLT) + '行 第' + str(mountPointCT + i + 1) + '列填充为-')
                    mountSearchLT += 1
                    continue
                if targetSheets[(mountSearchLT, mountSearchCT)].font.impl.xl.Strikethrough or targetSheets[
                    (mountSearchLT, mountSearchCT + 1)].font.impl.xl.Strikethrough:
                    targetSheets[(mountSearchLT, mountPointCT + i)].value = '非対象'
                    targetSheets[(mountSearchLT, mountPointCT + i)].color = 0x00FFFF
                    self.logSend('发现删除线,第' + str(mountSearchLT + 1) + '行 第' + str(
                        mountPointCT + i + 1) + '列填充为非対象,设置为黄色')
                    mountSearchLT += 1
                    continue
                if targetSheets[(mountSearchLT, mountSearchCT + 1)].font.impl.xl.Strikethrough or targetSheets[
                    (mountSearchLT, mountSearchCT + 1)].font.impl.xl.Strikethrough:
                    targetSheets[(mountSearchLT, mountPointCT + i)].value = '非対象'
                    targetSheets[(mountSearchLT, mountPointCT + i)].color = 0x00FFFF
                    self.logSend('发现删除线,第' + str(mountSearchLT + 1) + '行 第' + str(
                        mountPointCT + i + 1) + '列填充为非対象,设置为黄色')
                    mountSearchLT += 1
                    continue
                searchTarget = targetSheets[(mountSearchLT, mountSearchCT)].value
                msgValue = sourceSheets.range((1, msgC + 1), (sourceSheets.used_range.shape[0] + 1, msgC + 1)).value
                dataValue = sourceSheets.range((1, dataC + 1), (sourceSheets.used_range.shape[0] + 1, dataC + 1)).value
                searchValue = sourceSheets.range((1, searchC + 1),
                                                 (sourceSheets.used_range.shape[0] + 1, searchC + 1)).value
                if targetS == 0:
                    if searchTarget in msgValue:
                        searchTL = msgValue.index(searchTarget) + 1
                    if searchTL == -1:
                        targetSheets[(mountSearchLT, mountPointCT + i)].value = '非対象'
                        targetSheets[(mountSearchLT, mountPointCT + i)].color = 0x00FFFF
                        self.logSend(
                            '' + str(searchTarget) + '在Msg. Label中未找到目标,第' + str(
                                mountSearchLT + 1) + '行 第' + str(
                                mountPointCT + i + 1) + '列填充为非対象,设置为黄色')
                        mountSearchLT += 1
                        continue
                    if targetSheets[(mountSearchLT, mountSearchCT + 1)].value == '-':
                        if searchValue[searchTL - 1] is not None:
                            if 'R' in searchValue[searchTL - 1]:
                                if sourceSheets[searchTL - 1, searchC].color is None:
                                    targetSheets[(mountSearchLT, mountPointCT + i)].value = '対象'
                                    self.logSend('' + str(searchTarget) + '在Msg. Label中找到目标,存在R且无色,第' + str(
                                        mountSearchLT + 1) + '行 第' + str(mountPointCT + i + 1) + '列填充为対象')
                                elif sourceSheets[searchTL - 1, searchC].color[0] != \
                                        sourceSheets[searchTL - 1, searchC].color[
                                            1] and sourceSheets[searchTL - 1, searchC].color[0] != \
                                        sourceSheets[searchTL - 1, searchC].color[2]:
                                    targetSheets[(mountSearchLT, mountPointCT + i)].value = '対象'
                                    self.logSend(
                                        '' + str(searchTarget) + '在Msg. Label中找到目标,存在R有别色非灰色,第' + str(
                                            mountSearchLT + 1) + '行 第' + str(mountPointCT + i + 1) + '列填充为対象')
                                else:
                                    targetSheets[(mountSearchLT, mountPointCT + i)].value = '非対象'
                                    targetSheets[(mountSearchLT, mountPointCT + i)].color = 0x00FFFF
                                    self.logSend('' + str(searchTarget) + '在Msg. Label中找到目标,存在R有灰色,第' + str(
                                        mountSearchLT + 1) + '行 第' + str(
                                        mountPointCT + i + 1) + '列填充为非対象,设置为黄色')
                            else:
                                targetSheets[(mountSearchLT, mountPointCT + i)].value = '非対象'
                                targetSheets[(mountSearchLT, mountPointCT + i)].color = 0x00FFFF
                                self.logSend('' + str(searchTarget) + '在Msg. Label中找到目标,有内容非R,第' + str(
                                    mountSearchLT + 1) + '行 第' + str(
                                    mountPointCT + i + 1) + '列填充为非対象,设置为黄色')
                        else:
                            targetSheets[(mountSearchLT, mountPointCT + i)].value = '非対象'
                            targetSheets[(mountSearchLT, mountPointCT + i)].color = 0x00FFFF
                            self.logSend('' + str(searchTarget) + '在Msg. Label中找到目标,CSR列为空,第' + str(
                                mountSearchLT + 1) + '行 第' + str(
                                mountPointCT + i + 1) + '列填充为非対象,设置为黄色')
                        mountSearchLT += 1
                        continue
                    searchTemp = targetSheets[(mountSearchLT, mountSearchCT + 1)].value
                    while True:
                        if dataValue[searchTL] is None:
                            targetSheets[(mountSearchLT, mountPointCT + i)].value = '非対象'
                            targetSheets[(mountSearchLT, mountPointCT + i)].color = 0x00FFFF
                            self.logSend(
                                '' + str(searchTemp) + '在Data Label中未找到目标,第' + str(
                                    mountSearchLT + 1) + '行 第' + str(
                                    mountPointCT + i + 1) + '列填充为非対象,设置为黄色')
                            break
                        if dataValue[searchTL] == searchTemp:
                            if searchValue[searchTL] is not None:
                                if 'R' in searchValue[searchTL]:
                                    if sourceSheets[searchTL, searchC].color is None:
                                        targetSheets[(mountSearchLT, mountPointCT + i)].value = '対象'
                                        self.logSend(
                                            '' + str(searchTarget) + '在Msg. Label中找到目标,存在R且无色,第' + str(
                                                mountSearchLT + 1) + '行 第' + str(
                                                mountPointCT + i + 1) + '列填充为対象')
                                    elif sourceSheets[searchTL, searchC].color[0] != \
                                            sourceSheets[searchTL, searchC].color[
                                                1] and sourceSheets[searchTL, searchC].color[0] != \
                                            sourceSheets[searchTL, searchC].color[2]:
                                        targetSheets[(mountSearchLT, mountPointCT + i)].value = '対象'
                                        self.logSend(
                                            '' + str(
                                                searchTarget) + '在Msg. Label中找到目标,存在R有别色非灰色,第' + str(
                                                mountSearchLT + 1) + '行 第' + str(
                                                mountPointCT + i + 1) + '列填充为対象')
                                    else:
                                        targetSheets[(mountSearchLT, mountPointCT + i)].value = '非対象'
                                        targetSheets[(mountSearchLT, mountPointCT + i)].color = 0x00FFFF
                                        self.logSend(
                                            '' + str(searchTarget) + '在Msg. Label中找到目标,存在R有灰色,第' + str(
                                                mountSearchLT + 1) + '行 第' + str(
                                                mountPointCT + i + 1) + '列填充为非対象,设置为黄色')
                                else:
                                    targetSheets[(mountSearchLT, mountPointCT + i)].value = '非対象'
                                    targetSheets[(mountSearchLT, mountPointCT + i)].color = 0x00FFFF
                                    self.logSend('' + str(searchTarget) + '在Msg. Label中找到目标,有内容非R,第' + str(
                                        mountSearchLT + 1) + '行 第' + str(
                                        mountPointCT + i + 1) + '列填充为非対象,设置为黄色')
                            else:
                                targetSheets[(mountSearchLT, mountPointCT + i)].value = '非対象'
                                targetSheets[(mountSearchLT, mountPointCT + i)].color = 0x00FFFF
                                self.logSend('' + str(searchTarget) + '在Msg. Label中找到目标,CSR列为空,第' + str(
                                    mountSearchLT + 1) + '行 第' + str(
                                    mountPointCT + i + 1) + '列填充为非対象,设置为黄色')
                            break
                        searchTL += 1
                    mountSearchLT += 1
                else:
                    if searchTarget in msgValue:
                        searchTL = msgValue.index(searchTarget)
                    elif searchTarget in dataValue:
                        searchTL = dataValue.index(searchTarget)
                    if searchTL == -1:
                        targetSheets[(mountSearchLT, mountPointCT + i)].value = '非対象'
                        targetSheets[(mountSearchLT, mountPointCT + i)].color = 0x00FFFF
                        self.logSend(
                            '' + str(searchTarget) + '在Msg. Label中未找到目标,第' + str(
                                mountSearchLT + 1) + '行 第' + str(
                                mountPointCT + i + 1) + '列填充为非対象,设置为黄色')
                    else:
                        if searchValue[searchTL] is not None:
                            if 'R' in searchValue[searchTL]:
                                if sourceSheets[searchTL, searchC].color is None:
                                    targetSheets[(mountSearchLT, mountPointCT + i)].value = '対象'
                                    self.logSend('' + str(searchTarget) + '在Msg. Label中找到目标,存在R且无色,第' + str(
                                        mountSearchLT + 1) + '行 第' + str(mountPointCT + i + 1) + '列填充为対象')
                                elif sourceSheets[searchTL, searchC].color[0] != sourceSheets[searchTL, searchC].color[
                                    1] and sourceSheets[searchTL, searchC].color[0] != \
                                        sourceSheets[searchTL, searchC].color[2]:
                                    targetSheets[(mountSearchLT, mountPointCT + i)].value = '対象'
                                    self.logSend(
                                        '' + str(searchTarget) + '在Msg. Label中找到目标,存在R有别色非灰色,第' + str(
                                            mountSearchLT + 1) + '行 第' + str(mountPointCT + i + 1) + '列填充为対象')
                                else:
                                    targetSheets[(mountSearchLT, mountPointCT + i)].value = '非対象'
                                    targetSheets[(mountSearchLT, mountPointCT + i)].color = 0x00FFFF
                                    self.logSend('' + str(searchTarget) + '在Msg. Label中找到目标,存在R有灰色,第' + str(
                                        mountSearchLT + 1) + '行 第' + str(
                                        mountPointCT + i + 1) + '列填充为非対象,设置为黄色')
                            else:
                                targetSheets[(mountSearchLT, mountPointCT + i)].value = '非対象'
                                targetSheets[(mountSearchLT, mountPointCT + i)].color = 0x00FFFF
                                self.logSend('' + str(searchTarget) + '在Msg. Label中找到目标,有内容非R,第' + str(
                                    mountSearchLT + 1) + '行 第' + str(
                                    mountPointCT + i + 1) + '列填充为非対象,设置为黄色')
                        else:
                            targetSheets[(mountSearchLT, mountPointCT + i)].value = '非対象'
                            targetSheets[(mountSearchLT, mountPointCT + i)].color = 0x00FFFF
                            self.logSend('' + str(searchTarget) + '在Msg. Label中找到目标,CSR列为空,第' + str(
                                mountSearchLT + 1) + '行 第' + str(
                                mountPointCT + i + 1) + '列填充为非対象,设置为黄色')
                    mountSearchLT += 1
                    continue
        sourceBook.close()
        return mod

    def logSend(self, log):
        self.logs.write('%s:%s\n' % (time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())), log))
        self.logs.flush()
        self.infoSignal.emit(log)


class MainWindow(FramelessDialog, Ui_Form):
    runS = Signal(list, str, str, str, str)

    def __init__(self):
        super().__init__()
        self.targetFileName = str()
        self.logFileName = str()
        self.func = str()
        self.sheet = str()
        self.ExcelEdit = ExcelEditThread()
        self.ExcelThread = QThread()
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.RunButton.setEnabled(False)
        self.ProblemRadio.setChecked(True)
        self.func = self.ProblemRadio.text()
        self.NoFDRadio.setChecked(True)
        self.sheet = self.NoFDRadio.text()
        self.IndeterminateProgressBar.stop()
        self.FolderButton.clicked.connect(self.getFolder)
        self.TargetButton.clicked.connect(self.getFile)
        self.ExitButton.clicked.connect(self.ExitB)
        self.ExcelEdit.errorSignal.connect(self.ExcelError)
        self.ExcelEdit.completeSignal.connect(self.ExcelComplete)
        self.ExcelEdit.moveToThread(self.ExcelThread)
        self.ProblemRadio.clicked.connect(self.funcB)
        self.DistinguishRadio.clicked.connect(self.funcB)
        self.AllRadio.clicked.connect(self.funcB)
        self.NoFDRadio.clicked.connect(self.sheetB)
        self.FDRadio.clicked.connect(self.sheetB)
        self.runS.connect(self.ExcelEdit.run)
        self.RunButton.clicked.connect(self.RunB)
        self.ExcelEdit.infoSignal.connect(self.ExcelInfo)

    def getFolder(self):
        Dir = QFileDialog.getExistingDirectory(self, '作業リストを選びます')
        if Dir == '':
            t = MessageDialog('警告します', 'ディレクトリエラーです。', self)
            t.exec()
            return
        os.chdir(Dir)
        self.FolderLabel.setText(os.path.abspath(os.curdir))

    def getFile(self):
        if self.FolderLabel.text() == '作業フォルダ未選択です':
            t = MessageDialog('警告します', '作業ディレクトリは設定していません', self)
            t.exec()
            return
        self.targetFileName = \
        QFileDialog.getOpenFileName(self, '目的のファイルを選択します', os.path.abspath(os.curdir),
                                    'Officeフォームです(*.xls *.xlsx)')[0]
        self.targetFileName = self.targetFileName[self.targetFileName.rfind('/') + 1:]
        for file in os.listdir(os.path.abspath(os.curdir)):
            if not os.path.isdir(file):
                if self.targetFileName == file:
                    self.TargetLabel.setText(self.targetFileName)
                    self.RunButton.setEnabled(True)
                    return
        t = MessageDialog('警告します', '書類と目次が一致しません', self)
        t.exec()

    def funcB(self):
        self.func = self.sender().text()

    def sheetB(self):
        self.sheet = self.sender().text()

    def RunB(self):
        if self.SearchEdit_1.text() == '' and self.SearchEdit_2.text() == '' and self.SearchEdit_3.text() == '':
            t = MessageDialog('警告します', '検索目標は何も記入されていません', self)
            t.exec()
            return
        self.ExcelThread.start()
        self.logFileName = '%s.txt' % (time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())))
        search = [self.SearchEdit_1.text(), self.SearchEdit_2.text(), self.SearchEdit_3.text()]
        self.RunButton.setEnabled(False)
        self.FolderButton.setEnabled(False)
        self.TargetButton.setEnabled(False)
        self.ExitButton.setEnabled(False)
        self.IndeterminateProgressBar.start()
        self.runS.emit(search, self.targetFileName, self.func, self.sheet, self.logFileName)

    def ExcelError(self, errorString):
        self.RunButton.setEnabled(True)
        self.FolderButton.setEnabled(True)
        self.TargetButton.setEnabled(True)
        self.ExcelEdit.errorFlag = True
        self.ExitButton.setEnabled(True)
        self.IndeterminateProgressBar.stop()
        self.ExcelThread.quit()
        self.LogsLabel.setText('エラー発生ログを保存しました(%s) %s' % (self.logFileName, errorString))
        t = MessageDialog('異常です', errorString, self)
        t.exec()

    def ExcelComplete(self):
        self.RunButton.setEnabled(True)
        self.FolderButton.setEnabled(True)
        self.TargetButton.setEnabled(True)
        self.ExitButton.setEnabled(True)
        self.IndeterminateProgressBar.stop()
        self.ExcelThread.quit()
        self.LogsLabel.setText('実行完了ログを保存しました(%s)' % self.logFileName)
        t = MessageDialog('完成です', '実行完了です', self)
        t.exec()

    def ExcelInfo(self, info):
        self.LogsLabel.setText(info)

    def ExitB(self):
        self.ExcelThread.quit()
        self.ExcelThread.wait()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
