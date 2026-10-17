#include "TransactionFactory.h"

#include "AddCreditTransaction.h"
#include "BuyTransaction.h"
#include "CreateTransaction.h"
#include "DeleteTransaction.h"
#include "ListAccountsTransaction.h"
#include "ListGamesTransaction.h"
#include "LoginTransaction.h"
#include "LogoutTransaction.h"
#include "RefundTransaction.h"
#include "SellTransaction.h"

Transaction* TransactionFactory::createTransaction(std::string command) {
    if (command == "login") {
        return new LoginTransaction();
    }
    if (command == "logout") {
        return new LogoutTransaction();
    }
    if (command == "create") {
        return new CreateTransaction();
    }
    if (command == "delete") {
        return new DeleteTransaction();
    }
    if (command == "sell") {
        return new SellTransaction();
    }
    if (command == "buy") {
        return new BuyTransaction();
    }
    if (command == "refund") {
        return new RefundTransaction();
    }
    if (command == "addcredit") {
        return new AddCreditTransaction();
    }
    if (command == "list") {
        return new ListGamesTransaction();
    }
    if (command == "listaccounts") {
        return new ListAccountsTransaction();
    }

    return nullptr;
}
