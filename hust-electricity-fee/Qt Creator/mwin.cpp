#include "mwin.h"
#include "ui_mwin.h"

MWin::MWin(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MWin)
{
    ui->setupUi(this);
    /*
    QLabel * locationLabel_ = new QLabel("July");
    //locationLabel_ = new QLabel;
    locationLabel_->setAlignment(Qt::AlignCenter);  //水平居中(HCenter)。
    //locationLabel->setMinimumSize(200,15);   //设置控件最小尺度
    locationLabel_->setMinimumSize(locationLabel_->sizeHint());

    QLabel *aixLabel_ = new QLabel("\"CTRL + H\" for help");
    //Optional
    //statusBar()->setStyleSheet(QString("QStatusBar::item{border: 0px}")); // 设置不显示label的边框
//    statusBar()->setSizeGripEnabled(false); //设置是否显示右边的大小控制点

    statusBar()->addWidget(locationLabel_);
    statusBar()->addWidget(aixLabel_, 1);

    QLabel *per1 = new QLabel("Ready1", this);
    QLabel *per2 = new QLabel("Ready2", this);
    QLabel *per3 = new QLabel("Ready3", this);
    statusBar()->addPermanentWidget(per1); //现实永久信息
    statusBar()->addPermanentWidget(per2);
    statusBar()->insertPermanentWidget(2, per3);
    statusBar()->showMessage("Status is here...", 3000); // 显示临时信息，时间3秒钟.
    */
}

MWin::~MWin()
{
    delete ui;
}
