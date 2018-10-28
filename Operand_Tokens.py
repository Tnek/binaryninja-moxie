from binaryninja import InstructionTextToken, InstructionTextTokenType

DEFAULT_MODE = 0
EMPTY_MODE = 1
REGISTER_MODE = 2
IMM_ADDRESS_MODE = 3
IMM_INTEGER_MODE = 4

OperandTokens = [
    lambda reg, val: [ #: Default mode
        InstructionTextToken(InstructionTextTokenType.TextToken, str(reg)),
        InstructionTextToken(InstructionTextTokenType.TextToken, '('),
        InstructionTextToken(InstructionTextTokenType.TextToken, str(val)),
        InstructionTextToken(InstructionTextTokenType.TextToken, ')')
    ],

    lambda reg, val: [ #: Empty mode
    ],

    lambda reg, val: [ #: Register mode
        InstructionTextToken(InstructionTextTokenType.RegisterToken, reg)
    ],
    lambda reg, val: [ #: Immediate Address mode
        InstructionTextToken(InstructionTextTokenType.PossibleAddressToken, hex(val), val)
    ],

    lambda reg, val: [ #: Immediate Integer mode
        InstructionTextToken(InstructionTextTokenType.IntegerToken, hex(val), val)
    ],

]
