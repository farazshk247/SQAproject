#include "ListGamesTransaction.h"

ListGamesTransaction::ListGamesTransaction() {
    code = "list";
}

bool ListGamesTransaction::execute(FrontEndContext& ctx) {
    if (!requireLogin(ctx)) {
        return false;
    }

    ctx.console.showGameList(ctx.games.getAvailable());
    return true;
}
