#include "Console.h"

#include <iomanip>
#include <iostream>

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
}

bool Console::readLine(std::string& line) {
    return static_cast<bool>(std::getline(std::cin, line));
}

void Console::prompt(std::string message) {
    std::cout << message << '\n';
}

void Console::showMessage(std::string message) {
    std::cout << message << '\n';
}

void Console::showError(std::string message) {
    std::cout << "Error: " << message << '\n';
}

void Console::showGameList(std::vector<Game> games) {
    if (games.empty()) {
        showMessage("No games currently available for sale.");
        return;
    }

    showMessage("Available games:");
    for (Game& game : games) {
        std::cout << "  " << game.getName() << " - " << game.getSeller()
                  << " - $" << std::fixed << std::setprecision(2)
                  << game.getPrice() << '\n';
    }
}

void Console::showAccountList(std::vector<User> users) {
    showMessage("Active accounts:");
    for (User& user : users) {
        std::cout << "  " << user.getUsername() << " - "
                  << userTypeText(user.getType()) << " - $" << std::fixed
                  << std::setprecision(2) << user.getCredit() << '\n';
    }
}
