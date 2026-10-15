#include "LoginTransaction.h"

namespace {
std::string userTypeName(UserType type) {
    switch (type) {
        case UserType::AA:
            return "admin";
        case UserType::FS:
            return "full-standard";
        case UserType::BS:
            return "buy-standard";
        case UserType::SS:
            return "sell-standard";
    }

    return "";
}
}

LoginTransaction::LoginTransaction() {
    code = "";
}

bool LoginTransaction::execute(FrontEndContext& ctx) {
    if (ctx.session.isLoggedIn()) {
        ctx.console.showError("already logged in. Login ignored.");
        return false;
    }

    ctx.console.prompt("Username: ");

    std::string username;
    if (!ctx.console.readLine(username)) {
        ctx.console.showError("invalid username. Login failed.");
        return false;
    }

    User* user = ctx.accounts.findUser(username);
    if (user == nullptr || !ctx.session.login(user)) {
        ctx.console.showError("invalid username. Login failed.");
        return false;
    }

    ctx.console.showMessage(
        "Login successful. Welcome " + user->getUsername() + " (" +
        userTypeName(user->getType()) + ").");
    return true;
}
