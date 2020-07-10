#ifndef MWIN_H
#define MWIN_H

#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui { class MWin; }
QT_END_NAMESPACE

class MWin : public QMainWindow
{
    Q_OBJECT

public:
    MWin(QWidget *parent = nullptr);
    ~MWin();

private:
    Ui::MWin *ui;
};
#endif // MWIN_H
