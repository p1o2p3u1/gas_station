from unidiff import PatchSet

class UnidiffParser:

    def __init__(self):
        self.parser = None

    def parse(self, diff):
        """
        diff has the following format:

        Index: hello/test.txt
        ===================================================================
        --- hello/test.txt      (revision 6)
        +++ hello/test.txt      (revision 7)
        @@ -1,4 +1,3 @@
        .....source code...
         aaa
        +bbb
        +ccc
        :param diff: the diff result string
        :return: Return the change list. We only care about the addition and modification, and we don't
        need to care about the deletion
        """
        if diff is None or len(diff) == 0:
            return []
        patch = PatchSet(diff.split('\n'), encoding='utf8')
        # although we only have one patched file
        change = []
        for patched_file in patch:
            for hunk in patched_file:
                change.extend([i.target_line_no for i in hunk
                               if i.target_line_no is not None
                               and not i.is_context])
        return change


