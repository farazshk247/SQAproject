#pragma once

#include "Transaction.h"

class RefundTransaction : public Transaction {
private:
    bool validateRefund(
        FrontEndContext& ctx, std::string buyer, std::string seller,
        double amount);

public:
    RefundTransaction();
    bool execute(FrontEndContext& ctx) override;
};
