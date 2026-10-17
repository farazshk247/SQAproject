#pragma once

#include "Transaction.h"

class AddCreditTransaction : public Transaction {
private:
    bool validateCredit(FrontEndContext& ctx, double amount);

public:
    AddCreditTransaction();
    bool execute(FrontEndContext& ctx) override;
};
