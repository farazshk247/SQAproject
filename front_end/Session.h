#pragma once

#include "User.h"

class Session {
private:
    User* currentUser = nullptr;
    bool loggedIn = false;
    double creditAddedThisSession = 0.0;

public:
    bool login(User* user);
    bool logout();
    bool isLoggedIn();
    User* getCurrentUser();
    bool isAdmin();
    bool canSell();
    bool canBuy();
    bool addSessionCredit(double amount);
    double getSessionCredit();
};
