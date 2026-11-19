#pragma once

#include "Transaction.h"

class LoginTransaction : public Transaction {
public:
    LoginTransaction();
    bool execute(FrontEndContext& ctx) override;
};
