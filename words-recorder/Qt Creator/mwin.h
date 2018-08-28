#ifndef MWIN_H
#define MWIN_H

#include <QMainWindow>
#include <QFile>
namespace Ui {
class MWin;
}

class MWin : public QMainWindow
{
    Q_OBJECT

public:
    explicit MWin(QWidget *parent = 0);
    ~MWin();

private:
    Ui::MWin *ui;
};

#endif // MWIN_H
