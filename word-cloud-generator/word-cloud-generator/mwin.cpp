#include "mwin.h"
#include "ui_mwin.h"

MWin::MWin(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MWin)
{
    ui->setupUi(this);
    ui->groupBox_4->setHidden(true);
}

MWin::~MWin()
{
    delete ui;
}
