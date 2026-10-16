#pragma once

#include <string>

#include "UserType.h"

class User {
private:
    std::string username;
    UserType type = UserType::AA;
    double credit = 0.0;

public:
    User(std::string username, UserType type, double credit);
    std::string getUsername();
    UserType getType();
    double getCredit();
    void addCredit(double amount);
    bool deductCredit(double amount);
    bool isAdmin();
    bool canSell();
    bool canBuy();
};
