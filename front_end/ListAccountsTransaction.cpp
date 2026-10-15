#include "ListAccountsTransaction.h"

ListAccountsTransaction::ListAccountsTransaction() {
    code = "listaccounts";
}

bool ListAccountsTransaction::execute(FrontEndContext& ctx) {
    if (!requireAdmin(ctx)) {
        return false;
    }

    ctx.console.showAccountList(ctx.accounts.getAllUsers());
    return true;
}
