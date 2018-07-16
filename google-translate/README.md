## Google Translate
Google Translate App using PyQt5.

### 截图
<div align="center">
    <img src="images/img-1.png" alt="Screenshot">
</div>

### 背景
在我看论文的时候遇到看不懂的词、句子都是用 [谷歌翻译](https://translate.google.cn) ，然而每次都要 Ctrl+C，Ctrl+V，还有看 PDF 的时候复制会自带回车还有奇怪的符号，就很麻烦，然后想着为什么不能自己做个小应用使用谷歌翻译的 API 来直接翻译呢？在 Gayhub 上看了下关于谷歌翻译的项目，突然发现了一个 [有趣的项目](https://github.com/ssut/py-googletrans) ，然后就有了这个项目，主要是将英语翻译成中文。

### 功能介绍
1. 手动输入翻译。在原文对应的文本框中输入想要翻译的英文，然后点击 `翻译` 按钮，或者使用快捷键 Ctrl+Enter 
2. 论文模式。使用论文模式需要勾选实时翻译，我这里的实时翻译是监控剪贴板，然后将复制的文字翻译成中文，并且在论文模式下会自动将回车和多个空格替换为一个空格，以及去掉一个特殊的符号 `` 
3. 窗口总在前面。勾选此选框会导致窗口一直处于所有应用的最前面。

### 演示
1. 普通模式
<div align="center">
    <img src="images/img-2.gif" alt="普通模式">
</div>

2. 论文模式
<div align="center">
    <img src="images/img-3.gif" alt="论文模式">
</div>

3. 非论文模式
<div align="center">
    <img src="images/img-4.gif" alt="非论文模式">
</div>

### 安装说明
```
>> git clone https://github.com/LewisTian/GoogleTranslateApp.git
>> cd GoogleTranslateApp
>> pip install -r requirement.txt
>> python main.py
```

### 解压使用
除了上面的代码安装，这里提供了一个打包好的压缩包 ，下载解压即可使用，[点我下载](https://github.com/LewisTian/GoogleTranslateApp/releases)

### 参考
- https://github.com/ssut/py-googletrans
-  https://blog.csdn.net/killua_hzl/article/details/5288769

### License
GoogleTranslateApp is licensed under the [GNU General Public License v3.0 License](LICENSE).
本项目仅供学习交流和私人使用，禁止用作商业用途。
