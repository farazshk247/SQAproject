#include "DeleteTransaction.h"

DeleteTransaction::DeleteTransaction() {
    code = "02";
}

bool DeleteTransaction::execute(FrontEndContext& ctx) {
    if (!requireAdmin(ctx)) {
        return false;
    }

    std::string username;
    if (!ctx.console.readLine(username) || !validateTarget(ctx, username)) {
        return false;
    }

    bool hadAvailableGames = false;
    for (Game& game : ctx.games.getAvailable()) {
        if (game.getSeller() == username) {
            hadAvailableGames = true;
            break;
        }
    }

    User deletedUser = *ctx.accounts.findUser(username);
    const std::string currentUsername =
        ctx.session.getCurrentUser()->getUsername();
    const double sessionCredit = ctx.session.getSessionCredit();
    ctx.accounts.removeUser(username);
    ctx.session.logout();
    ctx.session.login(ctx.accounts.findUser(currentUsername));
    ctx.session.addSessionCredit(sessionCredit);
    cancelInventory(ctx, username);
    ctx.writer.writeDelete(deletedUser);

    std::string message = "User '" + username + "' deleted successfully.";
    if (hadAvailableGames) {
        message += " Associated games for sale removed.";
    }
    ctx.console.showMessage(message);
    return true;
}

bool DeleteTransaction::validateTarget(
    FrontEndContext& ctx, std::string username) {
    if (!ctx.accounts.userExists(username)) {
        ctx.console.showError("user '" + username + "' does not exist.");
        return false;
    }

    if (ctx.session.getCurrentUser()->getUsername() == username) {
        ctx.console.showError("cannot delete the currently logged in user.");
        return false;
    }

    return true;
}

void DeleteTransaction::cancelInventory(
    FrontEndContext& ctx, std::string seller) {
    ctx.games.removeBySeller(seller);
}
