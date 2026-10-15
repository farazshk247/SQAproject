#pragma once

#include <fstream>
#include <string>

#include "Game.h"
#include "User.h"

class DailyTransactionWriter {
private:
    std::ofstream out;

public:
    bool open(std::string path);
    void writeSessionEnd(User user);
    void writeCreate(User user);
    void writeDelete(User user);
    void writeSell(Game game);
    void writeBuy(Game game, std::string buyer);
    void writeRefund(std::string buyer, std::string seller, double amount);
    void writeAddCredit(User user);
    void close();
};
