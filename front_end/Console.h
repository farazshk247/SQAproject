#pragma once

#include <string>
#include <vector>

#include "Game.h"
#include "User.h"

class Console {
public:
    bool readLine(std::string& line);
    void prompt(std::string message);
    void showMessage(std::string message);
    void showError(std::string message);
    void showGameList(std::vector<Game> games);
    void showAccountList(std::vector<User> users);
};
