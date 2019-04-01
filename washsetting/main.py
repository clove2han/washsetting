# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication

from t_widget import Ui_MainWindow
import MySQLdb


HOST = '192.168.10.100'
DATABASE_USER = 'mallwash'
DATABASE_PASSWORD='Mallwash.1234'
DATABASE_DB = 'mallwash_agent'

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # 初始化省
        
        self.read_setting_pushButton.clicked.connect(self.on_read_setting_pushButton_clicked)
    @pyqtSlot(int)
    # 取市的键值
    def on_comboBox_activated(self, index):
        print("1231321313123")
        key = self.Province_ComboBox.itemData(index)
        print(key)
        self.City_ComboBox.clear()  # 清空items
        if key:
            self.City_ComboBox.addItem('请选择')
            # 初始化市
            for k, v in area.dictCity[key].items():
                self.City_ComboBox.addItem(v, k)  # 键、值反转

    @pyqtSlot()
    def on_pushButton_clicked(self):
        #获取当前选项框索引
        province_index = self.Province_ComboBox.currentIndex()
        city_index = self.City_ComboBox.currentIndex()
        # 取当前省市县名称
        province_name = self.Province_ComboBox.itemText(province_index)
        city_name = self.City_ComboBox.itemText(city_index)
        print(province_name,city_name)
        
    # 打开数据库连接   
    def connect_database(self):
        db = MySQLdb.connect(HOST,DATABASE_USER,DATABASE_PASSWORD,DATABASE_DB)
        return db
    
    # 关闭数据库连接
    def close_database(self,db):
        db.close()
        
    #获取站点编码    
    @pyqtSlot()     
    def get_sitecode(self):
        con = MainWindow.connect_database(self)
        cursor = con.cursor()
        
        sql = "select value from wc_sysparam where code ='3';"
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 查询到站点编码 
            results = cursor.fetchall()
            return results
        except:
            print("Error: unable to fecth data")
    
    
    #获取远程SSH端口号
    @pyqtSlot()
    def set_sitecode(self,site_code):
        pass
    
    @pyqtSlot()        
    def on_read_setting_pushButton_clicked(self):
        site_id = MainWindow.get_sitecode(self)
        code = site_id[0][0]
        #给文本框赋值
        self.site_id_textEdit.setText(code)
        print("22222222222222222222")
        print(code)
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())