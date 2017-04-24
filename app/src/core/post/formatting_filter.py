def format_text(text):
    ret = []
    for line in text.split('\n'):
        if not line:
            continue
        line = line.rstrip('\n')
        if len(line) > 80:
            split_lines = _split_lines(line, 80)
            ret += (split_lines)
        else:
            ret.append(line)
    return '\n'.join(ret)

def _split_lines(line, max_len=40):
    """
    Return line separated into a series of strings no longer than len max_len
    :param line: The long line to be separated into smaller lines
    :param max_len: Maximum length in characters for a line
    :return: Array of lines no longer than max len
    """
    ret_lines = []
    while len(line) > max_len:
        cut_off = None
        # find white space left of max_len:
        for i in range(max_len, 0, -1):
            if line[i] == ' ':
                cut_off = i
                break
        ret_lines.append(line[:cut_off].lstrip())
        line = line[cut_off:]
    return ret_lines

# # Test
# line = "So me mock on the me fon the chillen the muntion to the to the that you know the mantin', and d you dingar and the ray it aol with the eching the keess the exflous and the kicked the wahale on the bees around the slow the tome ander the pack in the "
#
# [print(it) for it in _split_lines(line,60)]