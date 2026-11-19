#include "SellTransaction.h"

#include <iomanip>
#include <sstream>

#include "InputValidator.h"

namespace {
std::string formatMoney(double amount) {
    std::ostringstream output;
    output << std::fixed << std::setprecision(2) << amount;
    return output.str();
}
}

SellTransaction::SellTransaction() {
    code = "03";
}

bool SellTransaction::execute(FrontEndContext& ctx) {
    if (!requireLogin(ctx)) {
        return false;
    }

    std::string gameName;
    std::string priceText;
    if (!ctx.console.readLine(gameName) || !ctx.console.readLine(priceText)) {
        return false;
    }

    if (!ctx.session.canSell()) {
        ctx.console.showError("insufficient privileges for 'sell'.");
        return false;
    }

    double price = 0.0;
    if (!InputValidator::parseNumber(priceText, price)) {
        ctx.console.showError("'" + priceText + "' is not a valid price.");
        return false;
    }

    if (!validateListing(ctx, gameName, price)) {
        return false;
    }

    Game game(
        gameName, ctx.session.getCurrentUser()->getUsername(), price);
    ctx.games.addPending(game);
    ctx.writer.writeSell(game);
    ctx.console.showMessage(
        "Game '" + gameName + "' listed for sale at $" +
        formatMoney(price) + ".");
    return true;
}

bool SellTransaction::validateListing(
    FrontEndContext& ctx, std::string name, double price) {
    if (!InputValidator::isValidGameName(name)) {
        if (name.size() > 25) {
            ctx.console.showError("game name exceeds 25 characters.");
        } else {
            ctx.console.showError("invalid game name.");
        }
        return false;
    }

    if (!InputValidator::isValidPrice(price)) {
        if (price > 999.99) {
            ctx.console.showError("price exceeds maximum of $999.99.");
        } else {
            ctx.console.showError("invalid price.");
        }
        return false;
    }

    if (ctx.games.nameInUse(name)) {
        ctx.console.showError("game '" + name + "' already exists.");
        return false;
    }

    return true;
}
