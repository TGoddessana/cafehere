def get_initial_consonant(input_str):
    """
    한글 문자열을 받아서 초성으로 변환하여 반환합니다.
    """
    initial_consonants = [
        "ㄱ",
        "ㄲ",
        "ㄴ",
        "ㄷ",
        "ㄸ",
        "ㄹ",
        "ㅁ",
        "ㅂ",
        "ㅃ",
        "ㅅ",
        "ㅆ",
        "ㅇ",
        "ㅈ",
        "ㅉ",
        "ㅊ",
        "ㅋ",
        "ㅌ",
        "ㅍ",
        "ㅎ",
    ]

    result = ""

    for char in input_str:
        if char == " " or ("가" <= char <= "힣" and len(char) == 1):
            if "가" <= char <= "힣":
                char_code = ord(char) - ord("가")
                initial = initial_consonants[char_code // 588]
                result += initial
            else:
                result += char
        else:
            result += char

    return result
