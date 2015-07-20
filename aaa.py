import os

for dirname, dirnames, filenames in os.walk('E:\\projects\\gitlab\\biubiu'):
    # print path to all subdirectories first.
    print dirnames
    for subdirname in dirnames:
        print(os.path.join(dirname, subdirname))

    # print path to all filenames.
    print filenames
    for filename in filenames:
        print(os.path.join(dirname, filename))

    # Advanced usage:
    # editing the 'dirnames' list will stop os.walk() from recursing into there.
    if '.git' in dirnames:
        # don't go into any .git directories.
        dirnames.remove('.git')
