#include "RefundTransaction.h"

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

RefundTransaction::RefundTransaction() {
    code = "05";
}

bool RefundTransaction::execute(FrontEndContext& ctx) {
    if (!requireLogin(ctx)) {
        return false;
    }

    std::string buyerUsername;
    std::string sellerUsername;
    std::string amountText;
    if (!ctx.console.readLine(buyerUsername) ||
        !ctx.console.readLine(sellerUsername) ||
        !ctx.console.readLine(amountText)) {
        return false;
    }

    if (!requireAdmin(ctx)) {
        return false;
    }

    double amount = 0.0;
    if (!InputValidator::parseNumber(amountText, amount)) {
        ctx.console.showError(
            "'" + amountText + "' is not a valid refund amount.");
        return false;
    }

    if (!validateRefund(ctx, buyerUsername, sellerUsername, amount)) {
        return false;
    }

    User* buyer = ctx.accounts.findUser(buyerUsername);
    User* seller = ctx.accounts.findUser(sellerUsername);
    seller->deductCredit(amount);
    buyer->addCredit(amount);
    ctx.writer.writeRefund(buyerUsername, sellerUsername, amount);
    ctx.console.showMessage(
        "Refund of $" + formatMoney(amount) + " processed from " +
        sellerUsername + " to " + buyerUsername + ".");
    return true;
}

bool RefundTransaction::validateRefund(
    FrontEndContext& ctx, std::string buyer, std::string seller,
    double amount) {
    User* buyerAccount = ctx.accounts.findUser(buyer);
    if (buyerAccount == nullptr) {
        ctx.console.showError("buyer '" + buyer + "' does not exist.");
        return false;
    }

    User* sellerAccount = ctx.accounts.findUser(seller);
    if (sellerAccount == nullptr) {
        ctx.console.showError("seller '" + seller + "' does not exist.");
        return false;
    }

    if (!InputValidator::isValidCreditAmount(amount)) {
        ctx.console.showError("invalid refund amount.");
        return false;
    }

    if (sellerAccount->getCredit() < amount) {
        ctx.console.showError(
            "seller '" + seller + "' has insufficient credit.");
        return false;
    }

    return true;
}
