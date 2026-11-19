#pragma once

#include "Transaction.h"

class DeleteTransaction : public Transaction {
private:
    bool validateTarget(FrontEndContext& ctx, std::string username);
    void cancelInventory(FrontEndContext& ctx, std::string seller);

public:
    DeleteTransaction();
    bool execute(FrontEndContext& ctx) override;
};
