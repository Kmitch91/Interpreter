from enum import (Enum)

class NodeType(Enum):

    PROGRAM = "<program>"
    DECLARE = "<declare>"
    ASSIGNMENT = "<assignment>"
    PRINT_METHOD = "<print_method>"
    IF_STMT = "<if_stmt>"
    WHILE_LOOP = "<while_loop>"
    VAR_TYPE = "<varType>"
    COND_OPER = "<cond_oper>"
    EXPR = "<expr>"
    TERM = "<term>"
    FACTOR = "<factor>"
    ELSE_STMT = "<else_stmt>"

