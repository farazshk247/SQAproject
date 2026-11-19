#include "Session.h"

bool Session::login(User* user) {
    if (loggedIn || user == nullptr) {
        return false;
    }

    currentUser = user;
    loggedIn = true;
    creditAddedThisSession = 0.0;
    return true;
}

bool Session::logout() {
    if (!loggedIn) {
        return false;
    }

    currentUser = nullptr;
    loggedIn = false;
    creditAddedThisSession = 0.0;
    return true;
}

bool Session::isLoggedIn() {
    return loggedIn;
}

User* Session::getCurrentUser() {
    return currentUser;
}

bool Session::isAdmin() {
    return loggedIn && currentUser->isAdmin();
}

bool Session::canSell() {
    return loggedIn && currentUser->canSell();
}

bool Session::canBuy() {
    return loggedIn && currentUser->canBuy();
}

bool Session::addSessionCredit(double amount) {
    if (!loggedIn || amount < 0.0 || creditAddedThisSession + amount > 1000.0) {
        return false;
    }

    creditAddedThisSession += amount;
    return true;
}

double Session::getSessionCredit() {
    return creditAddedThisSession;
}
