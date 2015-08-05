
class UnidiffParser:

    def __init__(self):
        pass

    def parse(self, diff):
        """
        diff has the following format:

        Index: hello/test.txt
        ===================================================================
        --- hello/test.txt      (revision 6)
        +++ hello/test.txt      (revision 7)
        @@ -1,4 +1,3 @@
        .....source code...
        
        :param diff:
        :return:
        """
        if diff is None or len(diff) == 0:
            return []
