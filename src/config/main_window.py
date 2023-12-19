import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout,
                               QWidget, QLabel, QFileDialog, QSizePolicy, QDockWidget, QSpacerItem)
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPixmap, QImage
from ..processing.transform import connectLine

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Image Processing')
        self.setGeometry(100, 100, 1200, 600)  # 设置窗口初始大小

        # 创建停靠窗口，但不设置标题
        self.dockWidget = QDockWidget("", self)
        self.dockWidget.setTitleBarWidget(QWidget())  # 移除标题栏
        self.dockWidget.setFeatures(QDockWidget.NoDockWidgetFeatures)  # 禁用停靠窗口的额外特性
        self.dockWidgetContents = QWidget()
        self.dockLayout = QVBoxLayout(self.dockWidgetContents)


        # 创建按钮并添加到布局中
        self.load_button = QPushButton('Load Image')
        self.search_button = QPushButton('Search Line')
        self.save_button = QPushButton('Save Image')
        self.dockLayout.addWidget(self.load_button)
        self.dockLayout.addWidget(self.search_button)
        self.dockLayout.addWidget(self.save_button)

        self.dockWidgetContents.setLayout(self.dockLayout)
        self.dockWidget.setWidget(self.dockWidgetContents)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget)

        # 按钮连接的函数
        self.load_button.clicked.connect(self.load_image)
        self.search_button.clicked.connect(self.search_line)
        self.save_button.clicked.connect(self.save_image)
        
        # 按钮样式
        button_style = "QPushButton { text-align: center; padding: 5px; margin: 2px; width: 100%}"
        self.load_button.setStyleSheet(button_style)
        self.search_button.setStyleSheet(button_style)
        self.save_button.setStyleSheet(button_style)

        # 按钮布局
        self.load_button.setSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self.search_button.setSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self.save_button.setSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self.dockLayout.addItem(
            QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        
        # 按钮最大高度
        self.load_button.setMaximumHeight(40) 
        self.search_button.setMaximumHeight(40)  
        self.save_button.setMaximumHeight(40) 

        # 设置布局间隔和边距
        self.dockLayout.setSpacing(0)  # 减少按钮间的间隔
        self.dockLayout.setContentsMargins(10,10,10,10)  # 减少布局边缘的空白区域

        # 设置图片显示区域
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.centralLayout = QVBoxLayout(self.centralWidget)
        self.inputImage = QLabel()
        self.centralLayout.addWidget(self.inputImage)
        self.rgbImge = QLabel()
        self.centralLayout.addWidget(self.rgbImge)
        # self.blackImage = QLabel()
        # self.centralLayout.addWidget(self.blackImage)
        

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Load Image')
        if file_name.endswith(('.jpg','.jpeg','.png','.tif','.tiff')):
            self.current_image_path = file_name
            pixmap = QPixmap(file_name)
            self.inputImage.setPixmap(pixmap.scaled(self.inputImage.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def search_line(self):
        if hasattr(self, 'current_image_path'):
            # 调用 transform.py 中的 connectLine 函数处理图片
            bgrImg, blackImg = connectLine(self.current_image_path)
            
            # 将 NumPy 数组转换为 QImage
            height, width, channel = bgrImg.shape
            bytesPerLine = 3 * width
            qImg1 = QImage(bgrImg.data, width, height, bytesPerLine, QImage.Format_BGR888)
            
            # height, width, channel = blackImg.shape
            # bytesPerLine = width
            # qImg2 = QImage(blackImg.data, width, height, bytesPerLine, QImage.Format_BGR888)
            
            # 将 QImage 转换为 QPixmap 并显示在 QLabel 中
            pixmap1 = QPixmap.fromImage(qImg1)
            # pixmap2 = QPixmap.fromImage(qImg2)
            
            self.rgbImge.setPixmap(pixmap1.scaled(self.rgbImge.size(), Qt.KeepAspectRatio))
            # self.blackImage.setPixmap(pixmap2.scaled(self.blackImage.size(), Qt.KeepAspectRatio))

    def save_image(self):
        if hasattr(self, 'current_image_path'):
            file_name, _ = QFileDialog.getSaveFileName(self, 'Save Image')
            if file_name:
                # 这里保存处理后的图片
                pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
