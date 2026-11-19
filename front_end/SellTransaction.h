#pragma once

#include "Transaction.h"

class SellTransaction : public Transaction {
private:
    bool validateListing(
        FrontEndContext& ctx, std::string name, double price);

public:
    SellTransaction();
    bool execute(FrontEndContext& ctx) override;
};
