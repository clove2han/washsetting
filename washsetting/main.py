# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication

from t_widget import Ui_MainWindow
import MySQLdb
from pkgutil import get_data


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
        
        self.read_setting_pushButton.clicked.connect(self.on_read_setting_pushButton_clicked)
        self.write_setting_pushButton.clicked.connect(self.on_write_setting_pushButton_clicked)
        self.init_pushButton.clicked.connect(self.initdb)
        
        
        self.textBrowser.append('''
        洗车机型：
        竹美： ZhuMeiX
        日森： RiSense
        德加福：DeJiaFu
        雅宝：washingYB
        --------------------
        洗车模式：        
        泡沫清洗： %01#WCCR0141014201200000**
        镀膜清洗： %01#WCCR0141014201000000**
        ''')
    # 打开数据库连接   
    def connect_database(self):
        db = MySQLdb.connect(HOST,DATABASE_USER,DATABASE_PASSWORD,DATABASE_DB,charset='utf8')
        print('database connected')
        return db
    
    def initdb(self):
        con = self.connect_database()
        cur = con.cursor()
#         sql = "select id from wc_equipment;"
#         res = self.get_data(sql)
#         for re in res:
#             if re[0] =='682':
#                 self.msg_label.setText("数据库已初始化！")
#             else:
        try:
            # 执行SQL语句
            cur.execute("insert into wc_equipment (id,code,status,site_id,site_code,eq_type,ip,port) values('682','gateOut',0,'dgBJCH','dgBJCH',2,'192.168.10.18',20108);")
            # 查询到站点编码 
            con.commit()
            self.msg_label.setText("提示信息：数据库初始化成功")
        except:
            print("Error: initdb failed")
            self.msg_label.setText("提示信息：数据库已初始化")
    
    def get_data(self,sql):
        con = self.connect_database()
        cursor = con.cursor()
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 查询到站点编码 
            results = cursor.fetchall()
            return results
        except:
            print("Error: get data failed")
        
    
    def set_data(self,sql):
        con = self.connect_database()
        cur = con.cursor()
        try:
            # 执行SQL语句
            cur.execute(sql)
            # 查询到站点编码 
            con.commit()
        except:
            print("Error: set data failed")

    # 关闭数据库连接
    def close_database(self,db):
        db.close()
        
    #获取站点编码    
    @pyqtSlot()     
    def get_wc_param(self):
        sql = "select id,value from wc_sysparam;"
        res = self.get_data(sql)
        return res
    
    #设置站点编码
    @pyqtSlot()
    def set_wc_param(self,param,id):
        sql = "update wc_sysparam set value='"+param+"' where id = '"+str(id)+"';"
        self.set_data(sql)
        
        
    #获取站点编码    
    @pyqtSlot()     
    def get_equipment(self):
        sql = "select id,status,site_id,site_code,ip,port from wc_equipment"
        res = self.get_data(sql)
        return res
    
    #设置站点编码
    @pyqtSlot()
    def set_equipment(self,sql):
        self.set_data(sql)

    @pyqtSlot()        
    def on_read_setting_pushButton_clicked(self):
        wc_param = self.get_wc_param()
        #给文本框赋值
        self.province_lineEdit.setText(wc_param[0][1])
        self.city_lineEdit.setText(wc_param[1][1])
        self.site_id_lineEdit.setText(wc_param[2][1])
        self.wash_type_lineEdit.setText(wc_param[3][1])
        self.wash_mode_lineEdit.setText(wc_param[4][1])     
        
        wc_equipment = self.get_equipment()
        self.ssh_port_lineEdit.setText(wc_equipment[0][2]) 
        
        for i in range(10):
            #闸门LED
            if wc_equipment[i][0] == '122':
                #是否有效
                print(wc_equipment[i][1])
                if wc_equipment[i][1] == 0:
                    self.doorled_checkBox.setChecked(True)
                elif wc_equipment[i][1] == 1:
                    self.doorled_checkBox.setChecked(False)
                self.doorled_ip_lineEdit.setText(wc_equipment[i][4])   
                self.doorled_port_lineEdit.setText(str(wc_equipment[i][5]))
            elif wc_equipment[i][0] == '123':
                #是否有效
                print(wc_equipment[i][1])
                if wc_equipment[i][1] == 0:
                    self.washing_checkBox.setChecked(True)
                elif wc_equipment[i][1] == 1:
                    self.washing_checkBox.setChecked(False)
                self.washing_ip_lineEdit.setText(wc_equipment[i][4])   
                self.washing_port_lineEdit.setText(str(wc_equipment[i][5]))
            elif wc_equipment[i][0] == '234':
                #是否有效
                print(wc_equipment[i][1])
                if wc_equipment[i][1] == 0:
                    self.gatein_checkBox.setChecked(True)
                elif wc_equipment[i][1] == 1:
                    self.gatein_checkBox.setChecked(False)
                self.gatein_ip_lineEdit.setText(wc_equipment[i][4])   
                self.gatein_port_lineEdit.setText(str(wc_equipment[i][5]))
            elif wc_equipment[i][0] == '345':
                #是否有效
                print(wc_equipment[i][1])
                if wc_equipment[i][1] == 0:
                    self.camerazs_checkBox.setChecked(True)
                elif wc_equipment[i][1] == 1:
                    self.camerazs_checkBox.setChecked(False)
                self.camerazs_ip_lineEdit.setText(wc_equipment[i][4])   
                self.camerazs_port_lineEdit.setText(str(wc_equipment[i][5]))
            elif wc_equipment[i][0] == '456':
                #是否有效
                print(wc_equipment[i][1])
                if wc_equipment[i][1] == 0:
                    self.cameraled_checkBox.setChecked(True)
                elif wc_equipment[i][1] == 1:
                    self.cameraled_checkBox.setChecked(False)
                self.cameraled_ip_lineEdit.setText(wc_equipment[i][4])   
                self.cameraled_port_lineEdit.setText(str(wc_equipment[i][5]))
                
            elif wc_equipment[i][0] == '678':
                #是否有效
                print(wc_equipment[i][1])
                if wc_equipment[i][1] == 0:
                    self.gs_checkBox.setChecked(True)
                elif wc_equipment[i][1] == 1:
                    self.gs_checkBox.setChecked(False)
                self.gs_ip_lineEdit.setText(wc_equipment[i][4])   
                self.gs_port_lineEdit.setText(str(wc_equipment[i][5]))
            elif wc_equipment[i][0] == '679':
                #是否有效
                print(wc_equipment[i][1])
                if wc_equipment[i][1] == 0:
                    self.wpc_checkBox.setChecked(True)
                elif wc_equipment[i][1] == 1:
                    self.wpc_checkBox.setChecked(False)
                self.wpc_ip_lineEdit.setText(wc_equipment[i][4])   
                self.wpc_port_lineEdit.setText(str(wc_equipment[i][5]))
            elif wc_equipment[i][0] == '680':
                #是否有效
                print(wc_equipment[i][1])
                if wc_equipment[i][1] == 0:
                    self.doorin_checkBox.setChecked(True)
                elif wc_equipment[i][1] == 1:
                    self.doorin_checkBox.setChecked(False)
                self.doorin_ip_lineEdit.setText(wc_equipment[i][4])   
                self.doorin_port_lineEdit.setText(str(wc_equipment[i][5]))
                
            elif wc_equipment[i][0] == '681':
                #是否有效
                print(wc_equipment[i][1])
                if wc_equipment[i][1] == 0:
                    self.doorout_checkBox.setChecked(True)
                elif wc_equipment[i][1] == 1:
                    self.doorout_checkBox.setChecked(False)
                self.doorout_ip_lineEdit.setText(wc_equipment[i][4])   
                self.doorout_port_lineEdit.setText(str(wc_equipment[i][5]))
            elif wc_equipment[i][0] == '682':
                #是否有效
                print(wc_equipment[i][1])
                if wc_equipment[i][1] == 0:
                    self.gateout_checkBox.setChecked(True)
                elif wc_equipment[i][1] == 1:
                    self.gateout_checkBox.setChecked(False)
                self.gateout_ip_lineEdit.setText(wc_equipment[i][4])   
                self.gateout_port_lineEdit.setText(str(wc_equipment[i][5]))
                
                
                
        self.msg_label.setText('提示信息：读取配置成功')
        
    @pyqtSlot()
    def on_write_setting_pushButton_clicked(self):
        province = self.province_lineEdit.text()
        city = self.city_lineEdit.text()
        site_code = self.site_id_lineEdit.text()
        wash_type = self.wash_type_lineEdit.text()
        wash_mode = self.wash_mode_lineEdit.text()
        wc_param=(province,city,site_code,wash_type,wash_mode)
        
        sshport = self.ssh_port_lineEdit.text()
        self.set_equipment("update wc_equipment set site_id='"+sshport+"';")
        self.set_equipment("update wc_equipment set site_code='"+site_code+"';")
        print(wc_param)
        for i in range(0,5):
            if wc_param[i]=="washingYB":
                self.set_wc_param(wc_param[i],i+1)
                self.set_equipment("update wc_equipment set code='washingYB' where id ='123';")
            else:
                self.set_wc_param(wc_param[i],i+1)  
                self.set_equipment("update wc_equipment set code='washingZM2' where id ='123';")
                 
        doorin_status=self.doorin_checkBox.isChecked()
        doorin_ip = self.doorin_ip_lineEdit.text()
        doorin_port= self.doorin_port_lineEdit.text()
        
        if doorin_status == True:
            doorin_status = 0
        else:
            doorin_status = 1
        sql="update wc_equipment set status='"+str(doorin_status)+"',ip='"+doorin_ip+"',port='"+str(doorin_port)+"' where id ='680';"
        self.set_equipment(sql)
        
        doorout_status = self.doorout_checkBox.isChecked()
        doorout_ip = self.doorout_ip_lineEdit.text()
        doorout_port= self.doorout_port_lineEdit.text()
        
        if doorout_status == True:
            doorout_status = 0
        else:
            doorout_status = 1
        sql="update wc_equipment set status='"+str(doorout_status)+"',ip='"+doorout_ip+"',port='"+str(doorout_port)+"' where id ='681';"
        self.set_equipment(sql)
        
        
        
        gatein_status = self.gatein_checkBox.isChecked()
        gatein_ip = self.gatein_ip_lineEdit.text()
        gatein_port= self.gatein_port_lineEdit.text()
        if gatein_status == True:
            gatein_status = 0
        else:
            gatein_status = 1
        sql="update wc_equipment set status='"+str(gatein_status)+"',ip='"+gatein_ip+"',port='"+str(gatein_port)+"' where id ='234';"
        self.set_equipment(sql)
        
        
        gateout_status = self.gateout_checkBox.isChecked()
        gateout_ip = self.gateout_ip_lineEdit.text()
        gateout_port= self.gateout_port_lineEdit.text()
        if gateout_status == True:
            gateout_status = 0
        else:
            gateout_status = 1
        sql="update wc_equipment set status='"+str(gateout_status)+"',ip='"+gateout_ip+"',port='"+str(gateout_port)+"' where id ='682';"
        self.set_equipment(sql)
        
        doorled_status = self.doorled_checkBox.isChecked()
        doorled_ip = self.doorled_ip_lineEdit.text()
        doorled_port= self.doorled_port_lineEdit.text()
        if doorled_status == True:
            doorled_status = 0
        else:
            doorled_status = 1
        sql="update wc_equipment set status='"+str(doorled_status)+"',ip='"+doorled_ip+"',port='"+str(doorled_port)+"' where id ='122';"
        self.set_equipment(sql)
        
        camerazs_status = self.camerazs_checkBox.isChecked()
        camerazs_ip = self.camerazs_ip_lineEdit.text()
        camerazs_port= self.camerazs_port_lineEdit.text()
        if camerazs_status == True:
            camerazs_status = 0
        else:
            camerazs_status = 1
        sql="update wc_equipment set status='"+str(camerazs_status)+"',ip='"+camerazs_ip+"',port='"+str(camerazs_port)+"' where id ='345';"
        self.set_equipment(sql)
        
        cameraled_status = self.cameraled_checkBox.isChecked()
        cameraled_ip = self.cameraled_ip_lineEdit.text()
        cameraled_port= self.cameraled_port_lineEdit.text()
        if cameraled_status == True:
            cameraled_status = 0
        else:
            cameraled_status = 1
        sql="update wc_equipment set status='"+str(cameraled_status)+"',ip='"+cameraled_ip+"',port='"+str(cameraled_port)+"' where id ='456';"
        self.set_equipment(sql)
        
        gs_status = self.gs_checkBox.isChecked()
        gs_ip = self.gs_ip_lineEdit.text()
        gs_port= self.gs_port_lineEdit.text()
        if gs_status == True:
            gs_status = 0
        else:
            gs_status = 1
        sql="update wc_equipment set status='"+str(gs_status)+"',ip='"+gs_ip+"',port='"+str(gs_port)+"' where id ='678';"
        self.set_equipment(sql)
        
        wpc_status = self.wpc_checkBox.isChecked()
        wpc_ip = self.wpc_ip_lineEdit.text()
        wpc_port= self.wpc_port_lineEdit.text()
        if wpc_status == True:
            wpc_status = 0
        else:
            wpc_status = 1
        sql="update wc_equipment set status='"+str(wpc_status)+"',ip='"+wpc_ip+"',port='"+str(wpc_port)+"' where id ='679';"
        self.set_equipment(sql)
        
        gateout_status = self.doorout_checkBox.isChecked()
        gateout_ip = self.doorout_ip_lineEdit.text()
        gateout_port= self.doorout_port_lineEdit.text()
        if gateout_status == True:
            gateout_status = 0
        else:
            gateout_status = 1
        sql="update wc_equipment set status='"+str(gateout_status)+"',ip='"+gateout_ip+"',port='"+str(gateout_port)+"' where id ='682';"
        self.set_equipment(sql)
        
        self.msg_label.setText('提示信息：保存配置成功')
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())