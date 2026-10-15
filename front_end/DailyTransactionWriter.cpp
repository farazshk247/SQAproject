#include "DailyTransactionWriter.h"

#include <iomanip>

namespace {
std::string userTypeText(UserType type) {
    switch (type) {
        case UserType::AA:
            return "AA";
        case UserType::FS:
            return "FS";
        case UserType::BS:
            return "BS";
        case UserType::SS:
            return "SS";
    }

    return "";
}

void writeMoney(std::ofstream& out, double amount, int width) {
    out << std::right << std::setfill('0') << std::setw(width) << std::fixed
        << std::setprecision(2) << amount << std::setfill(' ');
}
}

bool DailyTransactionWriter::open(std::string path) {
    if (out.is_open()) {
        out.close();
    }

    out.open(path, std::ios::out | std::ios::trunc);
    return out.is_open();
}

void DailyTransactionWriter::writeSessionEnd(User user) {
    (void)user;
    out << "00" << std::string(20, ' ') << "000000000\n";
}

void DailyTransactionWriter::writeCreate(User user) {
    out << "01 " << std::left << std::setw(15) << user.getUsername() << ' '
        << userTypeText(user.getType()) << ' ';
    writeMoney(out, user.getCredit(), 9);
    out << '\n';
}

void DailyTransactionWriter::writeDelete(User user) {
    out << "02 " << std::left << std::setw(18) << user.getUsername()
        << " 000000000\n";
}

void DailyTransactionWriter::writeSell(Game game) {
    out << "03 " << std::left << std::setw(25) << game.getName() << ' '
        << std::setw(15) << game.getSeller() << ' ';
    writeMoney(out, game.getPrice(), 6);
    out << '\n';
}

void DailyTransactionWriter::writeBuy(Game game, std::string buyer) {
    out << "04 " << std::left << std::setw(25) << game.getName() << ' '
        << std::setw(15) << game.getSeller() << ' ' << std::setw(15) << buyer
        << ' ';
    writeMoney(out, game.getPrice(), 6);
    out << '\n';
}

void DailyTransactionWriter::writeRefund(
    std::string buyer, std::string seller, double amount) {
    out << "05 " << std::left << std::setw(15) << buyer << ' '
        << std::setw(15) << seller << ' ';
    writeMoney(out, amount, 9);
    out << '\n';
}

void DailyTransactionWriter::writeAddCredit(User user) {
    out << "06 " << std::left << std::setw(18) << user.getUsername() << ' ';
    writeMoney(out, user.getCredit(), 9);
    out << '\n';
}

void DailyTransactionWriter::close() {
    if (out.is_open()) {
        out.close();
    }
}
