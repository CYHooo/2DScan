# 2DScan

- 这个库是用来画出通过雷达扫描后二维图的外轮廓线。

---

## <input type='checkbox' checked> TODO

 - <input type='checkbox' disabled> v1.1正在开发增加可视化窗口交互功能

---

## Package

 - `python` == 3.10.0
 - `numpy` == 1.26.2
 - `pillow` == 10.1.0
 - `scikit-image` == 0.22.0
 - `matplotlib` == 3.8.2
 - `opencv-python` == 4.8.1.78
 - `pyside6` == 6.6.1
---

## Usage

 - 运行`src/transform.py`即可。按照需要更改图片路径和保存路径。
    
    - 代码中有`crop`和`debug`两个选项 (默认为`False`不保存):
        
        `crop`：用来保存裁剪后的图片(按照图片中物体的最大外接矩形保存)

        `debug`：用来保存调试中的图片(傅里叶变换中的频谱图片，最大外接矩形，摆正后的图片，物体平移到中心的图片)。
        
        

 - `src/imgReader.py`是用来获取骨架线(`skeleton`)的代码。只做简单调试并不是主代码。

---

## Result
<div style="display: flex; justify-content: center; align-items: center; gap: 5px;">
  <div style="text-align: center;">
    <p>Original</p>
    <img src="/img/img2.jpg" alt="Original Image" style="width: 400px;">
  </div>
  <div style="text-align: center;">
    <p>MergeLine</p>
    <img src="/result/mergeLine.png" alt="MergeLine Image" style="width: 400px;">
  </div>
  <div style="text-align: center;">
    <p>OutLine</p>
    <img src="/result/outLine.png" alt="OutLine Image" style="width: 400px;">
  </div>
</div>