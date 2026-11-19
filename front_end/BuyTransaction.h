#pragma once

#include "Transaction.h"

class BuyTransaction : public Transaction {
private:
    bool validatePurchase(FrontEndContext& ctx, std::string gameName);

public:
    BuyTransaction();
    bool execute(FrontEndContext& ctx) override;
};
