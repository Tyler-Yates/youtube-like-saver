import os

from youtubelikesaver.src.backup_util import BackupUtil

TEST_VIDEO_URL = "https://www.youtube.com/watch?v=7_cDT5_Vmdc"


class TestBackupUtil:
    def test_save_video(self, tmpdir):
        backup_util = BackupUtil()
        video_title = "temp"
        backup_util.save_video(TEST_VIDEO_URL, str(tmpdir), video_title)

        listdir = os.listdir(os.path.join(tmpdir))
        print(listdir)
        assert f"{video_title}.mkv" in listdir

    def test_save_audio(self, tmpdir):
        backup_util = BackupUtil()
        video_title = "temp"
        backup_util.save_audio(TEST_VIDEO_URL, str(tmpdir), video_title)

        listdir = os.listdir(os.path.join(tmpdir))
        print(listdir)
        assert f"{video_title}.m4a" in listdir
