#include "LogoutTransaction.h"

LogoutTransaction::LogoutTransaction() {
    code = "00";
}

bool LogoutTransaction::execute(FrontEndContext& ctx) {
    if (!ctx.session.isLoggedIn()) {
        ctx.console.showError("not logged in. Logout ignored.");
        return false;
    }

    User* currentUser = ctx.session.getCurrentUser();
    ctx.writer.writeSessionEnd(*currentUser);
    ctx.games.commitPending();
    ctx.session.logout();
    ctx.console.showMessage("Logged out. Daily transaction file written.");
    return true;
}
