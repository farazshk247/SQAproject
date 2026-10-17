#include "AddCreditTransaction.h"

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

AddCreditTransaction::AddCreditTransaction() {
    code = "06";
}

bool AddCreditTransaction::execute(FrontEndContext& ctx) {
    if (!requireLogin(ctx)) {
        return false;
    }

    std::string amountText;
    if (!ctx.console.readLine(amountText)) {
        return false;
    }

    double amount = 0.0;
    if (!InputValidator::parseNumber(amountText, amount)) {
        ctx.console.showError(
            "'" + amountText + "' is not a valid credit amount.");
        return false;
    }

    std::string targetUsername =
        ctx.session.getCurrentUser()->getUsername();
    if (ctx.session.isAdmin()) {
        if (!ctx.console.readLine(targetUsername)) {
            return false;
        }

        if (!ctx.accounts.userExists(targetUsername)) {
            ctx.console.showError(
                "user '" + targetUsername + "' does not exist.");
            return false;
        }
    }

    if (!validateCredit(ctx, amount)) {
        return false;
    }

    User* target = ctx.accounts.findUser(targetUsername);
    if (!ctx.session.addSessionCredit(amount)) {
        return false;
    }

    target->addCredit(amount);
    User transactionEntry(target->getUsername(), target->getType(), amount);
    ctx.writer.writeAddCredit(transactionEntry);

    if (ctx.session.isAdmin()) {
        ctx.console.showMessage(
            "Added $" + formatMoney(amount) + " credit to " +
            targetUsername + "'s account.");
    } else {
        ctx.console.showMessage(
            "Added $" + formatMoney(amount) + " credit to your account.");
    }
    return true;
}

bool AddCreditTransaction::validateCredit(
    FrontEndContext& ctx, double amount) {
    if (!InputValidator::isValidCreditAmount(amount)) {
        if (amount > 1000.0) {
            ctx.console.showError(
                "cannot add more than $1000.00 of credit in a single session.");
        } else {
            ctx.console.showError("invalid credit amount.");
        }
        return false;
    }

    const double alreadyAdded = ctx.session.getSessionCredit();
    if (alreadyAdded + amount > 1000.0) {
        ctx.console.showError(
            "cannot add more than $1000.00 of credit in a single session (" +
            formatMoney(alreadyAdded) + " already added this session).");
        return false;
    }

    return true;
}
