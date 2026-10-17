#pragma once

#include <string>

#include "Transaction.h"

class TransactionFactory {
public:
    Transaction* createTransaction(std::string command);
};
