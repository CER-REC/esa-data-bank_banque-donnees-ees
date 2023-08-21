import random
import string


TMP_TABLE_PREFIX = "tmp_"


def get_temp_table_name():
    """ create a temp table name consisted of 10 random letters """
    return f"{TMP_TABLE_PREFIX}{''.join(random.choice(string.ascii_lowercase) for _ in range(10))}"
