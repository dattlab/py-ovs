import base64
import hashlib

import bcrypt


def sort_candidate_result(candidate_list: list[tuple], lo: int, hi: int) -> None:
    """
    Sort candidates based on their gathered votes
    using quicksort with Lomuto partition scheme

    Source: https://en.wikipedia.org/wiki/Quicksort#Lomuto_partition_scheme
    """
    def partition(arr: list[tuple], low: int, high: int) -> int:
        pivot = arr[high][1]
        i = low - 1

        for j in range(low, high):
            if arr[j][1] >= pivot:
                i += 1

                temp = arr[j]
                arr[j] = arr[i]
                arr[i] = temp

        i += 1
        temp = arr[high]
        arr[high] = arr[i]
        arr[i] = temp

        return i

    if lo >= hi or lo < 0:
        return

    p = partition(candidate_list, lo, hi)

    sort_candidate_result(candidate_list, lo, p - 1)
    sort_candidate_result(candidate_list, p + 1, hi)


def find_voter(voter_id: int):
    # TODO: Implement binary search for finding a voter with their voter's id
    ...


def encrypt_passwd(passwd: str) -> str:
    # Converts the input password into byte
    # string and hash it using bcrypt
    passwd_in_bytes = passwd.encode("UTF-8")

    hashed_passwd = bcrypt.hashpw(
        base64.b64encode(hashlib.sha256(passwd_in_bytes).digest()),
        bcrypt.gensalt()
    ).decode("UTF-8")

    return hashed_passwd


def passwd_match(input_passwd: str, expected: str) -> bool:
    input_passwd = base64.b64encode(
        hashlib.sha256(input_passwd.encode("UTF-8")).digest()
    )
    expected = expected.encode("UTF-8")

    return bcrypt.checkpw(input_passwd, expected)
