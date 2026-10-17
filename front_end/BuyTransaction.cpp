#include "BuyTransaction.h"

#include <iomanip>
#include <sstream>

namespace {
std::string formatMoney(double amount) {
    std::ostringstream output;
    output << std::fixed << std::setprecision(2) << amount;
    return output.str();
}
}

BuyTransaction::BuyTransaction() {
    code = "04";
}

bool BuyTransaction::execute(FrontEndContext& ctx) {
    if (!requireLogin(ctx)) {
        return false;
    }

    std::string gameName;
    std::string sellerUsername;
    if (!ctx.console.readLine(gameName) ||
        !ctx.console.readLine(sellerUsername)) {
        return false;
    }

    if (!ctx.session.canBuy()) {
        ctx.console.showError("insufficient privileges for 'buy'.");
        return false;
    }

    if (!validatePurchase(ctx, gameName)) {
        return false;
    }

    Game* game = ctx.games.findAvailable(gameName);
    if (game->getSeller() != sellerUsername) {
        ctx.console.showError(
            "game '" + gameName + "' is not sold by '" +
            sellerUsername + "'.");
        return false;
    }

    User* seller = ctx.accounts.findUser(sellerUsername);
    if (seller == nullptr) {
        ctx.console.showError(
            "seller '" + sellerUsername + "' does not exist.");
        return false;
    }

    User* buyer = ctx.session.getCurrentUser();
    if (!buyer->deductCredit(game->getPrice())) {
        return false;
    }

    seller->addCredit(game->getPrice());
    ctx.collection.addEntry(buyer->getUsername(), gameName);
    ctx.writer.writeBuy(*game, buyer->getUsername());
    ctx.console.showMessage(
        "Purchased '" + gameName + "' from " + sellerUsername +
        " for $" + formatMoney(game->getPrice()) + ".");
    return true;
}

bool BuyTransaction::validatePurchase(
    FrontEndContext& ctx, std::string gameName) {
    Game* game = ctx.games.findAvailable(gameName);
    if (game == nullptr) {
        if (ctx.games.nameInUse(gameName)) {
            ctx.console.showError(
                "game '" + gameName +
                "' is not available until the next session.");
        } else {
            ctx.console.showError("game '" + gameName + "' does not exist.");
        }
        return false;
    }

    User* buyer = ctx.session.getCurrentUser();
    if (ctx.collection.ownsGame(buyer->getUsername(), gameName)) {
        ctx.console.showError("you already own '" + gameName + "'.");
        return false;
    }

    if (buyer->getCredit() < game->getPrice()) {
        ctx.console.showError(
            "insufficient credit to purchase '" + gameName + "' ($" +
            formatMoney(game->getPrice()) + ").");
        return false;
    }

    return true;
}
