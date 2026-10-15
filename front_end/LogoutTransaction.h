#pragma once

#include "Transaction.h"

class LogoutTransaction : public Transaction {
public:
    LogoutTransaction();
    bool execute(FrontEndContext& ctx) override;
};
