import base64
import hashlib

import bcrypt


def sort_candidate_result(candidate_list: list[tuple], lo: int, hi: int, reverse=True) -> None:
    """
    Sort candidates based on their gathered votes
    using quicksort with Lomuto partition scheme

    Source: https://en.wikipedia.org/wiki/Quicksort#Lomuto_partition_scheme
    """
    def partition(arr: list[tuple], low: int, high: int) -> int:
        pivot = arr[high][1]
        i = low - 1

        for j in range(low, high):
            if arr[j][1] >= pivot if reverse else arr[j][1] <= pivot:
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

    sort_candidate_result(candidate_list, lo, p - 1, reverse)
    sort_candidate_result(candidate_list, p + 1, hi, reverse)


def find_voter(voter_id_list: list[tuple], target_voter_id: int, lo: int, hi: int):
    while lo <= hi:
        mid_idx = (hi + lo) // 2

        if voter_id_list[mid_idx][1] == target_voter_id:
            return voter_id_list[mid_idx]
        elif voter_id_list[mid_idx][1] < target_voter_id:
            lo = mid_idx + 1
        else:
            hi = mid_idx - 1

    return -1


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


def inputs_empty(*args):
    return True if "" in args else False
