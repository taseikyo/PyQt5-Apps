#ifndef MWIN_H
#define MWIN_H

#include <QMainWindow>

namespace Ui {
class MWin;
}

class MWin : public QMainWindow
{
    Q_OBJECT

public:
    explicit MWin(QWidget *parent = nullptr);
    ~MWin();

private:
    Ui::MWin *ui;
};

#endif // MWIN_H
