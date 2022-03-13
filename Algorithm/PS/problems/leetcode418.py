class Solution:
    def wordsTyping(self, sentence: List[str], rows: int, cols: int) -> int:
        # Time Complexity: O(num_of_rows * max_len_of_word_in_sentence) in total
        total_s = ' '.join(sentence) + ' '
        total_l = len(total_s)
        pointer = 0
        # O(num_of_rows)
        for _ in range(rows):
            pointer += cols
            if total_s[pointer % total_l] == ' ':
                # move to next new position
                pointer += 1
            else:
                # O(max_len_of_word_in_sentence)
                # find the previous space
                while pointer >= 0 and total_s[pointer % total_l] != ' ':
                    pointer -= 1
                # move to next new position
                pointer += 1
        
        return pointer // total_l