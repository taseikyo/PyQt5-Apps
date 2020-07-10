#include "mwin.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MWin w;
    w.show();
    return a.exec();
}
