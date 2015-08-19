from unidiff import PatchSet
import xml.etree.ElementTree as Xml_parser


def parse_unidiff(diff):
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


def parse_svn_log(xml):
    """
    parse svn log. The log is xml format to make it easy to parse.

    <?xml version="1.0" encoding="UTF-8"?>
        <log>
            <logentry revision="18">
                <author>test</author>
                <date>2015-08-18T07:47:36.623646Z</date>
                <msg>log message</msg>
            </logentry>
            ...more log entries
        </log>
    </xml>
    :param log:
    :return:
    """
    logs = []
    tree = Xml_parser.fromstring(xml)
    for log in tree:
        logs.append({
            'revision': log.attrib['revision'],
            'author': log[0].text,
            'date': log[1].text,
            'comment': log[2].text
        })
    return logs