#include "mwin.h"
#include "ui_mwin.h"

MWin::MWin(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MWin)
{
    ui->setupUi(this);
}

MWin::~MWin()
{
    delete ui;
}

void MWin::on_duration_check_stateChanged(int arg1)
{

}
