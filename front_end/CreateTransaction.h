#pragma once

#include "Transaction.h"

class CreateTransaction : public Transaction {
private:
    bool validateNewUser(
        FrontEndContext& ctx, std::string username, std::string type);

public:
    CreateTransaction();
    bool execute(FrontEndContext& ctx) override;
};
