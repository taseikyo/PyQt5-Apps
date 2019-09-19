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

private slots:
    void on_duration_check_stateChanged(int arg1);

private:
    Ui::MWin *ui;
};

#endif // MWIN_H
