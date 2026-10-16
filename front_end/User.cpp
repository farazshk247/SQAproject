#include "User.h"

User::User(std::string username, UserType type, double credit)
    : username(username), type(type), credit(credit) {
}

std::string User::getUsername() {
    return username;
}

UserType User::getType() {
    return type;
}

double User::getCredit() {
    return credit;
}

void User::addCredit(double amount) {
    credit += amount;
}

bool User::deductCredit(double amount) {
    if (amount < 0.0 || amount > credit) {
        return false;
    }

    credit -= amount;
    return true;
}

bool User::isAdmin() {
    return type == UserType::AA;
}

bool User::canSell() {
    return type == UserType::AA || type == UserType::FS || type == UserType::SS;
}

bool User::canBuy() {
    return type == UserType::AA || type == UserType::FS || type == UserType::BS;
}
