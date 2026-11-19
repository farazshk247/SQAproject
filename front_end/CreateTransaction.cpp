#include "CreateTransaction.h"

#include "InputValidator.h"

namespace {
UserType parseUserType(const std::string& type) {
    if (type == "FS") {
        return UserType::FS;
    }
    if (type == "BS") {
        return UserType::BS;
    }
    if (type == "SS") {
        return UserType::SS;
    }

    return UserType::AA;
}
}

CreateTransaction::CreateTransaction() {
    code = "01";
}

bool CreateTransaction::execute(FrontEndContext& ctx) {
    if (!requireAdmin(ctx)) {
        return false;
    }

    std::string username;
    std::string type;
    if (!ctx.console.readLine(username) || !ctx.console.readLine(type)) {
        return false;
    }

    if (!validateNewUser(ctx, username, type)) {
        return false;
    }

    User user(username, parseUserType(type), 0.0);
    const std::string currentUsername =
        ctx.session.getCurrentUser()->getUsername();
    const double sessionCredit = ctx.session.getSessionCredit();
    ctx.accounts.addUser(user);
    ctx.session.logout();
    ctx.session.login(ctx.accounts.findUser(currentUsername));
    ctx.session.addSessionCredit(sessionCredit);
    ctx.writer.writeCreate(user);
    ctx.console.showMessage("User '" + username + "' created successfully.");
    return true;
}

bool CreateTransaction::validateNewUser(
    FrontEndContext& ctx, std::string username, std::string type) {
    if (ctx.accounts.userExists(username)) {
        ctx.console.showError("username '" + username + "' already exists.");
        return false;
    }

    if (!InputValidator::isValidUsername(username)) {
        if (username.size() > 15) {
            ctx.console.showError("username exceeds 15 characters.");
        } else {
            ctx.console.showError("invalid username.");
        }
        return false;
    }

    if (!InputValidator::isValidUserType(type)) {
        ctx.console.showError("invalid user type '" + type + "'.");
        return false;
    }

    return true;
}
