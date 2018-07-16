## Google Translate
Google Translate is a translation app using [Google translate api](https://github.com/ssut/py-googletrans).

### Screenshot
<div align="center">
    <img src="../images/Google-Translate.png" alt="Google Translate English" height="350" />
    <img src="../images/Google-Translate-zh_CN.png" alt="Google Translate English" height="350" />
</div>

### Background
When I read the thesis, I used [Google Translate](https://translate.google.cn) to translate the words and sentences that I could not understand. But every time I had to Ctrl+C, Ctrl+V. Moreover when copying sentences from a PDF, it will bring a additional enter and a strange symbol. It is very troublesome. Then I wonder why I can't make a app to use the Google Translate API to translate directly. I view the Google Translate project on GitHub and suddenly found an [interesting repo](https://github.com/ssut/py-googletrans).

### Feature
1. Enter the translation manually. Enter the English you want to translate in the 'original' input field, then click the `translate` button, or use the shortcut Ctrl+Enter
2. paper model. To use the paper mode, you need to check the real-time translation. My real-time translation here is to monitor the clipboard, then translate the copied text into Chinese, and automatically replace the additional enter and multiple spaces with a space in the paper mode, and remove one special symbol ``
3. window top. Checking this box will cause the window to remain at the top of all applications.

### illustration
1. regular mode
<div align="center">
    <img src="../images/Google-Translate-1.gif" alt="regular mode">
</div>

2. paper mode
<div align="center">
    <img src="../images/Google-Translate-2.gif" alt="paper mode">
</div>

3. non paper mode
<div align="center">
    <img src="../images/Google-Translate-3.gif" alt="non paper mode">
</div>

### Installation
```
>> git clone https://github.com/LewisTian/GoogleTranslateApp.git
>> cd GoogleTranslateApp
>> pip install -r requirement.txt
>> python main.py
```

### Download
[click me to download](https://github.com/LewisTian/PyQt5-Tools/releases)

### References
- https://github.com/ssut/py-googletrans
-  https://blog.csdn.net/killua_hzl/article/details/5288769

### License
GNU General Public License v3.0 License
