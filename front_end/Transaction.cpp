#include "Transaction.h"

namespace {
std::string adminCommandName(const std::string& code) {
    if (code == "01") {
        return "create";
    }
    if (code == "02") {
        return "delete";
    }
    if (code == "05") {
        return "refund";
    }
    if (code == "listaccounts") {
        return "listaccounts";
    }

    return "";
}
}

std::string Transaction::getCode() {
    return code;
}

bool Transaction::requireLogin(FrontEndContext& ctx) {
    if (!ctx.session.isLoggedIn()) {
        ctx.console.showError("you must login before any other transaction.");
        return false;
    }

    return true;
}

bool Transaction::requireAdmin(FrontEndContext& ctx) {
    if (!requireLogin(ctx)) {
        return false;
    }

    if (!ctx.session.isAdmin()) {
        const std::string command = adminCommandName(code);
        if (command.empty()) {
            ctx.console.showError("insufficient privileges.");
        } else {
            ctx.console.showError(
                "insufficient privileges for '" + command + "'.");
        }
        return false;
    }

    return true;
}
