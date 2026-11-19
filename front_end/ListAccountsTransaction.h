#pragma once

#include "Transaction.h"

class ListAccountsTransaction : public Transaction {
public:
    ListAccountsTransaction();
    bool execute(FrontEndContext& ctx) override;
};
