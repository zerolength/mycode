import shutil
import os


def main():

    os.chdir("/home/student/mycode/")

    shutil.copy("/home/student/wSpa/tensoparse/log.txt", "/home/student/wSpa/tensoparse/log.txt.bak")

    shutil.copytree("/home/student/wSpa/tensoparse/.git", "/home/student/wSpa/tensoparse/.git.bak")

    shutil.move('chekov.obj', 'ceph_stor')

    xname = input('What is the new name for duran.obj? ')

    shutil.move('ceph_stor/duran.obj', 'ceph_stor/' + xname)



if __name__ == "__main__":
    main()
